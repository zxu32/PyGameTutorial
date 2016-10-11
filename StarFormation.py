import random as rand
import pygame
import PyParticles


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
pygame.display.set_caption('Star formation')
universe = PyParticles.Environment(w, h)
universe.color = (0, 0, 0)
universe.addFunctions(['move', 'attract', 'combine', 'bounce'])


def calculateRadius(mass):
    return 0.4 * mass ** 0.5

for p in range(0, 100):
    particleMass = rand.randint(10, 11)
    particleSize = int(calculateRadius(particleMass))
    universe.addParticles(mass=particleMass, size=particleSize, color=(255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    universe.update()
    screen.fill(universe.color)
    for p in universe.particles:
        if p.size < 2:
            pygame.draw.rect(screen, p.color, (int(p.x), int(p.y), 2, 2))
            # draw rectangle to approximate particle when they are too small
        else:
            pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), int(p.size), 0)

    particleToRemove = []
    for p in universe.particles:
        if 'collideWith' in p.__dict__:
            particleToRemove.append(p.collideWith)
            p.size = calculateRadius(p.mass)
            del p.__dict__['collideWith']
    for p in particleToRemove:
        if p in universe.particles:
            universe.particles.remove(p)

    pygame.display.flip()
