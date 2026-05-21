# Corresponding Source

MDPASTE Portable release `v0.1.1` redistributes upstream PasteMD `v0.1.6.8`.

The source published in this repository covers the visible modifications in this redistribution: modified upstream resource files, portable launcher scripts, configuration rewrite script, startup helper, packaging script, and documentation changes added for the portable release.

`v0.1.1` additionally patches the bundled PyInstaller executable to fix ChatGPT web fragment copy handling and protect code blocks from formula rewrites. The corresponding patch script is published as `tools/patch_release_exe.py`.

Upstream corresponding source:

- Repository: https://github.com/RICHQAQ/PasteMD
- Tag: https://github.com/RICHQAQ/PasteMD/tree/v0.1.6.8
- Commit: `84b2cea1f291d910d4cf2d0a1fbc829f6bfec524`
- License: AGPL-3.0

Packaging source in this repository:

- `assets/icons/*`
- `pastemd/i18n/locales/*`
- `MDPASTE.cmd`
- `MdPaste-portable.cmd`
- `portable-config.ps1`
- `switch-startup.cmd`
- `build-release.ps1`
- `tools/patch_release_exe.py`

Detailed modifications from upstream are listed in `MODIFICATIONS.md`. The comparison against upstream `v0.1.6.8` is summarized in `UPSTREAM_COMPARISON.md`.

The release ZIP includes bundled third-party runtime files. Their license files are kept in place where provided by the upstream package, including Pandoc files under `_internal\pandoc\`.
