#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Amazon multi-variant sales-weighted stocking formula for 2026 peak events.

用途：
- 用 3/7/14/30 天销量权重计算多变体备货建议
- 适用于亚马逊多颜色 / 多尺寸 / 多 ASIN / 多 MSKU 的大促备货预估
- 可读取 CSV，输出每个变体的建议备货数量、建议备货箱数、权重销量和风险标签

推荐默认权重：
- 3天销量：35%
- 7天销量：30%
- 14天销量：20%
- 30天销量：15%

核心逻辑：
weighted_daily_sales =
    sales_3d / 3  * 0.35 +
    sales_7d / 7  * 0.30 +
    sales_14d / 14 * 0.20 +
    sales_30d / 30 * 0.15

recommended_qty =
    weighted_daily_sales
    * event_days
    * promo_lift
    * safety_stock_factor
    - sellable_inventory
    - inbound_qty

最终向上取整，且不低于 0。
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


DEFAULT_WEIGHTS: Dict[str, float] = {
    "3d": 0.35,
    "7d": 0.30,
    "14d": 0.20,
    "30d": 0.15,
}


@dataclass(frozen=True)
class StockingConfig:
    """备货参数配置。"""

    event_days: int = 14
    promo_lift: float = 1.50
    safety_stock_factor: float = 1.20
    min_days_of_stock: int = 7
    round_to_case_pack: bool = True


REQUIRED_COLUMNS = {
    "sku",
    "parent_asin",
    "sales_3d",
    "sales_7d",
    "sales_14d",
    "sales_30d",
    "sellable_inventory",
    "inbound_qty",
    "case_pack",
}


OPTIONAL_COLUMNS = {
    "asin",
    "color",
    "size",
    "price",
    "gross_margin",
}


def validate_weights(weights: Dict[str, float]) -> None:
    """确认权重合计为 1。"""
    total = sum(weights.values())
    if not math.isclose(total, 1.0, abs_tol=0.0001):
        raise ValueError(f"权重合计必须等于 1，目前为 {total:.4f}: {weights}")


def weighted_daily_sales(
    sales_3d: float,
    sales_7d: float,
    sales_14d: float,
    sales_30d: float,
    weights: Optional[Dict[str, float]] = None,
) -> float:
    """
    计算加权日均销量。

    3天权重更高，适合捕捉大促前近期增长；
    30天权重较低，避免被旧数据过度拖累。
    """
    weights = weights or DEFAULT_WEIGHTS
    validate_weights(weights)

    return (
        (max(sales_3d, 0) / 3) * weights["3d"]
        + (max(sales_7d, 0) / 7) * weights["7d"]
        + (max(sales_14d, 0) / 14) * weights["14d"]
        + (max(sales_30d, 0) / 30) * weights["30d"]
    )


def recommended_stock_qty(
    weighted_daily: float,
    sellable_inventory: float,
    inbound_qty: float,
    config: Optional[StockingConfig] = None,
) -> int:
    """计算建议补货数量。"""
    config = config or StockingConfig()

    demand_forecast = (
        weighted_daily
        * config.event_days
        * config.promo_lift
        * config.safety_stock_factor
    )

    qty = demand_forecast - max(sellable_inventory, 0) - max(inbound_qty, 0)
    return max(0, math.ceil(qty))


def round_up_to_case_pack(qty: int, case_pack: float) -> int:
    """按装箱数向上取整。"""
    if case_pack is None or case_pack <= 0:
        return qty
    return int(math.ceil(qty / case_pack) * case_pack)


def risk_label(days_of_stock: float, min_days_of_stock: int) -> str:
    """根据可售库存覆盖天数给风险标签。"""
    if days_of_stock < min_days_of_stock:
        return "High Risk / 高风险"
    if days_of_stock < min_days_of_stock * 1.5:
        return "Medium Risk / 中风险"
    return "Low Risk / 低风险"


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """把列名统一成小写下划线格式，降低表格字段不一致的影响。"""
    normalized = df.copy()
    normalized.columns = [
        str(col).strip().lower().replace(" ", "_").replace("-", "_")
        for col in normalized.columns
    ]
    return normalized


