import numpy as np
import p5
import time

class Grid:
    def __init__(self, max_dia, start_x, start_y, end_x, end_y):
        self.max_dia = max_dia
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.grid_width = self.end_x - self.start_x
        self.grid_height = self.end_y - self.start_y
        self.grid_row = int(np.floor(self.grid_height / self.max_dia))
        self.grid_col = int(np.floor(self.grid_width / self.max_dia))
        self.cell_height = self.grid_height / self.grid_row
        self.cell_width = self.grid_width / self.grid_col
        self.grid_array = [[0 for i in range(self.grid_col)] for j in range(self.grid_row)]
        self.grid_store = [[[] for i in range(self.grid_col)] for j in range(self.grid_row)]

    def create(self):
        for i in range(self.grid_row):
            for j in range(self.grid_col):
                self.grid_array[i][j] = [self.start_x + (j * self.cell_width), self.start_y + (i * self.cell_height)]

    def scan(self, check):
            for pos in check:
                other_cell = []
                for dx in range(-1, 2, 1):
                    for dy in range(-1, 2, 1):
                        if dx == 0 and dy == 0:
                            current_cell = grid.grid_store[pos[0]][pos[1]]
                            # p5.noStroke()
                            # p5.fill(0)
                            # p5.rect(grid.grid_array[pos[0]][pos[1]][0], grid.grid_array[pos[0]][pos[1]][1]+20, grid.cell_width, grid.cell_height-40)
                        else:
                            if 0 <= pos[0] + dx < self.grid_row:
                                if 0 <= pos[1] + dy < self.grid_col:
                                    other_cell = other_cell + grid.grid_store[pos[0] + dx][pos[1] + dy]
                                    # p5.noStroke()
                                    # p5.fill(255,0,0)
                                    # p5.rect(grid.grid_array[pos[0]+dx][pos[1]+dy][0]+10, grid.grid_array[pos[0]+dx][pos[1]+dy][1]+10,
                                    #         grid.cell_width-20, grid.cell_height-20)

                if len(current_cell) > 1 or len(other_cell) > 0:
                    k = 0
                    for a in current_cell:
                        current_cell_other = current_cell[0:k] + current_cell[k + 1:len(current_cell)]
                        collision(a, other_cell + current_cell_other)
                        k = k + 1

    def locate(self, particle, check):
        x = particle.pos_current[0]
        y = particle.pos_current[1]

        locate_row = int(np.floor((y - self.start_y) / self.cell_height))
        locate_col = int(np.floor((x - self.start_x) / self.cell_width))

        self.grid_store[locate_row][locate_col].append(particle)
        check.append([locate_row, locate_col])

        return check

    def reset(self):
        self.grid_store = [[[] for i in range(self.grid_col)] for j in range(self.grid_row)]

    def show(self):
        p5.stroke(0)
        p5.strokeWeight(2)
        for i in range(self.grid_row):
            p5.line(self.start_x, self.grid_array[i][0][1], self.end_x, self.grid_array[i][-1][1])

        for j in range(self.grid_col):
            p5.line(self.grid_array[0][j][0], self.start_y, self.grid_array[-1][j][0], self.end_y)

        p5.line(self.start_x, self.end_y, self.end_x, self.end_y)
        p5.line(self.end_x, self.start_y, self.end_x, self.end_y)

    def border(self):
        p5.stroke(0)
        p5.strokeWeight(2)
        p5.line(self.start_x, self.start_y, self.end_x, self.start_y)
        p5.line(self.start_x, self.start_y, self.start_x, self.end_y)
        p5.line(self.start_x, self.end_y, self.end_x, self.end_y)
        p5.line(self.end_x, self.start_y, self.end_x, self.end_y)



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


def verlet(particle, dt):
    velocity_dt = particle.pos_current - particle.pos_old

    particle.pos_old = particle.pos_current

    particle.acc = particle.force / particle.mass

    particle.pos_current = particle.pos_current + velocity_dt + particle.acc * dt * dt


def apply_force(particle):
    g = 3
    particle.force = np.array([0, g * particle.mass])


