# #SWAG Workstation

The active Android development workspace for #SWAG. All application changes and workstation-owned GitHub Actions workflows are maintained here. The original `kaizen-flims/SWAG` repository remains untouched until a reviewed version is ready to publish.

## Repository layout

- `app/`: Android application source and build project.
- `archives/nuvio-mobile-enhanced/`: original source archive parts, preserved unchanged.
- `assets/icon.svg`: canonical #SWAG logo and wordmark supplied for the rebrand.
- `assets/incoming/`: original imported asset staging area.
- `.github/workflows/`: workstation automation.

## Upstream acknowledgements

#SWAG is based on source from **Nuvio Mobile** and **Nuvio Mobile Enhanced**. Their original work and required license notices are retained in the source tree. #SWAG is an independent rebrand and is not affiliated with or endorsed by the Nuvio team.

The upstream source is licensed under GNU GPL v3.0. See `app/LICENSE` and the preserved third-party notices for the applicable terms.

## Local Android setup

Requirements: JDK 17, Android SDK Platform 37.1, Build Tools 37.0.0, CMake 3.22.1, an Android NDK selected by the Android Gradle Plugin, Rust stable, `cargo-ndk`, and Python packages `cairosvg` and `Pillow` for generating Android branding assets.

From the repository root, restore the pinned upstream Android libraries (the binary AARs are intentionally not committed here):

```bash
bash scripts/restore-android-libs.sh
python3 -m pip install cairosvg pillow
python3 scripts/generate-android-icons.py
rustup target add aarch64-linux-android armv7-linux-androideabi i686-linux-android x86_64-linux-android
cargo install cargo-ndk --locked
```

Then build the full Android debug APK:

```bash
cd app
./gradlew --no-daemon :androidApp:assembleFullDebug
```

The restore script validates every required AAR before placing it in `app/composeApp/libs`. It uses a pinned upstream source revision so workstation builds do not silently drift when upstream changes.

## Development rules

- Keep existing backend behavior, authentication, and service endpoints unchanged unless explicitly requested.
- Make and verify changes in this workstation repository.
- Keep upstream attribution and license notices intact.
- Android is the active target in this workstation; iOS project and build targets have been removed.
