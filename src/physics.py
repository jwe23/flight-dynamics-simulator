# src/physics.py
import numpy as np

class PhysicsEngine:
    def __init__(self):
        self.g = 9.81
        self.max_thrust = 15000.0
        self.drag_coefficient = 0.5
        self.lift_coefficient = 2.0
        self.air_density = 1.225
    
    def calculate_forces(self, aircraft):
        speed = np.linalg.norm(aircraft.velocity)
        
        # Thrust along pitch angle
        thrust = aircraft.throttle * self.max_thrust
        thrust_x = thrust * np.cos(aircraft.pitch)
        thrust_z = thrust * np.sin(aircraft.pitch)
        
        # Drag opposes velocity direction
        if speed > 0.1:
            drag = 0.5 * self.air_density * self.drag_coefficient * speed ** 2
            drag_x = -drag * (aircraft.velocity[0] / speed)
            drag_z = -drag * (aircraft.velocity[2] / speed)
        else:
            drag_x = 0
            drag_z = 0
        
        # Lift perpendicular to velocity (upward when moving forward)
        # Only generate lift from horizontal speed, not vertical
        horizontal_speed = abs(aircraft.velocity[0])
        if horizontal_speed > 10:
            # Lift depends on angle of attack (pitch relative to velocity)
            angle_of_attack = aircraft.pitch
            lift = 0.5 * self.air_density * self.lift_coefficient * horizontal_speed ** 2 * np.sin(angle_of_attack + 0.1)
        else:
            lift = 0
        
        # Weight
        weight = aircraft.mass * self.g
        
        force = np.array([
            thrust_x + drag_x,
            0.0,
            thrust_z + drag_z + lift - weight
        ])
        
        return force
    
    def update(self, aircraft, dt):
        force = self.calculate_forces(aircraft)
        
        acceleration = force / aircraft.mass
        aircraft.velocity += acceleration * dt
        
        # Dampen vertical velocity to prevent runaway
        aircraft.velocity[2] = np.clip(aircraft.velocity[2], -50, 50)
        
        aircraft.position += aircraft.velocity * dt
        
        # Ground collision
        if aircraft.position[2] <= 0:
            aircraft.position[2] = 0
            aircraft.velocity[2] = max(0, aircraft.velocity[2])
            if aircraft.pitch < 0:
                aircraft.pitch = 0
