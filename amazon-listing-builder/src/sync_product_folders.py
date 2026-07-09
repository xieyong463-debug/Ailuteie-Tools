"""同步产品文件夹 / Sync product folders.

第一段实际执行代码：
读取 product_master.xlsx，按 product_id 去重，自动创建产品图片、审核、输出文件夹。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .config import DEFAULT_MASTER_SHEET
from .excel_io import normalize_text, read_table_with_english_header, unique_nonempty
from .paths import ProjectPaths, get_paths
from .schemas import PRODUCT_MASTER_COLUMNS
from .validators import issues_to_text, validate_product_master_rows, validate_required_columns


@dataclass
class FolderSyncResult:
    sku_row_count: int = 0
    unique_product_ids: list[str] = field(default_factory=list)
    created_dirs: list[str] = field(default_factory=list)
    existing_dirs: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    def to_log(self) -> str:
        lines = [
            "sync_product_folders 执行结果",
            "=" * 40,
            f"读取到 SKU 行数: {self.sku_row_count}",
            f"识别到唯一 product_id 数量: {len(self.unique_product_ids)}",
            "",
            "唯一 product_id:",
            *(f"- {pid}" for pid in self.unique_product_ids),
            "",
            f"新创建文件夹数量: {len(self.created_dirs)}",
            *(f"- {p}" for p in self.created_dirs),
            "",
            f"已存在文件夹数量: {len(self.existing_dirs)}",
            *(f"- {p}" for p in self.existing_dirs),
        ]
        if self.issues:
            lines.extend(["", "校验提醒:", *self.issues])
        return "\n".join(lines)


def _mkdir(path: Path, result: FolderSyncResult) -> None:
    if path.exists():
        result.existing_dirs.append(str(path))
        return
    path.mkdir(parents=True, exist_ok=True)
    result.created_dirs.append(str(path))


def sync_product_folders(paths: ProjectPaths | None = None) -> FolderSyncResult:
    """读取 product_master.xlsx 并创建 product_id 对应目录。"""
    paths = paths or get_paths()
    df = read_table_with_english_header(paths.product_master_path, DEFAULT_MASTER_SHEET)
    result = FolderSyncResult(sku_row_count=len(df))

    issues = []
    issues.extend(validate_required_columns(df, PRODUCT_MASTER_COLUMNS))
    if issues:
        result.issues.append(issues_to_text(issues))
        return result

    row_issues = validate_product_master_rows(df)
    if row_issues:
        result.issues.append(issues_to_text(row_issues))

    product_ids = unique_nonempty(df["product_id"])
    result.unique_product_ids = product_ids

    for product_id in product_ids:
        clean_product_id = normalize_text(product_id)
        _mkdir(paths.product_image_dir(clean_product_id), result)
        _mkdir(paths.product_review_dir(clean_product_id), result)
        _mkdir(paths.product_output_dir(clean_product_id), result)

    return result


def main() -> None:
    result = sync_product_folders()
    print(result.to_log())


if __name__ == "__main__":
    main()
