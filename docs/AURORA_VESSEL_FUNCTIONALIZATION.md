# Aurora Vessel Simulation: Functionalization Pass

## What was found

The existing Aurora design is in the `maya-node` repository, not the current `flux-drive-kernel` repository. The key source is `docs/aurora-mini-vessel-bluebook-v0.md`, supported by the Aurora manifest, vessel simulation, and integration test.

The Blue Book defines a miniature experimental vessel with acoustic and electromagnetic experiment layers, sensors, Jetson/FPGA compute, power management, consent policies, watchdogs, rail-cut behavior, telemetry, and CI stress tests.

## What is now functional

This pass adds a deterministic, simulation-only vessel runtime. It implements:

- consent-gated arming;
- acoustic, RF duty, and RF power limit checks;
- thermal trips and hard-reset behavior;
- emergency-stop behavior;
- fail-closed command rejection;
- replayable telemetry;
- hash-chain integrity verification;
- unit tests for all of the above.

It has no hardware I/O and cannot energize acoustic, RF, or propulsion hardware.

## Engineering assessment

The Blue Book is a useful prototype architecture, but several parts are still concept-level:

- the proposed shell materials and thermal paths need mechanical and thermal engineering;
- the acoustic and EM layers need EMC, exposure, and enclosure validation;
- the listed compute stack needs a verified carrier, power budget, cooling design, and software image;
- the “collapse” and “field manipulation” concepts are not established propulsion mechanisms;
- the Flux Drive kernel should remain a measurement/safety interface until a physical experiment produces independently reviewed evidence.

## Next safe milestones

1. Run the new simulation tests in GitHub Actions.
2. Add a JSON schema for vessel commands, telemetry, and safety events.
3. Add deterministic replay fixtures and tamper-detection tests.
4. Build a low-power sensor-only bench before connecting any acoustic or RF driver.
5. Have a qualified lab review the enclosure, exposure, EMC, thermal, and force-measurement plans.
6. Keep all physical actuation behind a hardware interlock and human approval.

## Definition of done for v0.2

- all simulation tests pass;
- telemetry replays with a valid hash chain;
- invalid commands fail closed;
- safety limits are visible in configuration;
- no network or hardware side effects occur during simulation;
- the physical test plan remains separate from claims of propulsion success.
