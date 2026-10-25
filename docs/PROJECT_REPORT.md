# Project report: recovered wireless-mesh routing baseline

## Objective

Package and execute a graduation-project model comparing AODV and DSDV as network size changes. The goal of this repository version is traceable execution and transparent measurement, rather than a new routing algorithm or an independent replication of the associated publication.

## Background

AODV discovers routes on demand; DSDV maintains routing information proactively. Their trade-offs depend on network conditions, traffic, topology, and implementation. The recovered experiment explores these protocols using existing INET modules.

## Implementation

The model defines an IPv4 configurator, a radio medium, and a host array. Two configuration profiles select the routing protocol. This repository preserves the original NED and INI files, supplies a standalone launcher, and extracts application-level measurements with a Python standard-library parser. Matplotlib generates figures from the extracted values.

## Execution

Ten cases were freshly executed: both protocols at 10, 20, 30, 40, and 50 nodes, each for 50 simulated seconds. The local environment uses OMNeT++ 6.3.0 and an INET directory reporting version 4.5.4. The standalone repository layout was additionally checked with both ten-node protocol cases. Their selected measurements match the reference dataset.

## Observed measurements

The destination also generates traffic in this preserved baseline. Consequently, these are application counters, including local traffic, rather than a pure wireless-delivery measurement. Packet lifetime is measured only among received packets. Values below summarize one repetition per case; no statistical confidence or general protocol ranking is inferred.

| Protocol | Nodes | Destination received packets | Destination received bytes | Mean received packet lifetime (ms) |
| --- | ---: | ---: | ---: | ---: |
| AODV | 10 | 301 | 301000 | 0.342 |
| AODV | 20 | 1154 | 1154000 | 14.830 |
| AODV | 30 | 1594 | 1594000 | 64.526 |
| AODV | 40 | 2326 | 2326000 | 37.999 |
| AODV | 50 | 2822 | 2822000 | 28.395 |
| DSDV | 10 | 301 | 301000 | 0.339 |
| DSDV | 20 | 1047 | 1047000 | 4.485 |
| DSDV | 30 | 1260 | 1260000 | 37.368 |
| DSDV | 40 | 1991 | 1991000 | 4.001 |
| DSDV | 50 | 2175 | 2175000 | 23.457 |

## Reproducibility findings

The ten-node AODV scalar measurements match the corresponding archived recording exactly. The archive contains missing scalar summaries, mixed recorded range settings, and a DSDV trace ending near 27.1 simulated seconds. Archived and fresh data are therefore treated as different artifacts rather than combined into a single comparison.

Raw output from the fresh ten-case check occupies approximately 4.4 GB. The Git repository contains compact summaries and input hashes, with raw recordings excluded. The runner preserves separate output directories for later invocations.

## Model limitations

1. The intended receiver application rule is shadowed by a more general earlier rule; the destination runs `UdpBasicApp` and sends to itself.
2. The instantiated medium is generic `RadioMedium`; the range setting alone does not establish the intended physical propagation behavior.
3. Ideal energy storage does not support a finite-battery lifetime conclusion.
4. One repetition per case is insufficient for statistical generalization, and the seed set changes with run index.
5. The locally installed framework is not a Git checkout; clean upstream compatibility is not established.

These findings concern the recovered baseline inspected here. They are not a determination about every experiment or result in the associated paper.

## Next experimental version

Correct and verify the receiver/medium configuration in a separate version, define unambiguous measurement and warm-up policies, run multiple independent repetitions with a controlled seed schedule, and archive effective parameters alongside the outputs. Validate connectivity and energy behavior before making physical-network or battery claims.

## Publication and attribution

The supplied ResearchGate record lists the related conference paper by Ala Khalifeh, Abdullah Ababneh, and Iacovos Ioannou. See the repository README and citation metadata for the record and DOI. This report describes a later execution check of recovered project files, not a replacement for or reconstruction of the publisher's paper.
