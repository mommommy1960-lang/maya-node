# MAYA Node - Deployment Matrix

## Overview
This matrix defines supported deployment configurations, feature availability, compliance requirements, and regional considerations for MAYA Node installations.

## Deployment Environments

### Environment Types

#### Production Environments

| Environment | Description | License Required | Min. Capacity | Max. Capacity | Support Tier |
|-------------|-------------|------------------|---------------|---------------|--------------|
| **Critical Infrastructure** | Telecom towers, data centers, hospitals | Professional+ | 50 kW | 1 MW | 24h SLA |
| **Industrial** | Manufacturing, fleet depots, mining operations | Standard+ | 100 kW | 500 kW | 48h SLA |
| **Commercial** | Retail, offices, warehouses | Standard+ | 25 kW | 250 kW | 48h SLA |
| **Residential Microgrid** | Community, multi-family housing | Standard+ | 50 kW | 200 kW | 48h SLA |
| **Humanitarian** | Refugee camps, disaster relief, clinics | Special Grant | 10 kW | 100 kW | Best Effort |
| **Remote/Off-Grid** | Islands, rural clinics, research stations | Standard+ | 10 kW | 100 kW | 48h SLA |

#### Non-Production Environments

| Environment | Description | License Required | Notes |
|-------------|-------------|------------------|-------|
| **Development** | Engineering development, testing | Community | Telemetry required |
| **Staging** | Pre-production validation | Community | Converted capacity limits |
| **Research** | Academic/research institutions | Research Grant | Publication requirements |
| **Training** | Operator training, demonstrations | Community | Time-limited |

## Feature Availability Matrix

### By License Tier

| Feature Category | Community | Standard | Professional | Enterprise |
|------------------|-----------|----------|--------------|------------|
| **Core Power Management** |
| Predictive dispatch | ✓ | ✓ | ✓ | ✓ |
| Priority load tiers (P1-P3) | ✓ | ✓ | ✓ | ✓ |
| SOC-aware scheduling | ✓ | ✓ | ✓ | ✓ |
| Brownout protection | ✓ | ✓ | ✓ | ✓ |
| **Advanced Features** |
| 6-hour load forecasting | Basic | ✓ | ✓ | ✓ |
| 24-hour solar forecasting | ✗ | ✗ | ✓ | ✓ |
| Weather API integration | ✗ | ✗ | ✓ | ✓ |
| Machine learning optimization | ✗ | ✗ | ✗ | ✓ |
| Multi-site coordination | ✗ | ✗ | Limited | ✓ |
| V2G/VPP participation | ✗ | ✗ | ✗ | ✓ |
| **Integrations** |
| Modbus TCP | ✓ | ✓ | ✓ | ✓ |
| OPC UA | ✗ | ✓ | ✓ | ✓ |
| MQTT telemetry | ✓ | ✓ | ✓ | ✓ |
| RESTful API | Read-only | ✓ | ✓ | ✓ |
| Custom protocols | ✗ | ✗ | ✗ | ✓ |
| **Monitoring & Control** |
| Local HMI | ✓ | ✓ | ✓ | ✓ |
| Web dashboard | Limited | ✓ | ✓ | ✓ |
| Mobile app | ✗ | ✗ | ✓ | ✓ |
| Cloud analytics | ✗ | ✗ | ✓ | ✓ |
| Custom reporting | ✗ | ✗ | ✗ | ✓ |
| **Maintenance** |
| OTA firmware updates | Manual | Auto | Auto | Auto |
| Remote diagnostics | ✗ | Basic | ✓ | ✓ |
| Predictive maintenance | ✗ | ✗ | ✗ | ✓ |
| Hot-swap support | ✗ | ✓ | ✓ | ✓ |

### By Deployment Type

| Feature | Telecom Tower | Fleet Depot | Clinic/Shelter | Data Center | Residential |
|---------|---------------|-------------|----------------|-------------|-------------|
| Genset integration | Required | Optional | Required | Optional | Optional |
| Grid interconnection | Optional | Recommended | Optional | Required | Recommended |
| Thermal integration | Optional | ✓ | ✓ | ✓ | Optional |
| 3-phase output | ✓ | ✓ | ✓ | ✓ | ✗ |
| Split-phase output | ✗ | ✗ | Optional | ✗ | ✓ |
| Battery capacity | 50-150 kWh | 100-500 kWh | 50-200 kWh | 500+ kWh | 20-100 kWh |
| Recommended license | Professional | Standard+ | Standard+ | Enterprise | Standard |

## Regional Deployment Matrix

### Compliance and Certification by Region

