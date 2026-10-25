#!/usr/bin/env python3
"""Check the included baseline summary for coverage and internal consistency."""
import csv
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "results/reference/summary.json").read_text())
    rows = data["measurements"]
    expected = {(p, n) for p in ["AODV", "DSDV"] for n in [10, 20, 30, 40, 50]}
    assert len(rows) == 10, "Expected ten baseline scenarios"
    assert {(r["protocol"], r["nodes"]) for r in rows} == expected, "Scenario coverage mismatch"
    for row in rows:
        assert row["repetition"] == 0
        assert row["configured_duration"] == "50s"
        assert row["recorded_range_setting"] == "100m"
        assert row["destination_app_type"].endswith("UdpBasicApp")
        assert row["medium_type"].endswith(".RadioMedium")
        assert row["destination_received_bytes"] == 1000 * row["destination_received_packets"]
        assert row["received_packet_lifetime_count"] == row["destination_received_packets"]
        assert len(row["scalar_sha256"]) == 64
    with (root / "results/reference/summary.csv").open(newline="") as source:
        csv_rows = list(csv.DictReader(source))
    assert len(csv_rows) == len(rows), "CSV coverage mismatch"
    for actual, row in zip(csv_rows, rows):
        for key, value in row.items():
            assert actual[key] == ("" if value is None else str(value)), f"CSV/JSON mismatch: {key}"
    print("Reference data checks passed: ten cases, consistent counters and matching CSV/JSON.")


if __name__ == "__main__":
    main()
