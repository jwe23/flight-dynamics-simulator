# src/renderer.py
import pygame
import numpy as np

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.sky_top = (70, 130, 180)
        self.sky_bottom = (135, 206, 250)
        self.ground_green = (34, 139, 34)
        self.ground_brown = (139, 90, 43)
        self.text_white = (255, 255, 255)
        self.hud_bg = (0, 0, 0, 200)
    
    def render(self, aircraft):
        self._draw_sky()
        self._draw_ground(aircraft)
        self._draw_aircraft(aircraft)
        self._draw_hud(aircraft)
        pygame.display.flip()
    
    def _draw_sky(self):
        for y in range(self.height // 2):
            ratio = y / (self.height // 2)
            color = tuple(int(self.sky_top[i] + (self.sky_bottom[i] - self.sky_top[i]) * ratio) for i in range(3))
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    def _draw_ground(self, aircraft):
        horizon = self.height // 2 + int(aircraft.position[2] * 0.5)
        horizon = max(100, min(self.height - 100, horizon))
        
        pygame.draw.rect(self.screen, self.ground_green, (0, horizon, self.width, self.height - horizon))
        pygame.draw.line(self.screen, self.ground_brown, (0, horizon), (self.width, horizon), 2)
    
    def _draw_aircraft(self, aircraft):
        x = self.width // 2
        y = self.height // 2
        
        scale = 2.5
        pitch_deg = np.degrees(aircraft.pitch)
        
        fuselage = [
            (-20, 0), (-15, -3), (-10, -4), (0, -4),
            (15, -3), (20, -2), (25, 0), (20, 2),
            (15, 3), (0, 4), (-10, 4), (-15, 3), (-20, 0)
        ]
        
        wings = [
            (-5, -4), (-5, -20), (0, -22), (5, -20), (5, -4),
            (5, 4), (5, 20), (0, 22), (-5, 20), (-5, 4)
        ]
        
        tail = [
            (-20, 0), (-25, -8), (-23, -10), (-20, -3)
        ]
        
        def rotate_and_scale(points):
            angle = np.radians(pitch_deg)
            result = []
            for px, py in points:
                px, py = px * scale, py * scale
                rx = px * np.cos(angle) - py * np.sin(angle)
                ry = px * np.sin(angle) + py * np.cos(angle)
                result.append((int(x + rx), int(y - ry)))
            return result
        
        fuselage_points = rotate_and_scale(fuselage)
        wings_points = rotate_and_scale(wings)
        tail_points = rotate_and_scale(tail)
        
        pygame.draw.polygon(self.screen, (200, 200, 200), wings_points)
        pygame.draw.polygon(self.screen, (255, 255, 255), fuselage_points)
        pygame.draw.polygon(self.screen, (220, 220, 220), tail_points)
        
        pygame.draw.aalines(self.screen, (100, 100, 100), True, fuselage_points)
        pygame.draw.aalines(self.screen, (100, 100, 100), False, wings_points)
        pygame.draw.aalines(self.screen, (100, 100, 100), False, tail_points)
    
    def _draw_hud(self, aircraft):
        hud_surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        hud_surface.fill(self.hud_bg)
        self.screen.blit(hud_surface, (15, 15))
        
        speed = np.linalg.norm(aircraft.velocity)
        
        hud_data = [
            f"ALT: {aircraft.position[2]:.0f} m",
            f"SPD: {speed:.0f} m/s",
            f"THR: {aircraft.throttle*100:.0f}%",
            f"PITCH: {np.degrees(aircraft.pitch):.1f}°"
        ]
        
        y_offset = 30
        for text in hud_data:
            surface = self.font_large.render(text, True, self.text_white)
            self.screen.blit(surface, (30, y_offset))
            y_offset += 40
        
        controls = ["W/S: Throttle", "↑/↓: Pitch", "ESC: Exit"]
        help_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
        help_surface.fill(self.hud_bg)
        self.screen.blit(help_surface, (self.width - 215, 15))
        
        y_offset = 30
        for text in controls:
            surface = self.font_small.render(text, True, self.text_white)
            self.screen.blit(surface, (self.width - 200, y_offset))
            y_offset += 30
