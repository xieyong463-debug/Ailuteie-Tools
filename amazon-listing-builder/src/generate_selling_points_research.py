"""卖点研究表生成入口 / Generate selling_points_research.xlsx.

当前先保留框架入口，具体图片分析、竞品分析由后续 Codex 在本框架中补充。
"""

from __future__ import annotations

from .paths import get_paths


def generate_selling_points_research(product_id: str) -> None:
    paths = get_paths()
    output_path = paths.selling_points_research_path(product_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    raise NotImplementedError(
        "generate_selling_points_research 框架已预留，后续由 Codex 根据图片、seller_notes、竞品链接补充实现。"
    )
