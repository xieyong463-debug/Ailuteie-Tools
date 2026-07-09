# 已确认方案 / Confirmed Decisions

本文记录本项目当前已经确认的规则，后续写代码时以这里为准。

## 1. 项目定位

```text
Codex 是辅助填表工具，不是自动上架工具。
不改变现有 Excel 上传方式，只减少重复操作和复制粘贴。
```

- 用户继续使用 Amazon 上传模板。
- 用户继续人工审核。
- Codex 负责读取资料、分析卖点、生成文案初稿、字段审核表和填表辅助。
- 流程不能过度复杂。

## 2. 输出语言

```text
中文为主，英文为辅
```

具体规则：

| 内容类型 | 输出语言 |
|---|---|
| 项目说明 | 中文为主，英文术语辅助 |
| 表格第一行中文说明 | 中文 |
| 表格第二行字段名 | 英文 |
| 卖点研究内容 | 中文为主，关键英文词保留 |
| 竞品分析 | 中文为主 |
| 风险提醒 | 中文说明 + 英文风险词 |
| 最终 Listing 文案 | 英文 |
| 上传模板字段值 | 按 Amazon 要求填写英文或固定值 |

## 3. product_master.xlsx

路径：

```text
data/input/product_facts/product_master.xlsx
```

Sheet 名：

```text
master
```

结构：

- 第一行：中文说明
- 第二行：英文字段名
- 第三行开始：数据

字段：

```text
product_id
sku_name
seller_notes
competitor_link_1
competitor_link_2
competitor_link_3
color
size
```

规则：

- 一行 = 一个 SKU / 一个 Child 变体。
- 同一个 product_id 可以有多行。
- product_id 用来创建产品文件夹。
- sku_name 用来识别具体 SKU。
- seller_notes 是用户提供的卖点、限制、注意事项。
- competitor_link_1/2/3 是竞品链接。
- color / size 用于变体标题生成。
- 不要合并单元格。

## 4. 关键词词库

路径：

```text
data/input/category_keywords/back_pillow.xlsx
data/input/category_keywords/body_pillow_keywords.xlsx
```

规则：

- 第一版直接读取用户提供的原始关键词表。
- 不要求用户新增或维护人工辅助列。
- A列：关键词。
- J列：月搜索量。
- K列：月购买量。
- B列翻译不作为核心依据。

词库分类：

| keyword_library | 文件 |
|---|---|
| back_pillow | back_pillow.xlsx |
| body_pillow | body_pillow_keywords.xlsx |

## 5. Amazon 上传模板样本

用户已提供三个类目上传模板样本：

| 样本文件 | 样本货号 | 产品方向 | item_type_keyword | 后续建议文件名 |
|---|---|---|---|---|
| yk-117.xlsm | YK-117 | 阅读用靠垫枕 / Reading Pillow | reading-pillows | reading_pillows_template_yk117.xlsm |
| ctz-039.xlsm | CTZ-039 | 身体枕 / Body Pillow | body-pillows | body_pillows_template_ctz039.xlsm |
| yk-132..xlsm | YK-132 | 腰椎枕 / Lumbar Pillow | lumbar-pillows | lumbar_pillows_template_yk132.xlsm |

核心规则：

```text
三个上传模板样本中，第7行 Parent 和第8行 Child 已填写字段，后续视为对应 item_type_keyword 类目的必填字段样本。
```

已分析统计：

| item_type_keyword | 已填写字段并集 | Parent 已填写字段 | Child 已填写字段 |
|---|---:|---:|---:|
| reading-pillows | 70 | 43 | 70 |
| body-pillows | 68 | 41 | 68 |
| lumbar-pillows | 68 | 40 | 68 |

后续生成：

```text
data/input/amazon_templates/template_required_fields.json
```

## 6. 产品图片

路径规则：

```text
data/input/product_images/{product_id}/
```

规则：

- 一个 product_id 一个图片文件夹。
- 图片文件名不强制统一。
- 不同款式不要混在同一个文件夹。
- 不要把旧版、错误版、竞品图混进去。
- 支持 jpg / jpeg / png / webp。

## 7. 自动创建文件夹

Codex 根据 product_master.xlsx 里的 product_id 自动创建：

```text
data/input/product_images/{product_id}/
data/review/{product_id}/
data/output/{product_id}/
```

即使同一个 product_id 有多行，也只创建一个产品文件夹。

## 8. 卖点研究

输出文件：

```text
data/output/{product_id}/selling_points_research.xlsx
```

来源：

- 产品图片
- product_master.xlsx 里的 seller_notes
- competitor_link_1 / 2 / 3
- 竞品页面联网分析

用途：

- 让 Codex 先理解产品。
- 输出卖点建议。
- 给用户审核。
- 不直接作为最终上传依据。

## 9. approved_product_info.xlsx

输出文件：

```text
data/review/{product_id}/approved_product_info.xlsx
```

规则：

- 由 Codex 自动生成初稿。
- 初始 review_status = need_review。
- 用户审核后手动改为 approved。
- 只有 review_status = approved 的 SKU 才允许进入 Listing 生成。
- 产品事实字段必须尽量覆盖上传模板必填字段样本里的非文案字段。

## 10. listing_review.xlsx

输出文件：

```text
data/output/{product_id}/listing_review.xlsx
```

现在定位升级为：

```text
Listing 文案审核 + Amazon 必填字段审核
```

建议 Sheet：

```text
listing_content
amazon_required_fields
missing_fields_check
```

规则：

- 由 Codex 根据 approved_product_info.xlsx 生成。
- 必须同时考虑 Parent 行和 Child 行。
- 同一个 product_id 生成 1 行 Parent。
- 同一个 product_id 下每个 sku_name 生成 1 行 Child。
- 初始 review_status = need_review。
- 用户审核后手动改为 approved。
- 最终上传内容字段用英文。
- 审核备注、keyword_notes 用中文为主。

## 11. 当前暂缓步骤

暂缓模块：

```text
generate_amazon_upload_file
```

原因：

```text
最终填入 Amazon 上传模板的模块后期再做。
但当前框架必须保证 listing_review.xlsx 的字段能匹配 Amazon 上传模板。
```
