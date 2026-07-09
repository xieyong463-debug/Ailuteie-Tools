"""表格字段结构 / Table schemas."""

from __future__ import annotations

PRODUCT_MASTER_CN_HEADERS = [
    "唯一货号",
    "SKU名称",
    "产品卖点/说明",
    "竞品链接1",
    "竞品链接2",
    "竞品链接3",
    "颜色",
    "尺寸",
]

PRODUCT_MASTER_COLUMNS = [
    "product_id",
    "sku_name",
    "seller_notes",
    "competitor_link_1",
    "competitor_link_2",
    "competitor_link_3",
    "color",
    "size",
]

RESEARCH_SUMMARY_CN_HEADERS = [
    "唯一货号",
    "SKU数量",
    "颜色汇总",
    "尺寸汇总",
    "用户卖点摘要",
    "图片识别摘要",
    "竞品摘要",
    "建议产品定位",
    "建议词库",
    "建议类目值",
    "风险提醒",
    "需要人工确认",
    "审核状态",
]

RESEARCH_SUMMARY_COLUMNS = [
    "product_id",
    "sku_count",
    "colors",
    "sizes",
    "seller_notes_summary",
    "image_summary",
    "competitor_summary",
    "recommended_positioning",
    "suggested_keyword_library",
    "suggested_item_type_keyword",
    "risk_summary",
    "needs_manual_confirmation",
    "review_status",
]

SELLING_POINTS_CN_HEADERS = [
    "唯一货号",
    "来源",
    "卖点内容",
    "是否建议使用",
    "优先级",
    "适合使用位置",
    "原因",
    "风险等级",
    "是否需要确认",
    "人工备注",
]

SELLING_POINTS_COLUMNS = [
    "product_id",
    "source",
    "selling_point",
    "recommended_use",
    "priority",
    "suggested_position",
    "reason",
    "risk_level",
    "needs_confirmation",
    "manual_note",
]

COMPETITOR_REFERENCE_CN_HEADERS = [
    "唯一货号",
    "竞品序号",
    "竞品链接",
    "竞品标题摘要",
    "竞品主卖点",
    "可借鉴方向",
    "不建议借鉴",
    "备注",
]

COMPETITOR_REFERENCE_COLUMNS = [
    "product_id",
    "competitor_no",
    "competitor_link",
    "competitor_title_summary",
    "competitor_key_points",
    "usable_reference",
    "avoid_reference",
    "notes",
]

APPROVED_PRODUCT_INFO_CN_HEADERS = [
    "唯一货号",
    "SKU名称",
    "颜色",
    "尺寸",
    "使用词库",
    "亚马逊类目值",
    "产品类型",
    "面料/外套材质",
    "填充材质",
    "核心卖点",
    "禁用卖点/禁用表达",
    "是否专利申请中",
    "是否可拆洗",
    "是否真空压缩",
    "回弹时间",
    "适用场景",
    "审核状态",
    "人工备注",
]

APPROVED_PRODUCT_INFO_COLUMNS = [
    "product_id",
    "sku_name",
    "color",
    "size",
    "keyword_library",
    "item_type_keyword",
    "product_type",
    "cover_material",
    "filling_material",
    "confirmed_selling_points",
    "avoid_points",
    "patent_pending",
    "washable_cover",
    "vacuum_packed",
    "recovery_time",
    "allowed_scenarios",
    "review_status",
    "manual_notes",
]

LISTING_CONTENT_CN_HEADERS = [
    "唯一货号",
    "SKU名称",
    "父子层级",
    "颜色",
    "尺寸",
    "标题75字符",
    "Item Name字符数",
    "产品亮点125字符",
    "Item Highlight字符数",
    "五点1",
    "五点2",
    "五点3",
    "五点4",
    "五点5",
    "产品描述",
    "ST关键词",
    "ST字符数",
    "使用关键词备注",
    "审核状态",
    "人工备注",
]

LISTING_CONTENT_COLUMNS = [
    "product_id",
    "sku_name",
    "parentage_level",
    "color",
    "size",
    "item_name_75",
    "item_name_char_count",
    "item_highlight_125",
    "item_highlight_char_count",
    "bullet_1",
    "bullet_2",
    "bullet_3",
    "bullet_4",
    "bullet_5",
    "product_description",
    "search_terms",
    "search_terms_char_count",
    "keyword_notes",
    "review_status",
    "manual_notes",
]

AMAZON_REQUIRED_FIELDS_CN_HEADERS = [
    "唯一货号",
    "SKU名称",
    "父子层级",
    "亚马逊类目值",
    "模板列",
    "Amazon字段显示名",
    "Amazon实际字段名",
    "字段来源",
    "Parent是否需要",
    "Child是否需要",
    "最终值",
    "是否缺失",
    "审核状态",
    "人工备注",
]

AMAZON_REQUIRED_FIELDS_COLUMNS = [
    "product_id",
    "sku_name",
    "parentage_level",
    "item_type_keyword",
    "template_column",
    "amazon_display_name",
    "amazon_attribute_name",
    "field_source",
    "required_for_parent",
    "required_for_child",
    "final_value",
    "is_missing",
    "review_status",
    "manual_notes",
]

MISSING_FIELDS_CHECK_CN_HEADERS = [
    "唯一货号",
    "SKU名称",
    "父子层级",
    "缺失字段",
    "Amazon实际字段名",
    "原因",
    "建议处理方式",
]

MISSING_FIELDS_CHECK_COLUMNS = [
    "product_id",
    "sku_name",
    "parentage_level",
    "missing_field",
    "amazon_attribute_name",
    "reason",
    "suggested_fix",
]