| Region | Standards | Certifications | Grid Code | License Tier | Notes |
|--------|-----------|----------------|-----------|--------------|-------|
| **North America** |
| USA | UL 1741 SB, IEEE 1547 | UL 9540, UL 9540A | IEEE 1547-2018 | All | Full support |
| Canada | CSA C22.2 | CSA | CSA C22.3 No. 9 | All | French documentation available |
| **Caribbean** |
| Islands | IEEE 1547 (adapted) | UL | Varies by territory | Standard+ | Hurricane-rated required |
| **Latin America** |
| Mexico | NOM-001-SEDE | NOM | CFE | Standard+ | Spanish support |
| Central America | IEC 62109 | Varies | Country-specific | Standard+ | Local partnerships |
| South America | IEC 62109 | INMETRO (Brazil) | Country-specific | Standard+ | Portuguese/Spanish |
| **Europe** |
| EU | EN 50549, IEC 62109 | CE | VDE-AR-N 4105 | Professional+ | GDPR compliant telemetry |
| UK | G98/G99 | BSI | G98/G99 | Professional+ | Post-Brexit standards |
| **Africa** |
| Sub-Saharan | IEC 62109 | SABS (varies) | Country-specific | Standard+ | Priority deployment region |
| North Africa | IEC 62109 | Local authorities | Country-specific | Standard+ | French/Arabic support |
| **Asia-Pacific** |
| Australia/NZ | AS/NZS 4777 | SAA | AS/NZS 4777.2 | Professional+ | Remote monitoring required |
| Southeast Asia | IEC 62109 | Varies | Country-specific | Standard+ | High-temperature validation |
| India | CEA regulations | BIS | CEA (Technical Standards) | Standard+ | Local partnership required |
| **Middle East** |
| Gulf States | IEC 62109 | ESMA, SASO | DEWA (Dubai), SEC (KSA) | Professional+ | High-temperature variant |

### Export Controls

| Country/Region | Export Classification | Special Requirements | Restrictions |
|----------------|----------------------|----------------------|--------------|
| USA | ECCN: TBD | EAR compliance | Embargo countries restricted |
| Canada | ECL: TBD | CEPA compliance | None currently |
| EU | Dual-use: TBD | EU Dual-Use Regulation | Country-specific |

## Deployment Size Matrix

### Small Deployments (10-50 kW)
- **Target:** Small clinics, residential communities, telecom shelters
- **Configuration:** Single cabinet, 1-2 inverters, 20-50 kWh battery
- **License:** Standard
- **Typical Users:** Rural healthcare, community centers, small businesses

### Medium Deployments (50-250 kW)
- **Target:** Telecom towers, industrial facilities, large clinics
- **Configuration:** 2 cabinets, 2-5 inverters, 50-200 kWh battery
- **License:** Standard or Professional
- **Typical Users:** Mobile operators, hospitals, manufacturing

### Large Deployments (250-1000 kW)
- **Target:** Data centers, fleet depots, campus microgrids
- **Configuration:** Multiple cabinets, 5-10 inverters, 200-500 kWh battery
- **License:** Professional or Enterprise
- **Typical Users:** Enterprises, utilities, large institutions

### Very Large Deployments (1+ MW)
- **Target:** Community microgrids, industrial parks, VPP aggregation
- **Configuration:** Distributed architecture, 10+ inverters, 500+ kWh battery
- **License:** Enterprise
- **Typical Users:** Municipalities, utility-scale projects, VPP operators

## Environmental Operating Conditions

| Parameter | Standard | Extended | Extreme |
|-----------|----------|----------|---------|
| Temperature range | -10°C to +45°C | -20°C to +55°C | -40°C to +65°C |
| Humidity | 5-95% non-condensing | 5-98% | 5-100% with coating |
| Altitude | 0-2000m | 0-3000m | 0-4000m (derated) |
| Enclosure | Type 3R | Type 4/4X | Custom |
| Salt fog | Moderate | High (coastal) | Extreme (offshore) |
| License tier | Standard+ | Professional+ | Enterprise |
| Cost multiplier | 1.0x | 1.3x | 1.8x |

## Connectivity Requirements

| Deployment Type | Internet Required | Cellular Option | Satellite Option | Offline Mode |
|-----------------|-------------------|-----------------|------------------|--------------|
| Community Ed. | Yes (telemetry) | N/A | N/A | 72h max |
| Standard | Recommended | ✓ | ✗ | 30 days |
| Professional | Recommended | ✓ | ✓ | 90 days |
| Enterprise | Optional | ✓ | ✓ | Unlimited |

## Update and Maintenance Schedule

| License Tier | Firmware Updates | Security Patches | Feature Updates | EOL Support |
|--------------|------------------|------------------|-----------------|-------------|
| Community | Manual, quarterly | Manual | None | 1 year |
| Standard | Auto, monthly | Auto, immediate | Minor only | 3 years |
| Professional | Auto, monthly | Auto, immediate | All | 5 years |
| Enterprise | Custom schedule | Auto, immediate | Priority access | 7+ years |

## Deployment Recommendations

### High Reliability (99.9%+ uptime)
- Professional or Enterprise license
- Redundant inverters
- Dual genset capability
- 24/7 monitoring
- <4h response SLA

### Cost-Optimized
- Standard license
- Single inverter configuration
- PV + grid/genset backup
- Cloud telemetry
- 48h response SLA

### Off-Grid Remote
- Professional license (satellite option)
- Oversized battery (2-3 days autonomy)
- Genset backup mandatory
- Local HMI + satellite uplink
- On-site spare parts

### Research/Educational
- Community license with Research Grant
- Full feature access for evaluation
- Publication/citation requirements
- Collaboration opportunities

---
*Last Updated: 2025-11-10*
*Document Version: 1.0*
