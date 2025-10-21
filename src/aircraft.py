# src/aircraft.py
import numpy as np

class Aircraft:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 200.0])  # Start higher
        self.velocity = np.array([80.0, 0.0, 0.0])   # Start faster for lift
        self.pitch = 0.0
        
        self.mass = 1000.0
        
        self.throttle = 0.7  # Start with more throttle
        self.pitch_input = 0.0
