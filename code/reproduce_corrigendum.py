#!/usr/bin/env python3
"""Reconstruct and audit the 2015 corrigendum's three-player game results.

The script reconstructs arrival outcomes from FIFO queueing with random order
among simultaneous departures, calculates private costs, applies the tolls
derived from the Janusch note's stated ``ISC - IPC`` method, and compares weak
pure-strategy Nash equilibria with the published corrected Table 11. It also
reports the result obtained from the note's internally inconsistent printed
``+0.5E`` sign in the epsilon toll.

Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

ACTIONS = ("v", "e", "o", "l")
DEPARTURE_TIME = {"v": -2, "e": -1, "o": 0, "l": 1}


def profiles_for_patterns(*patterns: str) -> tuple[str, ...]:
    values: set[str] = set()
    for pattern in patterns:
        values.update("".join(value) for value in set(permutations(pattern)))
    return tuple(sorted(values))


ALL_PROFILES = tuple(
    sorted("".join(profile) for profile in product(ACTIONS, repeat=3))
)

PUBLISHED_CASES = (
    {
        "parameters": (0, 0, 0),
        "unpriced": ALL_PROFILES,
        "priced": ALL_PROFILES,
        "minimum_total_cost": 0,
    },
    {
        "parameters": (0, 1, 0),
        "unpriced": profiles_for_patterns("veo", "vel", "vol", "eol"),
        "priced": profiles_for_patterns("veo", "vel", "vol", "eol"),
        "minimum_total_cost": 0,
    },
    {
        "parameters": (0, 0, 1),
        "unpriced": profiles_for_patterns("vvv", "vve", "vvo", "vee", "veo"),
        "priced": profiles_for_patterns("vvv", "vve", "vvo", "vee", "veo"),
        "minimum_total_cost": 0,
    },
    {
        "parameters": (0, 1, 1),
        "unpriced": profiles_for_patterns("veo"),
        "priced": profiles_for_patterns("veo"),
        "minimum_total_cost": 0,
    },
    {
        "parameters": (1, 0, 0),
        "unpriced": profiles_for_patterns("ooo", "lll", "ool", "oll"),
        "priced": profiles_for_patterns("ooo", "lll", "ool", "oll"),
        "minimum_total_cost": 0,
    },
    {
        "parameters": (1, 1, 0),
        "unpriced": profiles_for_patterns("ooo", "ool", "oll"),
        "priced": profiles_for_patterns("oll", "eol"),
        "minimum_total_cost": 1,
    },
    {
        "parameters": (1, 0, 1),
        "unpriced": profiles_for_patterns("ooo", "eee", "eoo"),
        "priced": profiles_for_patterns("eee", "eeo", "eol"),
        "minimum_total_cost": 2,
    },
    {
        "parameters": (1, 1, 1),
        "unpriced": profiles_for_patterns("eol", "eoo"),
        "priced": profiles_for_patterns("eol"),
        "minimum_total_cost": 2,
    },
    {
        "parameters": (3, 1, 4),
        "unpriced": profiles_for_patterns("eee"),
        "priced": profiles_for_patterns("eol"),
        "minimum_total_cost": 7,
    },
    {
        "parameters": (4, 0, 3),
        "unpriced": profiles_for_patterns("ooo", "eee"),
        "priced": profiles_for_patterns("eee", "eoo", "eol"),
        "minimum_total_cost": 7,
    },
    {
        "parameters": (4, 1, 3),
        "unpriced": profiles_for_patterns("ooo", "eoo"),
        "priced": profiles_for_patterns("eol"),
        "minimum_total_cost": 7,
    },
    {
        "parameters": (3, 0, 4),
        "unpriced": profiles_for_patterns("eee"),
        "priced": profiles_for_patterns("eee", "eeo", "eoo", "eol"),
        "minimum_total_cost": 7,
    },
)


def unique_permutations(items: list[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(set(permutations(items))))


def outcome_distribution(profile: tuple[str, ...]) -> tuple[tuple[int, ...], ...]:
    """Return equally likely service-time outcomes for a two- or three-player profile."""
    groups: dict[int, list[int]] = {}
    for player, action in enumerate(profile):
        groups.setdefault(DEPARTURE_TIME[action], []).append(player)

    group_orders = [
        unique_permutations(groups[departure_time])
        for departure_time in sorted(groups)
    ]
    outcomes: list[tuple[int, ...]] = []
    for chosen_orders in product(*group_orders):
        queue_order = [player for order in chosen_orders for player in order]
        service_times: list[int | None] = [None] * len(profile)
        previous_service = -10
        for player in queue_order:
            departure = DEPARTURE_TIME[profile[player]]
            service = max(departure, previous_service + 1)
            service_times[player] = service
            previous_service = service
        outcomes.append(tuple(int(value) for value in service_times))
    return tuple(outcomes)


def private_costs(
    profile: tuple[str, ...],
    early: int | Fraction,
    delay: int | Fraction,
    late: int | Fraction,
) -> tuple[Fraction, ...]:
    outcomes = outcome_distribution(profile)
    costs = [Fraction(0) for _ in profile]
    for service_times in outcomes:
        for player, service_time in enumerate(service_times):
            departure = DEPARTURE_TIME[profile[player]]
            journey_delay = service_time - departure
            schedule_cost = (
                -service_time * early
                if service_time < 0
                else service_time * late
            )
            costs[player] += journey_delay * delay + schedule_cost
    return tuple(value / len(outcomes) for value in costs)


def congestion_toll(
    player: int,
    profile: tuple[str, str, str],
    early: int | Fraction,
    delay: int | Fraction,
    late: int | Fraction,
    variant: str = "isc_ipc",
) -> Fraction:
    """Apply the note's toll placements using a selected epsilon formula.

    ``isc_ipc`` uses the arithmetic implied by the source table:
    (2D + L) - 0.5(E + D) = 1.5D + L - 0.5E.

    ``printed`` preserves the table's displayed, but arithmetically
    inconsistent, +0.5E term for comparison.
    """
    action = profile[player]
    pair = "".join(
        sorted(
            (profile[index] for index in range(3) if index != player),
            key=ACTIONS.index,
        )
    )

    alpha = max(delay - early, Fraction(0))
    beta = max(Fraction(3, 2) * (delay - early), Fraction(0))
    delta = max(Fraction(1, 2) * (delay - early), Fraction(0))
    theta = max(
        delay + Fraction(2, 3) * late - Fraction(1, 3) * early,
        Fraction(0),
    )
    if variant == "isc_ipc":
        epsilon = max(
            Fraction(3, 2) * delay + late - Fraction(1, 2) * early,
            Fraction(0),
        )
    elif variant == "printed":
        epsilon = max(
            Fraction(3, 2) * delay + late + Fraction(1, 2) * early,
            Fraction(0),
        )
    else:
        raise ValueError(f"Unknown toll variant: {variant}")
    mu = Fraction(1, 2) * (delay + late)
    lam = delay + late
    sigma = Fraction(3, 2) * (delay + late)

    toll_by_cell = {
        ("v", "vv"): alpha,
        ("v", "ve"): beta,
        ("v", "vo"): delta,
        ("v", "vl"): delta,
        ("e", "ve"): delta,
        ("e", "ee"): theta,
        ("e", "eo"): epsilon,
        ("e", "el"): delta,
        ("o", "vo"): mu,
        ("o", "eo"): mu,
        ("o", "oo"): lam,
        ("o", "ol"): sigma,
        ("l", "vl"): mu,
        ("l", "el"): mu,
        ("l", "ol"): mu,
        ("l", "ll"): lam,
    }
    return toll_by_cell.get((action, pair), Fraction(0))


def costs(
    profile: tuple[str, str, str],
    early: int,
    delay: int,
    late: int,
    priced: bool,
    toll_variant: str = "isc_ipc",
) -> tuple[Fraction, ...]:
    private = private_costs(profile, early, delay, late)
    if not priced:
        return private
    return tuple(
        private[player]
        + congestion_toll(
            player,
            profile,
            early,
            delay,
            late,
            variant=toll_variant,
        )
        for player in range(3)
    )


def equilibria(
    early: int,
    delay: int,
    late: int,
    priced: bool,
    toll_variant: str = "isc_ipc",
) -> tuple[str, ...]:
    result: list[str] = []
    for profile in product(ACTIONS, repeat=3):
        current_costs = costs(
            profile,
            early,
            delay,
            late,
            priced,
            toll_variant=toll_variant,
        )
        equilibrium = True
        for player in range(3):
            for alternative in ACTIONS:
                if alternative == profile[player]:
                    continue
                changed = list(profile)
                changed[player] = alternative
                changed_profile = tuple(changed)
                if (
                    costs(
                        changed_profile,
                        early,
                        delay,
                        late,
                        priced,
                        toll_variant=toll_variant,
                    )[player]
                    < current_costs[player]
                ):
                    equilibrium = False
                    break
            if not equilibrium:
                break
        if equilibrium:
            result.append("".join(profile))
    return tuple(sorted(result))


def minimum_total_cost(early: int, delay: int, late: int) -> Fraction:
    return min(
        sum(private_costs(profile, early, delay, late))
        for profile in product(ACTIONS, repeat=3)
    )


def fraction_value(value: Fraction) -> int | float:
    return int(value) if value.denominator == 1 else float(value)


def build_report() -> dict[str, object]:
    cases: list[dict[str, object]] = []
    for case in PUBLISHED_CASES:
        early, delay, late = case["parameters"]
        computed_unpriced = equilibria(early, delay, late, priced=False)
        computed_priced = equilibria(
            early,
            delay,
            late,
            priced=True,
            toll_variant="isc_ipc",
        )
        printed_priced = equilibria(
            early,
            delay,
            late,
            priced=True,
            toll_variant="printed",
        )
        computed_minimum = minimum_total_cost(early, delay, late)
        published_unpriced = tuple(case["unpriced"])
        published_priced = tuple(case["priced"])
        cases.append(
            {
                "early": early,
                "delay": delay,
                "late": late,
                "published_unpriced_count": len(published_unpriced),
                "computed_unpriced_count": len(computed_unpriced),
                "published_priced_count": len(published_priced),
                "computed_priced_count": len(computed_priced),
                "printed_priced_count": len(printed_priced),
                "published_minimum_total_cost": case["minimum_total_cost"],
                "computed_minimum_total_cost": fraction_value(computed_minimum),
                "published_unpriced_solutions": list(published_unpriced),
                "computed_unpriced_solutions": list(computed_unpriced),
                "published_priced_solutions": list(published_priced),
                "computed_priced_solutions": list(computed_priced),
                "printed_priced_solutions": list(printed_priced),
                "unpriced_match": computed_unpriced == published_unpriced,
                "priced_match": computed_priced == published_priced,
                "printed_priced_match": printed_priced == published_priced,
                "minimum_cost_match": computed_minimum
                == case["minimum_total_cost"],
                "exact_row_match": (
                    computed_unpriced == published_unpriced
                    and computed_priced == published_priced
                    and computed_minimum == case["minimum_total_cost"]
                ),
            }
        )
    return {
        "model": "corrected FIFO probabilities plus arithmetic ISC-IPC tolls",
        "comparison_model": (
            "same model with the Janusch table's printed +0.5E epsilon sign"
        ),
        "original_doi": "https://doi.org/10.1016/j.tra.2005.02.021",
        "corrigendum_doi": "https://doi.org/10.1016/j.tra.2015.05.009",
        "case_count": len(cases),
        "exact_row_matches": sum(bool(case["exact_row_match"]) for case in cases),
        "printed_exact_row_matches": sum(
            bool(
                case["unpriced_match"]
                and case["printed_priced_match"]
                and case["minimum_cost_match"]
            )
            for case in cases
        ),
        "cases": cases,
    }


def write_csv(report: dict[str, object], stream) -> None:
    fieldnames = [
        "early",
        "delay",
        "late",
        "published_unpriced_count",
        "computed_unpriced_count",
        "published_priced_count",
        "computed_priced_count",
        "printed_priced_count",
        "published_minimum_total_cost",
        "computed_minimum_total_cost",
        "unpriced_match",
        "priced_match",
        "printed_priced_match",
        "minimum_cost_match",
        "exact_row_match",
        "published_unpriced_solutions",
        "computed_unpriced_solutions",
        "published_priced_solutions",
        "computed_priced_solutions",
        "printed_priced_solutions",
    ]
    writer = csv.DictWriter(stream, fieldnames=fieldnames)
    writer.writeheader()
    for case in report["cases"]:
        row = dict(case)
        for field in (
            "published_unpriced_solutions",
            "computed_unpriced_solutions",
            "published_priced_solutions",
            "computed_priced_solutions",
            "printed_priced_solutions",
        ):
            row[field] = " ".join(row[field])
        writer.writerow({field: row[field] for field in fieldnames})


def write_markdown(report: dict[str, object], stream) -> None:
    stream.write(
        "# Corrigendum reproduction audit\n\n"
        f"Exact rows reproduced using the stated ISC - IPC arithmetic: "
        f"{report['exact_row_matches']} of {report['case_count']}.\n\n"
        f"Exact rows reproduced using the source table's printed +0.5E sign: "
        f"{report['printed_exact_row_matches']} of {report['case_count']}.\n\n"
        "| E | D | L | Published U | Computed U | Published P | ISC-IPC P | "
        "Printed-sign P | Minimum cost | Exact row |\n"
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|\n"
    )
    for case in report["cases"]:
        stream.write(
            f"| {case['early']} | {case['delay']} | {case['late']} | "
            f"{case['published_unpriced_count']} | {case['computed_unpriced_count']} | "
            f"{case['published_priced_count']} | {case['computed_priced_count']} | "
            f"{case['printed_priced_count']} | "
            f"{case['computed_minimum_total_cost']} | "
            f"{'yes' if case['exact_row_match'] else 'no'} |\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format",
        choices=("json", "csv", "markdown"),
        default="markdown",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = build_report()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        stream = args.output.open("w", encoding="utf-8", newline="")
    else:
        stream = sys.stdout

    try:
        if args.format == "json":
            json.dump(report, stream, indent=2)
            stream.write("\n")
        elif args.format == "csv":
            write_csv(report, stream)
        else:
            write_markdown(report, stream)
    finally:
        if args.output:
            stream.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
