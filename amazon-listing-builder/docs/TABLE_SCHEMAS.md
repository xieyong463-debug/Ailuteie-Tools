# 表格结构 / Table Schemas

所有给用户审核的 Excel 文件统一采用：

```text
第一行：中文说明
第二行：英文字段名
第三行开始：数据
```

内容语言规则：

```text
中文为主，英文为辅。
最终 Amazon Listing 文案字段使用英文。
```

---

## 1. product_master.xlsx

路径：

```text
data/input/product_facts/product_master.xlsx
```

Sheet：

```text
master
```

第一行中文说明：

```tsv
唯一货号	SKU名称	产品卖点/说明	竞品链接1	竞品链接2	竞品链接3	颜色	尺寸
```

第二行英文字段名：

```tsv
product_id	sku_name	seller_notes	competitor_link_1	competitor_link_2	competitor_link_3	color	size
```

说明：

| 字段 | 说明 |
|---|---|
| product_id | 产品唯一货号，用来创建文件夹 |
| sku_name | 具体 SKU 名称，一行一个 SKU |
| seller_notes | 用户提供卖点、限制、注意事项 |
| competitor_link_1 | 竞品链接 1 |
| competitor_link_2 | 竞品链接 2 |
| competitor_link_3 | 竞品链接 3 |
| color | 颜色 |
| size | 尺寸 |

---

## 2. selling_points_research.xlsx

路径：

```text
data/output/{product_id}/selling_points_research.xlsx
```

### Sheet 1：research_summary

第一行中文说明：

```tsv
唯一货号	SKU数量	颜色汇总	尺寸汇总	用户卖点摘要	图片识别摘要	竞品摘要	建议产品定位	建议词库	建议类目值	风险提醒	需要人工确认	审核状态
```

第二行英文字段名：

```tsv
product_id	sku_count	colors	sizes	seller_notes_summary	image_summary	competitor_summary	recommended_positioning	suggested_keyword_library	suggested_item_type_keyword	risk_summary	needs_manual_confirmation	review_status
```

### Sheet 2：selling_points

第一行中文说明：

```tsv
唯一货号	来源	卖点内容	是否建议使用	优先级	适合使用位置	原因	风险等级	是否需要确认	人工备注
```

第二行英文字段名：

```tsv
product_id	source	selling_point	recommended_use	priority	suggested_position	reason	risk_level	needs_confirmation	manual_note
```

字段取值建议：

| 字段 | 可选值 |
|---|---|
| source | image / seller_notes / competitor / codex_suggestion |
| recommended_use | yes / no / need_confirm |
| priority | high / medium / low |
| suggested_position | title / item_highlight / bullet / description / st / none |
| risk_level | low / medium / high |
| needs_confirmation | yes / no |

### Sheet 3：competitor_reference

第一行中文说明：

```tsv
唯一货号	竞品序号	竞品链接	竞品标题摘要	竞品主卖点	可借鉴方向	不建议借鉴	备注
```

第二行英文字段名：

```tsv
product_id	competitor_no	competitor_link	competitor_title_summary	competitor_key_points	usable_reference	avoid_reference	notes
```

---

## 3. approved_product_info.xlsx

路径：

```text
data/review/{product_id}/approved_product_info.xlsx
```

Sheet：

```text
approved_info
```

第一行中文说明：

```tsv
唯一货号	SKU名称	颜色	尺寸	使用词库	亚马逊类目值	产品类型	面料/外套材质	填充材质	核心卖点	禁用卖点/禁用表达	是否专利申请中	是否可拆洗	是否真空压缩	回弹时间	适用场景	审核状态	人工备注
```

第二行英文字段名：

```tsv
product_id	sku_name	color	size	keyword_library	item_type_keyword	product_type	cover_material	filling_material	confirmed_selling_points	avoid_points	patent_pending	washable_cover	vacuum_packed	recovery_time	allowed_scenarios	review_status	manual_notes
```

核心规则：

- Codex 自动生成初稿。
- 初始 review_status = need_review。
- 用户审核后改为 approved。
- 只有 approved 的 SKU 才能生成 listing_review.xlsx。

---

## 4. listing_review.xlsx

路径：

```text
data/output/{product_id}/listing_review.xlsx
```

Sheet：

```text
listing_content
```

第一行中文说明：

```tsv
唯一货号	SKU名称	颜色	尺寸	标题75字符	Item Name字符数	产品亮点125字符	Item Highlight字符数	五点1	五点2	五点3	五点4	五点5	产品描述	ST关键词	ST字符数	使用关键词备注	审核状态	人工备注
```

第二行英文字段名：

```tsv
product_id	sku_name	color	size	item_name_75	item_name_char_count	item_highlight_125	item_highlight_char_count	bullet_1	bullet_2	bullet_3	bullet_4	bullet_5	product_description	search_terms	search_terms_char_count	keyword_notes	review_status	manual_notes
```

核心规则：

- listing_review.xlsx 由 Codex 自动生成。
- 每个 SKU 一行。
- 只有 approved_product_info.xlsx 中 review_status = approved 的 SKU 才能生成。
- 初始 review_status = need_review。
- 用户确认文案后改成 approved。
- 最终 Listing 字段用英文。
- keyword_notes 和 manual_notes 中文为主。

---

## 5. 暂缓的 Amazon 上传模板填充

暂缓文件：

```text
data/output/{product_id}/amazon_upload_ready.xlsm
```

暂缓原因：

```text
BODY_POSITIONER 模板还没最终整理完成。
```

后期恢复时的原则：

```text
只读取 approved 的 Listing，不重新生成标题、五点、卖点或材质。
如果字段缺失，只提醒，不乱填。
```
