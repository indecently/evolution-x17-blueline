# Pixel 3 performance and battery notes

These are development-device observations, not a battery-life guarantee or controlled benchmark.

## Existing sustained-performance settings

The device power hints retain a 1.5-second big-core launch boost and a 2.6496 GHz big-core ceiling. Little-core and GPU limits were not changed in this iteration. These settings are in `powerhint.json` in the device source snapshot.

Earlier short load checks are retained in the repository's `performance-burst-followup-1min.txt` and `performance-burst-followup-5min.txt` records. Those runs were preliminary and did not isolate Android thermal policy from background work.

## Screen-off battery observation, 2026-11-27 to 2026-11-28

- About 10 hours 5 minutes elapsed, with roughly 9 hours 53 minutes screen-off.
- Battery use was approximately 25–26 percentage points, about 2.5 points per hour averaged over the full interval.
- Wi-Fi and LTE data were enabled for the main portion. Wi-Fi was disabled only for the final short portion; LTE remained enabled.
- The device's reported battery health/capacity is around 83% of design capacity, so runtime remains limited by the aging, small battery.

The result is a marked improvement over the earlier screen-off test, but the runs had different radio conditions and are not directly comparable. Do not attribute all of the improvement to one change.

## Kernel wake evidence

The current capture showed substantially fewer `IPA_RM12` wake events per hour than the earlier capture. The IPA inactivity-timer path now releases its wake lock when a new request supersedes a pending release. `WLAN_CE_2` still appears because it services firmware control events; suppressing that path would risk Wi-Fi behavior. The per-hour WLAN control-event rate was lower in the later capture, but Wi-Fi was disabled near the end of that run, so that comparison is not a Wi-Fi-on-only benchmark.

The latest installed OTA was built from the development checkout and installed through Evolution Recovery. Clean public-checkout reproducibility remains unverified.
