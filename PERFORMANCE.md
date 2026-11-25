# Pixel 3 performance iteration

This is a development measurement for the Android 17 Evolution X port, not a
release performance claim.

## Change in this iteration

The device power hints now use 2.6496 GHz as the big-core default ceiling and
restore a 1.5-second big-core launch boost. Little-core and GPU tuning were not
changed in this iteration. The settings are in `powerhint.json` inside the
[device source snapshot](blueline-device-source.zip).

## Build and installation

On November 25, 2026, the development OTA build completed successfully. It was
installed through Evolution Recovery with status 0 and booted on the Pixel 3
with build ID `CP2A.260605.016`. This was a development build from the existing
checkout; a clean public checkout build has not been verified.

## Measurements

The load check used four arithmetic workers pinned to big CPUs 4–7. The
five-minute run sampled every 15 seconds and stopped at a 43°C battery-sensor
threshold; it completed without reaching that threshold. Big-cluster current
frequency samples ranged from 1.2864 to 1.536 GHz. The battery sysfs reading
was 41.3°C at the start and 40.8°C at the end. The shorter one-minute run
recorded 2.5536–2.6496 GHz initially and 2.3232 GHz at its final sample, with
the battery reading rising from 38.0°C to 40.0°C.

These runs are preliminary. The five-minute run started after first boot, and
a concurrent sample showed Google Play services and system_server doing
substantial work. Android thermal-service details were not readable from the
shell, so the lower sustained frequencies cannot yet be attributed to a
specific thermal control. The Recovery install log also reported a 75°C
maximum from a different sensor; it should not be compared directly with the
battery readings above.

Raw samples: [five-minute run](performance-burst-followup-5min.txt) and
[one-minute run](performance-burst-followup-1min.txt).
