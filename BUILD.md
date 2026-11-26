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

Follow the pinned, reproducible source procedure in [CHECKOUT.md](CHECKOUT.md). It initializes the checkout from `blueline-checkout-manifest.xml`, verifies the device and platform source archives, applies the patches at their recorded base commits, and installs the complete B1C1 kernel source. Do not substitute moving branch tips for those pins. Resolve any inaccessible pinned dependency before starting a build.

## 3. Provide vendor dependencies

The published source archives omit proprietary binaries and Google APKs. The tested configuration used `vendor/google/blueline`, `vendor/google/crosshatch`, and Evolution X's matching `vendor/gms` prebuilts. Obtain them from sources you are authorized to use. The device tree includes extraction scripts and blob lists under `blueline/` and `crosshatch/`. Run the scripts with `--help` for the supported extraction sources and options. The patch archive's `OMITTED.txt` lists six modified proprietary blobs that require matching inputs. Stock extraction alone has not been verified to reproduce those blobs or the exact Google app build.

## 4. Build the OTA

Use the single default `out/` cache to conserve disk. Choose the build variant before the first full build and keep that variant for follow-up builds. For a release candidate or release build, use `user`:

```bash
source build/envsetup.sh
lunch lineage_blueline-user
set -o pipefail
mka otapackage -j2 2>&1 | tee blueline-release-build.log
```

For development-only builds, select `lineage_blueline-userdebug` in the same cache. Switching between `user` and `userdebug` can trigger substantial recompilation. Avoid switching variants unless needed; clean `out/` only if stale configuration prevents a correct build and you can afford the rebuild time. Keep logs outside `out/` so they survive cleaning. Bash's `pipefail` preserves build failures when using `tee`.

Expected files in `out/target/product/blueline/` are `lineage_blueline-ota.zip`, `boot.img` (contains Evolution Recovery), and `dtbo.img`. Confirm that the OTA metadata says `pre-device=blueline` and `ota-type=AB`.

```sh
cd out/target/product/blueline
unzip -p lineage_blueline-ota.zip META-INF/com/android/metadata | grep -E '^(pre-device|ota-type)='
sha256sum lineage_blueline-ota.zip boot.img dtbo.img > SHA256SUMS.txt
sha256sum -c SHA256SUMS.txt
```

Configure the project signing keys locally and keep private key files out of GitHub and the release package. Leave `PRODUCT_ADB_KEYS` unset so the workstation is not authorized by the image. Check the final target files and OTA to confirm the user variant, expected signing certificates, and absence of workstation ADB keys. Android still needs the matching public signing certificates to verify packages.

## 5. Validate before distributing

Keep OTA signing and recovery keys consistent across releases. See the [Evolution X unofficial signing template](https://github.com/Evolution-X/vendor_evolution-priv_keys-template). Verify that the target files contain no workstation ADB authorization or development boot loggers. Test with matching Evolution Recovery and its **Apply from ADB** menu. On a clean install, confirm first boot, brightness, and Google app launch both before and after Play services updates. Recovery status 0 verifies installation; Android boot and runtime checks are separate.
