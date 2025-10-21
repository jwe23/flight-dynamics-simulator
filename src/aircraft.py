# src/aircraft.py
import numpy as np

class Aircraft:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 100.0])
        self.velocity = np.array([50.0, 0.0, 0.0])
        self.pitch = 0.0
        
        self.mass = 1000.0
        
        self.throttle = 0.5
        self.pitch_input = 0.0
