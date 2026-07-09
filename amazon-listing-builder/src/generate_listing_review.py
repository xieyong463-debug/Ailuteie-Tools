"""listing_review.xlsx 生成入口。

后续 listing_review.xlsx 不只是文案审核表，还需要匹配 Amazon 上传模板必填字段。
建议包含：
- listing_content
- amazon_required_fields
- missing_fields_check
"""

from __future__ import annotations

from .config import REVIEW_STATUS_APPROVED, REVIEW_STATUS_NEED_REVIEW
from .paths import get_paths


def generate_listing_review(product_id: str) -> None:
    paths = get_paths()
    output_path = paths.listing_review_path(product_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError(
        "generate_listing_review 框架已预留。后续只处理 approved_product_info.xlsx 中 "
        f"review_status={REVIEW_STATUS_APPROVED} 的 SKU，输出默认 {REVIEW_STATUS_NEED_REVIEW}。"
    )
