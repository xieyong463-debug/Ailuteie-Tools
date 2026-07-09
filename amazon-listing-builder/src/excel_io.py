"""Excel 读取写入工具 / Excel I/O helpers.

项目统一规则：
- 第一行：中文说明
- 第二行：英文字段名
- 第三行开始：正式数据
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import EN_HEADER_ROW


def read_table_with_english_header(path: Path, sheet_name: str) -> pd.DataFrame:
    """读取第一行中文、第二行英文字段名的 Excel 表。"""
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")
    df = pd.read_excel(path, sheet_name=sheet_name, header=EN_HEADER_ROW, engine="openpyxl")
    df = df.dropna(how="all")
    df.columns = [str(col).strip() for col in df.columns]
    return df


def normalize_text(value: object) -> str:
    """把单元格值安全转成去空格文本。"""
    if value is None:
        return ""
    if pd.isna(value):
        return ""
    return str(value).strip()


def unique_nonempty(values: Iterable[object]) -> list[str]:
    """按原顺序保留唯一非空文本。"""
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = normalize_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def write_two_header_excel(
    path: Path,
    sheet_name: str,
    cn_headers: list[str],
    en_headers: list[str],
    rows: list[dict[str, object]] | None = None,
) -> None:
    """写出第一行中文说明、第二行英文字段名的 Excel 文件。"""
    rows = rows or []
    path.parent.mkdir(parents=True, exist_ok=True)
    data_rows = [[row.get(col, "") for col in en_headers] for row in rows]
    table = [cn_headers, en_headers, *data_rows]
    df = pd.DataFrame(table)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
