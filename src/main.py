# src/main.py
import pygame
from aircraft import Aircraft
from physics import PhysicsEngine
from controls import Controls
from renderer import Renderer
from telemetry import Telemetry

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flight Dynamics Simulator")
    
    aircraft = Aircraft()
    physics = PhysicsEngine()
    controls = Controls()
    renderer = Renderer(screen)
    telemetry = Telemetry()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        controls.process_input(aircraft)
        physics.update(aircraft, dt)
        telemetry.log(aircraft, dt)
        renderer.render(aircraft)
    
    telemetry.export_csv()
    pygame.quit()

if __name__ == "__main__":
    main()
