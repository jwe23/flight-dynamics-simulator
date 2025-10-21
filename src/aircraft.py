# src/aircraft.py
import numpy as np

class Aircraft:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 150.0])
        self.velocity = np.array([60.0, 0.0, 0.0])
        self.pitch = 0.05  # Slight positive pitch
        
        self.mass = 1000.0
        
        self.throttle = 0.6
        self.pitch_input = 0.0
