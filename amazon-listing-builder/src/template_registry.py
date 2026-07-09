"""三类 Amazon 上传模板样本映射 / Upload template registry.

用户已提供三个类目模板样本：
- YK-117：阅读用靠垫枕，reading-pillows
- CTZ-039：身体枕，body-pillows
- YK-132：腰椎枕，lumbar-pillows

这些模板中第7行 Parent 和第8行 Child 已填写字段，后续视为对应类目的必填字段样本。
"""

from __future__ import annotations

TEMPLATE_REGISTRY = {
    "reading-pillows": {
        "sample_product_id": "YK-117",
        "product_direction_cn": "阅读用靠垫枕",
        "product_direction_en": "Reading Pillow",
        "template_filename": "reading_pillows_template_yk117.xlsm",
        "source_upload_filename": "yk-117.xlsm",
        "rule_cn": "模板中第7行 Parent 和第8行 Child 已填写字段，后续视为 reading-pillows 必填字段样本。",
    },
    "body-pillows": {
        "sample_product_id": "CTZ-039",
        "product_direction_cn": "身体枕",
        "product_direction_en": "Body Pillow",
        "template_filename": "body_pillows_template_ctz039.xlsm",
        "source_upload_filename": "ctz-039.xlsm",
        "rule_cn": "模板中第7行 Parent 和第8行 Child 已填写字段，后续视为 body-pillows 必填字段样本。",
    },
    "lumbar-pillows": {
        "sample_product_id": "YK-132",
        "product_direction_cn": "腰椎枕",
        "product_direction_en": "Lumbar Pillow",
        "template_filename": "lumbar_pillows_template_yk132.xlsm",
        "source_upload_filename": "yk-132..xlsm",
        "rule_cn": "模板中第7行 Parent 和第8行 Child 已填写字段，后续视为 lumbar-pillows 必填字段样本。",
    },
}
