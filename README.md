# #SWAG Workstation

The active development workspace for rebuilding and rebranding #SWAG. App source, code changes, and workstation GitHub Actions workflows live here. The original `kaizen-flims/SWAG` repository is not changed by this import.

## Repository layout

- `app/`: extracted Nuvio Mobile Enhanced 0.6.12-beta project. Build commands should run from this directory.
- `archives/nuvio-mobile-enhanced/`: original three ZIP parts, preserved unchanged as source provenance.
- `assets/incoming/`: imported SVG awaiting visual identification.
- `.github/workflows/`: workstation-owned automation. Upstream workflows inside `app/.github/` are nested project files and are not active in this repository.

## Source handling

The three archive parts were concatenated in filename order and passed a ZIP CRC test before extraction. The extracted project is kept under `app/` so its original build files and upstream workflow definitions stay isolated from workstation automation.

## Development rules

- Preserve existing backend behavior and service endpoints during the rebrand.
- Make and test changes in this workstation repository.
- Keep the original `kaizen-flims/SWAG` repository untouched until a reviewed version is ready to publish.
- Inspect upstream licensing and submodule requirements before changing or redistributing source.
