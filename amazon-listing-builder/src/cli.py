"""命令行入口 / CLI entrypoint."""

from __future__ import annotations

import argparse

from .sync_product_folders import sync_product_folders
from .template_analyzer import analyze_all_upload_templates, save_required_fields_json
from .paths import get_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Amazon Listing Builder CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("sync-product-folders", help="根据 product_master.xlsx 创建产品文件夹")
    subparsers.add_parser("analyze-upload-templates", help="分析三类上传模板样本中的已填写字段")

    sp_research = subparsers.add_parser("generate-selling-points", help="生成 selling_points_research.xlsx（框架预留）")
    sp_research.add_argument("--product-id", required=True)

    sp_approved = subparsers.add_parser("generate-approved-info", help="生成 approved_product_info.xlsx（框架预留）")
    sp_approved.add_argument("--product-id", required=True)

    sp_listing = subparsers.add_parser("generate-listing-review", help="生成 listing_review.xlsx（框架预留）")
    sp_listing.add_argument("--product-id", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "sync-product-folders":
        result = sync_product_folders()
        print(result.to_log())
        return

    if args.command == "analyze-upload-templates":
        paths = get_paths()
        data = analyze_all_upload_templates(paths)
        save_required_fields_json(data, paths.template_required_fields_json)
        print(f"已生成: {paths.template_required_fields_json}")
        for item_type, category in data["categories"].items():
            print(item_type, category.get("status"), "字段数:", category.get("required_field_count_union", 0))
        return

    if args.command == "generate-selling-points":
        from .generate_selling_points_research import generate_selling_points_research

        generate_selling_points_research(args.product_id)
        return

    if args.command == "generate-approved-info":
        from .generate_approved_product_info import generate_approved_product_info

        generate_approved_product_info(args.product_id)
        return

    if args.command == "generate-listing-review":
        from .generate_listing_review import generate_listing_review

        generate_listing_review(args.product_id)
        return

    parser.error(f"未知命令: {args.command}")


if __name__ == "__main__":
    main()
