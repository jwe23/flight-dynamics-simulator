# src/physics.py
import numpy as np

class PhysicsEngine:
    def __init__(self):
        self.g = 9.81
        self.max_thrust = 10000.0
        self.drag_coefficient = 0.1
    
    def calculate_forces(self, aircraft):
        thrust = aircraft.throttle * self.max_thrust
        thrust_x = thrust * np.cos(aircraft.pitch)
        thrust_z = thrust * np.sin(aircraft.pitch)
        
        speed = np.linalg.norm(aircraft.velocity)
        drag_x = -self.drag_coefficient * speed ** 2 * np.sign(aircraft.velocity[0])
        
        gravity_z = -aircraft.mass * self.g
        
        force = np.array([
            thrust_x + drag_x,
            0.0,
            thrust_z + gravity_z
        ])
        
        return force
    
    def update(self, aircraft, dt):
        force = self.calculate_forces(aircraft)
        
        acceleration = force / aircraft.mass
        aircraft.velocity += acceleration * dt
        
        aircraft.position += aircraft.velocity * dt
        
        if aircraft.position[2] < 0:
            aircraft.position[2] = 0
            aircraft.velocity[2] = 0
            if aircraft.pitch < 0:
                aircraft.pitch = 0
