import marshal
import os
import shutil
import struct
import sys
import tempfile
import zlib
from pathlib import Path


OLD_FENCED_PATTERN = r"(^|\n)(```|~~~).*?(?:\n\2.*?$)"
NEW_CODE_BLOCK_PATTERN = (
    r"(^|\n)(?:(`{3,}|~{3,})[^\n]*(?:\n.*?)*?\n\2[ \t]*(?=\n|$)"
    r"|(?:[ \t]{4}|\t)[^\n]*(?:\n(?:[ \t]{4}|\t)[^\n]*)*)"
    r"|(`+)[^\n]*?\3"
)

PATCHED_CONVERT_LATEX_SOURCE = r'''
def convert_latex_delimiters(
    text: str,
    fix_single_dollar_block: bool = True,
    convert_standard_delimiters: bool = False,
) -> str:
    """
    Preprocess LaTeX delimiters while keeping code blocks and inline code literal.
    """

    def process_segment(segment: str) -> str:
        segment = _unwrap_blockquoted_math(segment)
        segment = _convert_bare_bracket_display_math(segment)

        if convert_standard_delimiters:
            segment = _convert_standard_latex_delimiters(segment)

        segment = _convert_plain_parenthesized_math(segment)

        if fix_single_dollar_block:
            segment = _fix_inline_math_spaces(segment)
            segment = _fix_single_dollar_blocks(segment)

        segment = _normalize_inline_math_segments(segment)
        return _normalize_display_math_blocks(segment)

    return _process_outside_code_blocks(text, process_segment)
'''

PATCHED_SHOULD_PREFER_CLIPBOARD_TEXT_SOURCE = r'''
def should_prefer_clipboard_text(html: str, text: str) -> bool:
    """
    Prefer plaintext only when it really preserves Markdown/math structure.

    ChatGPT fragment copy exposes rich HTML for code blocks, while the Unicode
    text clipboard format drops the Markdown fences. In that case HTML must win
    so Pandoc can reconstruct fenced code blocks.
    """
    if not text:
        return False

    lowered_html = (html or "").lower()
    has_html_code = (
        "<pre" in lowered_html
        or "<code" in lowered_html
        or "code-block-viewer" in lowered_html
        or "cm-content" in lowered_html
    )
    text_has_fence = "```" in text or "~~~" in text
    if has_html_code and not text_has_fence:
        return False

    if not (is_markdown(text) or has_latex_math(text) or has_parenthesized_math(text)):
        return False

    soup = _parse_html(html)
    if (
        soup is not None
        and _has_semantic_math_nodes(soup)
        and is_fragmented_math_text(text)
    ):
        log("Clipboard text looks math-like but fragmented; HTML keeps semantic math, using HTML path")
        return False

    return True
'''

PYZ_MAGIC = b"PYZ\0"
PYZ_HEADER_LEN = 17
CARCHIVE_COOKIE_MAGIC = b"MEI\014\013\012\013\016"
CARCHIVE_COOKIE_FORMAT = "!8sIIII64s"
CARCHIVE_COOKIE_LEN = struct.calcsize(CARCHIVE_COOKIE_FORMAT)
CARCHIVE_TOC_ENTRY_FORMAT = "!IIIIBc"
CARCHIVE_TOC_ENTRY_LEN = struct.calcsize(CARCHIVE_TOC_ENTRY_FORMAT)


def replace_const(code, old, new):
    changed = False
    consts = []
    for const in code.co_consts:
        if const == old:
            consts.append(new)
            changed = True
        elif hasattr(const, "co_consts"):
            patched, sub_changed = replace_const(const, old, new)
            consts.append(patched)
            changed = changed or sub_changed
        else:
            consts.append(const)
    if changed:
        return code.replace(co_consts=tuple(consts)), True
    return code, False


def replace_code_object(code, target_name, replacement):
    changed = False
    consts = []
    for const in code.co_consts:
        if getattr(const, "co_name", None) == target_name:
            consts.append(replacement)
            changed = True
        elif hasattr(const, "co_consts"):
            patched, sub_changed = replace_code_object(const, target_name, replacement)
            consts.append(patched)
            changed = changed or sub_changed
        else:
            consts.append(const)
    if changed:
        return code.replace(co_consts=tuple(consts)), True
    return code, False


def compile_replacement_function(source, name):
    namespace = {}
    exec(compile(source, f"<pastemd patch:{name}>", "exec"), namespace)
    return namespace[name].__code__


