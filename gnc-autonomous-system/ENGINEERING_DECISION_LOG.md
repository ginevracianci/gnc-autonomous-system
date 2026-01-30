# Engineering Decision Log
## Spacecraft Attitude Control and Guidance System

---

### Decision 1: Attitude Representation Method

**Date:** 2024-01-25

**Context:**
Need to select mathematical representation for spacecraft attitude to avoid singularities and ensure computational efficiency for real-time control applications.

**Constraints:**
- Must avoid gimbal lock
- Computational efficiency for onboard processing
- Compatibility with existing ESA GNC libraries
- Memory footprint < 100KB

**Options:**
1. Euler angles (roll, pitch, yaw)
2. Quaternions
3. Modified Rodrigues Parameters (MRP)
4. Direction Cosine Matrix (DCM)

**Trade-off Criteria:**
- Singularity avoidance: Critical
- Computational efficiency: High priority
- Implementation complexity: Medium priority
- Industry standard compliance: High priority

**Final Decision:**
**Quaternions** selected as primary attitude representation.

**Rationale:**
- No singularities unlike Euler angles
- More computationally efficient than DCM (4 parameters vs 9)
- Industry standard for spacecraft GNC (used in ISS, Sentinel satellites)
- Direct integration with TRIAD algorithm for sensor fusion
- 40% faster computation than MRP in preliminary benchmarks

**Risks Accepted:**
- Quaternion normalization drift over extended missions
- Team learning curve (1-2 weeks)

**Mitigation:**
- Implement automatic normalization every 100 iterations
- Add unit tests for quaternion operations (>95% coverage)
- Provide training documentation based on Wertz & Markley references

---

### Decision 2: Control Law Architecture

**Date:** 2024-02-10

**Context:**
Selection of control algorithm for 3-axis attitude stabilization with reaction wheels. Mission requires pointing accuracy of 0.01° for Earth observation payload.

**Constraints:**
- Pointing accuracy: ±0.01° (3σ)
- Settling time: < 30 seconds
- Reaction wheel saturation: ±3000 RPM
- Power budget: < 15W for control computation

**Options:**
1. PID controller
2. Linear Quadratic Regulator (LQR)
3. Sliding Mode Control (SMC)
4. Model Predictive Control (MPC)

**Trade-off Criteria:**
- Pointing accuracy: Critical
- Robustness to disturbances: High priority
- Implementation complexity: Medium priority
- Computational load: High priority

**Final Decision:**
**LQR with momentum management** selected.

**Rationale:**
- Achieves 0.008° accuracy in simulation (20% margin)
- Optimal balance between performance and actuator usage
- Well-established heritage (Mars Reconnaissance Orbiter, Sentinel-2)
- Deterministic computational load suitable for real-time systems
- Natural integration with Kalman filter for state estimation

**Risks Accepted:**
- Requires accurate system model (linearization errors)
- Suboptimal for large angle maneuvers (>45°)

**Mitigation:**
- Gain scheduling for different operational modes
- Separate slew maneuver controller for large angles
- Model validation campaign with hardware-in-the-loop testing
- Quarterly gain tuning based on on-orbit telemetry

---

### Decision 3: Sensor Fusion Algorithm

**Date:** 2024-03-05

**Context:**
Multiple sensors available (star tracker, gyroscopes, sun sensors). Need optimal fusion strategy for attitude determination with 0.005° accuracy requirement.

**Constraints:**
- Star tracker: 0.001° accuracy, 1 Hz update rate
- Gyroscopes: 0.01°/hr drift, 100 Hz sampling
- Sun sensors: 0.5° accuracy, 10 Hz update rate
- Processing time: < 10ms per cycle

**Options:**
1. Simple weighted average
2. Extended Kalman Filter (EKF)
3. Unscented Kalman Filter (UKF)
4. TRIAD + Kalman Filter combination

**Trade-off Criteria:**
- Accuracy: Critical
- Computational efficiency: High priority
- Sensor failure robustness: High priority
- Flight heritage: Medium priority

**Final Decision:**
**Multiplicative Extended Kalman Filter (MEKF)** with TRIAD initialization.

