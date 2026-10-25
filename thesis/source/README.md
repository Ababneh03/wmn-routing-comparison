> **Public portfolio edition:** administrative authorization/declaration pages are omitted. Chapters, appendices, bibliography, and research figures are retained from the supplied Overleaf export. The companion PDF was exported from Overleaf and had those two pages removed; its original printed pagination is retained. Recompiling this source can change front-matter numbering. This historical thesis is separate from the later baseline audit in the repository.

# Evaluation of Wireless Mesh Network Routing Protocols: AODV vs. DSDV

**Author:** Abdullah Mohammad Khair Ababneh  
**Institution:** German Jordanian University — Department of Computer Engineering  
**Supervisor:** Dr. Ala'a Khalifeh  
**Date:** 4 March 2026  

---

## About This Project

This is the LaTeX source for a Bachelor's thesis that evaluates two wireless mesh
network routing protocols — AODV and DSDV — through simulation in OMNeT++ 6.3 with
the INET 4.5 framework. The thesis covers protocol theory, simulation methodology,
results across five network densities, and deployment guidelines for IoT applications.

---

## How to Open and Compile on Overleaf

1. Go to [overleaf.com](https://www.overleaf.com)
2. Click **New Project → Upload Project** and upload this ZIP file
3. Click the **Menu** button (top-left) → set **Main document** to `main.tex`
4. Click **Menu** → set **Compiler** to `pdfLaTeX`
5. Click **Recompile**

> Click **Recompile a second time** after the first compile finishes. LaTeX needs
> two passes to resolve all cross-references, figure numbers, and the bibliography.
> A third pass may be needed for the table of contents page numbers.

---

## Project Structure

```
thesis_wmn/
├── main.tex                      ← Compile this file
├── references.bib                ← 21 bibliography entries
│
├── frontmatter/
│   ├── titlepage.tex
│   ├── dedication.tex
│   ├── acknowledgments.tex
│   ├── abstract.tex
│   └── abbreviations.tex
│
├── chapters/
│   ├── ch1_introduction.tex
│   ├── ch2_wmn_background.tex
│   ├── ch3_routing_mac.tex
│   ├── ch4_methodology.tex
│   ├── ch5_results.tex
│   └── ch6_conclusion.tex
│
├── appendices/
│   ├── appA_config.tex           ← Full omnetpp.ini and MeshNetwork.ned listings
│   └── appB_math.tex             ← Bianchi saturation model and retry-limit derivation
│
└── figures/                      ← All simulation screenshots
    ├── fig_ned_design.png
    ├── fig_ned_source.png
    ├── fig_analysis_tool.png
    ├── fig_delay_boxplot.png
    ├── fig_bytes_aodv.png
    ├── fig_bytes_dsdv.png
    ├── fig_pkts_aodv.png
    ├── fig_pkts_dsdv.png
    ├── fig_drops_aodv.png
    ├── fig_drops_dsdv.png
    ├── fig_energy_bar.png
    └── fig_energy_time.png
```

---

## Figures

All figures are real screenshots from OMNeT++ 6.3 / INET 4.5 simulation runs.

| Figure | File | Description |
|--------|------|-------------|
| 4.1 | `fig_ned_design.png` | OMNeT++ IDE NED Design view of the MeshNetwork model |
| 4.2 | `fig_ned_source.png` | MeshNetwork.ned source code in the OMNeT++ IDE |
| 4.3 | `fig_analysis_tool.png` | OMNeT++ Analysis Tool showing all 10 simulation runs |
| 5.1 | `fig_delay_boxplot.png` | End-to-end delay distribution for AODV and DSDV at all densities |
| 5.2a | `fig_bytes_aodv.png` | Total bytes received vs. N — AODV |
| 5.2b | `fig_bytes_dsdv.png` | Total bytes received vs. N — DSDV |
| 5.3a | `fig_pkts_aodv.png` | Packet reception count vs. N — AODV |
| 5.3b | `fig_pkts_dsdv.png` | Packet reception count vs. N — DSDV |
| 5.4a | `fig_drops_aodv.png` | Packet drops (no route found) vs. N — AODV |
| 5.4b | `fig_drops_dsdv.png` | Packet drops (no route found) vs. N — DSDV |
| 5.5 | `fig_energy_bar.png` | OMNeT++ Qtenv runtime view showing network activity |
| 5.6 | `fig_energy_time.png` | Residual energy at host[25] over time — AODV vs. DSDV |

---

## Simulation Setup

| Parameter | Value |
|-----------|-------|
| Simulation tool | OMNeT++ 6.3 + INET Framework 4.5 |
| Network area | 1000 m × 1000 m |
| Node counts | N ∈ {10, 20, 30, 40, 50} |
| Radio standard | IEEE 802.11g, mixed mode, 54 Mbps |
| Communication range | 100 m per node |
| Traffic pattern | Many-to-one UDP (all nodes → host[0]) |
| Packet size | 1000 B |
| Simulation duration | 50 s |
| Protocols compared | AODV (RFC 3561) vs. DSDV (Perkins & Bhagwat, 1994) |
| Metrics | Throughput, packet count, delay, energy, packet drop rate |

---

## Packages

All packages are available in Overleaf's default TeX Live installation. No additional
installation is needed.

`inputenc` · `fontenc` · `lmodern` · `geometry` · `setspace` · `graphicx` · `float` ·
`amsmath` · `amssymb` · `algorithm` · `algpseudocode` · `booktabs` · `longtable` ·
`array` · `multirow` · `tabularx` · `caption` · `subcaption` · `hyperref` · `xcolor` ·
`listings` · `fancyhdr` · `titlesec` · `acronym` · `parskip` · `microtype` · `natbib` ·
`pdfpages` · `emptypage` · `url`
