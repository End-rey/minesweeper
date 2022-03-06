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
main_font = pygame.font.SysFont("comicsansms", 40)

shrek = [pygame.image.load("./sprites/shrek.png"), pygame.image.load("./sprites/pressed_shrek.png"),
         pygame.image.load("./sprites/died_shrek.png"), pygame.image.load("./sprites/pressed_died_shrek.png")]

plates = []
timer = 0
click = 0
count = 10


class Plate:
    plate_image = [pygame.image.load("./sprites/plate.png"),
                   pygame.image.load("./sprites/flag.png")]
    mines = [pygame.image.load("./sprites/mine.png"), pygame.image.load("./sprites/bomb_exploded.png")]
    numbers = [pygame.image.load("./sprites/opened.png")]
    for i in range(1, 7):
        numbers.append(pygame.image.load(f"./sprites/{i}.png"))

    def __init__(self, x, y):
        self.clicked = False
        self.amount = 1
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
            if self.mine and self.amount == 1:
                screen.blit(self.mines[0], (self.x, self.y))
            elif self.mine and self.amount == 0:
                screen.blit(self.mines[1], (self.x, self.y))
            else:
                screen.blit(self.numbers[self.amount], (self.x, self.y))


def draw_text(text, font_rect, color, surface, x, y):
    text_obj = font_rect.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


def draw_window(clik):
    screen.blit(bg, (0, 0))

    reload = pygame.Rect(138, 26, 45, 45)
    screen.blit(shrek[0], (138, 26))
    time = pygame.Rect(138, 26, 45, 45)
    draw_text(str(timer // 16), main_font, "red", screen, 270, 45)
    draw_text(str(count), main_font, "red", screen, 35, 45)

    mx, my = pygame.mouse.get_pos()

    if reload.collidepoint(mx, my):
        screen.blit(shrek[1], (138, 26))
        if clik:
            game(False)

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
                if plates[i + l][k + j].mine and not plates[i + l][k + j].flag:
                    plates[i + l][k + j].amount = 0
                    death()


def check_opened():
    a = 81
    for i in range(9):
        for plate in plates[i]:
            if plate.opened or plate.mine:
                a -= 1
    if a == 0:
        return True
    else:
        return False


def events():
    global click, count
    reload = pygame.Rect(138, 26, 45, 45)

    mx, my = pygame.mouse.get_pos()

    clik = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_p:
                game(True)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clik = True
                for i in range(9):
                    for j in range(9):
                        if plates[i][j].x <= mx < plates[i][j].x + PLATE_SIZE and plates[i][j].y <= my <= plates[i][
                            j].y + PLATE_SIZE:
                            click += 1
                            if not plates[i][j].opened and not plates[i][j].flag:
                                plates[i][j].opened = True
                                if plates[i][j].amount == 0:
                                    open_plates(i, j)
                            elif plates[i][j].flag:
                                plates[i][j].flag = False
                                count += 1
                            if plates[i][j].opened:
                                if plates[i][j].mine:
                                    plates[i][j].amount = 0
                                    death()
                                else:
                                    if check_mines(i, j) == 0 or check_flag(i, j) >= plates[i][j].amount:
                                        open_plates(i, j)
                # if reload.collidepoint((mx, my)):
                #     game(False)
            elif event.button == 3:
                for i in range(9):
                    for plate in plates[i]:
                        if plate.x <= mx < plate.x + PLATE_SIZE and plate.y <= my <= plate.y + PLATE_SIZE:
                            if not plate.opened and not plate.flag:
                                plate.flag = True
                                count -= 1
    if check_opened():
        draw_window(clik)
        win()
    return clik


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


def secret_spawn():
    for i in range(1, 9):
        if i == 1:
            plates[1][i].mine = True
            plates[2][i].mine = True
            plates[6][i].mine = True
            plates[7][i].mine = True
        elif i == 2:
            plates[0][i].mine = True
            plates[3][i].mine = True
            plates[5][i].mine = True
            plates[8][i].mine = True
        elif i == 3:
            plates[0][i].mine = True
            plates[4][i].mine = True
            plates[8][i].mine = True
        elif i == 4:
            plates[0][i].mine = True
            plates[8][i].mine = True
        elif i == 5:
            plates[1][i].mine = True
            plates[7][i].mine = True
        elif i == 6:
            plates[2][i].mine = True
            plates[6][i].mine = True
        elif i == 7:
            plates[3][i].mine = True
            plates[5][i].mine = True
        elif i == 8:
            plates[4][i].mine = True


def spawn_mines2():
    mines = 10
    while mines > 0:
        loc = random.randint(0, 80)
        row = loc // 9
        col = loc % 9

        if check_mines(row, col) < 7 and not plates[row][col].mine:
            plates[row][col].mine = True
            mines -= 1


def spawn_mines():
    mines = 10
    for i in range(9):
        for j in range(9):
            if check_mines(i, j) < 7 and mines > 0:
                if random.randint(0, 6) == 1:
                    plates[i][j].mine = True
                    mines -= 1


def spawn_numbers():
    for i in range(9):
        for j in range(9):
            if not plates[i][j].mine:
                plates[i][j].amount = check_mines(i, j)


def initial(secret):
    global plates
    plates = []
    for i in range(9):
        a = []
        for j in range(9):
            a.append(Plate(17 + i * PLATE_SIZE, 92 + j * PLATE_SIZE))
        plates.append(a)
    if secret:
        secret_spawn()
        spawn_numbers()
    else:
        spawn_mines2()
        spawn_numbers()


def standard_event(clik):
    clik = False
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
                clik = True
    return clik


def win():
    clik = False
    while True:
        clock.tick(60)
        pygame.time.delay(60)

        reload = pygame.Rect(138, 26, 45, 45)
        draw_text('You win!', main_font, (255, 255, 255),
                  screen, WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
        screen.blit(shrek[0], (138, 26))

        mx, my = pygame.mouse.get_pos()

        if reload.collidepoint(mx, my):
            screen.blit(shrek[1], (138, 26))
            if clik:
                game(False)

        clik = standard_event(clik)

        pygame.display.update()


def death():
    clik = False
    for i in range(9):
        for plate in plates[i]:
            if plate.mine:
                plate.opened = True
    while True:
        clock.tick(60)
        pygame.time.delay(60)

        reload = pygame.Rect(138, 26, 45, 45)
        screen.blit(shrek[2], (138, 26))

        mx, my = pygame.mouse.get_pos()

        if reload.collidepoint(mx, my):
            screen.blit(shrek[3], (138, 26))
            if clik:
                game(False)

        clik = standard_event(clik)

        for i in range(9):
            for plate in plates[i]:
                plate.draw_plate()
        pygame.display.update()


def game(secret):
    global timer, click, count
    timer = 0
    click = 0
    count = 10
    initial(secret)
    while True:
        clock.tick(30)
        pygame.time.delay(60)

        if click >= 1:
            timer += 1

        clik = events()

        draw_window(clik)


if __name__ == '__main__':
    game(False)
