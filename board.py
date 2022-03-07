from plates import Plate
import random


class Board():
    def __init__(self, size, number_of_mines):
        self.board = None
        self.size = size
        self.PLATE_SIZE = 32
        self.number_of_mines = number_of_mines
        self.setBoard()

    def setBoard(self):
        self.board = []
        for row in range(self.size[0]):
            a = []
            for col in range(self.size[1]):
                plate = Plate(17 + row * self.PLATE_SIZE, 92 + col * self.PLATE_SIZE)
                a.append(plate)
            self.board.append(a)

    def getSize(self):
        return self.size

    def getPlate(self, index):
        return self.board[index[0]][index[1]]

    def open_plates(self, i, j):
        for n in range(-1, 2):
            for k in range(-1, 2):
                if self.size[0] > n + i >= 0 and self.size[1] > k + j >= 0:
                    if not self.board[i + n][k + j].opened and not self.board[i + n][k + j].mine and not \
                            self.board[i + n][k + j].flag:
                        self.board[i + n][k + j].opened = True
                        if self.board[i + n][k + j].amount == 0:
                            self.open_plates(i + n, k + j)
                    if self.board[i + n][k + j].mine and not self.board[i + n][k + j].flag:
                        self.board[i + n][k + j].amount = 0
                        return False
        return True

    def spawn_mines(self, i, j):
        mines = self.number_of_mines
        while mines > 0:
            loc1 = random.randint(0, self.size[0] ** 2 - 1)
            loc2 = random.randint(0, self.size[1] ** 2 - 1)
            row = loc1 // self.size[0]
            col = loc2 % self.size[1]

            if self.check_mines(row, col) < 7 and not self.board[row][col].mine \
                    and not self.check_plate(row, col, i, j):
                self.board[row][col].mine = True
                mines -= 1

    def check_mines(self, i, j):
        mines = 0
        for n in range(-1, 2):
            for k in range(-1, 2):
                if self.size[0] > n + i >= 0 and self.size[1] > k + j >= 0:
                    if self.board[n + i][k + j].mine:
                        mines += 1
        return mines

    @staticmethod
    def check_plate(row, col, i, j):
        test = False
        for n in range(-1, 2):
            for k in range(-1, 2):
                if n + row == i and k + col == j:
                    test = True
        return test

    def check_flag(self, i, j):
        flag = 0
        for n in range(-1, 2):
            for k in range(-1, 2):
                if self.size[0] > n + i >= 0 and self.size[1] > k + j >= 0:
                    if self.board[n + i][k + j].flag:
                        flag += 1
        return flag

    def spawn_numbers(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if not self.board[i][j].mine:
                    self.board[i][j].amount = self.check_mines(i, j)

    def check_opened(self):
        a = self.size[0] * self.size[1]
        for i in range(self.size[0]):
            for plate in self.board[i]:
                if plate.opened or plate.mine:
                    a -= 1
        if a == 0:
            return True
        else:
            return False
