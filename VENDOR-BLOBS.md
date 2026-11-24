# Recreate the Pixel 3 vendor fixups

After syncing the pinned manifest and applying the text patches in [CHECKOUT.md](CHECKOUT.md), download [the fixup script](restore-blueline-blobs.py) and [checksum file](blueline-blob-SHA256SUMS.txt). Run these commands from the Android checkout root.

```sh
python3 /absolute/path/to/restore-blueline-blobs.py 21b4fe5e00a992900436c56821916f6a056550a6 --apply
sha256sum -c /absolute/path/to/blueline-blob-SHA256SUMS.txt
```

Run without the apply flag to print hashes without writing files. The script reads the original blobs from the pinned vendor commit and uses the Android tree's patchelf. All six generated files matched the development build inputs byte for byte.
