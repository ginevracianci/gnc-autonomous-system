# Mission Architecture Context

## 📋 Overview

This GNC system was developed within the broader context of **asteroid sample return mission architecture studies**, representing the critical autonomous operations subsystem for proximity operations and sample collection.

The mission architecture leverages heritage from successful sample return missions (Hayabusa, Hayabusa2, OSIRIS-REx) while incorporating advanced autonomy for future deep space exploration missions.

---

## 🎯 Mission Concept

### Mission Objectives

**Primary Objectives:**
1. Rendezvous with Near-Earth Asteroid (NEA)
2. Characterize asteroid properties (shape, rotation, composition)
3. Collect surface sample (100-500g)
4. Return sample to Earth for analysis

**Secondary Objectives:**
- Demonstrate autonomous proximity operations
- Validate GNC systems for small body exploration
- Advance technology readiness for future missions

### Target Selection

**Candidate Asteroids:**
- **C-type carbonaceous asteroids** (organic-rich, primitive material)
- **NEA with favorable orbital parameters** (ΔV < 6 km/s)
- **Diameter**: 200-500m (similar to Bennu, Ryugu)
- **Rotation period**: < 10 hours (manageable for operations)

**Example Target**: 1999 JU3 (Ryugu-class)

---

## 🏗️ System Architecture

