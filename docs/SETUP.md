# Setup and requirements

## Verified local environment

- macOS on Apple Silicon.
- OMNeT++ 6.3.0, academic edition.
- INET installation reporting version 4.5.4 in its release notes.
- Python 3.14.3; the scripts target Python 3.10 or newer.
- Matplotlib 3.10.8 for figure generation.
- Bash for the command-line runner.

The local INET directory is not a Git checkout, so its relationship to an unchanged upstream release is not verified. Execution on a clean upstream installation, Linux, or Windows has not been verified. The runner targets macOS and Linux paths; use a compatible Bash environment or adapt it for Windows.

## Install the simulator and framework

Use the upstream installation instructions for [OMNeT++](https://omnetpp.org/) and [INET](https://inet.omnetpp.org/). Both must be built successfully before this repository can run. Their compiler, Python, and system dependencies are separate from this repository's plotting requirement.

The installed INET instructions describe this build sequence, after OMNeT++ is configured:

```bash
cd /path/to/inet
source setenv
python3 -m pip install -r python/requirements.txt
make makefiles
make
```

This repository loads the compiled release library directly. It does not install, download, or rebuild INET for you.

## Configure this repository

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export OMNETPP_ROOT=/path/to/omnetpp
export INET_ROOT=/path/to/inet
bash scripts/run.sh AODV_Test 0
```

Alternatively, copy `.env.example` to `.env`, fill in your paths, and load it into your shell. The runner does not automatically execute environment files.

The runner creates a separate random directory for each invocation inside `results/raw/`. Its absolute output path prevents output from being resolved relative to the configuration file. It loads NED files from this repository and INET's `src` directory; it does not require copying this project back into INET's examples.

## Run the experiment

```bash
bash scripts/run.sh all
```

Each protocol has five runs. Run indices 0–4 correspond to 10, 20, 30, 40, and 50 nodes. Each invocation writes logs alongside the scalar and vector output. The original configuration records vector data and can generate several gigabytes; these files are ignored by Git.

Select the single generated run directory printed by the runner when analyzing data:

```bash
python3 scripts/analyze.py --input results/raw/run-YOUR_RUN --output results/generated
python3 scripts/plot_results.py --input results/generated/summary.json --output figures/generated
```

`run-YOUR_RUN` is a placeholder. If the input tree contains multiple recordings for the same protocol, node count, and repetition, the analysis stops instead of silently choosing one.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Simulator executable not found | Set `OMNETPP_ROOT` to the compiled installation root. |
| INET library missing | Build the INET release library and set `INET_ROOT`. |
| Shared-library loading fails | Activate the simulator's environment and use a compatible INET build. |
| Network type cannot be found | Retain `simulations/package.ned` and the documented folder structure. |
| Unknown model or parameter | Compare the installed INET models with the verified local version; do not silently alter the baseline. |
| Duplicate scenario recordings | Analyze one invocation directory at a time. |
| Matplotlib import fails | Install `requirements.txt` in the Python environment used for plotting. |

Run `python3 scripts/check_reference.py` to check the bundled summary without any simulator installation.
