# amazon-listing-builder

Amazon Listing 自动化辅助项目。

本项目用于配合 Codex 做产品理解、卖点研究、Listing 文案生成和人工审核。第一版不改变现有上架方式，仍然以 Excel / Amazon flat file 上传模板为核心。

## 核心原则

- 中文为主，英文为辅。
- Codex 是辅助填表工具，不是自动上架工具。
- 不重构成复杂系统，不维护复杂词库辅助列。
- 继续使用 Excel 表格、人工审核、手动上传 Amazon。
- 竞品只能参考，不能照抄，也不能把竞品功能直接写成我们产品功能。
- 最终上传模板填充步骤暂时保留，等 BODY_POSITIONER 模板整理好后再做。

## 当前已确定流程

```text
product_master.xlsx
↓
Codex 读取产品、SKU、颜色、尺寸、seller_notes、竞品链接
↓
Codex 读取产品图片
↓
Codex 联网参考竞品
↓
生成 selling_points_research.xlsx
↓
自动生成 approved_product_info.xlsx 初稿
↓
人工审核，review_status 改成 approved
↓
生成 listing_review.xlsx
↓
人工审核，review_status 改成 approved
↓
后期再填入 BODY_POSITIONER 上传模板
```

## 当前目录规划

```text
amazon-listing-builder/
├── data/
│   ├── input/
│   │   ├── product_images/
│   │   ├── product_facts/
│   │   ├── category_keywords/
│   │   └── amazon_templates/
│   ├── review/
│   └── output/
├── docs/
└── templates/
```

## 关键文件路径

```text
data/input/product_facts/product_master.xlsx
data/input/category_keywords/back_pillow.xlsx
data/input/category_keywords/body_pillow_keywords.xlsx
data/input/amazon_templates/body_positioner_template.xlsm
data/output/{product_id}/selling_points_research.xlsx
data/review/{product_id}/approved_product_info.xlsx
data/output/{product_id}/listing_review.xlsx
```

## 暂时不做的步骤

```text
把 listing_review.xlsx 填入 Amazon 上传模板
```

原因：BODY_POSITIONER 上传模板还没有最终整理完成。该步骤后期直接在 Codex 里继续操作。
