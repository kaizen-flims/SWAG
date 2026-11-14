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

## Development rules

- Keep existing backend behavior, authentication, and service endpoints unchanged unless explicitly requested.
- Make and verify changes in this workstation repository.
- Keep upstream attribution and license notices intact.
- Android is the active target in this workstation; iOS project and build targets have been removed.
