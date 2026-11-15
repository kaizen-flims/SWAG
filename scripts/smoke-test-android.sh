#!/usr/bin/env bash
set -euo pipefail

ROOT="$GITHUB_WORKSPACE/app/androidApp/build/outputs/apk/full/release"
PACKAGE="com.swag.media"
APK="$ROOT/androidApp-full-release.apk"

if [[ ! -f "$APK" ]]; then
  echo "Expected universal release APK was not found: $APK" >&2
  find "$GITHUB_WORKSPACE/app/androidApp/build/outputs/apk" -maxdepth 4 -type f -name '*.apk' -print || true
  exit 1
fi

echo "Installing universal #SWAG release APK: $APK"
adb wait-for-device
adb logcat -c
adb install -r "$APK"
adb shell am force-stop "$PACKAGE"
adb shell am start -W -n "$PACKAGE/com.nuvio.app.launcher.AppIconDefault"
sleep 18

if ! adb shell pidof "$PACKAGE" >/dev/null; then
  adb logcat -d -t 3000 > "$RUNNER_TEMP/swag-release-launch-log.txt"
  grep -n -A45 -B12 'FATAL EXCEPTION' "$RUNNER_TEMP/swag-release-launch-log.txt" || true
  echo "Release app process did not remain alive after launch." >&2
  exit 1
fi

if adb logcat -d -s AndroidRuntime:E | grep -q 'FATAL EXCEPTION'; then
  adb logcat -d -s AndroidRuntime:E
  exit 1
fi

echo "#SWAG universal release stayed alive for 18 seconds after launch."
