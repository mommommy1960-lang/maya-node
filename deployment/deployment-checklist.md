# Deployment Checklist

## Pre-Deployment
- [ ] Site assessment completed
  - [ ] Load analysis & profiles captured
  - [ ] Mounting location validated (structural integrity)
  - [ ] Trenching plan for cabling reviewed
  - [ ] Grounding system design approved
  
- [ ] Permits & Compliance
  - [ ] Local electrical permits obtained
  - [ ] Interconnection agreement signed
  - [ ] UL certification verified
  - [ ] IEEE standards compliance confirmed
  
- [ ] Equipment Staging
  - [ ] MAYA Node unit inspected
  - [ ] Battery modules tested
  - [ ] Inverter hardware validated
  - [ ] Cable assemblies verified
  - [ ] Mounting hardware ready

## Installation Phase
- [ ] Physical Installation
  - [ ] Mounting rails secured
  - [ ] Node unit properly positioned
  - [ ] Lightning protection installed
  - [ ] Surge protection devices mounted
  
- [ ] Electrical Connections
  - [ ] AC input wiring completed (grid/genset)
  - [ ] DC connections to battery validated
  - [ ] Load circuits connected by priority tier
  - [ ] Grounding verified (< 5Ω resistance)
  
- [ ] Network & Communications
  - [ ] Control network configured
  - [ ] Telemetry uplink tested
  - [ ] Local monitoring interface accessible

## Commissioning
- [ ] Safety Checks
  - [ ] Insulation resistance test passed (>1MΩ)
  - [ ] Ground fault detection (GFD/RCD) verified
  - [ ] Emergency shutdown tested
  - [ ] Arc fault protection validated
  
- [ ] Functional Testing
  - [ ] Battery charge/discharge cycles
  - [ ] Inverter operation at rated power
  - [ ] Automatic transfer switch timing
  - [ ] Load shedding sequence verification
  - [ ] Genset auto-start (if applicable)
  
- [ ] Performance Validation
  - [ ] Round-trip efficiency measured
  - [ ] Thermal management verified
  - [ ] Failover timing < 50ms confirmed

## Burn-in Period (7 days)
- [ ] Day 1: Initial monitoring
- [ ] Day 2-3: Full load testing
- [ ] Day 4-5: Edge case scenarios
- [ ] Day 6-7: Continuous operation validation
- [ ] Alarm system tested
- [ ] On-call rotation activated
- [ ] Documentation package delivered

## Post-Deployment
- [ ] Site-specific runbook created
- [ ] Operator training completed
- [ ] Remote monitoring dashboard configured
- [ ] Maintenance schedule established
- [ ] Escalation procedures documented
- [ ] Final sign-off obtained

## Notes
_Use this checklist in conjunction with `orchestration.md` for deployment workflow guidance._
