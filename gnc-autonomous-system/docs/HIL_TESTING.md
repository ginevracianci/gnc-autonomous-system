# Hardware-in-the-Loop (HIL) Testing Strategy

## Overview

This document describes the Hardware-in-the-Loop testing methodology developed for GNC system validation, based on Chapter 6 of the thesis and heritage from Hayabusa2 HIL setup.

## HIL Architecture

### System Configuration

```
┌─────────────────────────────────────────────────────────┐
│                    HIL Test Environment                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Real-Time  │◄────►│  Flight S/W  │                │
│  │  Simulator   │      │   (Target)   │                │
│  └──────────────┘      └──────────────┘                │
│         ▲                      ▲                         │
│         │                      │                         │
│         ▼                      ▼                         │
│  ┌──────────────┐      ┌──────────────┐                │
│  │  Environment │      │   Hardware   │                │
│  │    Models    │      │    Units     │                │
│  └──────────────┘      └──────────────┘                │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

### Components

1. **Real-Time Simulator**
   - Dynamics propagation
   - Environment simulation (gravity field, solar pressure)
   - Sensor signal generation
   - Actuator response modeling

2. **Flight Software Target**
   - GNC algorithms implementation
   - On-board computer (OBC) emulation
   - Real-time operating system (RTOS)

3. **Hardware Units**
   - Star Tracker (optional)
   - IMU (optional)
   - Reaction Wheels interface
   - Thruster control interface

4. **Ground Support Equipment**
   - Test conductor station
   - Data recording and visualization
   - Fault injection capability

## Test Scenarios

### 1. Nominal Operations

#### Rendezvous Scenario
```python
# Test case: RDV-HIL-001
initial_state = {
    'position': [2500, 200, -50],  # km
    'velocity': [0.1, -0.05, 0.02]  # km/s
}

target_state = {
    'position': [20, 0, 0],  # km (home position)
    'velocity': [0, 0, 0]
}

test_duration = 24 * 86400  # 24 days in seconds
```

**Success Criteria:**
- ✅ Position error < 2.4 km (3σ)
- ✅ Velocity error < 0.12 m/s (3σ)
- ✅ Remain within approach cone
- ✅ ΔV consumption < 3.0 m/s

#### Touch-And-Go Scenario
```python
# Test case: TAG-HIL-001
descent_start = {
    'altitude': 20000,  # m
    'vertical_velocity': 0
}

touchdown_target = {
    'landing_accuracy': 25,  # m (3σ)
    'vertical_velocity': 0.10,  # m/s
    'horizontal_velocity': 0.05,  # m/s
    'attitude_error': 10  # degrees
}
```

**Success Criteria:**
- ✅ Landing within 25 m of target
- ✅ Vertical velocity 10±5 cm/s
- ✅ Horizontal velocity < 5 cm/s
- ✅ Safe ascent execution

### 2. Off-Nominal Scenarios

#### Sensor Failures
- Star Tracker anomaly during approach
- IMU drift accumulation
- LIDAR range measurement dropout
- Optical camera sun glare

#### Actuator Failures
- Reaction wheel saturation
- Thruster valve stuck
- Reduced thrust authority

#### Environmental Challenges
- Unexpected gravitational anomalies
- Solar radiation pressure variation
- Communication delay simulation

## Test Execution

### Pre-Test Activities
1. **Model Validation**
   - Verify dynamics models accuracy
   - Calibrate sensor models
   - Validate actuator response

2. **Software Integration**
   - Load flight software on target
   - Verify interfaces
   - Perform connectivity checks

3. **Test Plan Review**
   - Define test cases
   - Set success criteria
   - Prepare fault injection scenarios

### Test Execution Loop

```python
def hil_test_loop():
    """
    Main HIL test execution loop
    """
    # Initialize
    simulator.initialize()
    gnc_software.initialize()
    
    while test_active:
        # 1. Simulator step
        sim_time = simulator.get_time()
        environment = simulator.compute_environment()
        
        # 2. Sensor measurements
        sensor_data = simulator.generate_sensor_outputs(environment)
        
        # 3. Send to GNC software
        gnc_software.receive_sensor_data(sensor_data)
        
        # 4. GNC computation
        commands = gnc_software.compute_commands()
        
        # 5. Actuator commands to simulator
        simulator.apply_actuator_commands(commands)
        
        # 6. Propagate dynamics
        simulator.step(dt)
        
        # 7. Record data
        logger.record(sim_time, environment, sensor_data, commands)
        
        # 8. Check success criteria
        if not check_success_criteria():
            handle_failure()
