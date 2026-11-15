 <p align="center">
  <img src="assets/icon.svg" width="200" alt="#SWAG logo" />
</p>

# #SWAG

**An independent Android app project.**

This is the official #SWAG repository. It contains the Android application source, project assets, build automation, and the resources required to develop and build #SWAG.

## Project structure

- `app/`: Android application source and Gradle build project.
- `archives/nuvio-mobile-enhanced/`: preserved upstream source archive.
- `assets/icon.svg`: official #SWAG logo and wordmark.
- `assets/incoming/`: imported source assets.
- `.github/workflows/`: GitHub Actions workflows.

## Building from source

### Requirements

- JDK 17
- Android SDK Platform 37.1
- Android Build Tools 37.0.0
- CMake 3.22.1
- Android NDK selected by the Android Gradle Plugin
- Rust stable and `cargo-ndk`
- Python 3 with `cairosvg` and `Pillow`

### Prepare dependencies and branding assets

From the repository root:

```bash
bash scripts/restore-android-libs.sh
python3 -m pip install cairosvg pillow
python3 scripts/generate-android-icons.py
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android
cargo install cargo-ndk --locked
```

The restore script validates the required Android AAR files before placing them in `app/composeApp/libs`. It uses a pinned upstream source revision to keep dependency restoration reproducible.

### Build a debug APK

```bash
cd app
./gradlew --no-daemon :androidApp:assembleFullDebug
```

## Upstream acknowledgements and licensing

#SWAG is an independent rebrand based on source from **Nuvio Mobile** and **Nuvio Mobile Enhanced**. Their original work, required attribution, and license notices are retained in the source tree. #SWAG is not affiliated with or endorsed by the Nuvio team.

The upstream source is licensed under **GNU General Public License v3.0**. Refer to `app/LICENSE` and the preserved third-party notices for the applicable license terms.

## Project notes

- Existing backend behavior, authentication, and service endpoints should remain intact unless a change is explicitly intended.
- Preserve upstream attribution and applicable license notices when modifying or redistributing the project.
- Android is the active development and release target. iOS project and build targets have been removed.
