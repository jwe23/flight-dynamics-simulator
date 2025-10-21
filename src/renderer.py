# src/renderer.py
import pygame
import numpy as np

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font_large = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)
        
        # Better colors
        self.sky_blue = (135, 206, 250)
        self.ground_green = (34, 139, 34)
        self.ground_dark = (20, 100, 20)
        self.aircraft_white = (255, 255, 255)
        self.aircraft_red = (220, 50, 50)
        self.velocity_yellow = (255, 255, 0)
        self.text_white = (255, 255, 255)
        self.text_shadow = (0, 0, 0)
        self.hud_bg = (0, 0, 0, 128)
    
    def render(self, aircraft):
        self.screen.fill(self.sky_blue)
        
        # Draw horizon
        horizon_y = self.height // 2
        pygame.draw.rect(self.screen, self.ground_green, (0, horizon_y, self.width, self.height - horizon_y))
        pygame.draw.line(self.screen, self.ground_dark, (0, horizon_y), (self.width, horizon_y), 3)
        
        # Aircraft always centered horizontally
        self._draw_aircraft(aircraft)
        self._draw_hud(aircraft)
        self._draw_controls_help()
        
        pygame.display.flip()
    
    def _draw_aircraft(self, aircraft):
        # Keep aircraft centered horizontally
        x = self.width // 2
        
        # Vertical position based on altitude
        y = self.height // 2 - int(aircraft.position[2] * 0.8)
        y = max(50, min(self.height - 50, y))
        
        # Draw aircraft body (fuselage)
        fuselage_length = 30
        fuselage_width = 8
        
        # Calculate fuselage points based on pitch
        nose_x = x + int(fuselage_length * np.cos(aircraft.pitch))
        nose_y = y - int(fuselage_length * np.sin(aircraft.pitch))
        tail_x = x - int(fuselage_length * np.cos(aircraft.pitch))
        tail_y = y + int(fuselage_length * np.sin(aircraft.pitch))
        
        # Draw fuselage
        pygame.draw.line(self.screen, self.aircraft_white, (nose_x, nose_y), (tail_x, tail_y), fuselage_width)
        
        # Draw wings perpendicular to fuselage
        wing_angle = aircraft.pitch + np.pi/2
        wing_span = 40
        wing_left_x = x + int(wing_span * np.cos(wing_angle))
        wing_left_y = y - int(wing_span * np.sin(wing_angle))
        wing_right_x = x - int(wing_span * np.cos(wing_angle))
        wing_right_y = y + int(wing_span * np.sin(wing_angle))
        
        pygame.draw.line(self.screen, self.aircraft_white, (wing_left_x, wing_left_y), (wing_right_x, wing_right_y), 6)
        
        # Draw nose cone
        pygame.draw.circle(self.screen, self.aircraft_red, (nose_x, nose_y), 6)
        
        # Draw velocity vector
        vel_scale = 3
        vel_end_x = x + int(aircraft.velocity[0] * vel_scale)
        vel_end_y = y - int(aircraft.velocity[2] * vel_scale)
        pygame.draw.line(self.screen, self.velocity_yellow, (x, y), (vel_end_x, vel_end_y), 2)
        pygame.draw.circle(self.screen, self.velocity_yellow, (vel_end_x, vel_end_y), 3)
    
    def _draw_hud(self, aircraft):
        # HUD background
        hud_surface = pygame.Surface((280, 180), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 180))
        self.screen.blit(hud_surface, (10, 10))
        
        # Flight data
        speed = np.linalg.norm(aircraft.velocity)
        hud_data = [
            f"Altitude: {aircraft.position[2]:.0f} m",
            f"Speed: {speed:.0f} m/s",
            f"Throttle: {aircraft.throttle*100:.0f}%",
            f"Pitch: {np.degrees(aircraft.pitch):.1f}°",
        ]
        
        for i, text in enumerate(hud_data):
            # Shadow
            shadow = self.font_large.render(text, True, self.text_shadow)
            self.screen.blit(shadow, (21, 21 + i * 35))
            # Text
            surface = self.font_large.render(text, True, self.text_white)
            self.screen.blit(surface, (20, 20 + i * 35))
    
    def _draw_controls_help(self):
        # Control hints background
        help_surface = pygame.Surface((180, 90), pygame.SRCALPHA)
        help_surface.fill((0, 0, 0, 180))
        self.screen.blit(help_surface, (self.width - 190, 10))
        
        help_text = [
            "W/S: Throttle",
            "UP/DOWN: Pitch",
            "ESC: Exit"
        ]
        
        for i, text in enumerate(help_text):
            surface = self.font_small.render(text, True, self.text_white)
            self.screen.blit(surface, (self.width - 180, 20 + i * 25))
