# Evolution X 17 for Pixel 3 — source changelog

**Source snapshot:** 2026-11-28  
**Target:** Google Pixel 3 (`blueline`, SDM845)  
**Android:** 17 / Evolution X 17.0  
**Active kernel:** Google B1C1 Linux 4.9.337

This entry summarizes the source changes included in the current source package. It is not a ROM installation package. The separate [kernel source release notes](KERNEL-RELEASE-2026-11-28.md) describe the B1C1 archive.

## Kernel and power

- Updated the B1C1 4.9 kernel for Android 17's BPF, networking, arm64 probe, and related kernel interfaces while retaining the device's existing kernel line.
- Fixed the IPA resource-manager inactivity timer path so a new resource request that supersedes an in-flight release also releases the timer's wake lock. This targets the stale `IPA_RM12` suspend blocker seen during screen-off testing.
- Corrected QCA CE/HTT failure return values to use the QDF status type expected by the Wi-Fi driver.
- Kept the existing 1.5-second big-core launch boost and 2.6496 GHz big-core ceiling. Little-core and GPU limits were not changed in this iteration.

## Android 17 and device integration

- Added the Bionic `close_range(CLOSE_RANGE_CLOEXEC)` fallback for the legacy 4.9 kernel, with a regression test for the fallback behavior.
- Updated Android 17 Connectivity BPF loading and supporting system, fscrypt, property, zygote, and SELinux paths for the Pixel 3's legacy platform interfaces.
- Included current Pixel 3 device-tree and vendor integration updates, plus the display and Qualcomm audio build integration changes.
- Included the existing Pixel framework and Google package configuration changes in the platform patch bundle.

## Validation notes

- The 2026-11-27 Android 17 OTA was installed through Evolution Recovery and booted on the development Pixel 3. The device was usable after first boot.
- In the subsequent screen-off observation, the phone ran for about 10 hours 5 minutes with roughly 9 hours 53 minutes screen-off and used approximately 25–26 percentage points of battery. Wi-Fi and LTE were enabled for most of the run; Wi-Fi was disabled only near the end while LTE remained enabled. This is one device observation, not a controlled benchmark, and radio conditions differed from the earlier run.
- Kernel wake history showed a substantial reduction in `IPA_RM12` events per hour compared with the earlier capture. WLAN control-event wakeups also fell, but remain enabled because they are part of the firmware control path.
- A clean sync and rebuild from only the public source package has not been verified. Six modified proprietary blobs are intentionally omitted; see `OMITTED.txt` in the patch bundle and `VENDOR-BLOBS.md` for authorized inputs and reproduction notes.
