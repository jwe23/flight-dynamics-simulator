# src/physics.py
import numpy as np

class PhysicsEngine:
    def __init__(self):
        self.g = 9.81
        self.max_thrust = 12000.0
        self.drag_coefficient = 0.8
        self.lift_coefficient = 3.0
    
    def calculate_forces(self, aircraft):
        speed = np.linalg.norm(aircraft.velocity)
        
        # Thrust
        thrust = aircraft.throttle * self.max_thrust
        thrust_x = thrust * np.cos(aircraft.pitch)
        thrust_z = thrust * np.sin(aircraft.pitch)
        
        # Drag opposes all motion
        if speed > 0.1:
            drag = self.drag_coefficient * speed ** 2
            drag_x = -drag * (aircraft.velocity[0] / speed)
            drag_z = -drag * (aircraft.velocity[2] / speed)
        else:
            drag_x = 0
            drag_z = 0
        
        # Lift from horizontal speed only
        horizontal_speed = abs(aircraft.velocity[0])
        if horizontal_speed > 15:
            lift = self.lift_coefficient * horizontal_speed * np.sin(aircraft.pitch + 0.15)
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
        
        # Dampen to prevent runaway
        aircraft.velocity[0] = np.clip(aircraft.velocity[0], -100, 100)
        aircraft.velocity[2] = np.clip(aircraft.velocity[2], -30, 30)
        
        # Only update altitude, not horizontal position (keep centered)
        aircraft.position[2] += aircraft.velocity[2] * dt
        
        # Ground collision
        if aircraft.position[2] <= 0:
            aircraft.position[2] = 0
            aircraft.velocity[2] = max(0, aircraft.velocity[2])
            if aircraft.pitch < 0:
                aircraft.pitch = 0
