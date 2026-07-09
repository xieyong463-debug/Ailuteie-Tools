"""Amazon 上传模板字段分析 / Template analyzer.

用途：
读取用户提供的三份 Amazon 上传模板样本，识别 Template 表第7行 Parent 和第8行 Child
已经填写过的字段，并把这些字段作为对应 item_type_keyword 的必填字段样本。

说明：
这里不依赖 openpyxl 读取模板内容，而是直接解析 xlsm/xlsx 的 XML 结构，方便读取宏模板。
"""

from __future__ import annotations

import json
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from .paths import ProjectPaths, get_paths
from .template_registry import TEMPLATE_REGISTRY

NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}

TEMPLATE_SHEET_NAME = "Template"
DISPLAY_NAME_ROW = 4
ATTRIBUTE_NAME_ROW = 5
PARENT_SAMPLE_ROW = 7
CHILD_SAMPLE_ROW = 8


def col_to_num(col: str) -> int:
    n = 0
    for char in col.upper():
        n = n * 26 + ord(char) - 64
    return n


def num_to_col(n: int) -> str:
    text = ""
    while n:
        n, remainder = divmod(n - 1, 26)
        text = chr(65 + remainder) + text
    return text


def cell_ref_to_rc(ref: str) -> tuple[int, int]:
    match = re.match(r"([A-Z]+)(\d+)", ref)
    if not match:
        raise ValueError(f"无法解析单元格引用: {ref}")
    return int(match.group(2)), col_to_num(match.group(1))


def _read_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for si in root.findall("main:si", NS):
        texts = [node.text or "" for node in si.iter(f"{{{NS['main']}}}t")]
        strings.append("".join(texts))
    return strings


def _get_sheet_path(zf: zipfile.ZipFile, sheet_name: str) -> str:
    workbook_root = ET.fromstring(zf.read("xl/workbook.xml"))
    rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels_root.findall("pkgrel:Relationship", NS)
    }
    for sheet in workbook_root.find("main:sheets", NS).findall("main:sheet", NS):
        if sheet.attrib["name"] != sheet_name:
            continue
        rel_id = sheet.attrib[f"{{{NS['rel']}}}id"]
        target = rel_map[rel_id]
        if target.startswith("/"):
            return target.lstrip("/")
        return f"xl/{target}".replace("xl//", "xl/")
    raise ValueError(f"找不到工作表: {sheet_name}")


def extract_sheet_values(workbook_path: Path, sheet_name: str = TEMPLATE_SHEET_NAME) -> dict[str, str]:
    """从 xlsm/xlsx 中提取指定工作表的单元格文本值。"""
    values: dict[str, str] = {}
    with zipfile.ZipFile(workbook_path) as zf:
        shared_strings = _read_shared_strings(zf)
        sheet_path = _get_sheet_path(zf, sheet_name)
        root = ET.fromstring(zf.read(sheet_path))
        for cell in root.iter(f"{{{NS['main']}}}c"):
            ref = cell.attrib.get("r")
            if not ref:
                continue
            cell_type = cell.attrib.get("t")
            value_node = cell.find("main:v", NS)
            inline_node = cell.find("main:is", NS)
            value = ""
            if cell_type == "s" and value_node is not None and value_node.text is not None:
                index = int(value_node.text)
                value = shared_strings[index] if index < len(shared_strings) else ""
            elif cell_type == "inlineStr" and inline_node is not None:
                value = "".join(node.text or "" for node in inline_node.iter(f"{{{NS['main']}}}t"))
            elif value_node is not None and value_node.text is not None:
                value = value_node.text
            values[ref] = value.strip() if isinstance(value, str) else str(value).strip()
    return values


def analyze_upload_template(workbook_path: Path, item_type_keyword: str) -> dict[str, Any]:
    """分析单个上传模板样本，返回必填字段样本。"""
    values = extract_sheet_values(workbook_path, TEMPLATE_SHEET_NAME)
    required_fields: list[dict[str, Any]] = []
    max_col = max((cell_ref_to_rc(ref)[1] for ref in values), default=0)

    for col_index in range(1, max_col + 1):
        col = num_to_col(col_index)
        display_name = values.get(f"{col}{DISPLAY_NAME_ROW}", "")
        attribute_name = values.get(f"{col}{ATTRIBUTE_NAME_ROW}", "")
        parent_sample_value = values.get(f"{col}{PARENT_SAMPLE_ROW}", "")
        child_sample_value = values.get(f"{col}{CHILD_SAMPLE_ROW}", "")
        required_for_parent = bool(parent_sample_value)
        required_for_child = bool(child_sample_value)
        if not required_for_parent and not required_for_child:
            continue
        required_fields.append(
            {
                "template_column": col,
                "amazon_display_name": display_name,
                "amazon_attribute_name": attribute_name,
                "required_for_parent": required_for_parent,
                "required_for_child": required_for_child,
                "parent_sample_value": parent_sample_value,
                "child_sample_value": child_sample_value,
            }
        )

    return {
        "item_type_keyword": item_type_keyword,
        "template_path": str(workbook_path),
        "required_field_count_union": len(required_fields),
        "parent_required_count": sum(1 for field in required_fields if field["required_for_parent"]),
        "child_required_count": sum(1 for field in required_fields if field["required_for_child"]),
        "required_fields": required_fields,
    }


def analyze_all_upload_templates(paths: ProjectPaths | None = None) -> dict[str, Any]:
    """分析 registry 中登记的三类模板。"""
    paths = paths or get_paths()
    result: dict[str, Any] = {
        "note_cn": "用户提供的三个 Amazon 上传模板样本中，第7行 Parent 和第8行 Child 已填写字段，后续视为对应 item_type_keyword 的必填字段样本。",
        "note_en": "Fields filled in row 7 Parent and row 8 Child of the three sample Amazon upload templates are treated as required field samples for each item_type_keyword.",
        "categories": {},
    }
    for item_type_keyword, meta in TEMPLATE_REGISTRY.items():
        template_path = paths.amazon_templates_dir / meta["template_filename"]
        if not template_path.exists():
            result["categories"][item_type_keyword] = {
                **meta,
                "template_path": str(template_path),
                "status": "missing_template_file",
                "required_fields": [],
            }
            continue
        analysis = analyze_upload_template(template_path, item_type_keyword)
        result["categories"][item_type_keyword] = {
            **meta,
            "status": "analyzed",
            **analysis,
        }
    return result


def save_required_fields_json(data: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    paths = get_paths()
    data = analyze_all_upload_templates(paths)
    save_required_fields_json(data, paths.template_required_fields_json)
    print(f"已生成: {paths.template_required_fields_json}")
    for item_type_keyword, category in data["categories"].items():
        print(
            item_type_keyword,
            category.get("status"),
            "字段数:",
            category.get("required_field_count_union", 0),
        )


if __name__ == "__main__":
    main()
