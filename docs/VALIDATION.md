# Validation record

Checked on 25 October 2026 using the recovered local simulator installation.

## Completed execution checks

- Both protocols ran at all five node counts.
- All ten scenarios reached 50 simulated seconds and produced scalar output.
- The ten-node AODV scenario matched all 1,303 saved scalar values exactly.
- The analysis extracts recorded measurements; it does not synthesize replacement results.
- The reference CSV and JSON are checked for matching values, coverage, packet-byte consistency, and lifetime sample counts.

The repository runner is also checked against the standalone package layout. Its check is recorded in `packaging-check.json` after the packaged run completes.

## Recovered archive limitations

Missing scalar summaries:

- AODV, 30 nodes.
- AODV, 40 nodes.
- DSDV, 30 nodes.

Vector files exist for these scenarios, but are not substituted for missing complete summary recordings.

Archived configuration entries differ across scenarios. The old ten-node DSDV vector data stops near 27.1 simulated seconds, whereas the fresh run reaches the configured 50-second limit. Its saved totals differ from both fresh ten-node checks (100 m and 250 m recorded range entries).

## Scope of verification

Successful execution does not prove that the configuration implements the intended physical experiment, that its metrics support a particular conclusion, or that a clean upstream installation reproduces the local results. See the [methodology audit](METHODOLOGY.md) for effective-model findings.

Raw output is generated locally and excluded from Git. The reference summary records a SHA-256 hash for every source scalar file so an available raw recording can be matched to its summary. The raw data is not otherwise distributed by this draft repository.
