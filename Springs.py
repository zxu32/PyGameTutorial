import random as rand
import pygame
import PyParticles
import math


class UniverseScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1

    def scroll(self, dx=0, dy=0):
        self.dx += (dx * self.width)/(self.magnification * 10)
        self.dy += (dy * self.height)/(self.magnification * 10)

    def zoom(self, zoom):
        self.magnification *= zoom
        self.mx = (1 - self.magnification) * self.width / 2
        self.my = (1 - self.magnification) * self.height / 2

    def reset(self):
        (self.dx, self.dy) = (0, 0)
        (self.mx, self.my) = (0, 0)
        self.magnification = 1

(w, h) = (400, 400)
universeScreen = UniverseScreen(w, h)

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = universe.findParticles(mouseX, mouseY)
            if selected_particle:
                color_temp = selected_particle.color
        elif event.type == pygame.MOUSEBUTTONUP and selected_particle:
            selected_particle.color = color_temp
            selected_particle = None

    if selected_particle:
        selected_particle.color = (255, 0, 0)
        mouseX, mouseY = pygame.mouse.get_pos()
        selected_particle.mouseMove(mouseX, mouseY)
    if not paused:
        universe.update()
    screen.fill(universe.color)
    for p in universe.particles:
        x = int(universeScreen.mx + (universeScreen.dx + p.x) * universeScreen.magnification)
        y = int(universeScreen.my + (p.y + universeScreen.dy) * universeScreen.magnification)
        size = int(p.size * universeScreen.magnification)
        if p.size < 2:
            pygame.draw.rect(screen, p.color, (x, y, 2, 2))
            # draw rectangle to approximate particle when they are too small
        else:
            pygame.draw.circle(screen, p.color, (x, y), int(p.size), 0)

    pygame.display.flip()
