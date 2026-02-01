"""
Hardware-in-the-Loop Simulation Example
Demonstrates HIL test setup for GNC validation
Based on Chapter 6 methodology
"""

import numpy as np
from typing import Dict, Tuple
import time


class HILSimulator:
    """
    Simplified HIL simulator for GNC testing
    Based on Chapter 6 methodology
    
    This class demonstrates the basic structure of a Hardware-in-the-Loop
    test environment for spacecraft GNC validation.
    """
    
    def __init__(self, dt: float = 0.1):
        """
        Initialize HIL simulator
        
        Args:
            dt: Simulation timestep in seconds (default: 0.1s = 10 Hz)
        """
        self.dt = dt
        self.time = 0.0
        self.state = None
        self.test_log = []
        
        # Initialize spacecraft state
        self.initialize_state()
        
    def initialize_state(self) -> None:
        """Initialize spacecraft state vector"""
        self.state = {
            'position': np.array([2500.0, 200.0, -50.0]),  # km
            'velocity': np.array([0.1, -0.05, 0.02]),       # km/s
            'attitude': np.array([0.0, 0.0, 0.0]),          # rad (roll, pitch, yaw)
            'angular_velocity': np.array([0.0, 0.0, 0.0])   # rad/s
        }
        
    def run_test_scenario(self, scenario: str = 'RDV', duration: float = 100.0) -> None:
        """
        Execute HIL test scenario
        
        Args:
            scenario: Test scenario type ('RDV' for rendezvous, 'TAG' for touch-and-go)
            duration: Test duration in seconds
        """
        print(f"Starting HIL test: {scenario}")
        print(f"Duration: {duration} seconds")
        print(f"Update rate: {1/self.dt} Hz")
        print("-" * 50)
        
        # Initialize test
        self.initialize_state()
        self.test_log = []
        
        # Main test loop
        iteration = 0
        while self.time < duration:
            # 1. Generate sensor measurements
            sensor_data = self.generate_sensor_measurements()
            
            # 2. Navigation - State estimation
            estimated_state = self.estimate_state(sensor_data)
            
            # 3. Guidance - Compute desired trajectory
            desired_state = self.compute_guidance(estimated_state, scenario)
            
            # 4. Control - Compute actuator commands
            commands = self.compute_control(estimated_state, desired_state)
            
            # 5. Apply commands to simulator
            self.apply_actuator_commands(commands)
            
            # 6. Propagate dynamics
            self.propagate_dynamics()
            
            # 7. Log test data
            self.log_data(estimated_state, desired_state, commands, sensor_data)
            
            # 8. Check success criteria (every 10 iterations)
            if iteration % 10 == 0:
                self.check_success_criteria(scenario)
            
            iteration += 1
            
        print("-" * 50)
        print(f"HIL test complete: {iteration} iterations")
        self.print_final_statistics()
        
    def generate_sensor_measurements(self) -> Dict[str, np.ndarray]:
        """
        Simulate sensor measurements with realistic noise
        
        Returns:
            Dictionary containing sensor measurements
        """
        # IMU measurements (accelerometer + gyroscope)
        imu_accel = np.random.randn(3) * 1e-4  # m/s² noise
        imu_gyro = np.random.randn(3) * 1e-6   # rad/s noise
        
        # Star Tracker (attitude determination)
        star_tracker_attitude = self.state['attitude'] + np.random.randn(3) * 1e-6  # rad
        
        # LIDAR (range measurement)
        true_range = np.linalg.norm(self.state['position']) * 1000  # m
        lidar_range = true_range + np.random.randn() * 0.1  # m noise
        
        # Optical camera (relative position - simplified)
        camera_position = self.state['position'] + np.random.randn(3) * 0.001  # km
        
        return {
            'imu_accel': imu_accel,
            'imu_gyro': imu_gyro,
            'star_tracker': star_tracker_attitude,
            'lidar_range': lidar_range,
            'camera_position': camera_position
        }
    
    def estimate_state(self, sensor_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        State estimation using sensor fusion (simplified Kalman filter)
        
        Args:
            sensor_data: Raw sensor measurements
            
        Returns:
            Estimated spacecraft state
        """
        # Simplified state estimation
        # In reality, this would be a full Extended Kalman Filter
        estimated_state = {
            'position': sensor_data['camera_position'],
            'velocity': self.state['velocity'],  # Simplified
            'attitude': sensor_data['star_tracker'],
            'angular_velocity': self.state['angular_velocity']  # Simplified
        }
        
        return estimated_state
    
    def compute_guidance(self, current_state: Dict[str, np.ndarray], 
                        scenario: str) -> Dict[str, np.ndarray]:
        """
        Compute desired trajectory (guidance law)
        
        Args:
            current_state: Current estimated state
            scenario: Mission scenario
            
        Returns:
            Desired state
        """
        if scenario == 'RDV':
            # Rendezvous guidance - approach home position
            target_position = np.array([20.0, 0.0, 0.0])  # km
            target_velocity = np.array([0.0, 0.0, 0.0])   # km/s
            
        elif scenario == 'TAG':
            # Touch-and-go guidance - descend to surface
            target_position = np.array([0.0, 0.0, 0.0])  # Surface
            target_velocity = np.array([0.0, 0.0, -0.0001])  # 10 cm/s descent
            
        else:
            target_position = np.zeros(3)
            target_velocity = np.zeros(3)
        
        return {
            'position': target_position,
            'velocity': target_velocity,
            'attitude': np.zeros(3),
            'angular_velocity': np.zeros(3)
        }
    
    def compute_control(self, current_state: Dict[str, np.ndarray],
                       desired_state: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Compute actuator commands (control law)
        
        Args:
            current_state: Current estimated state
            desired_state: Desired state from guidance
            
        Returns:
            Actuator commands (thrust, torque)
        """
        # Position error
        pos_error = desired_state['position'] - current_state['position']
        vel_error = desired_state['velocity'] - current_state['velocity']
        
        # Simple PD control for translation
        Kp_pos = 0.01  # Proportional gain
        Kd_pos = 0.1   # Derivative gain
        
        thrust_command = Kp_pos * pos_error + Kd_pos * vel_error
        
        # Attitude control (simplified)
        att_error = desired_state['attitude'] - current_state['attitude']
        ang_vel_error = desired_state['angular_velocity'] - current_state['angular_velocity']
        
        Kp_att = 0.1
        Kd_att = 0.05
        
        torque_command = Kp_att * att_error + Kd_att * ang_vel_error
        
        return {
            'thrust': thrust_command,  # km/s² (later converted to N)
            'torque': torque_command   # N·m
        }
    
    def apply_actuator_commands(self, commands: Dict[str, np.ndarray]) -> None:
        """
        Apply actuator commands to spacecraft
        
        Args:
            commands: Thrust and torque commands
        """
        # Apply thrust (simplified - direct acceleration)
        self.state['velocity'] += commands['thrust'] * self.dt
        
        # Apply torque (simplified - direct angular acceleration)
        # Assuming unit moment of inertia for simplicity
        self.state['angular_velocity'] += commands['torque'] * self.dt
    
    def propagate_dynamics(self) -> None:
        """Propagate spacecraft dynamics one timestep"""
        # Translational dynamics
        self.state['position'] += self.state['velocity'] * self.dt
        
        # Rotational dynamics
        self.state['attitude'] += self.state['angular_velocity'] * self.dt
        
        # Normalize attitude angles to [-π, π]
        self.state['attitude'] = np.arctan2(
            np.sin(self.state['attitude']), 
            np.cos(self.state['attitude'])
        )
        
        # Update simulation time
        self.time += self.dt
    
    def log_data(self, estimated_state: Dict, desired_state: Dict,
                 commands: Dict, sensor_data: Dict) -> None:
        """
        Record test data for post-processing
        
        Args:
            estimated_state: Estimated spacecraft state
            desired_state: Desired state from guidance
            commands: Actuator commands
            sensor_data: Sensor measurements
        """
        log_entry = {
            'time': self.time,
            'position': self.state['position'].copy(),
            'velocity': self.state['velocity'].copy(),
            'position_error': np.linalg.norm(
                desired_state['position'] - estimated_state['position']
            ),
            'velocity_error': np.linalg.norm(
                desired_state['velocity'] - estimated_state['velocity']
            ),
            'thrust_magnitude': np.linalg.norm(commands['thrust'])
        }
        
        self.test_log.append(log_entry)
    
    def check_success_criteria(self, scenario: str) -> bool:
        """
        Check if success criteria are met
        
        Args:
            scenario: Test scenario
            
        Returns:
            True if criteria met, False otherwise
        """
        if scenario == 'RDV':
            # Rendezvous criteria
            pos_error = np.linalg.norm(self.state['position'] - np.array([20.0, 0.0, 0.0]))
            vel_error = np.linalg.norm(self.state['velocity'])
            
            if pos_error > 10.0:  # 10 km abort threshold
                print(f"WARNING: Position error {pos_error:.2f} km exceeds threshold!")
                return False
                
        elif scenario == 'TAG':
            # Touch-and-go criteria
            altitude = np.linalg.norm(self.state['position'])
            
            if altitude > 0.1 and self.time > 50:  # Should be descending
                print(f"WARNING: Altitude {altitude:.4f} km - descent too slow!")
                return False
        
        return True
    
    def print_final_statistics(self) -> None:
        """Print final test statistics"""
        if len(self.test_log) == 0:
            return
        
        final_entry = self.test_log[-1]
        
        print(f"\nFinal State:")
        print(f"  Position: {final_entry['position']} km")
        print(f"  Velocity: {self.state['velocity']} km/s")
        print(f"  Position error: {final_entry['position_error']:.4f} km")
        print(f"  Velocity error: {final_entry['velocity_error']:.6f} km/s")
        
        # Statistics over entire test
        pos_errors = [entry['position_error'] for entry in self.test_log]
        vel_errors = [entry['velocity_error'] for entry in self.test_log]
        
        print(f"\nTest Statistics:")
        print(f"  Mean position error: {np.mean(pos_errors):.4f} km")
        print(f"  Max position error: {np.max(pos_errors):.4f} km")
        print(f"  Mean velocity error: {np.mean(vel_errors):.6f} km/s")
        print(f"  Max velocity error: {np.max(vel_errors):.6f} km/s")


def main():
    """Main function to run HIL test examples"""
    print("=" * 50)
    print("Hardware-in-the-Loop (HIL) Test Examples")
    print("=" * 50)
    print()
    
    # Test 1: Rendezvous scenario
    print("\n### TEST 1: RENDEZVOUS SCENARIO ###\n")
    hil_rdv = HILSimulator(dt=0.1)
    hil_rdv.run_test_scenario(scenario='RDV', duration=100.0)
    
    # Test 2: Touch-and-go scenario
    print("\n### TEST 2: TOUCH-AND-GO SCENARIO ###\n")
    hil_tag = HILSimulator(dt=0.1)
    hil_tag.run_test_scenario(scenario='TAG', duration=100.0)
    
    print("\n" + "=" * 50)
    print("HIL tests completed successfully")
    print("=" * 50)


if __name__ == "__main__":
    main()
