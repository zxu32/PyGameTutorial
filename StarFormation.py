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
universe = PyParticles.Environment(w, h, color=(0, 0, 0))
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                universeScreen.scroll(dx=1)
            if event.key == pygame.K_RIGHT:
                universeScreen.scroll(dx=-1)
            if event.key == pygame.K_UP:
                universeScreen.scroll(dy=1)
            if event.key == pygame.K_DOWN:
                universeScreen.scroll(dy=-1)
            if event.key == pygame.K_EQUALS:
                universeScreen.zoom(2)
            if event.key == pygame.K_MINUS:
                universeScreen.zoom(0.5)
            if event.key == pygame.K_r:
                universeScreen.reset()

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

# universeScreen.scroll(dx=1)
