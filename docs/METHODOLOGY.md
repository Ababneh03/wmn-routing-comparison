# Methodology and model audit

## Research question

How do application-level reception and packet lifetime change with node count for AODV and DSDV in the recovered stationary network configuration?

This repository preserves an existing experiment. It separates what was intended in the configuration comments from what the instantiated model actually recorded.

## Baseline design

The NED network contains an IPv4 configurator, a radio medium, and a configurable number of INET `ManetRouter` hosts. The five node counts are 10, 20, 30, 40, and 50. Initial positions are sampled within configured bounds; the configured speed is zero. Both protocols run for 50 simulated seconds, with UDP traffic directed to `host[0]`.

AODV is selected through `routingApp`; DSDV is selected through `routing`. Existing INET implementations provide both protocols. No new routing algorithm implementation is claimed.

There is one repetition per scenario. The default seed set follows the run index, so changing density also changes the seed set. This is a baseline execution exercise, not a controlled multi-seed statistical comparison.

## Effective model findings

### Destination also sends traffic

The configuration's general application rule appears before its special receiver rule. Recorded parameters show `host[0].app[0]` is `UdpBasicApp`, not `UdpSink`. Destination counters therefore include traffic from a node that also transmits to itself. Do not treat these counters as a clean measure of successfully delivered over-the-air traffic.

A corrected experimental profile should put the specific receiver rule before the general sender rule, then verify the effective parameters and regenerate all recordings. That correction has deliberately not been applied to the historical baseline.

### Radio medium and range

The NED file instantiates a fixed `RadioMedium` submodule. Recorded parameters confirm the generic type, despite a configuration entry assigning a scalar IEEE 802.11 medium type. The baseline contains a communication-range entry, but its presence in the configuration alone does not establish that the chosen physical model uses it.

Before drawing conclusions about connectivity or a radio-range sweep, explicitly define the intended medium, propagation model, sensitivity, and transmitter parameters, and verify their effective values. Retest any such correction as a separate experiment.

### Energy model

The model uses `IdealEpEnergyStorage`. Its recorded consumption bookkeeping should not be interpreted as the lifetime of a finite 100 J battery. A battery-lifetime study would need an appropriate finite-storage model, consistent consumption parameters, and a validated failure/depletion mechanism.

### Archive consistency

The recovered archive mixes 100 m and 250 m configuration entries, lacks three scalar summaries, and contains a ten-node DSDV vector trace ending around 27.1 seconds. These recordings are not combined into the new dataset. A later 250 m ten-node DSDV check also failed to reproduce the old totals; the recorded range entry alone is not an explanation of the mismatch.

## Measurements reported here

| Field | Meaning |
| --- | --- |
| Destination received packets | `packetReceived:count` at `host[0].app[0]`, including any local traffic. |
| Destination received bytes | `packetReceived:sum(packetBytes)` at the same application. |
| Mean received packet lifetime | The `mean` field of `rcvdPkLifetime:stats`, in seconds. |
| Lifetime sample count | Number of received-packet lifetime observations. |

No loss ratio is inferred from these counters. Mean lifetime is measured only for received packets, so it does not describe packets that were never delivered. No confidence intervals are shown because there is one repetition per case.

## Recommended next experimental version

1. Correct and verify the receiver application and radio-medium selection.
2. Validate connectivity and distinguish local from wireless traffic.
3. Use the same scenario/seed schedule for a paired protocol comparison and run multiple independent repetitions.
4. Define a warm-up policy and measure the actual active traffic interval.
5. Validate metric definitions and any finite-energy model.
6. Archive effective parameters, simulator/framework revisions, complete durations, and analysis inputs.

Those changes would form a new experimental version. They should not be represented as the settings or results of the published paper without checking the original research records.
