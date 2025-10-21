# src/main.py
import pygame
import numpy as np
from aircraft import Aircraft

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Flight Simulator MVP")

aircraft = Aircraft()
running = True

while running:
    dt = clock.tick(60) / 1000.0  # 60 FPS
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        aircraft.throttle = min(1.0, aircraft.throttle + 0.01)
    if keys[pygame.K_s]:
        aircraft.throttle = max(0.0, aircraft.throttle - 0.01)
    
    # Update physics
    aircraft.update(dt)
    
    # Draw
    screen.fill((135, 206, 235))  # Sky blue
    
    # Draw ground
    pygame.draw.line(screen, (34, 139, 34), (0, 500), (800, 500), 100)
    
    # Draw aircraft (simple top-down)
    x = int(400 + aircraft.position[0] / 10)
    y = int(500 - aircraft.position[2])
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    
    # Draw HUD
    font = pygame.font.Font(None, 36)
    alt_text = font.render(f"Alt: {aircraft.position[2]:.1f}m", True, (0, 0, 0))
    vel_text = font.render(f"Vel: {aircraft.velocity[0]:.1f}m/s", True, (0, 0, 0))
    thr_text = font.render(f"Throttle: {aircraft.throttle*100:.0f}%", True, (0, 0, 0))
    
    screen.blit(alt_text, (10, 10))
    screen.blit(vel_text, (10, 50))
    screen.blit(thr_text, (10, 90))
    
    pygame.display.flip()

pygame.quit()
