# src/controls.py
import pygame
import numpy as np

class Controls:
    def __init__(self):
        self.pitch_rate = 0.03
        self.throttle_rate = 0.015
        self.max_pitch = np.pi / 3
    
    def process_input(self, aircraft):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            aircraft.throttle = min(1.0, aircraft.throttle + self.throttle_rate)
        if keys[pygame.K_s]:
            aircraft.throttle = max(0.0, aircraft.throttle - self.throttle_rate)
        
        if keys[pygame.K_UP]:
            aircraft.pitch = min(self.max_pitch, aircraft.pitch + self.pitch_rate)
        if keys[pygame.K_DOWN]:
            aircraft.pitch = max(-self.max_pitch, aircraft.pitch - self.pitch_rate)