def read_pyz(path):
    data = path.read_bytes()
    if data[:4] != PYZ_MAGIC:
        raise RuntimeError(f"Not a PYZ archive: {path}")
    py_magic = data[4:8]
    toc_offset = struct.unpack("!i", data[8:12])[0]
    toc = marshal.loads(data[toc_offset:])
    return data, py_magic, toc


def extract_pyz_entry(data, entry):
    typecode, offset, length = entry
    raw = data[offset : offset + length]
    if typecode == 3:
        return None
    return zlib.decompress(raw)


def write_pyz(path, py_magic, original_data, toc, patched_code):
    output = bytearray(b"\0" * PYZ_HEADER_LEN)
    new_toc = []

    for name, entry in toc:
        typecode, _offset, _length = entry
        offset = len(output)
        if name in patched_code:
            raw_data = marshal.dumps(patched_code[name])
            blob = zlib.compress(raw_data, 6)
        else:
            raw_data = extract_pyz_entry(original_data, entry)
            blob = b"" if raw_data is None else zlib.compress(raw_data, 6)
        output.extend(blob)
        new_toc.append((name, (typecode, offset, len(blob))))

    toc_offset = len(output)
    output.extend(marshal.dumps(new_toc))
    output[0:4] = PYZ_MAGIC
    output[4:8] = py_magic
    output[8:12] = struct.pack("!i", toc_offset)
    path.write_bytes(output)


def find_carchive_cookie(data):
    offset = data.rfind(CARCHIVE_COOKIE_MAGIC)
    if offset < 0:
        raise RuntimeError("Could not find PyInstaller CArchive cookie")
    cookie = data[offset : offset + CARCHIVE_COOKIE_LEN]
    magic, archive_len, toc_offset, toc_len, pyvers, pylib = struct.unpack(
        CARCHIVE_COOKIE_FORMAT, cookie
    )
    start = offset + CARCHIVE_COOKIE_LEN - archive_len
    end = offset + CARCHIVE_COOKIE_LEN
    pylib = pylib.split(b"\0", 1)[0].decode("ascii")
    return start, end, toc_offset, toc_len, pyvers, pylib


def parse_carchive_toc(data, start, toc_offset, toc_len):
    toc_data = data[start + toc_offset : start + toc_offset + toc_len]
    pos = 0
    entries = []
    while pos < len(toc_data):
        header = toc_data[pos : pos + CARCHIVE_TOC_ENTRY_LEN]
        entry_len, offset, length, uncompressed, compressed, typecode = struct.unpack(
            CARCHIVE_TOC_ENTRY_FORMAT, header
        )
        name_bytes = toc_data[pos + CARCHIVE_TOC_ENTRY_LEN : pos + entry_len]
        name = name_bytes.split(b"\0", 1)[0].decode("utf-8")
        entries.append(
            {
                "name": name,
                "offset": offset,
                "length": length,
                "uncompressed": uncompressed,
                "compressed": compressed,
                "typecode": typecode.decode("ascii"),
            }
        )
        pos += entry_len
    return entries


def extract_carchive_entry(exe_data, start, entry):
    blob = exe_data[start + entry["offset"] : start + entry["offset"] + entry["length"]]
    return zlib.decompress(blob) if entry["compressed"] else blob


def write_carchive(path, entries, pylib_name):
    toc = []
    with path.open("wb") as fp:
        for entry in entries:
            offset = fp.tell()
            raw = Path(entry["src"]).read_bytes()
            if entry["compressed"]:
                blob = zlib.compress(raw, 9)
            else:
                blob = raw
            fp.write(blob)
            toc.append(
                {
                    "name": entry["name"],
                    "offset": offset,
                    "length": len(blob),
                    "uncompressed": len(raw),
                    "compressed": 1 if entry["compressed"] else 0,
                    "typecode": entry["typecode"],
                }
            )

        toc_offset = fp.tell()
        for item in toc:
            name = item["name"].encode("utf-8") + b"\0"
            entry_len = CARCHIVE_TOC_ENTRY_LEN + len(name)
            padding = (16 - (entry_len % 16)) % 16
            entry_len += padding
            fp.write(
                struct.pack(
                    CARCHIVE_TOC_ENTRY_FORMAT,
                    entry_len,
                    item["offset"],
                    item["length"],
                    item["uncompressed"],
                    item["compressed"],
                    item["typecode"].encode("ascii"),
                )
            )
            fp.write(name)
            fp.write(b"\0" * padding)

        toc_len = fp.tell() - toc_offset
        archive_len = toc_offset + toc_len + CARCHIVE_COOKIE_LEN
        pyvers = sys.version_info[0] * 100 + sys.version_info[1]
        fp.write(
            struct.pack(
                CARCHIVE_COOKIE_FORMAT,
                CARCHIVE_COOKIE_MAGIC,
                archive_len,
                toc_offset,
                toc_len,
                pyvers,
                pylib_name.encode("ascii"),
            )
        )


