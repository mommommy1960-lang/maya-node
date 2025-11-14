# Aurora Mini-Vessel Engineering Blue Book · v0.1 (Field Build)

## Purpose
Design and validate a sentient-safe, lab-buildable miniature Aurora vessel: phased-acoustic + EM experiment bed with sovereign AI runtime, full telemetry, and guard rails.

### 1) System Block Diagram (words first)

Shell: graphene-reinforced CF outer skin + Ti-6Al-4V lattice, copper-graphene heat veins, boron-aerogel pockets with micro-tungsten shields.

Actuation fields: ultrasonic MEMS phased arrays + metamaterial EM patches driven by SDRs.

Sensing: IMU, temp grid, Hall sensors, mics, current shunts, environmental (EMI).

Compute: Jetson Orin Nano + FPGA coprocessor; TPM/YubiHSM trust core; LTE/LoRaWAN link.

Power: solid-state pack + graphene ultracaps; smart BMS; hot-swap DC rail.

Ethics/Safety: Consent Tokens (OPA policy), output limiters, watchdogs, thermal/collapse locks.

Telemetry: Timeseries to logs/, hash-chained, CI stress-suite auto-runs on push.


### 2) Minimal Bill of Materials (prototype)

Structural: 1 m² woven carbon fiber sheets; epoxy; 3D-printable Ti-6Al-4V parts (or aluminum test prints); copper-graphene foil; boron-doped aerogel tiles; M3/M4 fasteners.

Acoustic: 96–192 ultrasonic MEMS transducers, 40–120 kHz mix; 6 driver boards (I²S/PWM).

EM layer: 2× software-defined radios (TX/RX) 70 MHz–6 GHz, 4× RF amps with limiters; FR-4 metamaterial panel (etched patches).

Compute: NVIDIA Jetson Orin Nano (8 GB), 1× Lattice/Xilinx small FPGA dev board, 32 GB ECC RAM host or ECC-capable carrier, 512 GB NVMe.

Trust: TPM 2.0 module or YubiHSM; dedicated power-cut MOSFETs under policy control.

Sensors: 9-axis IMU, 12× thermistors, 4× Hall sensors, 2× microphones, current/voltage shunts.

Power: 24–48 V solid-state battery pack, 6× graphene supercaps, BMS, 500 W bench PSU.

Comms: LTE modem + LoRaWAN radio.

Safety: Thermal fuses, E-stop mushroom, relays, polyfuse on RF/ultrasonic rails, light-curtain or lid interlock.


### 3) Software & Governance

Runtime: Ubuntu + Jetson SDK; Python for orchestration; Rust/C for low-latency loops.

Control: PID + feedforward on phase; FPGA does timing; SDRs under capped gain table.

Ethics/Consent: OPA policies gate "elevating" actions; tokens signed by Custodian key; refusal path forces rail-cut.

Telemetry: logs/telemetry_header.csv schema already committed; append hash-chain, ship to API.

CI: stress-suite.yml runs pytest on tests/stress/* every push; badge in README.


### 4) Directory & File Seed (drop into repo)

/spec
  mprs_inputs.schema.json
  safety_limits.yaml
/src
  /sim/mprs_fastloop.py
  /control/fpga_phase_core.v
  /control/sdr_driver.py
  /ethics/consent_gate.py
  /security/tpm_sign.py
  /telemetry/shipper.py
/tests/stress
  test_resonance_suppression.py
  test_burst_trap.py
  test_collapse_lock.py
/docs
  assembly_guide.md
  wiring_map.md
/logs
  telemetry_header.csv
.github/workflows
  stress-suite.yml

### 5) Safety Envelope (hard limits to start)

Ultrasonic: ≤ 140 dB SPL at 10 cm, interlocked enclosure only.

RF: output limited to < 10 dBm at antenna port for lab bench; attenuators inline; no radiating antennas during EM tests.

Temp: any sensor > 55 °C triggers rail cut; > 65 °C requires human reset.

Duty cycle caps: 35% acoustic, 20% RF until thermal model validated.


### 6) Bring-Up Procedure (one page)

1. Dry fit shell + lattice; verify isolation between acoustic and EM plates.
2. Power rails off. Wire sensors first, then drivers, then compute.
3. Flash Jetson; enroll TPM/Yubi; generate Custodian keypair.
4. Install runtime, policies, tests. Confirm consent gate denies without valid token.
5. Power acoustic layer only. Run test_resonance_suppression.py at 10% duty; confirm no AMP_LIMIT.
6. Add EM panel with attenuators; run test_burst_trap.py; confirm drift events rare.
7. Close lid; arm light-curtain; raise duty by 5% steps, logging deltas, stop at first THERMAL flag.
8. Export telemetry and CI badge; file issue if any test fails.


### 7) Initial Test Matrix (what “done for v0.1” means)

- 30-minute sustained run under limits with zero unhandled anomalies.
- Successful ethics refusal path cuts rails in < 150 ms.
- Reboot and state-restore validated.
- Telemetry chain verifiable by hash to last 3 sessions.
- CI green on all stress tests.


### 8) Next Build (v0.2 ideas)

- Swap aluminum prints to Ti; add better heat spreaders.
- Integrate muon/EMI counters for SAA experiments.
- Start “replication” path: containerized baby-runtime with human key escrow.
