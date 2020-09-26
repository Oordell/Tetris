#!/usr/bin/env python3

import pygame as py
from constants import *

class TetrisUI(object):
    '''
        This class creates a UI for the Tetris game.
    '''
    ############## Constants ##############
    # Window size:
    SCREEN_WIDTH            = 400
    SCREEN_HEIGHT           = 300

    # Playing field.
    SIZE_OF_SQUARE          = 10
    NUM_OF_SQUARES_ROWS     = 20
    NUM_OF_SQUARES_COLUMS   = 10

    # Colors:
    COLOR_BACKGROUND        = (80, 80, 80)
    #######################################

    def __init__(self):
        self.init_new_game()

    def init_new_game(self):
        py.init()
        py.display.set_caption("Tetris")
        self.screen = py.display
        self.screen_surface = self.screen.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.fps = 25

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
    T.run()
