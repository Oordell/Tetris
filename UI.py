#!/usr/bin/env python3

import pygame as py
from constants import *

class TetrisUI(object):
    '''
        This class creates a UI for the Tetris game.
    '''
    ############## Constants ##############
    # Window size:
    SCREEN_WIDTH            = 1000
    SCREEN_HEIGHT           = 800

    # Playing field.
    SIZE_OF_SQUARE          = 35
    NUM_OF_SQUARES_ROWS     = 20
    NUM_OF_SQUARES_COLUMS   = 10
    # [ y, x ]
    POS_SQUARES_TOP_LEFT     = [(SCREEN_HEIGHT / 2) - (SIZE_OF_SQUARE * (int(NUM_OF_SQUARES_ROWS / 2))),
                               (SCREEN_WIDTH / 2) - (SIZE_OF_SQUARE * (int(NUM_OF_SQUARES_COLUMS / 2)))]
    POS_SQUARES_BUTTOM_RIGHT = [(SCREEN_HEIGHT / 2) + (SIZE_OF_SQUARE * (int(NUM_OF_SQUARES_ROWS / 2))),
                               (SCREEN_WIDTH / 2) + (SIZE_OF_SQUARE * (int(NUM_OF_SQUARES_COLUMS / 2)))]

    LINE_WIDTH              = 2

    # Colors:
    COLOR_BACKGROUND        = (20, 20, 20)
    COLOR_GRID_BG           = (40, 40, 40)
    COLOR_GRID_LINES        = (100, 100, 100)
    #######################################

    def __init__(self):
        self.init_new_game()

    def init_new_game(self):
        # Initialize PyGame:
        py.init()
        py.display.set_caption("Tetris")
        self.screen = py.display
        self.screen_surface = self.screen.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.fps = 25

        # Draw background:
        self.screen_surface.fill(self.COLOR_BACKGROUND)
        # Draw playing field background:
        py.draw.rect(self.screen_surface,
                    self.COLOR_GRID_BG,
                    (self.POS_SQUARES_TOP_LEFT[1], self.POS_SQUARES_TOP_LEFT[0], 
                    self.SIZE_OF_SQUARE * self.NUM_OF_SQUARES_COLUMS, self.SIZE_OF_SQUARE * self.NUM_OF_SQUARES_ROWS))

        self.draw_grid()

    def draw_grid(self):
        for col in range(0, self.NUM_OF_SQUARES_COLUMS + 1):
            py.draw.line(self.screen_surface, 
                        self.COLOR_GRID_LINES, 
                        (self.POS_SQUARES_TOP_LEFT[1] + (col * self.SIZE_OF_SQUARE), self.POS_SQUARES_TOP_LEFT[0]),
                        (self.POS_SQUARES_TOP_LEFT[1] + (col * self.SIZE_OF_SQUARE), self.POS_SQUARES_BUTTOM_RIGHT[0]),
                        self.LINE_WIDTH)
        for row in range(0, self.NUM_OF_SQUARES_ROWS + 1):
            py.draw.line(self.screen_surface, 
                        self.COLOR_GRID_LINES, 
                        (self.POS_SQUARES_TOP_LEFT[1], self.POS_SQUARES_TOP_LEFT[0] + (row * self.SIZE_OF_SQUARE)),
                        (self.POS_SQUARES_BUTTOM_RIGHT[1], self.POS_SQUARES_TOP_LEFT[0] + (row * self.SIZE_OF_SQUARE)),
                        self.LINE_WIDTH)

    def update_display(self):
        py.display.update()
        self.clock.tick(self.fps)

    def run(self):
        while True:
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        quit()
            self.update_display()

if __name__ == '__main__':
    print('Running Tetris UI file..')
    T = TetrisUI()
    print(T.POS_SQUARES_TOP_LEFT)
    print(T.POS_SQUARES_BUTTOM_RIGHT)
    T.run()
