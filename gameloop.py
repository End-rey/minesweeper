import sys

import pygame
from board import Board


class Game():
    def __init__(self, size, board_size, number_mines, level):
        self.main_font = None
        self.level = level
        self.click = 0
        self.board = Board(board_size, number_mines)
        self.number_mines = number_mines
        self.WINDOW_SIZE = size
        self.PLATE_SIZE = 32
        self.images = {}
        self.load_image()
        self.run()

    def run(self):
        clock = pygame.time.Clock()
        pygame.init()
        screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('Minesweeper')
        pygame.display.set_icon(self.images["icon"])
        self.main_font = pygame.font.SysFont("comicsansms", 40)
        # self.board.spawn_mines(0, 0)
        # self.board.spawn_numbers()
        running = True
        while running:
            self.events(screen)

    @staticmethod
    def draw_text(text, font_rect, color, surface, x, y):
        text_obj = font_rect.render(text, 1, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    def load_image(self):
        self.images.update({"icon": pygame.image.load("./sprites/icon.png")})
        self.images.update({"bg": [pygame.image.load("./sprites/bg.png"), pygame.image.load("./sprites/bg1.png"),
                                   pygame.image.load("./sprites/wall1.png"), pygame.image.load("./sprites/wall2.png"),
                                   pygame.image.load("./sprites/wall3.png")]})
        self.images.update({"corner": [pygame.image.load("./sprites/corner.png"),
                                       pygame.image.load("./sprites/corner2.png"),
                                       pygame.image.load("./sprites/corner3.png")]})
        self.images.update({"plate_image": [pygame.image.load("./sprites/plate.png"),
                                            pygame.image.load("./sprites/flag.png")]})
        self.images.update(
            {"mines": [pygame.image.load("./sprites/mine.png"), pygame.image.load("./sprites/bomb_exploded.png")]})
        self.images.update({"numbers": [pygame.image.load("./sprites/opened.png")]})
        for i in range(1, 7):
            self.images["numbers"].append(pygame.image.load(f"./sprites/{i}.png"))

        self.images.update(
            {"shrek": [pygame.image.load("./sprites/shrek.png"), pygame.image.load("./sprites/pressed_shrek.png"),
                       pygame.image.load("./sprites/died_shrek.png"),
                       pygame.image.load("./sprites/pressed_died_shrek.png")]})
        self.images.update(
            {"level": [pygame.image.load("./sprites/beginner.png"), pygame.image.load("./sprites/pressed_beginner.png"),
                       pygame.image.load("./sprites/intermediate.png"),
                       pygame.image.load("./sprites/pressed_intermediate.png"),
                       pygame.image.load("./sprites/expert.png"), pygame.image.load("./sprites/pressed_expert.png")]})

    def draw_bg(self, screen):
        screen.fill((191, 191, 191))
        screen.blit(self.images["bg"][1], (0, 0))
        screen.blit(self.images["bg"][4], (self.WINDOW_SIZE[0] - 17, 0))
        screen.blit(self.images["corner"][1], (self.WINDOW_SIZE[0] - 17, self.WINDOW_SIZE[1] - 17))
        screen.blit(self.images["corner"][2], (0, self.WINDOW_SIZE[1] - 17))
        for i in range(3, self.board.size[0]):
            screen.blit(self.images["bg"][3], (17 + i * self.PLATE_SIZE, 0))
            screen.blit(self.images["bg"][3], (17 + i * self.PLATE_SIZE, 75))

        for i in range(0, self.board.getSize()[0]):
            screen.blit(self.images["bg"][3], (17 + i * self.PLATE_SIZE, self.WINDOW_SIZE[1] - 17))

        for i in range(0, self.board.getSize()[1]):
            screen.blit(self.images["bg"][2], (0, 92 + i * self.PLATE_SIZE))
            screen.blit(self.images["bg"][2], (self.WINDOW_SIZE[0] - 17, 92 + i * self.PLATE_SIZE))

    def draw_plates(self, screen):
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                plate = self.board.getPlate((row, col))
                if not plate.opened and not plate.flag:
                    screen.blit(self.images["plate_image"][0], (plate.x, plate.y))
                elif plate.flag:
                    screen.blit(self.images["plate_image"][1], (plate.x, plate.y))
                if plate.opened:
                    if plate.mine and plate.amount == 1:
                        screen.blit(self.images["mines"][0], (plate.x, plate.y))
                    elif plate.mine and plate.amount == 0:
                        screen.blit(self.images["mines"][1], (plate.x, plate.y))
                    else:
                        screen.blit(self.images["numbers"][plate.amount], (plate.x, plate.y))

    def draw_button(self, screen, clik):
        reload = pygame.Rect(self.WINDOW_SIZE[0] / 2 - 45 / 2, 26, 45, 45)
        level_button = pygame.Rect(self.WINDOW_SIZE[0] / 2 - 45 - 45, 26, 45, 45)
        screen.blit(self.images["shrek"][0], (self.WINDOW_SIZE[0] / 2 - 45 / 2, 26))
        screen.blit(self.images["level"][self.level - 1], (self.WINDOW_SIZE[0] / 2 - 45 - 45, 26))

        mx, my = pygame.mouse.get_pos()

        if reload.collidepoint(mx, my):
            screen.blit(self.images["shrek"][1], (self.WINDOW_SIZE[0] / 2 - 45 / 2, 26))
            if clik:
                self.__init__(self.WINDOW_SIZE, self.board.getSize(), self.number_mines, self.level)

        if level_button.collidepoint(mx, my):
            screen.blit(self.images["level"][self.level], (self.WINDOW_SIZE[0] / 2 - 45 - 45, 26))
            if clik:
                self.level += 2
                if self.level > 5:
                    self.level = 1
                if self.level == 1:
                    board_size = (9, 9)
                    bombs = 10
                    window_size = (34 + board_size[0] * 32, 109 + board_size[1] * 32)
                    self.__init__(window_size, board_size, bombs, self.level)
                elif self.level == 3:
                    board_size = (16, 16)
                    bombs = 40
                    window_size = (34 + board_size[0] * 32, 109 + board_size[1] * 32)
                    self.__init__(window_size, board_size, bombs, self.level)
                elif self.level == 5:
                    board_size = (30, 16)
                    bombs = 99
                    window_size = (34 + board_size[0] * 32, 109 + board_size[1] * 32)
                    self.__init__(window_size, board_size, bombs, self.level)

    def draw(self, screen, clik):
        self.draw_bg(screen)
        self.draw_plates(screen)

        self.draw_text(str(self.board.number_of_mines), self.main_font, "red", screen, 40, 45)

        self.draw_button(screen, clik)

        pygame.display.flip()

    def main_menu(self, screen):
        pass

    def events(self, screen):
        reload = pygame.Rect(138, 26, 45, 45)

        mx, my = pygame.mouse.get_pos()

        clik = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()
                if event.key == pygame.K_p:
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clik = True
                    for i in range(self.board.size[0]):
                        for j in range(self.board.size[1]):
                            if self.board.getPlate([i, j]).x <= mx < self.board.getPlate([i, j]).x + self.PLATE_SIZE \
                                    and self.board.getPlate([i, j]).y <= my <= \
                                    self.board.getPlate([i, j]).y + self.PLATE_SIZE:
                                self.click += 1
                                if self.click == 1:
                                    self.board.spawn_mines(i, j)
                                    self.board.spawn_numbers()
                                if not self.board.getPlate([i, j]).opened and not self.board.getPlate([i, j]).flag:
                                    self.board.getPlate([i, j]).opened = True
                                    if self.board.getPlate([i, j]).amount == 0:
                                        if not self.board.open_plates(i, j):
                                            self.death(screen)

                                if self.board.getPlate([i, j]).opened:
                                    if self.board.getPlate([i, j]).mine:
                                        self.board.getPlate([i, j]).amount = 0
                                        self.death(screen)
                                    else:
                                        if self.board.check_mines(i, j) == 0 or self.board.check_flag(i, j) >= \
                                                self.board.getPlate([i, j]).amount:
                                            if not self.board.open_plates(i, j):
                                                self.death(screen)
                elif event.button == 3:
                    for i in range(self.board.size[0]):
                        for plate in self.board.board[i]:
                            if plate.x <= mx < plate.x + self.PLATE_SIZE and plate.y <= my <= plate.y + self.PLATE_SIZE:
                                if not plate.opened and not plate.flag and self.board.number_of_mines > 0:
                                    plate.flag = True
                                    self.board.number_of_mines -= 1
                                elif plate.flag:
                                    plate.flag = False
                                    self.board.number_of_mines += 1
            self.draw(screen, clik)

        if self.board.check_opened():
            self.draw(screen, clik)
            self.win(screen)
        return clik

    def standard_event(self):
        clik = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clik = True
        return clik

    def death(self, screen):
        clik = False
        for row in range(self.board.getSize()[0]):
            for plate in self.board.board[row]:
                if plate.mine:
                    plate.opened = True
        while True:
            clik = self.standard_event()
            self.draw_plates(screen)
            self.draw_text(str(self.board.number_of_mines), self.main_font, "red", screen, 40, 45)
            self.draw_button(screen, clik)
            pygame.display.flip()

    def win(self, screen):
        clik = False
        while True:
            clik = self.standard_event()
            self.draw_text(str(self.board.number_of_mines), self.main_font, "red", screen, 40, 45)
            self.draw_button(screen, clik)
            self.draw_text('You win!', self.main_font, (255, 255, 255),
                           screen, self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2)
            pygame.display.flip()

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()
