import pygame
import random as rand
import math


class Particle:
    def __init__(self, x, y, size, color=(0, 0, 255), mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.thickness = 0
        self.speed = 1
        self.angle = 0
        self.mass = mass
        mass_of_air = 0.2
        self.drag = (self.mass/(self.mass + mass_of_air))**self.size

    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        # add gravity
        # (self.angle, self.speed) = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.speed *= self.drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = -self.angle
            self.speed *= elasticity
        if self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = -self.angle
            self.speed *= elasticity
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
        if self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity


# take 2 vectors with same origin, return resultant vector of the them
def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1)*length1 + math.sin(angle2)*length2
    y = math.cos(angle1)*length1 + math.cos(angle2)*length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return angle, length


# check if x, y is within any particles
def findParticles(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p


# handling colliding between two particles
def collide(p1, p2):
    d_x = p1.x - p2.x
    d_y = p1.y - p2.y
    distance = math.hypot(d_x, d_y)
    if distance < p1.size + p2.size:  # flip angle and reverse speed
        angle = math.atan2(d_y, d_x) + 0.5*math.pi
        total_mass = p1.mass + p2.mass
        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass - p2.mass)/total_mass,
                                          angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass - p1.mass)/total_mass,
                                          angle+math.pi, 2*p1.speed*p1.mass/total_mass)
        # tangent = math.atan2(d_y, d_x)
        # p1.angle = 2*tangent - p1.angle
        # p2.angle = 2*tangent - p2.angle
        # (p1.speed, p2.speed) = (p2.speed, p1.speed)
        p1.speed *= elasticity
        p2.speed *= elasticity
        # solve 'sticking' problem
        # angle = 0.5 * math.pi + tangent
        overlap = 0.5*(p1.size + p2.size - distance + 1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap


# pygame.init()

# create game window
(width, height) = 400, 400
background_color = (255, 255, 255)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
screen.fill(background_color)

# generate randomly a number of particles
number_of_particles = 30
my_random_particles = []
for i in range(0, number_of_particles):
    size_part = rand.randint(10, 20)
    density_part = rand.randint(1, 20)
    color_part = (200 - density_part*10, 200 - density_part*10, 255)
    x_coord = rand.randint(size_part, width - size_part)
    y_coord = rand.randint(size_part, height - size_part)
    particle = Particle(x_coord, y_coord, size_part, color_part, density_part * size_part**2)
    particle.speed = rand.random()
    particle.angle = rand.uniform(0, math.pi*2)
    my_random_particles.append(particle)

# kinematics parameters to be used for particles
# gravity = (math.pi, .02)
# drag = .999
elasticity = .75

running = True
selected_particle = None
while running:
    # keeps game window running
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            selected_particle = findParticles(my_random_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP and selected_particle:
            selected_particle.color = (0, 0, 255)
            selected_particle = None
        if event.type == pygame.QUIT:
            running = False

    # create moving particles
    for i, particle in enumerate(my_random_particles):
        if selected_particle:  # check if particle is selected
            selected_particle.color = (255, 0, 0)
            mouseX, mouseY = pygame.mouse.get_pos()
            dx = mouseX - selected_particle.x
            dy = mouseY - selected_particle.y
            selected_particle.angle = math.atan2(dy, dx) + 0.5*math.pi
            selected_particle.speed = math.hypot(dx, dy) * .1
        particle.move()
        particle.bounce()
        for particle2 in my_random_particles[i+1:]:  # check collide
            collide(particle, particle2)
        particle.display()
    pygame.display.flip()
    screen.fill(background_color)
