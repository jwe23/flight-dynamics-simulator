# src/aircraft.py
import numpy as np

class Aircraft:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 100.0])  # x, y, altitude
        self.velocity = np.array([50.0, 0.0, 0.0])   # m/s
        self.mass = 1000.0  # kg
        self.throttle = 0.5
        
    def update(self, dt):
        # Super simple physics
        thrust = self.throttle * 10000  # Newtons
        drag = 0.5 * np.linalg.norm(self.velocity)**2
        gravity = self.mass * 9.81
        
        # Net force (simplified)
        force_x = thrust - drag * 0.1
        force_z = -gravity
        
        # Update velocity
        self.velocity[0] += (force_x / self.mass) * dt
        self.velocity[2] += (force_z / self.mass) * dt
        
        # Update position
        self.position += self.velocity * dt
        
        # Don't go below ground
        if self.position[2] < 0:
            self.position[2] = 0
            self.velocity[2] = 0
