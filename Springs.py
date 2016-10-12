import random as rand
import pygame
import PyParticles
import math


(w, h) = (400, 400)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Springs')
universe = PyParticles.Environment(w, h, color=(255, 255, 255))
universe.acceleration = (math.pi, 0.01)
universe.mass_of_air = 0.02
universe.addFunctions(['move', 'drag', 'combine', 'bounce', 'collide', 'accelerate'])

for p in range(0, 4):
    particleMass = 100
    particleSize = 16
    universe.addParticles(mass=particleMass, size=particleSize, color=(20, 40, 200))

running = True
paused = False
selected_particle = None
color_temp = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]  # flip the current value of paused
        elif event.type == pygame.MOUSEBUTTONDOWN:  # check particle selection
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = universe.findParticles(mouseX, mouseY)
            if selected_particle:
                color_temp = selected_particle.color
        elif event.type == pygame.MOUSEBUTTONUP and selected_particle:  # de-select particle
            selected_particle.color = color_temp
            selected_particle = None

    if selected_particle:  # move the selected particle with cursor
        selected_particle.color = (255, 0, 0)
        mouseX, mouseY = pygame.mouse.get_pos()
        selected_particle.mouseMove(mouseX, mouseY)
    if not paused:
        universe.update()
    screen.fill(universe.color)  # this has to go before pygame's draw function
    for p in universe.particles:  # display particles from previous step
        pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.size, p.thickness)
    pygame.display.flip()