def validate_input_columns(df: pd.DataFrame) -> None:
    """检查必填字段。"""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            "CSV 缺少必填列: "
            + ", ".join(sorted(missing))
            + "\n必填列为: "
            + ", ".join(sorted(REQUIRED_COLUMNS))
        )


def calculate_stocking_plan(
    df: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
    config: Optional[StockingConfig] = None,
) -> pd.DataFrame:
    """
    为多变体表生成备货建议。

    输入字段：
    sku,parent_asin,asin,color,size,
    sales_3d,sales_7d,sales_14d,sales_30d,
    sellable_inventory,inbound_qty,case_pack

    asin/color/size 可选，但建议保留，方便多变体分析。
    """
    weights = weights or DEFAULT_WEIGHTS
    config = config or StockingConfig()
    validate_weights(weights)

    work = normalize_columns(df)
    validate_input_columns(work)

    numeric_cols = [
        "sales_3d",
        "sales_7d",
        "sales_14d",
        "sales_30d",
        "sellable_inventory",
        "inbound_qty",
        "case_pack",
    ]
    for col in numeric_cols:
        work[col] = pd.to_numeric(work[col], errors="coerce").fillna(0)

    work["weighted_daily_sales"] = work.apply(
        lambda row: weighted_daily_sales(
            row["sales_3d"],
            row["sales_7d"],
            row["sales_14d"],
            row["sales_30d"],
            weights,
        ),
        axis=1,
    )

    work["forecast_event_demand"] = (
        work["weighted_daily_sales"]
        * config.event_days
        * config.promo_lift
        * config.safety_stock_factor
    )

    work["current_available_total"] = (
        work["sellable_inventory"].clip(lower=0) + work["inbound_qty"].clip(lower=0)
    )

    work["days_of_stock_now"] = work.apply(
        lambda row: (
            row["current_available_total"] / row["weighted_daily_sales"]
            if row["weighted_daily_sales"] > 0
            else 9999
        ),
        axis=1,
    )

    work["recommended_qty_raw"] = work.apply(
        lambda row: recommended_stock_qty(
            row["weighted_daily_sales"],
            row["sellable_inventory"],
            row["inbound_qty"],
            config,
        ),
        axis=1,
    )

    if config.round_to_case_pack:
        work["recommended_qty"] = work.apply(
            lambda row: round_up_to_case_pack(
                int(row["recommended_qty_raw"]),
                row["case_pack"],
            ),
            axis=1,
        )
    else:
        work["recommended_qty"] = work["recommended_qty_raw"]

    work["recommended_cases"] = work.apply(
        lambda row: (
            math.ceil(row["recommended_qty"] / row["case_pack"])
            if row["case_pack"] > 0
            else 0
        ),
        axis=1,
    )

    work["stock_risk"] = work["days_of_stock_now"].apply(
        lambda value: risk_label(value, config.min_days_of_stock)
    )

    work["weight_formula"] = (
        f"3d:{weights['3d']:.0%}, "
        f"7d:{weights['7d']:.0%}, "
        f"14d:{weights['14d']:.0%}, "
        f"30d:{weights['30d']:.0%}"
    )

    preferred_order = [
        "parent_asin",
        "asin",
        "sku",
        "color",
        "size",
        "sales_3d",
        "sales_7d",
        "sales_14d",
        "sales_30d",
        "weighted_daily_sales",
        "sellable_inventory",
        "inbound_qty",
        "current_available_total",
        "days_of_stock_now",
        "forecast_event_demand",
        "case_pack",
        "recommended_qty_raw",
        "recommended_qty",
        "recommended_cases",
        "stock_risk",
        "weight_formula",
    ]

    existing_cols = [col for col in preferred_order if col in work.columns]
    remaining_cols = [col for col in work.columns if col not in existing_cols]
    return work[existing_cols + remaining_cols].sort_values(
        by=["stock_risk", "recommended_qty"], ascending=[True, False]
    )


