# src/renderer.py
import pygame
import numpy as np

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.sky_blue = (135, 206, 235)
        self.ground_green = (34, 139, 34)
        self.aircraft_red = (255, 0, 0)
        self.velocity_green = (0, 255, 0)
        self.text_black = (0, 0, 0)
    
    def render(self, aircraft):
        self.screen.fill(self.sky_blue)
        pygame.draw.line(self.screen, self.ground_green, (0, 500), (800, 500), 100)
        self._draw_aircraft(aircraft)
        self._draw_hud(aircraft)
        self._draw_controls_help()
        pygame.display.flip()
    
    def _draw_aircraft(self, aircraft):
        x = int(400 + aircraft.position[0] / 10)
        y = int(500 - aircraft.position[2])
        
        size = 10
        nose_x = x + int(size * np.cos(aircraft.pitch))
        nose_y = y - int(size * np.sin(aircraft.pitch))
        left_x = x + int(size * np.cos(aircraft.pitch + 2.5))
        left_y = y - int(size * np.sin(aircraft.pitch + 2.5))
        right_x = x + int(size * np.cos(aircraft.pitch - 2.5))
        right_y = y - int(size * np.sin(aircraft.pitch - 2.5))
        
        pygame.draw.polygon(self.screen, self.aircraft_red, 
                          [(nose_x, nose_y), (left_x, left_y), (right_x, right_y)])
        
        vel_end_x = x + int(aircraft.velocity[0] / 2)
        vel_end_y = y - int(aircraft.velocity[2] / 2)
        pygame.draw.line(self.screen, self.velocity_green, (x, y), 
                        (vel_end_x, vel_end_y), 2)
    
    def _draw_hud(self, aircraft):
        hud_data = [
            f"Alt: {aircraft.position[2]:.1f}m",
            f"Vel: {aircraft.velocity[0]:.1f}m/s",
            f"Throttle: {aircraft.throttle*100:.0f}%",
            f"Pitch: {np.degrees(aircraft.pitch):.1f}°"
        ]
        
        for i, text in enumerate(hud_data):
            surface = self.font_large.render(text, True, self.text_black)
            self.screen.blit(surface, (10, 10 + i * 40))
    
    def _draw_controls_help(self):
        help_text = [
            "W/S: Throttle",
            "UP/DOWN: Pitch",
            "ESC: Exit"
        ]
        
        for i, text in enumerate(help_text):
            surface = self.font_small.render(text, True, self.text_black)
            self.screen.blit(surface, (600, 10 + i * 30))
