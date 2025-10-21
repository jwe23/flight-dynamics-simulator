# src/physics.py
import numpy as np

class PhysicsEngine:
    def __init__(self):
        self.g = 9.81
        self.rho = 1.225
        
        self.mass = 1500.0
        self.wing_area = 16.0
        self.max_thrust = 20000.0
        
        self.CL0 = 0.3
        self.CLalpha = 5.0
        self.CD0 = 0.025
        self.K = 0.04
        
    def calculate_forces(self, aircraft):
        vx = aircraft.velocity[0]
        vz = aircraft.velocity[2]
        V = np.sqrt(vx**2 + vz**2)
        
        if V < 0.1:
            V = 0.1
        
        gamma = np.arctan2(vz, vx)
        alpha = aircraft.pitch - gamma
        alpha = np.clip(alpha, -0.3, 0.5)
        
        q = 0.5 * self.rho * V**2
        
        CL = self.CL0 + self.CLalpha * alpha
        CL = np.clip(CL, -1.5, 1.8)
        
        CD = self.CD0 + self.K * CL**2
        
        L = q * self.wing_area * CL
        D = q * self.wing_area * CD
        
        T = aircraft.throttle * self.max_thrust
        W = aircraft.mass * self.g
        
        Lx = -L * np.sin(gamma)
        Lz = L * np.cos(gamma)
        
        Dx = -D * np.cos(gamma)
        Dz = -D * np.sin(gamma)
        
        Tx = T * np.cos(aircraft.pitch)
        Tz = T * np.sin(aircraft.pitch)
        
        Fx = Tx + Dx + Lx
        Fz = Tz + Dz + Lz - W
        
        return np.array([Fx, 0.0, Fz])
    
    def update(self, aircraft, dt):
        force = self.calculate_forces(aircraft)
        acceleration = force / aircraft.mass
        aircraft.velocity += acceleration * dt
        aircraft.position[2] += aircraft.velocity[2] * dt
        
        if aircraft.position[2] <= 0:
            aircraft.position[2] = 0
            if aircraft.velocity[2] < 0:
                aircraft.velocity[2] = -aircraft.velocity[2] * 0.3
            aircraft.velocity[0] *= 0.95
            if aircraft.velocity[0] < 1.0:
                aircraft.velocity[0] = 0
                aircraft.velocity[2] = 0
