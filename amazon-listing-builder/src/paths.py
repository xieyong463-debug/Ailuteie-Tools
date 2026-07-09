"""统一项目路径 / Centralized project paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """项目路径集合。所有模块都应从这里取路径，避免各写各的。"""

    root: Path

    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    @property
    def input_dir(self) -> Path:
        return self.data_dir / "input"

    @property
    def product_facts_dir(self) -> Path:
        return self.input_dir / "product_facts"

    @property
    def product_master_path(self) -> Path:
        return self.product_facts_dir / "product_master.xlsx"

    @property
    def product_images_dir(self) -> Path:
        return self.input_dir / "product_images"

    def product_image_dir(self, product_id: str) -> Path:
        return self.product_images_dir / product_id

    @property
    def category_keywords_dir(self) -> Path:
        return self.input_dir / "category_keywords"

    @property
    def back_pillow_keywords_path(self) -> Path:
        return self.category_keywords_dir / "back_pillow.xlsx"

    @property
    def body_pillow_keywords_path(self) -> Path:
        return self.category_keywords_dir / "body_pillow_keywords.xlsx"

    @property
    def amazon_templates_dir(self) -> Path:
        return self.input_dir / "amazon_templates"

    @property
    def template_required_fields_json(self) -> Path:
        return self.amazon_templates_dir / "template_required_fields.json"

    @property
    def template_required_fields_xlsx(self) -> Path:
        return self.amazon_templates_dir / "template_required_fields.xlsx"

    @property
    def review_dir(self) -> Path:
        return self.data_dir / "review"

    def product_review_dir(self, product_id: str) -> Path:
        return self.review_dir / product_id

    def approved_product_info_path(self, product_id: str) -> Path:
        return self.product_review_dir(product_id) / "approved_product_info.xlsx"

    @property
    def output_dir(self) -> Path:
        return self.data_dir / "output"

    def product_output_dir(self, product_id: str) -> Path:
        return self.output_dir / product_id

    def selling_points_research_path(self, product_id: str) -> Path:
        return self.product_output_dir(product_id) / "selling_points_research.xlsx"

    def listing_review_path(self, product_id: str) -> Path:
        return self.product_output_dir(product_id) / "listing_review.xlsx"


def find_project_root(start: Path | None = None) -> Path:
    """向上查找 amazon-listing-builder 项目根目录。"""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if candidate.name == "amazon-listing-builder":
            return candidate
        if (candidate / "amazon-listing-builder").is_dir():
            return candidate / "amazon-listing-builder"
    raise FileNotFoundError("未找到 amazon-listing-builder 项目根目录。请在项目目录内运行。")


def get_paths(start: Path | None = None) -> ProjectPaths:
    return ProjectPaths(root=find_project_root(start))
