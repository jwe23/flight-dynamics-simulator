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
        self.ground_dark = (28, 120, 28)
        self.text_white = (255, 255, 255)
        self.hud_bg = (0, 0, 0, 180)
        
        self.aircraft_sprite = self._load_aircraft_sprite()
        
        self.cloud_offset = 0
        self.ground_offset = 0
        self.clouds = self._generate_clouds()
    
    def _load_aircraft_sprite(self):
        try:
            sprite = pygame.image.load('airplane.png').convert_alpha()
            sprite = pygame.transform.scale(sprite, (80, 80))
            return sprite
        except:
            return self._create_fallback_sprite()
    
    def _create_fallback_sprite(self):
        size = 60
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        pygame.draw.rect(surface, (200, 200, 200), (center - 5, center - 20, 10, 40))
        pygame.draw.rect(surface, (180, 180, 180), (center - 30, center - 3, 60, 6))
        nose_points = [(center + 5, center - 5), (center + 20, center), (center + 5, center + 5)]
        pygame.draw.polygon(surface, (220, 50, 50), nose_points)
        return surface
    
    def _generate_clouds(self):
        clouds = []
        for i in range(8):
            x = i * 250
            y = np.random.randint(50, 200)
            size = np.random.randint(40, 80)
            clouds.append({'x': x, 'y': y, 'size': size})
        return clouds
    
    def render(self, aircraft):
        speed = aircraft.velocity[0]
        
        self.cloud_offset += speed * 0.02
        self.ground_offset += speed * 0.1
        
        self.screen.fill(self.sky_color)
        
        self._draw_clouds()
        
        horizon_y = int(self.height * 0.65 + aircraft.position[2] * 0.3)
        horizon_y = max(self.height // 3, min(self.height - 50, horizon_y))
        
        pygame.draw.rect(self.screen, self.ground_color, (0, horizon_y, self.width, self.height - horizon_y))
        pygame.draw.line(self.screen, (100, 100, 100), (0, horizon_y), (self.width, horizon_y), 2)
        
        self._draw_ground_pattern(horizon_y)
        
        self._draw_aircraft(aircraft)
        self._draw_hud(aircraft)
        
        pygame.display.flip()
    
    def _draw_clouds(self):
        for cloud in self.clouds:
            x = (cloud['x'] - self.cloud_offset) % (self.width + 200) - 100
            y = cloud['y']
            size = cloud['size']
            
            pygame.draw.ellipse(self.screen, (255, 255, 255), (x, y, size, size * 0.6))
            pygame.draw.ellipse(self.screen, (255, 255, 255), (x + size * 0.3, y - size * 0.2, size * 0.8, size * 0.5))
            pygame.draw.ellipse(self.screen, (255, 255, 255), (x + size * 0.5, y, size * 0.7, size * 0.6))
    
    def _draw_ground_pattern(self, horizon_y):
        stripe_width = 100
        num_stripes = (self.width // stripe_width) + 2
        
        for i in range(num_stripes):
            x = (i * stripe_width - int(self.ground_offset) % stripe_width)
            if i % 2 == 0:
                pygame.draw.rect(self.screen, self.ground_dark, (x, horizon_y, stripe_width, self.height - horizon_y))
    
    def _draw_aircraft(self, aircraft):
        x = self.width // 2
        y = self.height // 2
        
        angle = np.degrees(aircraft.pitch)
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
