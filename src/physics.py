# src/physics.py
import numpy as np

class PhysicsEngine:
    def __init__(self):
        self.g = 9.81
        self.max_thrust = 20000.0
        self.drag_coefficient = 0.02
        self.lift_coefficient = 0.5
    
    def calculate_forces(self, aircraft):
        speed = np.linalg.norm(aircraft.velocity)
        
        # Thrust along pitch angle
        thrust = aircraft.throttle * self.max_thrust
        thrust_x = thrust * np.cos(aircraft.pitch)
        thrust_z = thrust * np.sin(aircraft.pitch)
        
        # Drag opposes motion
        if speed > 0:
            drag = self.drag_coefficient * speed ** 2
            drag_x = -drag * (aircraft.velocity[0] / speed)
            drag_z = -drag * (aircraft.velocity[2] / speed)
        else:
            drag_x = 0
            drag_z = 0
        
        # Lift (perpendicular to velocity, depends on speed and angle of attack)
        # Simplified: lift is proportional to speed squared
        lift = self.lift_coefficient * speed ** 2
        
        # Gravity
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
        
        aircraft.position += aircraft.velocity * dt
        
        # Ground collision
        if aircraft.position[2] <= 0:
            aircraft.position[2] = 0
            if aircraft.velocity[2] < 0:
                aircraft.velocity[2] = 0
            if aircraft.pitch < 0:
                aircraft.pitch = 0
