import numpy as np
import p5
from random import randrange

class Particle:
    lst = []

    def __init__(self, pos_current, pos_old, force, mass, dia, fixed):
        self.pos_current = pos_current
        self.pos_old = pos_old
        self.mass = mass
        self.force = force
        self.acc = self.force / mass
        self.dia = dia
        self.fixed = fixed

        Particle.lst.append(self)

    def update(self, pos_new, pos_old, acc):
        self.pos_current = pos_new
        self.pos_old = pos_old
        self.acc = acc

    def show(self):
        p5.no_stroke()
        p5.fill(150)
        p5.circle(self.pos_current[0], self.pos_current[1], self.dia)


class Stick:
    lst = []

    def __init__(self, particle_1, particle_2):
        self.particle_1 = particle_1
        self.particle_2 = particle_2
        self.length = np.linalg.norm(self.particle_1.pos_current - self.particle_2.pos_current)

        Stick.lst.append(self)

    def stick_constrain(self):
        delta = self.particle_1.pos_current - self.particle_2.pos_current
        dist = np.linalg.norm(delta)
        difference = self.length - dist
        percent = difference / dist / 2
        offset = delta * percent

        if not self.particle_1.fixed:
            self.particle_1.pos_current = self.particle_1.pos_current + offset
        if not self.particle_2.fixed:
            self.particle_2.pos_current = self.particle_2.pos_current - offset

    def show(self):
        p5.stroke(255)
        p5.strokeWeight(5)
        p5.line(self.particle_1.pos_current[0], self.particle_1.pos_current[1], self.particle_2.pos_current[0], self.particle_2.pos_current[1])


def verlet(particle, dt):
    velocity_dt = particle.pos_current - particle.pos_old

    particle.pos_old = particle.pos_current

    particle.acc = particle.force / particle.mass

    particle.pos_current = particle.pos_current + velocity_dt + particle.acc * dt * dt


def apply_force(particle):
    g = 10
    particle.force = np.array([0, g * particle.mass])


def constrain(particle, centre, circle_dia):
    dist_vector = particle.pos_current - centre

    dist = np.linalg.norm(dist_vector)
    n = dist_vector / dist
    if dist > (circle_dia / 2 - particle.dia / 2):
        particle.pos_current = centre + n * (circle_dia / 2 - particle.dia / 2)


def collision(particle, remaining):
    for x in remaining:
        coll_vector = particle.pos_current - x.pos_current
        dist = np.linalg.norm(coll_vector)
        n = coll_vector / dist
        if dist < (particle.dia / 2 + x.dia / 2):
            delta = (particle.dia / 2 + x.dia / 2) - dist
            particle.pos_current = particle.pos_current + 0.5 * delta * n
            if not x.fixed:
                x.pos_current = x.pos_current - 0.5 * delta * n


def setup():

    global width, height, dt, sub_step
    width = 1600
    height = 800
    p5.size(width, height)

    dt = 0.1
    sub_step = 1

    dia = 40

    pos_cur = np.array([width / 2 - 300, height / 2])
    pos_old = np.array([width / 2 - 300, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, True)

    pos_cur = np.array([width / 2 - 250, height / 2])
    pos_old = np.array([width / 2 - 250, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, False)

    pos_cur = np.array([width / 2 - 200, height / 2])
    pos_old = np.array([width / 2 - 200, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, False)

    pos_cur = np.array([width / 2 - 150, height / 2])
    pos_old = np.array([width / 2 - 150, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, False)

    pos_cur = np.array([width / 2 - 100, height / 2])
    pos_old = np.array([width / 2 - 100, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, False)

    pos_cur = np.array([width / 2 - 50, height / 2])
    pos_old = np.array([width / 2 - 50, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, False)

    pos_cur = np.array([width / 2, height / 2])
    pos_old = np.array([width / 2, height / 2])
    force = np.array([0, 0])
    mass = 1
    Particle(pos_cur, pos_old, force, mass, dia, True)

    Stick(Particle.lst[0], Particle.lst[1])
    Stick(Particle.lst[1], Particle.lst[2])
    Stick(Particle.lst[2], Particle.lst[3])
    Stick(Particle.lst[3], Particle.lst[4])
    Stick(Particle.lst[4], Particle.lst[5])
    Stick(Particle.lst[5], Particle.lst[6])


def draw():
    global dt, sub_step
    p5.background(255)
    p5.fill(0)
    circle_dia = 800
    p5.circle(width / 2, height / 2, circle_dia)

    if mouse_is_pressed:
        x = mouse_x
        y = mouse_y
        dia = randrange(30, 75)
        dia = 30
        Particle(np.array([x,y]), np.array([x,y]), np.array([0, 0]), 1, dia, False)

    i = 0
    for particle in Particle.lst:
        if not particle.fixed:
            apply_force(particle)
            verlet(particle, dt)

            constrain(particle, np.array([width / 2, height / 2]), circle_dia)
            remaining = Particle.lst[0:i] + Particle.lst[i+1:len(Particle.lst)]
            collision(particle, remaining)

        i += 1

    for j in range(5):
        for stick in Stick.lst:
            stick.stick_constrain()

    [particle.show() for particle in Particle.lst]
    [stick.show() for stick in Stick.lst]


if __name__ == '__main__':
    p5.run()