### Top-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Asteroid Sample Return Spacecraft          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │   Cruise     │    │  Proximity   │    │  Sample   │ │
│  │   Stage      │    │  Operations  │    │  Return   │ │
│  │              │    │              │    │  Capsule  │ │
│  │ • Propulsion │    │ • GNC System │◄───│           │ │
│  │ • Power      │    │ • Payload    │    │ • Samples │ │
│  │ • Telecom    │    │ • Sampler    │    │ • Re-entry│ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
│         │                    ▲                   │       │
│         └────────────────────┴───────────────────┘       │
│                    Data & Control Bus                     │
└─────────────────────────────────────────────────────────┘
```

### GNC System Position in Architecture

**The GNC system developed in this repository is the core subsystem enabling:**
- Autonomous rendezvous from 2500 km
- Proximity operations at 20 km home position
- Touch-And-Go sample collection
- Hazard avoidance and safe operations

---

## 📊 Mission Phases

### Phase 1: Launch and Cruise (Year 0-2)

**Duration**: 1.5-3 years  
**ΔV Budget**: 0-500 m/s (trajectory corrections)

**Trajectory Options Analyzed:**

| Option | Type | Duration | ΔV | Pros | Cons |
|--------|------|----------|-----|------|------|
| **Ballistic** | Hohmann-like | 2-3 years | 3.5 km/s | Simple, reliable | Long duration |
| **SEP** | Solar Electric | 1.5-2 years | 6 km/s | Flexible, faster | Complex, heritage limited |
| **Hybrid** | Ballistic + SEP | 2 years | 4.5 km/s | Balanced | Moderate complexity |

**Selected**: Hybrid approach (baseline from lunar SEP trajectory study)

*Reference*: Related work on SEP trajectories for small satellites applied to asteroid missions

### Phase 2: Rendezvous (Months 0-1 at asteroid)

**Duration**: 20-30 days  
**ΔV Budget**: 100-200 m/s

**GNC Requirements** (from this repository):
- Approach from 2500 km to 20 km home position
- Autonomous trajectory control with <5% fuel margin
- Position accuracy: ±2.4 km (3σ)
- Velocity accuracy: ±0.12 m/s (3σ)
- Maintain spacecraft within 1° approach cone

**Key Challenges:**
- Uncertain asteroid gravity field
- No GPS - relative navigation only
- Light-time delay (5-20 minutes Earth communication)
- **Solution**: Autonomous GNC system (this repository)

### Phase 3: Proximity Operations (Months 1-6)

**Duration**: 3-6 months  
**Home Position**: 20 km from asteroid center

**Operations:**
- Global mapping (shape, rotation, gravity)
- Target site selection
- Rehearsal descents
- TAG operations

**GNC System Role**:
- Station-keeping at home position
- Descent/ascent trajectories
- Hazard detection and avoidance
- Real-time navigation

### Phase 4: Touch-And-Go Sample Collection

**Duration**: 5-10 attempts (2-5 seconds contact each)  
**Target**: 100-500g sample

**GNC Performance Requirements** (verified in this repository):

| Parameter | Requirement | Achieved (HIL) | Status |
|-----------|-------------|----------------|--------|
| Landing accuracy | ≤ 25 m (3σ) | 18.3 m | ✅ PASS |
| Vertical velocity | 10 ± 5 cm/s | 11.2 cm/s | ✅ PASS |
| Horizontal velocity | ≤ 5 cm/s | 3.8 cm/s | ✅ PASS |
| Attitude error | ≤ 10° | 7.2° | ✅ PASS |

**Verification**: Hardware-in-the-Loop testing documented in [HIL_TESTING.md](HIL_TESTING.md)

### Phase 5: Return Cruise (Years 2-4)

**Duration**: 1-2 years  
**ΔV Budget**: 500 m/s (Earth approach)

**GNC System**: Minimal use, cruise navigation only

### Phase 6: Earth Return

**Duration**: Days (re-entry)  
**Sample Recovery**: Direct entry capsule

---

## ⚖️ Key Trade-Offs

### Trade-Off 1: Trajectory Type

**Analysis**: Ballistic vs Solar Electric Propulsion (SEP)

**Criteria:**
- Mission duration
- ΔV budget
- Spacecraft mass
- Technology readiness
- Cost

**Decision**: Hybrid trajectory
- Launch on ballistic trajectory
- SEP for final approach phase
- Balances duration and complexity

**Heritage**: Lunar mission SEP trajectory study (Master's thesis)

### Trade-Off 2: GNC Autonomy Level

**Options:**

| Level | Description | Pros | Cons | Selected |
|-------|-------------|------|------|----------|
| **Ground-commanded** | All maneuvers planned on Earth | Simple S/C | Limited operations | ❌ |
| **Semi-autonomous** | Major maneuvers autonomous | Balanced | Moderate complexity | ❌ |
| **Fully autonomous** | All operations autonomous | Maximum flexibility | Complex GNC | ✅ |

**Decision**: Fully autonomous GNC
- **Rationale**: Light-time delay (5-20 min) makes ground commanding impractical for TAG
- **Risk Mitigation**: Extensive HIL testing, abort sequences
- **Heritage**: Hayabusa2 successful autonomous TAG

### Trade-Off 3: Sensor Suite

**Requirements**: Relative state estimation with 25m position accuracy

**Options Evaluated:**

| Sensor | Pros | Cons | Cost | Selected |
|--------|------|------|------|----------|
| **LIDAR** | Direct range, high accuracy | Power, mass | High | ✅ |
| **Optical Camera** | Low cost, high heritage | Processing intensive | Low | ✅ |
| **Star Tracker** | Absolute attitude | No relative position | Medium | ✅ |
| **IMU** | High rate, no external ref | Drift over time | Medium | ✅ |
| **Radar** | All-weather | Power, mass | Very High | ❌ |

**Selected Suite**: LIDAR + Optical Camera + Star Tracker + IMU
- Redundancy for critical operations
- Multi-sensor fusion in Kalman filter
- Cost-performance balance

**Implementation**: See [sensors.py](../src/system_architecture/sensors.py)

### Trade-Off 4: Sample Collection Method

**Options:**
- Touch-And-Go (TAG) with contact pad ← **SELECTED**
- Harpoon collection
- Net capture
- Claw/gripper

**Decision**: TAG with contact pad (Hayabusa2 heritage)
- **Pros**: Proven, minimal contamination, multiple attempts
- **Cons**: Requires precise GNC (this repository addresses this!)

---

## 🔬 Mission Analysis

### Mass Budget

| Element | Mass (kg) | Notes |
|---------|-----------|-------|
| Cruise Stage | 300-400 | Structure, propulsion, power |
| Proximity Ops Stage | 200-300 | GNC sensors, sampler |
| Sample Return Capsule | 50-100 | Heat shield, parachute |
| Propellant | 200-400 | Depends on trajectory |
| Sample | 0.1-0.5 | Target collection |
| **Total** | **750-1200** | Launch vehicle: Vega-C class |

### Power Budget

| Phase | Power (W) | Source |
|-------|-----------|--------|
| Cruise | 300-500 | Solar arrays |
| Proximity Ops | 500-800 | Solar arrays (GNC sensors high power) |
| TAG Operations | 800-1000 | Peak during descent |

**GNC System Power**: 150-200W during proximity operations

### Cost Estimate

**Rough Order of Magnitude** (ESA M-class mission):

| Element | Cost (M€) |
|---------|-----------|
| Spacecraft | 150-200 |
| Launch | 50-80 |
| Operations | 30-50 |
| Ground Segment | 20-30 |
| **Total** | **250-360** |

**Cost Category**: ESA Medium-class mission (M4/M5)

---

## 🎓 Systems Engineering Approach

### Requirements Flow

```
Mission Objectives
    ↓