def build_example_data() -> pd.DataFrame:
    """生成示例数据，方便第一次运行测试。"""
    return pd.DataFrame(
        [
            {
                "parent_asin": "B0EXAMPLE01",
                "asin": "B0SKU0001",
                "sku": "CTZ-285-1M-Beige",
                "color": "Beige",
                "size": "1m",
                "sales_3d": 18,
                "sales_7d": 36,
                "sales_14d": 62,
                "sales_30d": 120,
                "sellable_inventory": 40,
                "inbound_qty": 24,
                "case_pack": 8,
            },
            {
                "parent_asin": "B0EXAMPLE01",
                "asin": "B0SKU0002",
                "sku": "CTZ-285-1.5M-Grey",
                "color": "Grey",
                "size": "1.5m",
                "sales_3d": 30,
                "sales_7d": 64,
                "sales_14d": 100,
                "sales_30d": 180,
                "sellable_inventory": 20,
                "inbound_qty": 12,
                "case_pack": 6,
            },
        ]
    )


def write_example_csv(path: Path) -> None:
    """写入示例 CSV。"""
    build_example_data().to_csv(path, index=False, encoding="utf-8-sig")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Amazon 2026 peak-event multi-variant stocking calculator."
    )
    parser.add_argument(
        "--input",
        "-i",
        type=Path,
        help="输入 CSV 文件路径。不传则自动生成 example_input.csv 并用示例数据计算。",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("stocking_plan_output.csv"),
        help="输出 CSV 文件路径，默认 stocking_plan_output.csv",
    )
    parser.add_argument("--event-days", type=int, default=14, help="大促覆盖天数，默认 14")
    parser.add_argument("--promo-lift", type=float, default=1.50, help="大促销量放大系数，默认 1.50")
    parser.add_argument(
        "--safety-stock-factor",
        type=float,
        default=1.20,
        help="安全库存系数，默认 1.20",
    )
    parser.add_argument(
        "--min-days-of-stock",
        type=int,
        default=7,
        help="低库存风险阈值，默认 7 天",
    )
    parser.add_argument("--w3", type=float, default=0.35, help="3天权重，默认 0.35")
    parser.add_argument("--w7", type=float, default=0.30, help="7天权重，默认 0.30")
    parser.add_argument("--w14", type=float, default=0.20, help="14天权重，默认 0.20")
    parser.add_argument("--w30", type=float, default=0.15, help="30天权重，默认 0.15")
    parser.add_argument(
        "--no-case-pack-rounding",
        action="store_true",
        help="不按装箱数量向上取整",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    weights = {
        "3d": args.w3,
        "7d": args.w7,
        "14d": args.w14,
        "30d": args.w30,
    }

    config = StockingConfig(
        event_days=args.event_days,
        promo_lift=args.promo_lift,
        safety_stock_factor=args.safety_stock_factor,
        min_days_of_stock=args.min_days_of_stock,
        round_to_case_pack=not args.no_case_pack_rounding,
    )

    input_path = args.input
    if input_path is None:
        input_path = Path("example_input.csv")
        write_example_csv(input_path)
        print(f"未传入 --input，已生成示例文件: {input_path}")

    df = pd.read_csv(input_path)
    result = calculate_stocking_plan(df, weights=weights, config=config)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False, encoding="utf-8-sig")

    print(f"备货计划已生成: {args.output}")
    print("核心公式：")
    print(
        "weighted_daily_sales = sales_3d/3*w3 + sales_7d/7*w7 "
        "+ sales_14d/14*w14 + sales_30d/30*w30"
    )
    print(
        "recommended_qty = weighted_daily_sales * event_days * promo_lift "
        "* safety_stock_factor - sellable_inventory - inbound_qty"
    )


if __name__ == "__main__":
    main()
