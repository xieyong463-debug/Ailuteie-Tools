"""approved_product_info.xlsx 生成入口。

当前先保留框架入口。后续由 Codex 根据 selling_points_research.xlsx 和模板必填字段
生成产品事实审核表初稿，默认 review_status = need_review。
"""

from __future__ import annotations

from .config import REVIEW_STATUS_NEED_REVIEW
from .paths import get_paths


def generate_approved_product_info(product_id: str) -> None:
    paths = get_paths()
    output_path = paths.approved_product_info_path(product_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError(
        f"generate_approved_product_info 框架已预留，后续生成初稿时默认 review_status={REVIEW_STATUS_NEED_REVIEW}。"
    )