Mission Requirements
    ↓
System Requirements
    ↓
Subsystem Requirements (including GNC)
    ↓
Component Requirements
```

**Example Flow:**

```
Mission Objective: "Collect pristine asteroid sample"
    ↓
Mission Requirement: "Sample collection accuracy"
    ↓
System Requirement: "Spacecraft landing within target site"
    ↓
GNC Requirement: "Landing accuracy ≤ 25m (3σ)"
    ↓
Component Requirement: "LIDAR range accuracy ≤ 0.1m"
```

**Full GNC requirements traceability**: See [requirements.py](../src/functional_analysis/requirements.py)

### Verification Approach

Following ECSS-E-ST-10-02C:

| Level | Method | Where |
|-------|--------|-------|
| Mission | Analysis + Mission Ops | In flight |
| System | Integration Test | Ground facility |
| Subsystem (GNC) | HIL Testing | This repository |
| Component | Unit Test | Lab testing |

**GNC Verification**: [HIL_TESTING.md](HIL_TESTING.md)

### MBSE Application

**Model-Based Systems Engineering** used throughout:

- **Tool**: CATIA Cameo Systems Modeler
- **Language**: SysML
- **Methodology**: ESA SysML Solution guidelines

**Artifacts**:
- Mission objectives tree
- Requirements diagrams
- System architecture (BDD, IBD)
- Activity diagrams for operations
- State machines for modes

**See**: [VISUAL_GUIDE.md](VISUAL_GUIDE.md) for complete diagrams

---

## 🌍 Heritage Missions

### Hayabusa (JAXA, 2003-2010)

**Lessons Applied:**
- ✅ Autonomous navigation essential
- ✅ Multiple TAG attempts needed
- ✅ Robust abort sequences critical
- ⚠️ Communication failures → need full autonomy

### Hayabusa2 (JAXA, 2014-2020)

**Direct Heritage:**
- ✅ TAG approach sequence
- ✅ Proximity operations concept
- ✅ Target marker deployment
- ✅ HIL testing methodology (Chapter 6 of thesis)

**Improvements in This Work:**
- Enhanced autonomous decision-making
- Improved hazard detection
- Higher landing accuracy

### OSIRIS-REx (NASA, 2016-2023)

**Lessons Applied:**
- ✅ Extensive site characterization
- ✅ Rehearsal descents before TAG
- ✅ Natural Feature Tracking (NFT) navigation
- ✅ GRALS-style HIL testing

**Requirements Derived:**
- 25m landing accuracy (from OSIRIS-REx specs)
- Approach cone constraints
- Abort triggers

---

## 🔗 Connection to Research Work

### Lunar SEP Trajectory Study

**Master's Thesis**: "Lunar Missions Design with Electric Propulsion"

**Relevance to Asteroid Mission:**
- SEP trajectory optimization techniques
- Multi-objective optimization (time, ΔV, mass)
- Low-thrust trajectory design
- Applicable to asteroid missions with flexible launch windows

**Key Findings Applied:**
- Hybrid propulsion approach
- ΔV budgeting methodology
- Trade-off analysis framework

### ISAE-SUPAERO SaCLaB Research

**Thesis**: "Systems Engineering for Asteroid Exploration GNC Validation Test"

**Contribution:**
- This GNC system repository
- MBSE methodology for space systems
- ECSS-compliant requirements engineering
- HIL testing strategy

**Collaboration**: ESA stakeholders in GNC requirements and validation

---

## 🎯 Mission Success Criteria

### Level 1 (Mission Success)

- ✅ Spacecraft arrives at asteroid
- ✅ At least 60g sample collected
- ✅ Sample returned to Earth

### Level 2 (Full Success)

- ✅ Level 1 criteria
- ✅ Global asteroid characterization
- ✅ 100-500g sample collected
- ✅ Multiple successful TAG operations

### Level 3 (Threshold Success)

- ✅ Spacecraft arrives at asteroid
- ✅ Remote sensing characterization
- ✅ Any amount of sample returned

**GNC System Contribution**: Critical for Level 1+ success (enables TAG operations)

---

## 📚 Related Documentation

### In This Repository

- [Technical Documentation](TECHNICAL_DOC.md) - GNC system design
- [HIL Testing Strategy](HIL_TESTING.md) - Verification approach
- [ESA Collaboration](ESA_COLLABORATION.md) - Research context
- [Visual Guide](VISUAL_GUIDE.md) - MBSE models

### External References

- **Hayabusa2 Mission**: https://www.hayabusa2.jaxa.jp/en/
- **OSIRIS-REx Mission**: https://www.asteroidmission.org/
- **ESA AIDA Mission Concept**: https://www.esa.int/Safety_Security/Hera
- **ECSS Standards**: https://ecss.nl/

### Academic Work

- Master's Thesis: Lunar SEP trajectory optimization
- ISAE-SUPAERO SaCLaB: GNC validation methodology
- Publications: *(in preparation)*

---

## 🔮 Future Work

### Technology Advancement

**Next-Generation GNC:**
- AI/ML for autonomous decision-making
- Enhanced hazard detection (deep learning)
- Multi-spacecraft operations (formation flying)
- Increased autonomy levels

### Mission Extensions

**Potential Applications:**
- **Binary asteroids**: Navigate between components
- **Comets**: Adapt GNC for outgassing environment
- **Martian moons** (Phobos, Deimos): Similar proximity ops
- **Lunar far-side**: Autonomous operations with no Earth comm

### Standards Development

Contributing to:
- ECSS-E-ST-60-30C updates (GNC verification)
- Autonomous systems standards
- MBSE best practices for space missions

---

## 💡 Key Takeaways

### For Mission Architects

1. **Autonomy is Essential**: Light-time delay requires autonomous GNC
2. **Heritage Builds Confidence**: Learn from Hayabusa2, OSIRIS-REx
3. **Verification is Critical**: HIL testing reduces mission risk
4. **MBSE Enables Complexity**: Manage requirements with models
5. **Trade-offs Drive Design**: Trajectory, sensors, autonomy level

### For GNC Engineers

1. **Context Matters**: GNC doesn't exist in isolation
2. **Mission Phases Drive Requirements**: Different needs for rendezvous vs TAG
3. **Uncertainty is the Challenge**: Unknown gravity, shape, rotation
4. **Autonomy = Capability**: Enables operations impossible with ground commanding

### For Systems Engineers

1. **Requirements Flow from Mission**: Top-down decomposition
2. **Traceability is Essential**: Mission to component level
3. **Verification Planned Early**: Not an afterthought
4. **MBSE Improves Communication**: Models > documents
5. **Standards Provide Structure**: ECSS framework enables success

---

## 📧 Questions?

For questions about mission architecture or GNC system integration:

**Author**: Ginevra Cianci  
**Email**: ginevra.cianci@polito.it  
**LinkedIn**: [linkedin.com/in/ginevracianci](https://linkedin.com/in/ginevracianci)

**Institution**: ISAE-SUPAERO SaCLaB, Toulouse, France  
**Collaboration**: ESA (European Space Agency)

---

**This document demonstrates mission-level thinking while highlighting the critical role of the GNC system in enabling autonomous asteroid sample return missions.**
