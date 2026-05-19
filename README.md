# MDPASTE Portable

> 让 Markdown 从 AI 对话顺畅进入 Word / WPS / Office<br>
> 基于上游 PasteMD 的 Windows 便携封装，内置 Pandoc，可在新电脑上解压即用。

<p align="center">
  <strong>语言 / Languages:</strong><br>
  中文 |
  <a href="./i18n/README.en.md">English</a>
</p>

## MDPASTE是什么

MDPASTE Portable 是一个面向 Windows 的 PasteMD 便携发行包。它用于把复制出来的 Markdown 内容转换成更适合粘贴到 Word、WPS、Office 等软件中的格式。

典型场景：

- 从 AI 对话中复制回答内容。
- 保留标题、列表、代码块、表格、公式等 Markdown 结构。
- 将内容转换后粘贴到文档中，减少手动排版。

本发行包已经内置 Pandoc，用户不需要单独安装 Python、Pandoc 或其他命令行工具。

## 快速开始

1. 打开 GitHub Releases 页面。
2. 下载 `MDPASTE-portable-v0.1.0.0.zip`。
3. 解压到任意文件夹。
4. 双击 `MDPASTE.cmd` 启动。
5. 复制 Markdown 内容后，按默认快捷键 `Ctrl+Alt+B` 进行转换/粘贴。

不要直接双击 `MdPaste.exe`。请使用 `MDPASTE.cmd`，因为它会先准备便携数据目录，并按当前电脑路径自动写入配置。

## 便携机制

每次从 `MDPASTE.cmd` 启动时，程序都会按当前文件夹重写配置：

- `APPDATA` -> `portable-data\Roaming`
- `LOCALAPPDATA` -> `portable-data\Local`
- `pandoc_path` -> 当前文件夹下的 `_internal\pandoc\pandoc.exe`
- `save_dir` -> 当前文件夹下的 `cache`

因此，把整个文件夹复制到另一台 Windows 电脑后，仍然双击 `MDPASTE.cmd` 即可，不需要手动修改路径。

## 主要文件

```text
MDpaste/
├── MDPASTE.cmd                 # 用户启动入口
├── MdPaste-portable.cmd         # 便携启动脚本
├── portable-config.ps1          # 启动时重写本机路径
├── switch-startup.cmd           # 开机自启管理
├── build-release.ps1            # 生成 Release ZIP
├── README.md                    # 中文说明
├── i18n/
│   └── README.en.md             # English README
├── MODIFICATIONS.md             # 相对上游的修改说明
├── UPSTREAM_COMPARISON.md       # 与上游 v0.1.6.8 的对比
├── SOURCE.md                    # 对应源码说明
├── NOTICE.md                    # 许可说明
├── assets/                      # 已提交的修改资源
├── pastemd/                     # 已提交的修改资源
├── MdPaste.exe                  # 上游程序二进制，Release 中分发
└── _internal/                   # 上游运行时和内置 Pandoc，Release 中分发
```

## Pandoc

PasteMD 的文档/富文本转换依赖 Pandoc。本便携包已经把 Pandoc 放在：

```text
_internal\pandoc\pandoc.exe
```

不要删除 `_internal` 目录。如果 Pandoc 缺失，启动脚本会停止并提示重新下载完整 ZIP。

## 本地数据

这些文件会在用户电脑上自动生成：

- 配置文件：`portable-data\Roaming\PasteMD\config.json`
- 日志文件：`portable-data\Roaming\PasteMD\pastemd.log`
- 缓存目录：`cache`

这些是本机运行数据，不提交到 Git，也不会打入干净的发布 ZIP。

## 相对上游的修改

代码和资源修改说明主要看这两个文件：

- `MODIFICATIONS.md`：逐项说明本仓库相对上游新增或修改了哪些文件，以及每个脚本/资源文件的作用。
- `UPSTREAM_COMPARISON.md`：列出与上游 PasteMD `v0.1.6.8` 对比后确认发生变化的文件。

本仓库已提交从本地发行包中识别出的上游资源修改：

- `pastemd/i18n/locales` 下的语言文件。
- `assets/icons` 下的图标文件。

本仓库还新增了便携封装相关内容：

- `MDPASTE.cmd`
- `MdPaste-portable.cmd`
- `portable-config.ps1`
- `switch-startup.cmd`
- `build-release.ps1`
- 说明文档、许可文件和源码对比文件。

如果发布的 `MdPaste.exe` 中还包含 Python 逻辑修改，则需要继续补充用于构建该二进制的对应修改源码。

## 版本维护

如果发行版本发生变化，需要同步修改以下位置：

- `README.md` 和 `i18n/README.en.md` 中的下载文件名。
- `RELEASE_NOTES.md` 中的版本号和附件名。
- `SOURCE.md` 中对应的上游 tag、commit 和源码链接。
- `build-release.ps1` 中的默认 `$Version`。
- Git tag，例如 `v0.1.0.0`。
- GitHub Release 标题、说明和附件 ZIP 名称。

版本号不一致会导致用户下载说明、Release 附件和源码说明互相对不上，所以每次发布新版本都应统一检查。

## 发布

本地生成发布 ZIP：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build-release.ps1
```

输出文件：

```text
dist\MDPASTE-portable-v0.1.0.0.zip
```

完整可运行包通过 GitHub Release 附件发布。Git 仓库只保存启动脚本、打包脚本、说明文档、许可证、源码说明和已识别的修改资源。

## Codex 声明

本仓库中的便携启动脚本、路径配置脚本、打包脚本、README、Release notes、NOTICE、SOURCE、MODIFICATIONS 和 UPSTREAM_COMPARISON 说明由 OpenAI Codex 在与项目维护者的对话过程中辅助撰写和整理。

上游 PasteMD 程序本体不属于 Codex 创作内容。

## 上游项目和许可

上游项目：<https://github.com/RICHQAQ/PasteMD>

本便携封装发行版本为 `v0.1.0.0`。它重新分发的上游 PasteMD 对应版本为 `v0.1.6.8`：<https://github.com/RICHQAQ/PasteMD/tree/v0.1.6.8>

PasteMD 采用 AGPL-3.0 许可。本仓库是对 PasteMD Windows 便携包的再分发/封装，仓库内启动脚本和打包文件也按 AGPL-3.0 发布。发布时请保留 `LICENSE`、`NOTICE.md` 和 `SOURCE.md`。
