#!/usr/bin/env python3
"""Extract application-level baseline measurements from OMNeT++ scalar files."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shlex


def read_scalar(path):
    records = {"attr": {}, "config": {}, "itervar": {}, "par": {}, "scalar": {}, "statistics": {}}
    statistic = None
    with path.open(encoding="utf-8") as source:
        for line in source:
            if not line.strip() or line.startswith("#"):
                continue
            parts = shlex.split(line)
            if not parts:
                continue
            kind = parts[0]
            if kind == "statistic":
                statistic = (parts[1], parts[2])
                records["statistics"][statistic] = {}
            elif kind == "field" and statistic is not None:
                records["statistics"][statistic][parts[1]] = parts[2]
            elif kind in ("scalar", "par"):
                statistic = None
                records[kind][(parts[1], parts[2])] = " ".join(parts[3:])
            elif kind in ("attr", "config", "itervar"):
                records[kind][parts[1]] = " ".join(parts[2:])
    return records


def number(value):
    if value is None:
        return None
    parsed = float(value)
    return parsed if math.isfinite(parsed) else None


def measurement(path):
    data = read_scalar(path)
    config = data["attr"].get("configname")
    if config not in ("AODV_Test", "DSDV_Test"):
        return None
    sink = "MeshNetwork.host[0].app[0]"
    delay = data["statistics"].get((sink, "rcvdPkLifetime:stats"), {})
    rx = number(data["scalar"].get((sink, "packetReceived:count")))
    received_bytes = number(data["scalar"].get((sink, "packetReceived:sum(packetBytes)")))
    if rx is None or received_bytes is None:
        raise ValueError(f"Missing required application counters: {path.name}")
    return {
        "protocol": config.removesuffix("_Test"),
        "nodes": int(data["itervar"]["N"]),
        "repetition": int(data["attr"].get("repetition", "0")),
        "seedset": data["attr"].get("seedset"),
        "configured_duration": data["config"].get("sim-time-limit"),
        "recorded_range_setting": data["config"].get("**.wlan[*].radio.transmitter.communicationRange"),
        "destination_app_type": data["par"].get((sink, "typename"), "").strip('"'),
        "medium_type": data["par"].get(("MeshNetwork.radioMedium", "typename"), "").strip('"'),
        "destination_received_packets": int(rx),
        "destination_received_bytes": int(received_bytes),
        "destination_sent_packets": number(data["scalar"].get((sink, "packetSent:count"))),
        "received_packet_lifetime_mean_s": number(delay.get("mean")),
        "received_packet_lifetime_count": number(delay.get("count")),
        "scalar_file": path.name,
        "scalar_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    seen = set()
    for path in sorted(args.input.rglob("*.sca")):
        row = measurement(path)
        if row is None:
            continue
        key = (row["protocol"], row["nodes"], row["repetition"])
        if key in seen:
            parser.error("Multiple recordings for the same scenario. Select one run directory instead of combining invocations.")
        seen.add(key)
        rows.append(row)
    if not rows:
        parser.error("No matching AODV or DSDV scalar recordings found.")
    rows.sort(key=lambda row: (row["protocol"], row["nodes"], row["repetition"]))
    args.output.mkdir(parents=True, exist_ok=True)
    summary = {
        "schema_version": 1,
        "scope": "Recovered baseline; application counters include destination self-traffic. Not a publication reproduction.",
        "measurements": rows,
    }
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (args.output / "summary.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Summarized {len(rows)} scenarios.")


if __name__ == "__main__":
    main()
