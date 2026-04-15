#!/usr/bin/env python3
"""Lightweight calculation helper for industry research skills.

Supports:
- sizing: scenario-based market sizing formulas
- cycle: capacity-cycle and concentration calculations
- valuation: relative valuation calculations

Input is JSON for reproducibility.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
from pathlib import Path
from typing import Any


ALLOWED_FUNCS = {
    "min": min,
    "max": max,
    "abs": abs,
    "round": round,
}


def safe_eval(expr: str, variables: dict[str, float]) -> float:
    node = ast.parse(expr, mode="eval")

    def _eval(current: ast.AST) -> float:
        if isinstance(current, ast.Expression):
            return _eval(current.body)
        if isinstance(current, ast.Constant) and isinstance(current.value, (int, float)):
            return float(current.value)
        if isinstance(current, ast.Name):
            if current.id not in variables:
                raise KeyError(current.id)
            return variables[current.id]
        if isinstance(current, ast.BinOp):
            left = _eval(current.left)
            right = _eval(current.right)
            if isinstance(current.op, ast.Add):
                return left + right
            if isinstance(current.op, ast.Sub):
                return left - right
            if isinstance(current.op, ast.Mult):
                return left * right
            if isinstance(current.op, ast.Div):
                return left / right
            if isinstance(current.op, ast.Pow):
                return left**right
            raise ValueError(f"Unsupported operator: {type(current.op).__name__}")
        if isinstance(current, ast.UnaryOp):
            operand = _eval(current.operand)
            if isinstance(current.op, ast.USub):
                return -operand
            if isinstance(current.op, ast.UAdd):
                return operand
            raise ValueError(f"Unsupported unary operator: {type(current.op).__name__}")
        if isinstance(current, ast.Call) and isinstance(current.func, ast.Name):
            fn_name = current.func.id
            if fn_name not in ALLOWED_FUNCS:
                raise ValueError(f"Unsupported function: {fn_name}")
            args = [_eval(arg) for arg in current.args]
            return float(ALLOWED_FUNCS[fn_name](*args))
        raise ValueError(f"Unsupported expression node: {type(current).__name__}")

    return _eval(node)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_value(raw: Any) -> float:
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, dict) and "value" in raw:
        return float(raw["value"])
    raise ValueError(f"Unsupported variable format: {raw!r}")


def collect_times(variables: dict[str, Any]) -> list[str]:
    times: list[str] = []
    for raw in variables.values():
        if isinstance(raw, dict):
            time = raw.get("time")
            if time:
                times.append(str(time))
    return times


def collect_units(variables: dict[str, Any]) -> list[str]:
    units: list[str] = []
    for raw in variables.values():
        if isinstance(raw, dict):
            unit = raw.get("unit")
            if unit:
                units.append(str(unit))
    return units


def format_large_number(value: float, unit: str | None = None) -> str:
    if unit == "元":
        if abs(value) >= 1e8:
            return f"{value / 1e8:.2f}亿元"
        if abs(value) >= 1e4:
            return f"{value / 1e4:.2f}万元"
    if abs(value) >= 1e8:
        return f"{value / 1e8:.2f}e8"
    if abs(value) >= 1e4:
        return f"{value / 1e4:.2f}e4"
    return f"{value:.4f}"


def base_warnings(variables: dict[str, Any], target_period: str | None) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    times = collect_times(variables)
    if target_period and times:
        mismatched = sorted({time for time in times if time != target_period})
        if mismatched:
            warnings.append(
                {
                    "code": "mixed_time_basis",
                    "message": f"Target period is {target_period}, but found variable times: {', '.join(mismatched)}",
                }
            )
    missing_units = [name for name, raw in variables.items() if isinstance(raw, dict) and not raw.get("unit")]
    if missing_units:
        warnings.append(
            {
                "code": "missing_unit",
                "message": f"Variables missing unit: {', '.join(sorted(missing_units))}",
            }
        )
    missing_times = [name for name, raw in variables.items() if isinstance(raw, dict) and not raw.get("time")]
    if missing_times:
        warnings.append(
            {
                "code": "missing_source_time",
                "message": f"Variables missing time: {', '.join(sorted(missing_times))}",
            }
        )
    return warnings


def eval_formula(formula: str, variables: dict[str, Any]) -> float:
    numeric_vars = {name: normalize_value(raw) for name, raw in variables.items()}
    try:
        return safe_eval(formula, numeric_vars)
    except KeyError as exc:
        missing = str(exc).strip("'")
        raise ValueError(f"formula_variable_missing:{missing}") from exc


def run_formula_payload(payload: dict[str, Any]) -> dict[str, Any]:
    target_period = payload.get("target_period")
    formula = payload["formula"]
    variables = payload["variables"]
    result = eval_formula(formula, variables)
    unit = payload.get("result_unit")
    warnings = base_warnings(variables, target_period)
    return {
        "target_period": target_period,
        "formula": formula,
        "variables": variables,
        "result": result,
        "result_unit": unit,
        "result_display": format_large_number(result, unit),
        "warnings": warnings,
    }


def run_sizing(payload: dict[str, Any]) -> dict[str, Any]:
    if "scenarios" in payload:
        results: dict[str, Any] = {}
        for name, variables in payload["scenarios"].items():
            scenario_payload = {
                "target_period": payload.get("target_period"),
                "formula": payload["formula"],
                "variables": variables,
                "result_unit": payload.get("result_unit"),
            }
            results[name] = run_formula_payload(scenario_payload)
        return {
            "mode": "scenario",
            "target_period": payload.get("target_period"),
            "results": results,
        }
    return run_formula_payload(payload)


def run_cycle(payload: dict[str, Any]) -> dict[str, Any]:
    metric = payload.get("metric")
    if metric == "capex_ratio":
        capex = normalize_value(payload["variables"]["capex"])
        depreciation = normalize_value(payload["variables"]["depreciation_amortization"])
        result = capex / depreciation
        warnings = base_warnings(payload["variables"], payload.get("target_period"))
        return {
            "metric": metric,
            "target_period": payload.get("target_period"),
            "result": result,
            "result_display": f"{result:.4f}",
            "judgement": (
                "expansion"
                if result > 1.5
                else "improving"
                if result >= 1.0
                else "bottom"
            ),
            "warnings": warnings,
        }
    if metric == "working_capital_power":
        vars_ = payload["variables"]
        result = (
            normalize_value(vars_["accounts_payable"])
            + normalize_value(vars_["advances_from_customers"])
            + normalize_value(vars_["contract_liabilities"])
            - normalize_value(vars_["accounts_receivable"])
            - normalize_value(vars_["prepayments"])
            - normalize_value(vars_["contract_assets"])
        )
        warnings = base_warnings(vars_, payload.get("target_period"))
        return {
            "metric": metric,
            "target_period": payload.get("target_period"),
            "result": result,
            "result_unit": payload.get("result_unit"),
            "result_display": format_large_number(result, payload.get("result_unit")),
            "judgement": "strong" if result > 0 else "weak",
            "warnings": warnings,
        }
    if metric == "crn":
        shares = payload["shares"]
        result = sum(float(x) for x in shares)
        return {
            "metric": metric,
            "result": result,
            "result_display": f"{result:.2f}%",
            "judgement": (
                "highly_concentrated"
                if result > 70
                else "moderately_concentrated"
                if result >= 30
                else "fragmented"
            ),
            "warnings": [],
        }
    return run_formula_payload(payload)


def run_valuation(payload: dict[str, Any]) -> dict[str, Any]:
    metric = payload.get("metric")
    if metric == "relative_pe":
        industry_pe = normalize_value(payload["variables"]["industry_pe"])
        market_pe = normalize_value(payload["variables"]["market_pe"])
        result = industry_pe / market_pe
        warnings = base_warnings(payload["variables"], payload.get("target_period"))
        return {
            "metric": metric,
            "target_period": payload.get("target_period"),
            "result": result,
            "result_display": f"{result:.4f}x",
            "warnings": warnings,
        }
    return run_formula_payload(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculation helper for industry-research skill")
    parser.add_argument("mode", choices=["sizing", "cycle", "valuation"])
    parser.add_argument("input", help="Path to JSON input")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    payload = load_json(Path(args.input))
    if args.mode == "sizing":
        output = run_sizing(payload)
    elif args.mode == "cycle":
        output = run_cycle(payload)
    else:
        output = run_valuation(payload)

    json.dump(output, fp=None if False else __import__("sys").stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    print()


if __name__ == "__main__":
    main()
