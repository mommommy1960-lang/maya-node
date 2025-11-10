# MAYA Node - Intellectual Property Registry

## Overview
This document tracks intellectual property (IP) assets within the MAYA Node project, including patents, trade secrets, proprietary algorithms, and confidential designs.

## Patent Portfolio

### Filed Patents
- **None currently filed**

### Potential Patent Areas
1. **Predictive Power Dispatch Algorithm**
   - Location: `firmware/controller/scheduler.py`
   - Description: Multi-tier priority-based power scheduling with SOC-aware forecasting
   - Status: Trade secret / proprietary
   - Protection: BUSL-1.1 license

2. **Thermal Integration Control System**
   - Description: PCM/hydronic thermal loop integration with power management
   - Status: Proprietary design
   - Protection: BUSL-1.1 license

3. **Fast Load Shedding Protocol**
   - Description: <50ms transfer time for priority loads during brownout conditions
   - Status: Proprietary implementation
   - Protection: BUSL-1.1 license

## Trade Secrets

### Core Algorithms
1. **Battery SOC Forecasting**
   - File: `firmware/controller/scheduler.py`
   - Protection Level: High
   - Access: Internal development only

2. **Load Prediction Models**
   - File: `firmware/edge-tests/sim_load_profiles.py`
   - Protection Level: Medium
   - Access: Internal + licensed partners

3. **Efficiency Optimization**
   - File: `firmware/edge-tests/efficiency_model.py`
   - Protection Level: High
   - Access: Internal development only

## Proprietary Designs

### Hardware Designs
- Cabinet layout and thermal management integration
- PCM storage system design
- Multi-phase power conversion topology

### Software Architecture
- Real-time control loop (250ms cycle)
- Safety interlock system
- Telemetry and logging infrastructure

## Third-Party Components

### Open Source Dependencies
- Python standard library (PSF License)
- React (MIT License)
- TypeScript (Apache 2.0 License)

### Commercial Dependencies
- TBD based on hardware integration choices

## IP Protection Strategy

### Licensing Model
- **Open Source Components**: Apache 2.0
- **Core Business Logic**: BUSL-1.1 (converts to Apache 2.0 after 4 years)
- **Hardware Designs**: Proprietary, licensed per deployment

### Geographic Protection
- Primary markets: North America, Caribbean, Sub-Saharan Africa
- Export compliance: ECCN classification pending

## Confidential Information

### Not for Public Disclosure
- Manufacturing costs and BOMs
- Supplier agreements and pricing
- Customer deployment data
- Performance benchmarks vs. competitors
- Future roadmap details (V2G, VPP aggregation)

## Review Schedule
- Quarterly IP review by engineering leadership
- Annual patent landscape analysis
- Continuous monitoring of competitor activities

## Contact
For IP-related inquiries: legal@maya-node.example.com

---
*Last Updated: 2025-11-10*
*Document Classification: Confidential*
