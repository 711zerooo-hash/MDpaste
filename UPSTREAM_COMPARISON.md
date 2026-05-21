# Upstream Comparison

Comparison target:

- Upstream repository: https://github.com/RICHQAQ/PasteMD
- Upstream tag: `v0.1.6.8`
- Upstream commit: `84b2cea1f291d910d4cf2d0a1fbc829f6bfec524`
- Local portable release: `v0.1.1`

The local package was compared against the upstream source ZIP for `v0.1.6.8`.

## Different Files Committed in This Repository

These files differ from upstream and are committed as source/resource changes:

| Path | Upstream status | Local status |
| --- | --- | --- |
| `pastemd/i18n/locales/en-US.json` | exists | modified |
| `pastemd/i18n/locales/ja-JP.json` | exists | modified |
| `pastemd/i18n/locales/zh-CN.json` | exists | modified |
| `assets/icons/logo.ico` | exists | modified |
| `assets/icons/logo.png` | exists | modified |
| `assets/icons/logo_white.png` | exists | modified |
| `assets/icons/logoTemplate.png` | exists | modified |
| `assets/icons/logo_toast.png` | absent | added |

## Visible Files Compared as Unchanged

These visible runtime files match upstream `v0.1.6.8`:

| Path | Status |
| --- | --- |
| `pastemd/lua/keep-latex-math.lua` | unchanged |
| `pastemd/lua/latex-replacements.lua` | unchanged |

## Packaging-Only Additions

These files are not upstream PasteMD files. They were added for the portable Windows release:

| Path | Purpose |
| --- | --- |
| `MDPASTE.cmd` | user-facing launcher |
| `MdPaste-portable.cmd` | portable startup script |
| `portable-config.ps1` | rewrites portable paths on startup |
| `switch-startup.cmd` | Windows login startup helper |
| `build-release.ps1` | builds the Release ZIP |
| `tools/patch_release_exe.py` | applies the v0.1.1 executable compatibility patch |
| `README.md` | user and maintenance documentation |
| `README.txt` | short user instructions included in ZIP |
| `RELEASE_NOTES.md` | GitHub Release notes |
| `NOTICE.md` | license notice |
| `SOURCE.md` | corresponding source information |
| `MODIFICATIONS.md` | detailed modification list |
| `GITHUB_UPLOAD_STEPS.md` | maintainer upload workflow |

## Limitations

The local portable package does not contain full readable Python source files outside `MdPaste.exe`. The v0.1.1 executable compatibility patch is documented and reproduced by `tools/patch_release_exe.py`.
