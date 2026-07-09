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
| sku_name | 具体 SKU 名称，一行一个 SKU / Child 变体 |
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
- 产品事实字段必须能覆盖上传模板样本中已填写的非文案字段；若缺失，需要在 `listing_review.xlsx` 的 `missing_fields_check` 中提醒。

---

## 4. listing_review.xlsx

路径：

```text
data/output/{product_id}/listing_review.xlsx
```

现在这张表升级为：

```text
Listing 文案审核 + Amazon 必填字段审核
```

建议 Sheet：

```text
listing_content
amazon_required_fields
missing_fields_check
```

### Sheet 1：listing_content

第一行中文说明：

```tsv
唯一货号	SKU名称	父子层级	颜色	尺寸	标题75字符	Item Name字符数	产品亮点125字符	Item Highlight字符数	五点1	五点2	五点3	五点4	五点5	产品描述	ST关键词	ST字符数	使用关键词备注	审核状态	人工备注
```

第二行英文字段名：

```tsv
product_id	sku_name	parentage_level	color	size	item_name_75	item_name_char_count	item_highlight_125	item_highlight_char_count	bullet_1	bullet_2	bullet_3	bullet_4	bullet_5	product_description	search_terms	search_terms_char_count	keyword_notes	review_status	manual_notes
```

### Sheet 2：amazon_required_fields

这个 Sheet 必须匹配上传模板样本中已填写字段。

第一行中文说明：

```tsv
唯一货号	SKU名称	父子层级	亚马逊类目值	模板列	Amazon字段显示名	Amazon实际字段名	字段来源	Parent是否需要	Child是否需要	最终值	是否缺失	审核状态	人工备注
```

第二行英文字段名：

```tsv
product_id	sku_name	parentage_level	item_type_keyword	template_column	amazon_display_name	amazon_attribute_name	field_source	required_for_parent	required_for_child	final_value	is_missing	review_status	manual_notes
```

说明：

| 字段 | 说明 |
|---|---|
| template_column | Amazon 模板列号，例如 A / B / G |
| amazon_display_name | 模板第4行字段显示名 |
| amazon_attribute_name | 模板第5行 Amazon 实际字段名 |
| field_source | 字段来源，如 listing_content / approved_product_info / fixed_value / need_manual |
| final_value | 最终准备填入 Amazon 模板的值 |
| is_missing | yes / no |

### Sheet 3：missing_fields_check

第一行中文说明：

```tsv
唯一货号	SKU名称	父子层级	缺失字段	Amazon实际字段名	原因	建议处理方式
```

第二行英文字段名：

```tsv
product_id	sku_name	parentage_level	missing_field	amazon_attribute_name	reason	suggested_fix
```

核心规则：

- listing_review.xlsx 由 Codex 自动生成。
- 必须同时包含 Parent 行和 Child 行检查。
- 同一个 product_id 生成 1 行 Parent。
- 同一个 product_id 下每个 sku_name 生成 1 行 Child。
- 只有 approved_product_info.xlsx 中 review_status = approved 的 SKU 才能生成。
- 初始 review_status = need_review。
- 用户确认文案和字段后改成 approved。
- 最终 Listing 文案字段用英文。
- keyword_notes 和 manual_notes 中文为主。

---

## 5. 上传模板样本 required fields

已提供三份模板样本：

| item_type_keyword | 样本货号 | 已填写字段并集 | Parent 已填写字段 | Child 已填写字段 |
|---|---:|---:|---:|---:|
| reading-pillows | YK-117 | 70 | 43 | 70 |
| body-pillows | CTZ-039 | 68 | 41 | 68 |
| lumbar-pillows | YK-132 | 68 | 40 | 68 |

后续通过以下文件记录模板必填字段：

```text
data/input/amazon_templates/template_required_fields.json
```

后续通过以下命令重新分析：

```bash
python -m src.cli analyze-upload-templates
```

---

## 6. 暂缓的 Amazon 上传模板填充

暂缓文件：

```text
data/output/{product_id}/amazon_upload_ready.xlsm
```

暂缓原因：

```text
最终填入 Amazon 上传模板的模块后期再做。
```

后期恢复时的原则：

```text
只读取 approved 的 Listing 和 Amazon required fields。
不重新生成标题、五点、卖点或材质。
如果字段缺失，只提醒，不乱填。
```
