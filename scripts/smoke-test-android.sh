#!/usr/bin/env bash
set -euo pipefail

ROOT="$GITHUB_WORKSPACE/app/androidApp/build/outputs/apk/full"

install_and_check() {
  local variant="$1"
  local package="$2"
  local apk_dir="$ROOT/$variant"
  local apk=""

  # The CI emulator is x86_64. Always install the matching ABI split;
  # selecting the first debug APK can pick x86 and fail with NO_MATCHING_ABIS.
  apk="$(find "$apk_dir" -maxdepth 1 -type f -name '*x86_64*.apk' -print -quit)"

  if [[ -z "$apk" ]]; then
    echo "No $variant APK found in $apk_dir" >&2
    find "$ROOT" -maxdepth 3 -type f -print || true
    exit 1
  fi

  echo "Installing $variant APK: $apk"
  adb wait-for-device
  adb logcat -c
  adb install -r "$apk"
  adb shell am force-stop "$package"
  adb shell am start -W -n "$package/com.nuvio.app.launcher.AppIconDefault"
  sleep 18

  if ! adb shell pidof "$package" >/dev/null; then
    adb logcat -d -t 3000 > "$RUNNER_TEMP/swag-$variant-launch-log.txt"
    grep -n -A45 -B12 'FATAL EXCEPTION' "$RUNNER_TEMP/swag-$variant-launch-log.txt" || true
    echo "$variant app process did not remain alive after launch." >&2
    exit 1
  fi

  if adb logcat -d -s AndroidRuntime:E | grep -q 'FATAL EXCEPTION'; then
    adb logcat -d -s AndroidRuntime:E
    exit 1
  fi

  echo "#SWAG $variant stayed alive for 18 seconds after launch."
}

install_and_check debug com.nuviodebug.com
install_and_check release com.nuvio.media
