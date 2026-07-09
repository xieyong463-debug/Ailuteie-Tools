"""项目固定配置 / Project configuration."""

from __future__ import annotations

PROJECT_NAME = "amazon-listing-builder"

# Excel 统一读取规则：第一行中文说明，第二行英文字段名，第三行开始数据。
CN_HEADER_ROW = 0
EN_HEADER_ROW = 1
DATA_START_ROW = 2

DEFAULT_MASTER_SHEET = "master"
DEFAULT_APPROVED_INFO_SHEET = "approved_info"
DEFAULT_LISTING_CONTENT_SHEET = "listing_content"

REVIEW_STATUS_NEED_REVIEW = "need_review"
REVIEW_STATUS_APPROVED = "approved"
REVIEW_STATUS_REJECTED = "rejected"

ALLOWED_REVIEW_STATUS = {
    REVIEW_STATUS_NEED_REVIEW,
    REVIEW_STATUS_APPROVED,
    REVIEW_STATUS_REJECTED,
}

ALLOWED_ITEM_TYPE_KEYWORDS = {
    "reading-pillows",
    "body-pillows",
    "lumbar-pillows",
}

ALLOWED_KEYWORD_LIBRARIES = {
    "back_pillow",
    "body_pillow",
}

# 当前已确认：Amazon 上传模板填充模块暂缓。
ENABLE_AMAZON_UPLOAD_GENERATION = False