def constrain_wall(particle, grid):
    if particle.pos_current[0] + (particle.dia*0.5) > grid.end_x:
        vx = particle.pos_current[0] - particle.pos_old[0]
        particle.pos_current[0] = grid.end_x - particle.dia*0.5
        particle.pos_old[0] = particle.pos_current[0] + vx

    if particle.pos_current[0] - (particle.dia*0.5) < grid.start_x:
        vx = particle.pos_current[0] - particle.pos_old[0]
        particle.pos_current[0] = grid.start_x + particle.dia*0.5
        particle.pos_old[0] = particle.pos_current[0] + vx

    if particle.pos_current[1] + (particle.dia*0.5) > grid.end_y:
        vy = particle.pos_current[1] - particle.pos_old[1]
        particle.pos_current[1] = grid.end_y - particle.dia*0.5
        particle.pos_old[1] = particle.pos_current[1] + vy

    if particle.pos_current[1] - (particle.dia*0.5) < grid.start_y:
        vy = particle.pos_current[1] - particle.pos_old[1]
        particle.pos_current[1] = grid.start_y + particle.dia*0.5
        particle.pos_old[1] = particle.pos_current[1] + vy


def constrain_circle(particle, centre, circle_dia):
    dist_vector = particle.pos_current - centre

    dist = np.linalg.norm(dist_vector)
    n = dist_vector / dist
    if dist > (circle_dia / 2 - particle.dia / 2):
        particle.pos_current = centre + n * (circle_dia / 2 - particle.dia / 2)


def collision(particle, remaining):
    p5.strokeWeight(3)
    p5.stroke(0,255,0)
    for x in remaining:
        coll_vector = particle.pos_current - x.pos_current
        dist = np.linalg.norm(coll_vector)
        n = coll_vector / dist
        if dist < (particle.dia / 2 + x.dia / 2):
            delta = (particle.dia / 2 + x.dia / 2) - dist
            particle.pos_current = particle.pos_current + 0.5 * delta * n
            if not x.fixed:
                x.pos_current = x.pos_current - 0.5 * delta * n

       # p5.line(particle.pos_current[0], particle.pos_current[1], x.pos_current[0], x.pos_current[1])


def setup():
    global grid, dt, dia, width, height, new, b, k
    width = 1600
    height = 800
    p5.size(width, height)

    new = True
    b = 'new'
    k = 0

    dt = 0.1
    dia = 60

    grid = Grid(dia, 100, 100, width - 600, height - 300)
    grid.create()

    Particle(np.array([200, 200]), np.array([200, 200]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([800, 400]), np.array([800, 400]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([150, 450]), np.array([150, 450]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([500, 150]), np.array([500, 150]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([560, 400]), np.array([560, 400]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([700, 385]), np.array([700, 385]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([720, 300]), np.array([720, 300]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([400, 300]), np.array([400, 300]), np.array([0, 0]), 1, dia, False)
    Particle(np.array([300, 250]), np.array([300, 250]), np.array([0, 0]), 1, dia, False)
    #
    Particle(np.array([752, 302]), np.array([750, 300]), np.array([0, 0]), 1, dia, False)


def draw():
    start_tot = time.time()
    global grid, dt, dia, width, height, new, b, k
    p5.background(255)
    #grid.show()
    grid.border()
    check = []

    if new:
        p5.text("Collision New", 30, 40)
    else:
        p5.text("Collision Old", 30, 40)

    if key == 'ENTER':
        if new:
            new = False
            b = 'old'
        else:
            new = True
            b = 'new'

    if mouse_is_pressed:
        x = mouse_x
        y = mouse_y
        Particle(np.array([x,y]), np.array([x,y]), np.array([0, 0]), 1, dia, False)

    start = time.time()
    [apply_force(particle) for particle in Particle.lst]
    [verlet(particle, dt) for particle in Particle.lst]
    [constrain_wall(particle, grid) for particle in Particle.lst]
    i = 0
    for particle in Particle.lst:
        if new:
            check_lst = grid.locate(particle, check)
        if not new:
            remaining = Particle.lst[0:i] + Particle.lst[i + 1:len(Particle.lst)]
            collision(particle, remaining)
        i += 1

    if new and Particle.lst != []:
        grid.scan(check_lst)
        grid.reset()

    end = time.time()

    [particle.show() for particle in Particle.lst]


    p5.strokeWeight(1)
    p5.fill(0)
    p5.text(str(frame_rate), 30, 30)
    k = k + 1

    if k % 100 == 0:
        print("Physics " + b + ": ", end - start)
        print("Total " + b + ": ", time.time() - start_tot)


if __name__ == '__main__':
    p5.run()