**Rationale:**
- Specifically designed for quaternion-based attitude estimation
- Handles sensor noise optimally with known covariance
- 0.003° accuracy achieved in Monte Carlo simulations
- Used successfully on Hubble Space Telescope, James Webb
- Graceful degradation with sensor failures
- Computational load: 6ms per cycle on target processor

**Risks Accepted:**
- EKF linearization errors during high dynamics
- Requires sensor noise characterization (testing overhead)

**Mitigation:**
- UKF fallback mode for high-rate maneuvers (>5°/s)
- Pre-flight sensor calibration campaign (2 weeks)
- Adaptive noise covariance tuning based on residuals
- Continuous health monitoring with automatic sensor exclusion

---

### Decision 4: Actuator Selection and Redundancy

**Date:** 2024-03-20

**Context:**
Need to select reaction wheel configuration for 3-axis control with redundancy for 5-year mission lifetime.

**Constraints:**
- Mission lifetime: 5 years
- Reliability requirement: 0.99
- Maximum torque: 0.1 Nm per axis
- Total mass budget: < 8 kg for AOCS

**Options:**
1. Three wheels (one per axis) - no redundancy
2. Four wheels (pyramid configuration)
3. Six wheels (full redundancy)
4. Four wheels + magnetic torquers

**Trade-off Criteria:**
- Reliability: Critical
- Mass: High priority
- Power consumption: High priority
- Momentum management: Medium priority

**Final Decision:**
**Four reaction wheels in pyramid configuration** (skew angle: 54.74°) **+ three magnetic torquers**.

**Rationale:**
- Single-fault tolerant (maintains 3-axis control after one wheel failure)
- Pyramid configuration provides torque in all axes with any 3 wheels
- Magnetic torquers for momentum desaturation (no propellant required)
- Mass: 6.5 kg (within budget)
- Flight proven on Sentinel-1, -2, -3 missions
- Reliability: 0.995 over 5 years (Monte Carlo FMEA)

**Risks Accepted:**
- Magnetic torquers ineffective above 800 km altitude
- 15% performance degradation in single-wheel failure mode

**Mitigation:**
- Mission orbit: 600 km (optimal for magnetic torquers)
- Wheel momentum monitoring with predictive maintenance
- Onboard wheel failure detection and reconfiguration (< 5 seconds)
- Ground-commanded safe mode procedures documented

---

### Decision 5: Software Architecture and Real-Time Requirements

**Date:** 2024-04-15

**Context:**
Define software architecture for GNC system to meet real-time constraints and ensure deterministic behavior for safety-critical operations.

**Constraints:**
- Control loop: 100 Hz (10 ms period)
- Processor: LEON3 (100 MHz)
- Memory: 512 KB RAM available for GNC
- Must comply with ECSS-E-ST-40C software standard

**Options:**
1. Single-threaded polling architecture
2. Multi-threaded with priority scheduling
3. Time-triggered architecture
4. Event-driven architecture

**Trade-off Criteria:**
- Determinism: Critical
- Timing predictability: Critical
- Development complexity: Medium priority
- Testing effort: High priority

**Final Decision:**
**Time-triggered architecture** with fixed 10 ms major frame.

**Rationale:**
- Deterministic execution (zero jitter)
- Predictable worst-case execution time (WCET analysis)
- Compliant with ECSS-E-ST-40C for space software
- Simplified testing and verification (schedule is static)
- Heritage: Used on BepiColombo, ExoMars missions
- WCET analysis shows 7.2 ms maximum (28% margin)

**Risks Accepted:**
- Less flexible than event-driven approaches
- CPU utilization: 72% (limited headroom for future features)

**Mitigation:**
- Reserve 1 ms per frame for contingency tasks
- Code optimization sprint before delivery
- Profiling tools integrated in development environment
- Annual performance review for margin verification

---

## Summary of Key Decisions

| Decision | Selection | Primary Driver | Status |
|----------|-----------|----------------|--------|
| Attitude Representation | Quaternions | Singularity-free | Implemented |
| Control Law | LQR | Accuracy + Heritage | Implemented |
| Sensor Fusion | MEKF | Optimal accuracy | Implemented |
| Actuators | 4 RW + 3 MT | Redundancy | Baselined |
| Software Architecture | Time-triggered | Determinism | Implemented |

---

**Last Updated:** 2024-04-15  
**Document Owner:** GNC Engineering Team  
**Review Status:** Approved by Technical Authority
