# Setup Python
import random
import sys
import pygame

# Setup pygame
clock = pygame.time.Clock()
pygame.init()

icon = pygame.image.load("./sprites/icon.png")
WINDOW_SIZE = [322, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Minesweeper')
pygame.display.set_icon(icon)
bg = pygame.image.load("./sprites/bg.png")
PLATE_SIZE = 32


class Plate:
    plate_image = [pygame.image.load("./sprites/plate.png"),
                   pygame.image.load("./sprites/flag.png")]
    mines = pygame.image.load("./sprites/mine.png")
    numbers = [pygame.image.load("./sprites/opened.png")]
    for i in range(1, 7):
        numbers.append(pygame.image.load(f"./sprites/{i}.png"))

    def __init__(self, x, y):
        self.clicked = False
        self.amount = 0
        self.mine = False
        self.opened = False
        self.flag = False
        self.x = x
        self.y = y

    def draw_plate(self):
        if not self.opened and not self.flag:
            screen.blit(self.plate_image[0], (self.x, self.y))
        elif self.flag:
            screen.blit(self.plate_image[1], (self.x, self.y))
        if self.opened:
            if self.mine:
                screen.blit(self.mines, (self.x, self.y))
            else:
                screen.blit(self.numbers[self.amount], (self.x, self.y))


def draw_window():
    screen.blit(bg, (0, 0))

    reload = pygame.Rect(138, 26, 45, 45)
    pygame.draw.rect(screen, "red", reload)

    for i in range(9):
        for plate in plates[i]:
            plate.draw_plate()

    pygame.display.update()


def open_plates(i, j):
    for l in range(-1, 2):
        for k in range(-1, 2):
            if 9 > l + i >= 0 and 9 > k + j >= 0:
                if not plates[i + l][k + j].opened and not plates[i + l][k + j].mine and not plates[i + l][k + j].flag:
                    plates[i + l][k + j].opened = True
                    if plates[i + l][k + j].amount == 0:
                        open_plates(i + l, k + j)
                    # if plates[i + l][k + l].mine:
                    #     death()


def events(event):
    reload = pygame.Rect(138, 26, 45, 45)

    mx, my = pygame.mouse.get_pos()

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for i in range(9):
                for j in range(9):
                    if plates[i][j].x <= mx < plates[i][j].x + PLATE_SIZE and plates[i][j].y <= my <= plates[i][
                        j].y + PLATE_SIZE:
                        if not plates[i][j].opened and not plates[i][j].flag:
                            plates[i][j].opened = True
                            if plates[i][j].amount == 0:
                                open_plates(i, j)
                        elif plates[i][j].flag:
                            plates[i][j].flag = False
                        if plates[i][j].opened:
                            if plates[i][j].mine:
                                death()
                            else:
                                if check_mines(i, j) == 0 or check_flag(i, j) >= plates[i][j].amount:
                                    open_plates(i, j)
            if reload.collidepoint((mx, my)):
                game()
        elif event.button == 3:
            for i in range(9):
                for plate in plates[i]:
                    if plate.x <= mx < plate.x + PLATE_SIZE and plate.y <= my <= plate.y + PLATE_SIZE:
                        if not plate.opened and not plate.flag:
                            plate.flag = True


def check_mines(i, j):
    mines = 0
    for l in range(-1, 2):
        for k in range(-1, 2):
            if 9 > l + i >= 0 and 9 > k + j >= 0:
                if plates[l + i][k + j].mine:
                    mines += 1
    return mines


def check_flag(i, j):
    flag = 0
    for l in range(-1, 2):
        for k in range(-1, 2):
            if 9 > l + i >= 0 and 9 > k + j >= 0:
                if plates[l + i][k + j].flag:
                    flag += 1
    return flag


def spawn_mines():
    mines = 10
    for i in range(9):
        for j in range(9):
            if check_mines(i, j) < 7 and mines > 0:
                if random.randint(0, 5) == 1:
                    plates[i][j].mine = True
                    mines -= 1


def spawn_numbers():
    for i in range(9):
        for j in range(9):
            plates[i][j].amount = check_mines(i, j)


plates = []


def initial():
    global plates
    plates = []
    for i in range(9):
        a = []
        for j in range(9):
            a.append(Plate(17 + i * PLATE_SIZE, 92 + j * PLATE_SIZE))
        plates.append(a)
    spawn_mines()
    spawn_numbers()


def death():
    for i in range(9):
        for plate in plates[i]:
            if plate.mine:
                plate.opened = True
    while True:
        clock.tick(60)
        pygame.time.delay(60)

        reload = pygame.Rect(138, 26, 45, 45)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if reload.collidepoint((mx, my)):
                        game()

        draw_window()


def game():
    initial()
    while True:
        clock.tick(60)
        pygame.time.delay(60)

        for event in pygame.event.get():
            events(event)

        draw_window()


if __name__ == '__main__':
    game()
