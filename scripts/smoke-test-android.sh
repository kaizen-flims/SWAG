#!/usr/bin/env bash
set -euo pipefail

APK_DIR="$GITHUB_WORKSPACE/app/androidApp/build/outputs/apk/full/debug"
APK="$(find "$APK_DIR" -maxdepth 1 -type f -name '*.apk' -print -quit)"
if [[ -z "$APK" ]]; then
  echo "No APK found in $APK_DIR" >&2
  find "$GITHUB_WORKSPACE/app/androidApp/build/outputs" -maxdepth 5 -type f -print || true
  exit 1
fi

echo "Installing $APK"
adb wait-for-device
adb logcat -c
adb install -r "$APK"
adb shell am force-stop com.nuviodebug.com
adb shell am start -W -n com.nuviodebug.com/com.nuvio.app.launcher.AppIconDefault
sleep 18

if ! adb shell pidof com.nuviodebug.com >/dev/null; then
  adb logcat -d -t 3000 > "$RUNNER_TEMP/swag-launch-log.txt"
  grep -n -A45 -B12 'FATAL EXCEPTION' "$RUNNER_TEMP/swag-launch-log.txt" || true
  echo "App process did not remain alive after launch." >&2
  exit 1
fi

if adb logcat -d -s AndroidRuntime:E | grep -q 'FATAL EXCEPTION'; then
  adb logcat -d -s AndroidRuntime:E
  exit 1
fi

echo "#SWAG stayed alive for 18 seconds after launch."
