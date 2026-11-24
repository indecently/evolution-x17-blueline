#!/usr/bin/env python3
"""Recreate six local blob fixups using the pinned vendor checkout."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import tempfile

VENDOR = Path("vendor/google/blueline")
PATCHELF = Path("prebuilts/extract-tools/linux-x86/bin/patchelf-0_18").resolve()
FIXUPS = {
    "system_ext/lib64/libsecureuisvc_jni.so": ("--add-needed", "libgui_shim_secureui.so"),
    "vendor/bin/hw/android.hardware.biometrics.fingerprint@2.1-service.fpc": (),
    "vendor/bin/mm-pp-dpps": ("--replace-needed", "libtinyxml2.so", "libtinyxml2-v34.so"),
    "vendor/lib64/camera/components/com.qti.node.eisv2.so": ("--replace-needed", "libtinyxml2.so", "libtinyxml2-v34.so"),
    "vendor/lib64/camera/components/com.qti.node.eisv3.so": ("--replace-needed", "libtinyxml2.so", "libtinyxml2-v34.so"),
    "vendor/lib64/hw/camera.sdm845.so": ("--replace-needed", "libtinyxml2.so", "libtinyxml2-v34.so"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", help="vendor/google/blueline base commit from BASES.tsv")
    parser.add_argument("--apply", action="store_true", help="write blobs into the vendor tree")
    args = parser.parse_args()
    candidates = {}
    with tempfile.TemporaryDirectory() as staging:
        for path, options in FIXUPS.items():
            relative = f"proprietary/{path}"
            data = subprocess.check_output(
                ["git", "-C", VENDOR, "show", f"{args.base}:{relative}"]
            )
            candidate = Path(staging) / Path(path).name
            if options:
                candidate.write_bytes(data)
                subprocess.run([PATCHELF, *options, candidate], check=True)
                data = candidate.read_bytes()
            else:
                data = data.replace(b"_ZN7android10frameworks5stats", b"_ZN7lineage10frameworks5stats")
                data = data.replace(b"android.frameworks.stats@1.0", b"lineage.frameworks.stats@1.0")
            candidates[VENDOR / relative] = data
    for destination, data in candidates.items():
        print(hashlib.sha256(data).hexdigest(), destination)
        if args.apply:
            destination.write_bytes(data)


if __name__ == "__main__":
    main()
