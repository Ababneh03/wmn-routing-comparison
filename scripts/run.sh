#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
usage() {
    printf '%s\n' 'Usage: bash scripts/run.sh [all|AODV_Test|DSDV_Test] [0-4|all]' \
        'Requires OMNETPP_ROOT and INET_ROOT for existing compiled installations.'
}
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then usage; exit 0; fi
PROTOCOL="${1:-all}"
RUNS="${2:-all}"
case "$PROTOCOL" in all|AODV_Test|DSDV_Test) ;; *) usage >&2; exit 2 ;; esac
case "$RUNS" in all|[0-4]) ;; *) usage >&2; exit 2 ;; esac
: "${OMNETPP_ROOT:?Set OMNETPP_ROOT to your compiled OMNeT++ installation}"
: "${INET_ROOT:?Set INET_ROOT to your compiled INET installation}"
OMNETPP_ROOT="$(cd "$OMNETPP_ROOT" && pwd)"
INET_ROOT="$(cd "$INET_ROOT" && pwd)"
OPP_RUN="$OMNETPP_ROOT/bin/opp_run"
[[ -x "$OPP_RUN" ]] || { printf 'Simulator executable not found.\n' >&2; exit 2; }
[[ -d "$INET_ROOT/src/inet" ]] || { printf 'INET source directory not found.\n' >&2; exit 2; }
library_found=false
for candidate in "$INET_ROOT/src/libINET.dylib" "$INET_ROOT/src/libINET.so" "$INET_ROOT/src/INET.dll" "$INET_ROOT/src/libINET.dll"; do
    if [[ -f "$candidate" ]]; then library_found=true; break; fi
done
if [[ "$library_found" != true ]]; then
    printf 'Compile the INET release library before running this project.\n' >&2
    exit 2
fi

RESULT_ROOT="$PROJECT_ROOT/results/raw"
# Use a new directory on every invocation so previous recordings remain available.
mkdir -p "$RESULT_ROOT"
RUN_DIR="$(mktemp -d "$RESULT_ROOT/run-XXXXXXXX")"
printf 'Writing this invocation to %s\n' "$RUN_DIR"
"$OPP_RUN" -v > "$RUN_DIR/simulator-version.txt" 2>&1
protocols=("$PROTOCOL")
if [[ "$PROTOCOL" == all ]]; then protocols=(AODV_Test DSDV_Test); fi
for protocol in "${protocols[@]}"; do
    args=(-u Cmdenv -l "$INET_ROOT/src/INET"
        -n "$INET_ROOT/src:$PROJECT_ROOT/simulations"
        -f "$PROJECT_ROOT/simulations/thesis_wmn/omnetpp.ini"
        -c "$protocol" "--result-dir=$RUN_DIR" --cmdenv-express-mode=true)
    if [[ "$RUNS" != all ]]; then args+=(-r "$RUNS"); fi
    printf 'Running %s (%s).\n' "$protocol" "$RUNS"
    if ! "$OPP_RUN" "${args[@]}" > "$RUN_DIR/$protocol.log" 2>&1; then
        printf 'Run failed; see %s\n' "$RUN_DIR/$protocol.log" >&2
        tail -n 20 "$RUN_DIR/$protocol.log" >&2
        exit 1
    fi
    printf 'Completed %s.\n' "$protocol"
done
printf 'Analyze this invocation with:\npython3 scripts/analyze.py --input "%s" --output results/generated\n' "$RUN_DIR"
