# Assemble the pinned Pixel 3 Android 17 checkout

This procedure overlays the current device snapshot, source patches, and full
B1C1 kernel source onto the pinned Android checkout. A clean public sync and
compile have not yet been verified.

## Fetch the base checkout

Use [BUILD.md](BUILD.md) to prepare the Linux host. Then run:

```sh
mkdir evolution-x17 && cd evolution-x17
repo init -u https://github.com/indecently/evolution-x17-blueline.git -b main -m blueline-checkout-manifest.xml --git-lfs
repo sync -j2 --fail-fast
```

The manifest excludes the abandoned 4.19 kernel experiment and two paths that
were absent from the development checkout. The active kernel source and full
device tree are supplied with the [2026-11-28 source release](https://github.com/indecently/evolution-x17-blueline/releases/tag/blueline-b1c1-source-20261128).
Resolve any unavailable pinned dependency rather than substituting a moving
branch tip.

## Download and verify the source overlays

Download these three archives and their matching checksum files from the
[source release](https://github.com/indecently/evolution-x17-blueline/releases/tag/blueline-b1c1-source-20261128):

- `blueline-device-source.zip` and `blueline-device-source-SHA256SUMS.txt`
- `blueline-source-patches.zip` and `blueline-source-patches-SHA256SUMS.txt`
- `blueline-b1c1-kernel-source.tar.gz` and `blueline-b1c1-kernel-SHA256SUMS.txt`

Run checks from the directory containing those files:

```sh
sha256sum -c blueline-device-source-SHA256SUMS.txt
sha256sum -c blueline-source-patches-SHA256SUMS.txt
sha256sum -c blueline-b1c1-kernel-SHA256SUMS.txt
```

Then, from the Android checkout root:

```sh
unzip /absolute/path/to/blueline-device-source.zip
tar -xzf /absolute/path/to/blueline-b1c1-kernel-source.tar.gz
unzip /absolute/path/to/blueline-source-patches.zip -d /absolute/path/to/unpacked-patches
```

The device archive populates `device/google/crosshatch/`; the kernel archive
populates `kernel/google/b1c1/`. The patch bundle includes the kernel patch for
review, but applying it is unnecessary after extracting the complete kernel
archive. Every other patch must be applied at the base commit recorded in
`BASES.tsv`:

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

## Supply vendor inputs and build

The public source archives omit proprietary binaries and Google APKs. Follow
[VENDOR-BLOBS.md](VENDOR-BLOBS.md) to recreate and verify the six local
proprietary blob fixups from authorized inputs. Then follow [BUILD.md](BUILD.md)
for host setup, build configuration, OTA generation, and validation.
