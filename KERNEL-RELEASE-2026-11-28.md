# Pixel 3 B1C1 kernel source release — 2026-11-28

This release publishes the complete source tree for the Google Pixel 3 (`blueline`) B1C1 Linux 4.9.337 kernel used by the current Evolution X 17 source snapshot.

## Changes

- Android 17 compatibility work for the existing 4.9 kernel, including BPF verifier/JIT and networking support plus arm64 probe interfaces.
- IPA resource-manager inactivity-timer fix: release the timer wake lock when a new resource request supersedes the pending release.
- QCA Wi-Fi CE/HTT failure returns use the expected QDF status values.
- Kernel configuration and device defconfig updates required by the current port.

## Files

- `blueline-b1c1-kernel-source.tar.gz`: complete kernel source archive, including the current uncommitted source changes and new source files.
- `blueline-b1c1-kernel-SHA256SUMS.txt`: SHA-256 verification for the archive.

Extract the archive from the Android checkout root to populate `kernel/google/b1c1/`. Verify the archive before extraction. This is source code, **not** a flashable kernel image or ROM. Build instructions are in `BUILD.md`.

The full device and platform source overlays are also attached to this source release. Their checksums are provided beside each archive.