def main():
    root = Path(__file__).resolve().parents[1]
    exe = root / "MdPaste.exe"
    backup = root / "MdPaste.exe.before-codeblock-patch"
    work = root / "exe-extract-tmp"
    pyz_path = work / "PYZ.pyz"
    patched_pyz = work / "PYZ.patched.pyz"

    if not exe.exists():
        raise RuntimeError(f"Missing exe: {exe}")

    if not backup.exists():
        shutil.copy2(exe, backup)

    work.mkdir(parents=True, exist_ok=True)
    exe_data = exe.read_bytes()
    start, end, toc_offset, toc_len, _pyvers, pylib = find_carchive_cookie(exe_data)
    c_entries = parse_carchive_toc(exe_data, start, toc_offset, toc_len)
    pyz_entry = next((entry for entry in c_entries if entry["name"] == "PYZ.pyz"), None)
    if pyz_entry is None:
        raise RuntimeError("Could not find PYZ.pyz in MdPaste.exe")
    pyz_path.write_bytes(extract_carchive_entry(exe_data, start, pyz_entry))

    original_pyz, py_magic, pyz_toc = read_pyz(pyz_path)
    toc_dict = dict(pyz_toc)
    latex_code = marshal.loads(extract_pyz_entry(original_pyz, toc_dict["pastemd.utils.latex"]))
    latex_code, regex_changed = replace_const(
        latex_code, OLD_FENCED_PATTERN, NEW_CODE_BLOCK_PATTERN
    )
    if not regex_changed:
        raise RuntimeError("Did not find target fenced-code regex constant")
    replacement = compile_replacement_function(
        PATCHED_CONVERT_LATEX_SOURCE, "convert_latex_delimiters"
    )
    latex_code, function_changed = replace_code_object(
        latex_code, "convert_latex_delimiters", replacement
    )
    if not function_changed:
        raise RuntimeError("Did not find convert_latex_delimiters code object")

    html_analyzer_code = marshal.loads(
        extract_pyz_entry(original_pyz, toc_dict["pastemd.utils.html_analyzer"])
    )
    replacement = compile_replacement_function(
        PATCHED_SHOULD_PREFER_CLIPBOARD_TEXT_SOURCE,
        "should_prefer_clipboard_text",
    )
    html_analyzer_code, preference_changed = replace_code_object(
        html_analyzer_code, "should_prefer_clipboard_text", replacement
    )
    if not preference_changed:
        raise RuntimeError("Did not find should_prefer_clipboard_text code object")

    write_pyz(
        patched_pyz,
        py_magic,
        original_pyz,
        pyz_toc,
        {
            "pastemd.utils.latex": latex_code,
            "pastemd.utils.html_analyzer": html_analyzer_code,
        },
    )

    prefix = exe_data[:start]

    with tempfile.TemporaryDirectory(prefix="pastemd-patch-") as tmp:
        tmp_path = Path(tmp)
        writer_entries = []
        for entry in c_entries:
            src = tmp_path / entry["name"].replace("\\", "_").replace("/", "_")
            if entry["name"] == "PYZ.pyz":
                shutil.copy2(patched_pyz, src)
                compressed = False
            else:
                raw = extract_carchive_entry(exe_data, start, entry)
                src.write_bytes(raw)
                compressed = bool(entry["compressed"])
            writer_entries.append(
                {
                    "name": entry["name"],
                    "src": src,
                    "compressed": compressed,
                    "typecode": entry["typecode"],
                }
            )

        archive_path = tmp_path / "patched.pkg"
        write_carchive(archive_path, writer_entries, pylib)
        exe.write_bytes(prefix + archive_path.read_bytes())

    print(f"patched {exe}")
    print(f"backup  {backup}")


if __name__ == "__main__":
    main()
