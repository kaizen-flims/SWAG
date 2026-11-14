# #SWAG Workstation

This repository is the active workspace for rebuilding and rebranding #SWAG. Development changes and GitHub Actions workflows belong here. The original `kaizen-flims/SWAG` repository is not modified by this workspace setup.

## Workspace layout

```
.
├── README.md
├── archives/
│   └── nuvio-mobile-enhanced/
│       ├── NuvioMobile-Enhanced-0.6.12-beta_part1.zip
│       ├── NuvioMobile-Enhanced-0.6.12-beta_part2.zip
│       └── NuvioMobile-Enhanced-0.6.12-beta_part3.zip
└── assets/
    └── incoming/
        └── 78754-1.svg
```

## Imported source

The three Nuvio archive parts are preserved unchanged under `archives/nuvio-mobile-enhanced/`. They have not been concatenated or extracted yet; their multipart format and integrity need to be verified before reconstruction.

The SVG is staged under `assets/incoming/` until its purpose is confirmed. It is not assumed to be the app logo.

## Next stage

1. Verify and reconstruct the Nuvio source archive.
2. Extract and inspect the complete project tree.
3. Establish the clean app/source, assets, documentation, and workflow layout from the actual project.
4. Apply #SWAG branding without changing backend behavior.
5. Run builds and CI workflows from this repository.
