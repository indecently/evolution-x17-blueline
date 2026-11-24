# Assemble the pinned Pixel 3 Android 17 checkout

This manifest records the base revisions from the development checkout.
A clean public sync and compile have not yet been verified.

## Fetch the base

Use [BUILD.md](BUILD.md) to set up the Linux host. Then run:

```sh
mkdir evolution-x17 && cd evolution-x17
repo init -u https://github.com/indecently/evolution-x17-blueline.git -b main -m blueline-checkout-manifest.xml --git-lfs
repo sync -j2 --fail-fast
```

The manifest excludes the experimental 4.19 kernel and two paths that were
absent in the development checkout (Google Sans Flex and SM8850 audio MCS).
The device tree and active B1C1 kernel are supplied by the archives below.
If a dependency cannot be fetched at its pin, record the exact project and
commit. Substituting an arbitrary branch tip changes the build inputs.

## Overlay the port

Save the archives outside the Android checkout. Run these commands from its root.
Both archives contain the destination directories in their paths.

```sh
unzip /absolute/path/to/blueline-device-source.zip
tar -xzf /absolute/path/to/blueline-b1c1-kernel-source.tar.gz
unzip /absolute/path/to/blueline-source-patches.zip -d /absolute/path/to/unpacked-patches
```

Use the [device snapshot](blueline-device-source.zip),
[kernel source release](https://github.com/indecently/evolution-x17-blueline/releases/tag/blueline-b1c1-source-20261124),
and [patch bundle](blueline-source-patches.zip). Verify the kernel archive
against the SHA-256 file on its release page before extracting it.

In the following Bash snippet, set the patch directory to your actual absolute path.
The complete kernel archive already contains the kernel changes, so its patch
is skipped. Each other project must be at its recorded base before applying.

```bash
set -e
patch_dir=/absolute/path/to/unpacked-patches
while IFS=$'\t' read -r project expected patch; do
    [[ "$project" == kernel/google/b1c1 ]] && continue
    actual=$(git -C "$project" rev-parse HEAD)
    if [[ "$actual" != "$expected" ]]; then
        printf 'Unexpected base for %s: %s (expected %s)\n' "$project" "$actual" "$expected" >&2
        exit 1
    fi
    git -C "$project" apply --check "$patch_dir/$patch"
    git -C "$project" apply "$patch_dir/$patch"
done < <(tail -n +2 "$patch_dir/BASES.tsv")
```

## Supply vendor blobs and build

The base manifest references the upstream Evolution X vendor repositories.
The six locally modified proprietary files in the patch archive's
`OMITTED.txt` are reproduced by fixups in
`device/google/crosshatch/blueline/extract-files.py` when supplied with matching
unmodified inputs. Obtain those inputs from an authorized Android 12 Pixel 3
factory image or an equivalent extraction. Inspect the script's `--help`
before running it. The extraction has not been independently verified from a
clean download. Compare the generated vendor makefiles with the patched ones
because the extractor can regenerate them.

Once all dependencies are available, follow [BUILD.md](BUILD.md) for the
`lineage_blueline-userdebug` OTA build and verification.
