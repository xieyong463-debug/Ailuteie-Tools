# Codex 工作流 / Codex Workflow

本文给 Codex 使用，说明当前项目第一版应该怎么跑。

## 总原则

```text
第一版先简单能跑。
不改变用户现有 Excel 上传方式。
中文为主，英文为辅。
最终 Amazon Listing 文案用英文。
```

## Step 1：同步产品文件夹

输入：

```text
data/input/product_facts/product_master.xlsx
```

读取规则：

- Sheet：master
- 第二行是英文字段名
- 从第三行开始是数据
- 按 product_id 去重

需要创建：

```text
data/input/product_images/{product_id}/
data/review/{product_id}/
data/output/{product_id}/
```

注意：

```text
同一个 product_id 即使有多个 SKU，也只创建一个产品图片文件夹。
不要删除已有文件。
不要覆盖已有文件。
```

## Step 2：分析上传模板样本

用户已提供三份 Amazon 上传模板样本：

| 样本货号 | 产品方向 | item_type_keyword | 模板文件名 |
|---|---|---|---|
| YK-117 | 阅读用靠垫枕 / Reading Pillow | reading-pillows | reading_pillows_template_yk117.xlsm |
| CTZ-039 | 身体枕 / Body Pillow | body-pillows | body_pillows_template_ctz039.xlsm |
| YK-132 | 腰椎枕 / Lumbar Pillow | lumbar-pillows | lumbar_pillows_template_yk132.xlsm |

核心规则：

```text
模板中第 7 行 Parent 和第 8 行 Child 已填写字段，后续视为该 item_type_keyword 类目的必填字段样本。
```

命令：

```bash
python -m src.cli analyze-upload-templates
```

输出：

```text
data/input/amazon_templates/template_required_fields.json
```

已分析统计：

| item_type_keyword | 已填写字段并集 | Parent 已填写字段 | Child 已填写字段 |
|---|---:|---:|---:|
| reading-pillows | 70 | 43 | 70 |
| body-pillows | 68 | 41 | 68 |
| lumbar-pillows | 68 | 40 | 68 |

## Step 3：生成 selling_points_research.xlsx

输入：

```text
data/input/product_facts/product_master.xlsx
data/input/product_images/{product_id}/
competitor_link_1 / competitor_link_2 / competitor_link_3
```

输出：

```text
data/output/{product_id}/selling_points_research.xlsx
```

Sheet：

```text
research_summary
selling_points
competitor_reference
```

输出语言：

```text
中文为主，英文为辅。
关键英文 Listing 词可以保留。
```

必须遵守：

- 图片可见信息可以作为 image 来源。
- 用户 seller_notes 可以作为 seller_notes 来源。
- 竞品信息只能作为 competitor 来源。
- 竞品有但我们没确认的功能，标记 need_confirm。
- 医疗、治疗、疼痛缓解等表达直接标记 no。
- 不要照抄竞品 Listing 文案。

## Step 4：生成 approved_product_info.xlsx 初稿

输入：

```text
product_master.xlsx
selling_points_research.xlsx
template_required_fields.json
产品图片识别结果
seller_notes
竞品参考结果
```

输出：

```text
data/review/{product_id}/approved_product_info.xlsx
```

初始状态：

```text
review_status = need_review
```

用户审核后手动改为：

```text
review_status = approved
```

限制：

```text
只有 approved 的 SKU 才允许进入 Listing 生成。
```

## Step 5：生成 listing_review.xlsx

输入：

```text
data/review/{product_id}/approved_product_info.xlsx
data/input/category_keywords/back_pillow.xlsx 或 body_pillow_keywords.xlsx
data/input/amazon_templates/template_required_fields.json
```

输出：

```text
data/output/{product_id}/listing_review.xlsx
```

现在 `listing_review.xlsx` 不只是文案审核表，而是：

```text
Listing 文案审核 + Amazon 必填字段审核
```

建议 Sheet：

```text
listing_content
amazon_required_fields
missing_fields_check
```

初始状态：

```text
review_status = need_review
```

用户审核后手动改为：

```text
review_status = approved
```

Listing 文案字段：

```text
item_name_75
item_highlight_125
bullet_1
bullet_2
bullet_3
bullet_4
bullet_5
product_description
search_terms
```

字符控制：

```text
item_name_75 <= 75 characters
item_highlight_125 <= 125 characters
```

内容语言：

- Listing 文案：英文
- keyword_notes：中文为主，英文关键词保留
- manual_notes：中文

## Step 6：Amazon 上传模板填充，暂缓

暂缓模块：

```text
generate_amazon_upload_file
```

原因：

```text
最终填模板模块后期再做。
但当前框架必须保证 listing_review.xlsx 的字段能匹配 Amazon 上传模板。
```

后期恢复时的输入：

```text
data/input/amazon_templates/body_positioner_template.xlsm 或三类目模板样本
data/review/{product_id}/approved_product_info.xlsx
data/output/{product_id}/listing_review.xlsx
```

后期恢复时的输出：

```text
data/output/{product_id}/amazon_upload_ready.xlsm
```

后期规则：

```text
只填已审核 approved 的 SKU。
只搬运已审核内容。
不能在这一步重新生成标题、五点、卖点、材质或类目。
字段缺失时只提醒，不乱填。
```

## Parent / Child 行规则

`product_master.xlsx` 中：

```text
一行 = 一个 SKU / 一个 Child 变体
```

Amazon 上传模板需要：

```text
Parent 行 + Child 行
```

所以后续生成最终 Amazon 字段时必须自动处理：

```text
同一个 product_id 生成 1 行 Parent
同一个 product_id 下每个 sku_name 生成 1 行 Child
```

例如：

```text
YK-048 有 10 个 SKU
→ 1 行 Parent + 10 行 Child
→ 合计 11 行
```

## 基础禁用规则

Codex 应自动避开或提醒：

```text
竞品品牌词
医疗功效词
pain relief
orthopedic
therapy
cure
discomfort relief
儿童/婴儿词，除非用户确认
孕妇词，除非用户确认
office chair，除非产品确实适用
bolster / cylinder / tube，除非产品确实为圆柱款
pillowcase / cover，除非卖的是枕套
wedge / knee / leg pillow，除非产品确实对应
```

## 关键词读取规则

词库文件：

```text
data/input/category_keywords/back_pillow.xlsx
data/input/category_keywords/body_pillow_keywords.xlsx
```

读取重点：

```text
A列：关键词
J列：月搜索量
K列：月购买量
```

B列翻译不作为核心依据。