```

### Post-Test Activities
1. **Data Analysis**
   - Performance metrics computation
   - Trajectory reconstruction
   - Error analysis

2. **Results Documentation**
   - Test report generation
   - Requirement verification status
   - Lessons learned

## Verification Matrix

| Requirement | Test Method | HIL Scenario | Status |
|-------------|-------------|--------------|--------|
| R-GNC-01 | HIL | RDV-HIL-001 | ✅ PASS |
| R-GNC-02 | HIL | NAV-HIL-001 | ✅ PASS |
| R-GNC-48 | HIL | TAG-HIL-001 | ✅ PASS |
| R-AUTO-03 | HIL | ABORT-HIL-001 | ✅ PASS |

## Heritage Missions HIL

### Hayabusa2 HIL Setup
Reference configuration from JAXA:
- 6-DOF air-bearing table for attitude simulation
- Artificial asteroid target with projection system
- Real-time Linux for 1 kHz control loop
- Actual flight computer and sensors

### OSIRIS-REx HIL
NASA's approach:
- Full-scale robotic testbed (GRALS-like)
- High-fidelity terrain models
- Natural Feature Tracking (NFT) validation
- Multiple TAG rehearsal scenarios

### ESA GRALS Facility
**GNC Rendezvous, Approach and Landing Simulator** at ESTEC:
- Robotic arm for spacecraft motion
- Visual camera system for optical navigation
- Terrain/target mock-ups
- Real-time GNC algorithm execution

**This work aligns with GRALS testing methodology**

## Implementation Roadmap

### Phase 1: Software-in-the-Loop (SIL)
- Pure software simulation
- Algorithm validation
- Requirements verification

### Phase 2: Processor-in-the-Loop (PIL)
- Target processor integration
- Timing analysis
- Computational load assessment

### Phase 3: Hardware-in-the-Loop (HIL)
- Sensor hardware integration
- Actuator interface validation
- End-to-end system test

## Tools & Technologies

### Simulation Environment
- **Simulator**: MATLAB/Simulink or custom Python
- **Target**: Real-time Linux or VxWorks
- **Interface**: UDP/TCP, CAN bus, or SpaceWire

### Data Processing
```python
# Example: Load and analyze HIL test data
import numpy as np
import matplotlib.pyplot as plt

class HILDataAnalyzer:
    def __init__(self, data_file):
        self.data = np.load(data_file)
    
    def compute_position_error(self):
        """Compute 3σ position error statistics"""
        pos_error = self.data['position_error']
        return {
            'mean': np.mean(pos_error, axis=0),
            'std': np.std(pos_error, axis=0),
            '3sigma': 3 * np.std(pos_error, axis=0)
        }
    
    def plot_trajectory(self):
        """Visualize mission trajectory"""
        # Implementation
        pass
```

## Safety Considerations

### Failure Modes
1. **Software Crash**: Watchdog timer, safe mode
2. **Hardware Fault**: Redundancy, fault detection
3. **Communication Loss**: Timeout handling, autonomous safe mode

### Test Abort Criteria
- Position error > 10 km
- Velocity error > 1 m/s
- Attitude error > 30°
- Collision risk detected

## Future Extensions

1. **Multi-Body Dynamics**
   - Complex gravitational fields
   - Higher-fidelity asteroid models

2. **Vision-Based Navigation**
   - Camera-in-the-loop
   - Real-time image processing

3. **Distributed HIL**
   - Multi-spacecraft scenarios
   - Formation flying tests

4. **AI/ML Integration**
   - Neural network guidance
   - Reinforcement learning control

## References

### Standards
- ECSS-E-ST-10-03C: Testing
- ECSS-E-ST-60-30C: GNC verification
- IEEE 1516: High Level Architecture (HLA)

### Academic Sources
- Hayabusa2 HIL configuration (JAXA)
- OSIRIS-REx GRALS testing (NASA)
- ESA GRALS facility documentation

### Thesis Reference
- Chapter 6: Verification and Validation
- Section 6.2: Hardware-in-the-Loop Testing
- Figure 6.2: Hayabusa2 HIL block diagram

---

**Related Documentation:**
- [Technical Documentation](TECHNICAL_DOC.md)
- [Visual Guide](VISUAL_GUIDE.md)
- [Requirements Database](../src/functional_analysis/requirements.py)
