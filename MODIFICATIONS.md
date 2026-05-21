# Modifications from Upstream PasteMD

This repository redistributes upstream PasteMD `v0.1.6.8` as MDPASTE Portable `v0.1.1`.

The release package includes the upstream application binary:

- `MdPaste.exe` is redistributed as part of the portable release package.
- The bundled runtime under `_internal\` is redistributed as part of the portable release package.

The changes published in this repository include both portable packaging changes and modified upstream resource files that were visible in the packaged runtime.

`v0.1.1` includes a PyInstaller archive patch applied to `MdPaste.exe`. The corresponding patch script is committed as `tools/patch_release_exe.py`.

## Modified Upstream Resource Files

These files are committed using the same relative paths as the upstream PasteMD project:

### `pastemd\i18n\locales\en-US.json`

Modified from upstream `v0.1.6.8`.

### `pastemd\i18n\locales\ja-JP.json`

Modified from upstream `v0.1.6.8`.

### `pastemd\i18n\locales\zh-CN.json`

Modified from upstream `v0.1.6.8`.

### `assets\icons\logo.ico`

Modified from upstream `v0.1.6.8`.

### `assets\icons\logo.png`

Modified from upstream `v0.1.6.8`.

### `assets\icons\logo_white.png`

Modified from upstream `v0.1.6.8`.

### `assets\icons\logoTemplate.png`

Modified from upstream `v0.1.6.8`.

### `assets\icons\logo_toast.png`

New icon file present in the distributed runtime package. This file is not present in upstream `v0.1.6.8`.

## Unchanged Visible Upstream Resource Files

These visible files were compared and matched upstream `v0.1.6.8`:

- `pastemd\lua\keep-latex-math.lua`
- `pastemd\lua\latex-replacements.lua`

## Added Files

### `MDPASTE.cmd`

User-facing launcher. Users double-click this file instead of `MdPaste.exe`.

It delegates to `MdPaste-portable.cmd` so all portable environment setup happens before the upstream app starts.

### `MdPaste-portable.cmd`

Portable startup script.

It performs these changes compared with directly launching upstream `MdPaste.exe`:

- Sets `MDPASTE_HOME` to the current folder.
- Changes the working directory to `MDPASTE_HOME`.
- Redirects `APPDATA` to `portable-data\Roaming`.
- Redirects `LOCALAPPDATA` to `portable-data\Local`.
- Adds the app folder, `_internal`, and `_internal\pandoc` to `PATH`.
- Creates missing `portable-data` and `cache` folders.
- Checks that `MdPaste.exe` exists.
- Checks that bundled Pandoc exists at `_internal\pandoc\pandoc.exe`.
- Runs `portable-config.ps1` before launching the upstream app.

### `portable-config.ps1`

Portable configuration rewrite script.

It creates or updates:

- `portable-data\Roaming\PasteMD\config.json`
- `portable-data\Local`
- `cache`

It rewrites these PasteMD configuration values on every start:

- `pandoc_path`: absolute path to the bundled Pandoc under the current folder.
- `save_dir`: absolute path to the current folder's `cache`.
- `auto_start`: `false`, because portable startup is managed separately.
- default `hotkey`: `<ctrl>+<alt>+b`, only when missing.
- LaTeX compatibility options:
  - `enable_latex_replacements`
  - `fix_single_dollar_block`
  - `convert_standard_latex_delimiters`

This makes the package portable after it is moved to a different Windows computer or extracted to a different folder.

### `switch-startup.cmd`

Windows login startup helper.

It creates or removes a Windows scheduled task named `PasteMD-Portable`, pointing to the current folder's `MdPaste-portable.cmd`.

If the folder is moved, users should run this script again to refresh the scheduled task path.

### `build-release.ps1`

Release packaging script.

It creates `dist\MDPASTE-portable-v0.1.1.zip` from:

- upstream binary/runtime files: `MdPaste.exe`, `_internal`
- portable launcher/config scripts
- documentation and license/source notice files

It intentionally does not include local runtime state such as `portable-data` config/log files.

### `tools\patch_release_exe.py`

Patch script for the bundled PyInstaller executable.

It updates the embedded Python archive in `MdPaste.exe` to:

- prefer clipboard HTML when ChatGPT fragment-copy HTML contains code blocks but plaintext has no Markdown fence;
- protect fenced code blocks, indented code blocks, and inline code from LaTeX/formula rewrites;
- keep normal body formula conversion enabled.

## Documentation and Compliance Files

These files were added or rewritten for redistribution:

- `README.md`
- `README.txt`
- `RELEASE_NOTES.md`
- `GITHUB_UPLOAD_STEPS.md`
- `NOTICE.md`
- `SOURCE.md`
- `LICENSE`
- `.gitignore`
- `.gitattributes`

They document:

- first-run usage
- portable path handling
- Pandoc dependency
- version maintenance rules
- AGPL-3.0 license status
- corresponding upstream source
- files changed by this portable packaging repository
- Codex-assisted authorship of the portable scripts and documentation

The upstream comparison table is kept in `UPSTREAM_COMPARISON.md`.

## Runtime Files Not Committed to Git

The following files are intentionally not committed to the Git repository:

- `MdPaste.exe`
- `_internal\`
- `portable-data\`
- `cache\`
- `dist\`

They are either upstream/bundled runtime files or local generated state. The complete runnable package is distributed through GitHub Release assets.
