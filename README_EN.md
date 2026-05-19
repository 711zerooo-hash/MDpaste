# MDPASTE Portable

> Convert Markdown to Word/WPS/Office formats with one click

MDPASTE Portable is a Windows-friendly packaging of the upstream PasteMD project. It converts clipboard Markdown content into formats better suited for Word, WPS, Office, and other rich-text editors.

**Common use case:** Copy AI assistant responses (headings, lists, code blocks, tables, formulas, etc.) and paste formatted content directly into your documents — no manual reformatting needed.

The portable package bundles Pandoc internally, so no separate installation of Python, Pandoc, or any command-line tools is required.

---

## Getting Started

1. Download `MDPASTE-portable-v0.1.0.0.zip` from the [GitHub Releases](https://github.com/yesooner/MDpaste/releases) page.
2. Extract to any folder.
3. Double-click `MDPASTE.cmd` to launch.
4. Copy your Markdown content.
5. Press the default shortcut `Ctrl+Alt+B` to convert and paste.

> **Do NOT double-click `MdPaste.exe` directly.** Always use `MDPASTE.cmd` — it prepares the portable data directory and rewrites paths relative to your current folder automatically.

---

## File Guide

| File | Description |
| ---- | ----------- |
| `MDPASTE.cmd` | Normal user launch entry point — double-click this |
| `MdPaste-portable.cmd` | Actual portable launch script — sets up paths and checks dependencies |
| `MdPaste.exe` | Upstream PasteMD binary — do not launch directly |
| `_internal\pandoc\pandoc.exe` | Bundled Pandoc — handles document and rich-text conversion |
| `switch-startup.cmd` | Toggle auto-start on Windows logon |
| `portable-data` | Per-machine config and logs — created automatically on first run |
| `cache` | Conversion cache — created automatically on first run |

---

## Portability & Path Rewriting

Every time you launch from `MDPASTE.cmd`, the app rewrites all paths relative to the current folder:

| Original Path | Rewritten To |
| ------------ | ------------ |
| `APPDATA` | `portable-data\Roaming` |
| `LOCALAPPDATA` | `portable-data\Local` |
| `pandoc_path` | `_internal\pandoc\pandoc.exe` |
| `save_dir` | `cache` |

Simply copy the entire folder to another Windows PC and double-click `MDPASTE.cmd` — no manual path edits needed.

---

## Pandoc

All document and rich-text conversion relies on Pandoc, which is bundled at:

```
_internal\pandoc\pandoc.exe
```

**Do not delete the `_internal` folder.** If Pandoc is missing, the launch script will halt and prompt you to re-download the full ZIP.

---

## Auto-Start on Logon

Run `switch-startup.cmd` and follow the prompts to enable or disable auto-start.

If you move the folder, re-run `switch-startup.cmd` once so the Windows Task Scheduler updates to the new path.

---

## Local Data

These files are generated automatically on your machine:

| File | Location |
| ---- | -------- |
| Config | `portable-data\Roaming\PasteMD\config.json` |
| Log | `portable-data\Roaming\PasteMD\pastemd.log` |
| Cache | `cache` |

These are local runtime data — not committed to git, not included in release ZIPs.

---

## Version Maintenance

When a new release is published, sync all of the following:

- Download filename in `README.md` and `README.txt`
- Version number and attachment name in `RELEASE_NOTES.md`
- Upstream tag, commit, and source link in `SOURCE.md`
- Default `$Version` in `build-release.ps1`
- Git tag, e.g. `v0.1.0.0`
- GitHub Release title, description, and ZIP attachment name

Inconsistent version numbers cause user confusion — always verify all locations match before publishing.

---

## Repository & Release Model

The git repository stores only launch scripts, build scripts, documentation, licenses, and source attribution. Full runnable packages are distributed via GitHub Release attachments.

To build a release ZIP locally:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build-release.ps1
```

Output: `dist\MDPASTE-portable-v0.1.0.0.zip`

---

## Codex Attribution

The portable launch scripts, path configuration scripts, build scripts, README, release notes, NOTICE, SOURCE, and MODIFICATIONS in this repository were collaboratively authored by OpenAI Codex during conversations with the project maintainer.

The upstream PasteMD binary itself is not Codex-authored content.

---

## Modifications Relative to Upstream

For detailed per-file modification notes, see:

- `MODIFICATIONS.md` — itemized list of files added or changed relative to upstream
- `UPSTREAM_COMPARISON.md` — confirmed changed files compared to upstream PasteMD `v0.6.8`

This repository includes identified upstream modifications from the distributed binary:

- Language files under `pastemd/i18n/locales`
- Icon files under `assets/icons`

This repository also adds portable packaging:

- `MDPASTE.cmd`
- `MdPaste-portable.cmd`
- `portable-config.ps1`
- `switch-startup.cmd`
- `build-release.ps1`
- Documentation, license, and source comparison files

If the published `MdPaste.exe` includes Python-level logic changes, the corresponding modified source for building that binary should also be included.

---

## Upstream Project & License

**Upstream:** [RICHQAQ/PasteMD](https://github.com/RICHQAQ/PasteMD)

This portable packaging release is `v0.1.0.0`, redistributing upstream PasteMD version `v0.6.8`: https://github.com/RICHQAQ/PasteMD/tree/v0.6.8

PasteMD is licensed under **AGPL-3.0**. This repository's launch scripts and build files are also published under **AGPL-3.0**. When redistributing, always retain `LICENSE`, `NOTICE.md`, and `SOURCE.md`.
