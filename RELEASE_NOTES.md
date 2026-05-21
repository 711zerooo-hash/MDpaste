# MDPASTE Portable v0.1.1

## Assets

- `MDPASTE-portable-v0.1.1.zip`: portable package. Extract and run `MDPASTE.cmd`.

## What Changed

- Fixed ChatGPT web fragment copy handling so HTML code blocks are preferred when plaintext clipboard content has already lost Markdown fences.
- Protected fenced code blocks, indented code blocks, and inline code from LaTeX/formula rewrites.
- Kept normal body formula conversion enabled for copied Markdown and web fragments.
- Added `tools/patch_release_exe.py` as the corresponding patch script used to update the bundled PyInstaller executable.

## Portability Check

- Startup still derives the app home from `MDPASTE.cmd` / `MdPaste-portable.cmd`; no local machine path is required.
- `portable-config.ps1` rewrites `pandoc_path` and `save_dir` from the current folder on every start.
- Runtime state remains under `portable-data` and `cache`, so the extracted folder can be copied to another Windows computer.

## Versioning

This project should use SemVer-style release names going forward:

- Patch fixes: `0.1.1`, `0.1.2`
- New compatible features: `0.2.0`
- Stable public release: `1.0.0`

## User Notes

- First run: extract the ZIP, then double-click `MDPASTE.cmd`.
- Do not run `MdPaste.exe` directly.
- The portable launcher rewrites `pandoc_path` and `save_dir` for the current computer on every start.
- Bundled Pandoc is required and included under `_internal\pandoc\pandoc.exe`.
- Local user config/log/cache files are not included in the clean release package.
- If startup on login is enabled and the folder is moved, run `switch-startup.cmd` again.

## Purpose

MDPASTE converts copied Markdown, including AI chat answers, into formatted paste output for Word/WPS/Office and other supported applications.

## License and Source

- Upstream project: <https://github.com/RICHQAQ/PasteMD>
- Portable release version: `v0.1.1`
- Upstream corresponding source: <https://github.com/RICHQAQ/PasteMD/tree/v0.1.6.8>
- License: AGPL-3.0. The release keeps `LICENSE`, `NOTICE.md`, and `SOURCE.md`.
