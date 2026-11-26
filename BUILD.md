# Building Evolution X 17 for Google Pixel 3

Target: Google Pixel 3 (`blueline`, SDM845), Android 17, Evolution X 12.4. The active kernel is `kernel/google/b1c1` (4.9.337).

## 1. Prepare the host

Use a 64-bit Linux host with Bash, Git, Git LFS, Python 3, Repo, and the Android build packages listed in the [AOSP host setup guide](https://source.android.com/docs/setup/start/requirements). Keep the checkout and output on a Linux filesystem with ample free space. The development checkout and outputs occupied several hundred GiB. A 16 GiB host can spend hours in Soong and use tens of GiB of swap. Use an SSD, confirm swap is active, and start with two jobs on a low-memory host.

```sh
git lfs install
free -h
swapon --show
df -h .
```

## 2. Assemble the source checkout

The development baseline used [Evolution X's manifest](https://github.com/Evolution-X/manifest) branch `cnb`, manifest commit `6a8c7f78ef8620d63016512694044aacf9795ceb`. The published files are snapshots and patches. A public manifest that resolves every dependency and a fresh end-to-end build are still pending. A branch-only sync can fetch newer revisions or fail on restricted projects.

```sh
mkdir evolution-x17 && cd evolution-x17
repo init -u https://github.com/Evolution-X/manifest.git -b cnb --git-lfs
repo sync -c -j2 --fail-fast
```

Bring in the Pixel 3 device tree and B1C1 kernel checkout at the paths below. The development tree used [Evolution-X-Devices/device_google_crosshatch](https://github.com/Evolution-X-Devices/device_google_crosshatch) and [Evolution-X-Devices/kernel_google_b1c1](https://github.com/Evolution-X-Devices/kernel_google_b1c1). The patches also touch framework, hardware, build, and system projects. Use the checkout paths and exact base commits in `BASES.tsv` rather than applying patches against arbitrary branch tips. A missing base commit or inaccessible dependency must be resolved before continuing.

Download [device source](blueline-device-source.zip), [source patches](blueline-source-patches.zip), and both SHA-256 files into a separate directory. Verify the archives before extraction. Extract the device snapshot into an empty staging directory and use its `device/google/crosshatch` tree as that project's source. If the workspace already has an upstream tree there, replace its contents in a fresh checkout or compare the trees first so deleted upstream files do not remain. Preserve executable permissions when unpacking.

Extract the patch ZIP. For each row of `BASES.tsv`, run the following from the Android root, substituting the row's path, commit, and absolute patch path. Use a clean worktree before switching revisions.

```sh
git -C <checkout-path> switch --detach <base-commit>
git -C <checkout-path> apply --check /absolute/path/to/<patch>
git -C <checkout-path> apply /absolute/path/to/<patch>
```

## 3. Provide vendor dependencies

The published archives omit proprietary binaries and Google APKs. The tested configuration used `vendor/google/blueline`, `vendor/google/crosshatch`, and Evolution X's matching `vendor/gms` prebuilts. Obtain them from sources you are authorized to use. The device tree includes extraction scripts and blob lists under `blueline/` and `crosshatch/`. Run the scripts with `--help` for the supported extraction sources and options. The patch archive's `OMITTED.txt` lists six modified proprietary blobs that require matching inputs. Stock extraction alone has not been verified to reproduce those blobs or the exact Google app build.

## 4. Build the OTA

Run from the Android checkout root under Bash. Put the build log outside `out/` so it survives cleaning. Bash's `pipefail` preserves build failures when using `tee`.

```bash
source build/envsetup.sh
lunch lineage_blueline-userdebug
set -o pipefail
mka otapackage -j2 2>&1 | tee blueline-build.log
```

Expected files in `out/target/product/blueline/` are `lineage_blueline-ota.zip`, `boot.img` (contains Evolution Recovery), and `dtbo.img`. Confirm that the OTA metadata says `pre-device=blueline` and `ota-type=AB`.

```sh
cd out/target/product/blueline
unzip -p lineage_blueline-ota.zip META-INF/com/android/metadata | grep -E '^(pre-device|ota-type)='
sha256sum lineage_blueline-ota.zip boot.img dtbo.img > SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```



For a release candidate, use `lunch lineage_blueline-user` instead of `userdebug`. Configure the project signing keys locally and keep private key files out of GitHub and the release package. Leave `PRODUCT_ADB_KEYS` unset so the workstation is not authorized by the image. Check the final target files and OTA to confirm the user variant, expected signing certificates, and absence of workstation ADB keys. Android still needs the matching public signing certificates to verify packages.

## 5. Validate before distributing

Keep OTA signing and recovery keys consistent across releases. See the [Evolution X unofficial signing template](https://github.com/Evolution-X/vendor_evolution-priv_keys-template). Verify that the target files contain no workstation ADB authorization or development boot loggers. Test with matching Evolution Recovery and its **Apply from ADB** menu. On a clean install, confirm first boot, brightness, and Google app launch both before and after Play services updates. Recovery status 0 verifies installation; Android boot and runtime checks are separate.



## 6. Keep release and development caches separate

Reserve the default `out/` for release builds (`lineage_blueline-user`). Use `out-userdebug/` for development builds, setting `OUT_DIR` before sourcing the build environment:

```bash
export OUT_DIR="$PWD/out-userdebug"
source build/envsetup.sh
lunch lineage_blueline-userdebug
mka otapackage -j2
```

In a fresh shell, `unset OUT_DIR` returns release builds to the default `out/`. Each directory needs its own initial build; later builds reuse the matching variant cache instead of repeatedly switching one tree between `userdebug` and `user`. Separate outputs do not fix missing Repo checkouts or source errors, so complete the sync and manifest check first.
