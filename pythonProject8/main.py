import queue
import pygame
import random


class Button:
    def __init__(self, x, y, w, h, unpr, pr, act, action, text):
        self.x = x
        self.y = y
        self.unpr = unpr
        self.pr = pr
        self.act = act
        self.h = h
        self.w = w
        self.action = action
        self.text = text

    def draw(self):
        pygame.draw.rect(win, self.unpr, (self.x, self.y, self.w, self.h))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.x < mouse[0] < self.x + self.w:
            if self.y < mouse[1] < self.y + self.h:
                if click[0]:
                    pygame.draw.rect(win, self.pr, (self.x + 10, self.y + 10, self.w - 20, self.h - 20))
                    if self.action is not None:
                        self.action()
                else:
                    pygame.draw.rect(win, self.act, (self.x + 10, self.y + 10, self.w - 20, self.h - 20))
        print_text(self.text, self.x + 20, self.y + 10)


pygame.init()
win = pygame.display.set_mode((1380, 900))
pygame.display.set_caption("nian")
wp = [pygame.image.load('skin/wy.png'), pygame.image.load('skin/wb.png'), pygame.image.load('skin/wg.png'),
      pygame.image.load('skin/wl.png'), pygame.image.load('skin/ws.png'), pygame.image.load('skin/we.png')]
men = pygame.image.load('skin/menu9.png')

Xx = 31
Yy = 41
Cage_Size = 30
na_active = 0
a = []
Sx = 3
Sy = 2
Ex = 3
Ey = 6
for i in range(Xx + 1):
    a.append([0] * (Yy + 1))

a[Sx][Sy] = 4
a[Ex][Ey] = 5



b = []

for i in range(Xx + 1):
    b.append([0] * (Yy + 1))


def print_text(message, x, y, font_color=(0, 0, 0), font_size=30):
    # font_type = pygame.font.Font(font_type, font_size)
    font = pygame.font.SysFont('comicsansms', font_size)
    text = font.render(message, 1, font_color)
    win.blit(text, (x, y))


def drawWindow():
    for i in range(1, Xx):
        for j in range(1, Yy):
            win.blit(wp[a[i][j]], ((j - 1) * Cage_Size, (i - 1) * Cage_Size))


def recountMas():
    for i in range(1, Xx):
        for j in range(1, Yy):
            sum = a[i - 1][j - 1] + a[i - 1][j] + a[i - 1][j + 1] + a[i][j - 1] + a[i][j + 1] + a[i + 1][j - 1] + \
                  a[i + 1][j] + a[i + 1][j + 1]
            if a[i][j] == 0:
                if sum == 3:
                    b[i][j] = 1
            if a[i][j] == 1:
                b[i][j] = 1
                if (sum == 3) or (sum == 2):
                    b[i][j] = 1
                # else:
                #    b[i][j] = 0
    for i in range(1, Xx):
        for j in range(1, Yy):
            a[i][j] = b[i][j]


def delete():
    for i in range(1, Xx):
        for j in range(1, Yy):
            a[i][j] = 0
            b[i][j] = 0


def ran():
    for i in range(1, Xx):
        for j in range(1, Yy):
            a[i][j] = random.randint(0, 1)
            b[i][j] = 0

def field():
    global na_active
    na_active = 0

def mountain():
    global na_active
    na_active = 1

def forest():
    global na_active
    na_active = 2

def water():
    global na_active
    na_active = 3

def start():
    global na_active
    na_active = 4

def esc():
    global na_active
    na_active = 5

def drawAstar(path):
    for i in range(len(path) - 1):
        xs = path[i][0] * 30 + 15
        ys = path[i][1] * 30 + 15
        xe = path[i + 1][0] * 30 + 15
        ye = path[i + 1][1] * 30 + 15
        pygame.draw.line(win, (255, 0, 0), [ys, xs], [ye, xe], 6)
    kek = True
    while kek:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            kek = False
        pygame.display.update()

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, weight):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            if maze[node_position[0]][node_position[1]] == 1:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            fl = 0
            for closed_child in closed_list:
                if child == closed_child:
                    fl = 1
            if fl == 1:
                continue
            child.g = current_node.g + weight[maze[child.position[0]][child.position[1]]]
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h
            fl = 0
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    fl = 1
            if fl == 1:
                continue
            open_list.append(child)

def calculate():
    start = (Sx - 1, Sy - 1)
    end = (Ex - 1, Ey - 1)
    a[Sx][Sy] = 0
    a[Ex][Ey] = 0
    weight = [1, None, 3, 5]
    k = []
    for i in range(Xx - 1):
        k.append([0] * (Yy - 1))
    for i in range(1, Xx):
        for j in range(1, Yy):
            k[i-1][j-1] = a[i][j]
    path = astar(k, start, end, weight)
    drawAstar(path)
    print(path)
    a[Sx][Sy] = 4
    a[Ex][Ey] = 5

kh = 120
lk = 1230
button_delete = Button(250, 120, 130, 70, (255, 211, 155), (236, 74, 180), (255, 164, 255), delete, 'delete')
button_select_s = Button(lk, 280, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), start, 'start')
button_select_e = Button(lk, 330, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), esc, 'esc')
button_select_y = Button(lk, 30, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), field, 'field')
button_select_b = Button(lk, 80, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), mountain, 'mountain')
button_select_g = Button(lk, 130, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), forest, 'forest')
button_select_l = Button(lk, 180, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), water, 'water')
button_calculate = Button(lk, 230, kh, 30, (255, 211, 155), (236, 74, 180), (255, 164, 255), calculate, 'calculate')


def menu():
    kek = True
    while kek:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            kek = False
        drawWindow()
        win.blit(men, (0, 0))
        button_delete.draw()
        pygame.display.update()


drawWindow()
menu()
run = True
fl = False
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        fl = False
        menu()
    if keys[pygame.K_n]:
        fl = True
    if keys[pygame.K_m]:
        fl = False
    if fl or keys[pygame.K_SPACE]:
        recountMas()
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0] and (pos[0] < 1200):
        if (na_active != 4) and (na_active != 5):
            x = ((pos[1] - 1) // Cage_Size) + 1
            y = ((pos[0] - 1) // Cage_Size) + 1
            if ((x != Sx) or (y != Sy)) and ((x != Ex) or (y != Ey)):
                a[x][y] = na_active
        if na_active == 4:
            x = ((pos[1] - 1) // Cage_Size) + 1
            y = ((pos[0] - 1) // Cage_Size) + 1
            if (x != Ex) or (y != Ey):
                a[Sx][Sy] = 0
                Sx = x
                Sy = y
                a[Sx][Sy] = na_active
        if na_active == 5:
            x = ((pos[1] - 1) // Cage_Size) + 1
            y = ((pos[0] - 1) // Cage_Size) + 1
            if (x != Sx) or (y != Sy):
                a[Ex][Ey] = 0
                Ex = x
                Ey = y
                a[Ex][Ey] = na_active
    drawWindow()
    button_select_y.draw()
    button_select_b.draw()
    button_select_g.draw()
    button_select_l.draw()
    button_select_s.draw()
    button_select_e.draw()
    button_calculate.draw()
    pygame.display.update()
pygame.quit()
