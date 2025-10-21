# src/renderer.py
import pygame
import numpy as np

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font_large = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 24)
        
        self.sky_color = (135, 206, 250)
        self.ground_color = (34, 139, 34)
        self.text_white = (255, 255, 255)
        self.hud_bg = (0, 0, 0, 180)
        
        self.aircraft_sprite = self._create_aircraft_sprite()
    
    def _create_aircraft_sprite(self):
        size = 60
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        center = size // 2
        
        # Fuselage (simple rectangle)
        pygame.draw.rect(surface, (200, 200, 200), (center - 5, center - 20, 10, 40))
        
        # Wings (horizontal line)
        pygame.draw.rect(surface, (180, 180, 180), (center - 30, center - 3, 60, 6))
        
        # Nose (triangle pointing right)
        nose_points = [(center + 5, center - 5), (center + 20, center), (center + 5, center + 5)]
        pygame.draw.polygon(surface, (220, 50, 50), nose_points)
        
        # Tail
        tail_points = [(center - 5, center - 20), (center - 15, center - 25), (center - 5, center - 15)]
        pygame.draw.polygon(surface, (180, 180, 180), tail_points)
        
        return surface
    
    def render(self, aircraft):
        self.screen.fill(self.sky_color)
        
        horizon_y = int(self.height * 0.65 + aircraft.position[2] * 0.3)
        horizon_y = max(self.height // 3, min(self.height - 50, horizon_y))
        
        pygame.draw.rect(self.screen, self.ground_color, (0, horizon_y, self.width, self.height - horizon_y))
        pygame.draw.line(self.screen, (100, 100, 100), (0, horizon_y), (self.width, horizon_y), 2)
        
        self._draw_aircraft(aircraft)
        self._draw_hud(aircraft)
        
        pygame.display.flip()
    
    def _draw_aircraft(self, aircraft):
        x = self.width // 2
        y = self.height // 2
        
        angle = -np.degrees(aircraft.pitch)
        rotated_sprite = pygame.transform.rotate(self.aircraft_sprite, angle)
        rect = rotated_sprite.get_rect(center=(x, y))
        self.screen.blit(rotated_sprite, rect)
    
    def _draw_hud(self, aircraft):
        hud_surface = pygame.Surface((280, 180), pygame.SRCALPHA)
        hud_surface.fill(self.hud_bg)
        self.screen.blit(hud_surface, (20, 20))
        
        speed = np.linalg.norm(aircraft.velocity)
        
        hud_data = [
            f"ALT: {aircraft.position[2]:.0f}m",
            f"SPD: {speed:.0f}m/s",
            f"THR: {aircraft.throttle*100:.0f}%",
            f"PITCH: {np.degrees(aircraft.pitch):.1f}°"
        ]
        
        y_pos = 35
        for text in hud_data:
            surface = self.font_large.render(text, True, self.text_white)
            self.screen.blit(surface, (35, y_pos))
            y_pos += 38
        
        help_surface = pygame.Surface((180, 90), pygame.SRCALPHA)
        help_surface.fill(self.hud_bg)
        self.screen.blit(help_surface, (self.width - 200, 20))
        
        controls = ["W/S: Throttle", "UP/DN: Pitch", "ESC: Exit"]
        y_pos = 35
        for text in controls:
            surface = self.font_small.render(text, True, self.text_white)
            self.screen.blit(surface, (self.width - 185, y_pos))
            y_pos += 28
