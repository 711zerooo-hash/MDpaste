# MDPASTE Portable

> Move Markdown from AI chats into Word / WPS / Office with less manual formatting.<br>
> A Windows portable package based on upstream PasteMD, bundled with Pandoc and ready to run after extraction.

<p align="center">
  <strong>Other Languages / 其他语言:</strong><br>
  <a href="../README.md">中文</a> |
  English
</p>

## What It Is

MDPASTE Portable is a Windows portable distribution of PasteMD. It converts copied Markdown into formatted content that can be pasted into Word, WPS, Office, and other supported applications.

Common use cases:

- Copy answers from AI chat tools.
- Preserve Markdown structures such as headings, lists, code blocks, tables, and formulas.
- Paste the converted result into documents with less manual cleanup.

Pandoc is bundled in this package, so users do not need to install Python, Pandoc, or other command-line tools separately.

## Quick Start

1. Open the GitHub Releases page.
2. Download `MDPASTE-portable-v0.1.0.0.zip`.
3. Extract it to any folder.
4. Double-click `MDPASTE.cmd`.
5. Copy Markdown content, then press the default hotkey `Ctrl+Alt+B` to convert/paste.

Do not start the app by double-clicking `MdPaste.exe`. Use `MDPASTE.cmd`, because it prepares the portable data folders and rewrites paths for the current computer.

## Portable Behavior

Every time `MDPASTE.cmd` starts the app, it rewrites runtime paths based on the current folder:

- `APPDATA` -> `portable-data\Roaming`
- `LOCALAPPDATA` -> `portable-data\Local`
- `pandoc_path` -> `_internal\pandoc\pandoc.exe` under the current folder
- `save_dir` -> `cache` under the current folder

This means the whole folder can be copied to another Windows computer. Start it again with `MDPASTE.cmd`; no manual path edits are required.

## Main Files

```text
MDpaste/
├── MDPASTE.cmd                 # user-facing launcher
├── MdPaste-portable.cmd         # portable startup script
├── portable-config.ps1          # rewrites local paths on startup
├── switch-startup.cmd           # login startup helper
├── build-release.ps1            # builds the Release ZIP
├── README.md                    # Chinese README
├── i18n/
│   └── README.en.md             # English README
├── MODIFICATIONS.md             # modifications from upstream
├── UPSTREAM_COMPARISON.md       # comparison with upstream v0.1.6.8
├── SOURCE.md                    # corresponding source notes
├── NOTICE.md                    # license notice
├── assets/                      # committed modified resources
├── pastemd/                     # committed modified resources
├── MdPaste.exe                  # upstream binary, distributed in Release
└── _internal/                   # upstream runtime and bundled Pandoc, distributed in Release
```

## Pandoc

PasteMD depends on Pandoc for document and rich-text conversion. The portable package includes Pandoc at:

```text
_internal\pandoc\pandoc.exe
```

Do not delete `_internal`. If Pandoc is missing, the launcher stops and asks the user to download the complete ZIP again.

## Local Data

These files are generated on the user's computer:

- Config: `portable-data\Roaming\PasteMD\config.json`
- Log: `portable-data\Roaming\PasteMD\pastemd.log`
- Cache: `cache`

They are local runtime data. They are not committed to Git and are not included in a clean release package.

## Changes from Upstream

Code and resource changes are documented in two files:

- `MODIFICATIONS.md`: explains which files were added or modified and what each script/resource file does.
- `UPSTREAM_COMPARISON.md`: lists files that differ from upstream PasteMD `v0.1.6.8`.

This repository commits the modified upstream resources identified from the local release package:

- locale files under `pastemd/i18n/locales`
- icon files under `assets/icons`

This repository also adds portable packaging files:

- `MDPASTE.cmd`
- `MdPaste-portable.cmd`
- `portable-config.ps1`
- `switch-startup.cmd`
- `build-release.ps1`
- documentation, license files, and source comparison files

If the distributed `MdPaste.exe` contains Python logic changes, the corresponding modified Python source used to build that binary must also be added.

## Version Maintenance

When the release version changes, update these places together:

- Download filename in `README.md` and `i18n/README.en.md`.
- Version and asset name in `RELEASE_NOTES.md`.
- Upstream tag, commit, and source link in `SOURCE.md`.
- Default `$Version` in `build-release.ps1`.
- Git tag, for example `v0.1.0.0`.
- GitHub Release title, notes, and ZIP asset name.

Keeping these values aligned avoids mismatches between user instructions, release assets, and source notes.

## Release

Build the portable ZIP locally:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build-release.ps1
```

Output:

```text
dist\MDPASTE-portable-v0.1.0.0.zip
```

The complete runnable package is distributed as a GitHub Release asset. The Git repository stores launcher scripts, packaging scripts, documentation, licenses, source notes, and identified modified resources.

## Codex Notice

The portable launcher scripts, path configuration script, packaging script, README files, Release notes, NOTICE, SOURCE, MODIFICATIONS, and UPSTREAM_COMPARISON notes in this repository were drafted and organized with assistance from OpenAI Codex in conversation with the project maintainer.

The upstream PasteMD application itself is not authored by Codex.

## Upstream and License

Upstream project: <https://github.com/RICHQAQ/PasteMD>

This portable package release is `v0.1.0.0`. It redistributes upstream PasteMD `v0.1.6.8`: <https://github.com/RICHQAQ/PasteMD/tree/v0.1.6.8>

PasteMD is licensed under AGPL-3.0. This repository redistributes and packages PasteMD for Windows portable use. The launcher and packaging files in this repository are also provided under AGPL-3.0. Keep `LICENSE`, `NOTICE.md`, and `SOURCE.md` with the release.
