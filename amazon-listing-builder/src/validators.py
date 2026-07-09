"""基础校验工具 / Validation helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass

import pandas as pd

from .excel_io import normalize_text


@dataclass(frozen=True)
class ValidationIssue:
    row_number: int | None
    field: str
    message: str
    value: str = ""


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> list[ValidationIssue]:
    """检查是否缺少必填列。"""
    issues: list[ValidationIssue] = []
    columns = set(df.columns)
    for col in required_columns:
        if col not in columns:
            issues.append(ValidationIssue(None, col, f"缺少必填字段: {col}"))
    return issues


def validate_product_master_rows(df: pd.DataFrame) -> list[ValidationIssue]:
    """检查 product_master.xlsx 的基础数据问题。"""
    issues: list[ValidationIssue] = []
    for idx, row in df.iterrows():
        excel_row = int(idx) + 3  # 第一行中文，第二行英文，第三行开始数据
        product_id = normalize_text(row.get("product_id"))
        sku_name = normalize_text(row.get("sku_name"))
        if not product_id:
            issues.append(ValidationIssue(excel_row, "product_id", "product_id 为空，已忽略该行"))
            continue
        if not re.match(r"^[A-Za-z0-9_.\-]+$", product_id):
            issues.append(
                ValidationIssue(
                    excel_row,
                    "product_id",
                    "product_id 建议只使用英文、数字、下划线、短横线或点号",
                    product_id,
                )
            )
        if not sku_name:
            issues.append(ValidationIssue(excel_row, "sku_name", "sku_name 为空，后续生成 Listing 可能缺少 SKU 名称", product_id))
    return issues


def issues_to_text(issues: list[ValidationIssue]) -> str:
    """把校验问题转成日志文本。"""
    if not issues:
        return "未发现基础校验问题。"
    lines = []
    for issue in issues:
        prefix = f"第 {issue.row_number} 行" if issue.row_number else "表头"
        value_part = f"；当前值: {issue.value}" if issue.value else ""
        lines.append(f"- {prefix} [{issue.field}] {issue.message}{value_part}")
    return "\n".join(lines)
