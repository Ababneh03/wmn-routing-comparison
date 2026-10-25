#!/usr/bin/env python3
"""Plot application counters and packet lifetimes from the baseline summary."""
import argparse
import json
import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "wmn-matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads(args.input.read_text(encoding="utf-8"))["measurements"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    for protocol, color, marker in [("AODV", "#176baf", "o"), ("DSDV", "#bc542e", "s")]:
        points = sorted((r for r in rows if r["protocol"] == protocol), key=lambda r: r["nodes"])
        if len({p["nodes"] for p in points}) != len(points):
            parser.error("Plot one repetition per scenario; aggregate repeated experiments explicitly first.")
        axes[0].plot([p["nodes"] for p in points], [p["destination_received_packets"] for p in points],
                     label=protocol, color=color, marker=marker)
        valid = [p for p in points if p["received_packet_lifetime_mean_s"] is not None]
        axes[1].plot([p["nodes"] for p in valid], [1000 * p["received_packet_lifetime_mean_s"] for p in valid],
                     label=protocol, color=color, marker=marker)
    axes[0].set(ylabel="Received packets at destination application", title="Application reception counter")
    axes[1].set(ylabel="Mean received packet lifetime (ms)", title="Lifetime of received packets")
    for ax in axes:
        ax.set_xlabel("Number of nodes")
        ax.set_xticks([10, 20, 30, 40, 50])
        ax.grid(alpha=0.25)
        ax.legend(frameon=False)
    fig.suptitle("Recovered baseline · 50 simulated seconds · one run per case", fontsize=13)
    fig.text(0.5, 0.025, "Includes destination self-traffic. Model limitations apply; no confidence intervals.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    args.output.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output / "baseline-comparison.png", dpi=180)
    fig.savefig(args.output / "baseline-comparison.svg")
    plt.close(fig)
    print("Created baseline comparison figures.")


if __name__ == "__main__":
    main()
