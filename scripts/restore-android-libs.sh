#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
LIB_DIR="$REPO_ROOT/app/composeApp/libs"

# The original repository revision previously used here was deleted. These
# binaries are restored from the matching Nuvio Mobile Enhanced library set,
# pinned to an immutable upstream commit rather than a moving branch.
UPSTREAM="https://raw.githubusercontent.com/luqmanfadlli/NuvioMobile-Enhanced/acde636a75d0e8f670bc0863d07a2fcb417eeee9/composeApp/libs"

FILES=(
  "lib-decoder-av1-release.aar"
  "lib-decoder-ffmpeg-release.aar"
  "lib-decoder-mpegh-release.aar"
  "lib-exoplayer-release.aar"
  "lib-nuvio-engine-android-0.1.6.aar"
  "lib-ui-release.aar"
  "nuvio-libass-release.aar"
  "quickjs-kt-android-1.0.5-nuvio.aar"
)

mkdir -p "$LIB_DIR"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

for file in "${FILES[@]}"; do
  destination="$LIB_DIR/$file"
  if [[ -s "$destination" ]] && unzip -tq "$destination" >/dev/null 2>&1; then
    printf 'Verified existing %s\n' "$file"
    continue
  fi

  printf 'Restoring %s\n' "$file"
  curl --fail --location --retry 3 --retry-all-errors \
    "$UPSTREAM/$file" --output "$TMP_DIR/$file"
  unzip -tq "$TMP_DIR/$file"
  mv "$TMP_DIR/$file" "$destination"
done

printf 'All %s required Android AAR libraries are present and valid.\n' "${#FILES[@]}"
