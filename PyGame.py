import pygame
import PyParticles
import math

(width, height) = (400, 400)
# background_color = (255, 255, 255)
pygame.display.set_caption('Tutorial 1')
screen = pygame.display.set_mode((width, height))
env = PyParticles.Environment(width, height)
env.addParticles(n=15, color=(0, 0, 255))
env.addFunctions(['move', 'accelerate', 'drag', 'bounce', 'collide'])
env.acceleration = (math.pi, 0.002)

running = True
selected_particle = None
color_temp = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = env.findParticles(mouseX, mouseY)
            if selected_particle:
                color_temp = selected_particle.color
        elif event.type == pygame.MOUSEBUTTONUP and selected_particle:
            selected_particle.color = color_temp
            selected_particle = None
    if selected_particle:
        selected_particle.color = (255, 0, 0)
        mouseX, mouseY = pygame.mouse.get_pos()
        selected_particle.mouseMove(mouseX, mouseY)
    env.update()  # collide, bounce and move all particles
    for p in env.particles:  # display particles from previous step
        pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), p.size, p.thickness)
    pygame.display.flip()
    screen.fill(env.color)
