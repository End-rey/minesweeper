from gameloop import Game

BOARD_SIZE = (16, 16)
BOMBS = 40
WINDOW_SIZE = (34 + BOARD_SIZE[0] * 32, 109 + BOARD_SIZE[1] * 32)
game = Game(WINDOW_SIZE, BOARD_SIZE, BOMBS)
