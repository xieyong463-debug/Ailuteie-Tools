# 上传模板分析 / Upload Template Analysis

用户已提供 3 个 Amazon 上传模板样本。后续这些模板不是普通参考文件，而是对应类目的 **必填字段样本 / Required Field Sample**。

## 1. 类目对应关系

| 样本文件 | 样本货号 | 产品方向 | item_type_keyword | 后续模板文件名 |
|---|---|---|---|---|
| yk-117.xlsm | YK-117 | 阅读用靠垫枕 / Reading Pillow | reading-pillows | reading_pillows_template_yk117.xlsm |
| ctz-039.xlsm | CTZ-039 | 身体枕 / Body Pillow | body-pillows | body_pillows_template_ctz039.xlsm |
| yk-132..xlsm | YK-132 | 腰椎枕 / Lumbar Pillow | lumbar-pillows | lumbar_pillows_template_yk132.xlsm |

## 2. 核心规则

```text
模板中第 7 行 Parent 和第 8 行 Child 已填写字段，后续视为该 item_type_keyword 类目的必填字段样本。
```

英文辅助：

```text
Fields filled in row 7 Parent and row 8 Child are treated as required field samples for each item_type_keyword.
```

## 3. 已分析结果

| item_type_keyword | 样本货号 | 已填写字段并集 | Parent 已填写字段 | Child 已填写字段 |
|---|---:|---:|---:|---:|
| reading-pillows | YK-117 | 70 | 43 | 70 |
| body-pillows | CTZ-039 | 68 | 41 | 68 |
| lumbar-pillows | YK-132 | 68 | 40 | 68 |

## 4. 对流程的影响

原先 `listing_review.xlsx` 只考虑：

```text
Item Name
Item Highlight
Bullet Point 1-5
Product Description
Generic Keyword
```

现在需要升级为：

```text
Listing 文案审核 + Amazon 必填字段审核
```

也就是说，后续 `listing_review.xlsx` 应至少包含：

```text
listing_content
amazon_required_fields
missing_fields_check
```

## 5. 必须生成 Parent 行

`product_master.xlsx` 中：

```text
一行 = 一个 SKU / 一个 Child 变体
```

但 Amazon 上传模板需要：

```text
Parent 行 + Child 行
```

所以后续生成最终字段时必须自动处理：

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

## 6. 新增流程步骤

完整闭环更新为：

```text
product_master.xlsx
↓
sync_product_folders
↓
analyze_upload_templates
↓
template_required_fields.json / xlsx
↓
selling_points_research.xlsx
↓
approved_product_info.xlsx
↓
listing_review.xlsx
   - listing_content
   - amazon_required_fields
   - missing_fields_check
↓
人工审核，review_status = approved
↓
后期 generate_amazon_upload_file
↓
amazon_upload_ready.xlsm
```

## 7. 当前边界

当前阶段可以做：

```text
分析上传模板字段
记录 required_fields
搭建代码框架
让 listing_review.xlsx 未来匹配 Amazon 上传模板
```

当前阶段仍然暂缓：

```text
自动把 listing_review.xlsx 填入 Amazon 上传模板
```

原因：最终填模板模块后期再做，但现在框架必须保证字段闭环。
