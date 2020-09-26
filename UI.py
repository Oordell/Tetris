#!/usr/bin/env python3

import pygame as py
from constants import *
from time import time
from grid_square import GridSquare
from dataclasses import dataclass
import random as rand

#@dataclass
#class TetrisPeice:
#    id: int
#    color: tuple
#    shape_id: int

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
    
    # Line width for grid:
    LINE_WIDTH              = 2

    # Colors:
    COLOR_BACKGROUND        = (20, 20, 20)
    COLOR_GRID_BG           = (40, 40, 40)
    COLOR_GRID_LINES        = (100, 100, 100)
    COLOR_PEICE_L           = (250, 150, 10)
    COLOR_PEICE_J           = (10, 10, 250)
    COLOR_PEICE_5           = (10, 250, 10)
    COLOR_PEICE_Z           = (250, 10, 10)
    COLOR_PEICE_T           = (250, 10, 250)
    COLOR_PEICE_I           = (10, 250, 250)
    COLOR_PEICE_O           = (250, 250, 10)
    COLOR_PEICES            = [COLOR_PEICE_L, COLOR_PEICE_J, COLOR_PEICE_5, COLOR_PEICE_Z, COLOR_PEICE_T, COLOR_PEICE_I, COLOR_PEICE_O]

    FALL_SPEED_UPDATE_SEC   = 20
    FALL_SPEED_INIT         = float(0.5)
    FALL_SPEED_FREQ_INC     = float(0.2)

    # Peices:
    NUM_OF_SHAPES           = 7
    SHAPE_ID                = [0, 1, 2, 3, 4, 5, 6]    # [L, J, 5, Z, T, |, 0]
    #######################################

    def __init__(self):
        self.game_grid = []

        self.current_peice_id = -1
        self.current_peice_rotation_center = (0, 0)

        self.fall_freq = self.FALL_SPEED_INIT
        self.timer_fall_freq_start = time()
        self.timer_fall_freq_end = time()
        self.timer_peice_fall_start = time()
        self.timer_peice_fall_end = time()

        self.init_new_game()

    def init_new_game(self):
        for row in range(0, self.NUM_OF_SQUARES_ROWS):
            temp_row = []
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):        
                temp_row.append(GridSquare(row, col, self.COLOR_GRID_BG, True))
            self.game_grid.append(temp_row)

        # Initialize PyGame:
        py.init()
        py.display.set_caption("Tetris")
        self.screen = py.display
        self.screen_surface = self.screen.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.fps = 25

        # Draw background:
        self.screen_surface.fill(self.COLOR_BACKGROUND)
        self.new_current_peice()
        self.draw_whole_playing_field()

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
    
    def draw_whole_playing_field(self):
        for row in range(0, self.NUM_OF_SQUARES_ROWS):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                py.draw.rect(self.screen_surface, self.game_grid[row][col].color,
                    (self.POS_SQUARES_TOP_LEFT[1] + self.SIZE_OF_SQUARE * col, 
                    self.POS_SQUARES_TOP_LEFT[0] + self.SIZE_OF_SQUARE * row, 
                    self.SIZE_OF_SQUARE, self.SIZE_OF_SQUARE))
        self.draw_grid()

    def new_current_peice(self):
        shape = rand.randint(0, self.NUM_OF_SHAPES - 1)
        self.current_peice_id += 1
        # shape = self.current_peice_id - (int(self.current_peice_id / self.NUM_OF_SHAPES) * self.NUM_OF_SHAPES)
        self.place_new_peice(shape)

    def place_new_peice(self, shape_id):
        # [0, 1, 2, 3, 4, 5, 6]
        # [L, J, 5, Z, T, |, O]
        if shape_id == 0:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[2][4] = GridSquare(2, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[2][5] = GridSquare(2, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (1, 4)
        elif shape_id == 1:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[2][4] = GridSquare(2, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[2][3] = GridSquare(2, 3, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (1, 4)
        elif shape_id == 2:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[0][5] = GridSquare(0, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][3] = GridSquare(1, 3, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (1, 4)
        elif shape_id == 3:
            self.game_grid[0][3] = GridSquare(0, 3, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (1, 4)
        elif shape_id == 4:
            self.game_grid[1][3] = GridSquare(1, 3, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (1, 4)
        elif shape_id == 5:
            self.game_grid[1][3] = GridSquare(1, 3, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][6] = GridSquare(1, 6, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (1.5, 4.5)
        elif shape_id == 6:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[0][5] = GridSquare(0, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PEICES[shape_id], False, self.current_peice_id)
            self.current_peice_rotation_center = (0.5, 4.5)
        else:
            print('Error: shape_id is incorrect')

    def is_collision_down_at_next_time_step(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 1, -1, -1):
                if self.game_grid[row][col].peice_id == self.current_peice_id:
                    if row == self.NUM_OF_SQUARES_ROWS - 1:
                        return True
                    elif not self.game_grid[row + 1][col].peice_id == -1 and not self.game_grid[row + 1][col].peice_id == self.current_peice_id:
                        return True
        return False

    def is_collision_left(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                if self.game_grid[row][col].peice_id == self.current_peice_id:
                    if col == 0:
                        return True
                    elif not self.game_grid[row][col - 1].empty and not self.game_grid[row][col - 1].peice_id == self.current_peice_id:
                        return True
        return False

    def is_collision_right(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 1, -1, -1):
                if self.game_grid[row][col].peice_id == self.current_peice_id:
                    if col == self.NUM_OF_SQUARES_COLUMS - 1:
                        return True
                    elif not self.game_grid[row][col + 1].empty and not self.game_grid[row][col + 1].peice_id == self.current_peice_id:
                        return True
        return False

    def move_current_piece_one_down(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 2, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 1, -1, -1):
                if self.game_grid[row][col].peice_id == self.current_peice_id:
                    if self.game_grid[row + 1][col].empty:
                        self.game_grid[row + 1][col].empty = False
                        self.game_grid[row + 1][col].color = self.game_grid[row][col].color
                        self.game_grid[row + 1][col].peice_id = self.current_peice_id
                        self.game_grid[row][col].empty = True
                        self.game_grid[row][col].color = self.COLOR_GRID_BG
                        self.game_grid[row][col].peice_id = -1
        self.current_peice_rotation_center = (self.current_peice_rotation_center[0] + 1, self.current_peice_rotation_center[1])

    def move_current_piece_one_left(self):
        if self.is_collision_left():
            return
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(1, self.NUM_OF_SQUARES_COLUMS):
                if self.game_grid[row][col].peice_id == self.current_peice_id:
                    if self.game_grid[row][col - 1].empty:
                        self.game_grid[row][col - 1].empty = False
                        self.game_grid[row][col - 1].color = self.game_grid[row][col].color
                        self.game_grid[row][col - 1].peice_id = self.current_peice_id
                        self.game_grid[row][col].empty = True
                        self.game_grid[row][col].color = self.COLOR_GRID_BG
                        self.game_grid[row][col].peice_id = -1
        self.current_peice_rotation_center = (self.current_peice_rotation_center[0], self.current_peice_rotation_center[1] - 1)

    def move_current_piece_one_right(self):
        if self.is_collision_right():
            return
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 2, -1, -1):
                if self.game_grid[row][col].peice_id == self.current_peice_id:
                    if self.game_grid[row][col + 1].empty:
                        self.game_grid[row][col + 1].empty = False
                        self.game_grid[row][col + 1].color = self.game_grid[row][col].color
                        self.game_grid[row][col + 1].peice_id = self.current_peice_id
                        self.game_grid[row][col].empty = True
                        self.game_grid[row][col].color = self.COLOR_GRID_BG
                        self.game_grid[row][col].peice_id = -1
        self.current_peice_rotation_center = (self.current_peice_rotation_center[0], self.current_peice_rotation_center[1] + 1)

    def drop_current_peice_to_bottom(self):
        while not self.is_collision_down_at_next_time_step():
            self.move_current_piece_one_down()
        self.new_current_peice()

    def rotate_peice(self):
        pass

    def update_timers(self):
        self.timer_peice_fall_end = time()
        if self.timer_peice_fall_end - self.timer_peice_fall_start > float(1 / self.fall_freq):
            self.timer_peice_fall_start = time()
            if not self.is_collision_down_at_next_time_step():
                self.move_current_piece_one_down()
            else:
                self.new_current_peice()
            print(self.current_peice_rotation_center)
        
        self.timer_fall_freq_end = time()
        if self.timer_fall_freq_end - self.timer_fall_freq_start > self.FALL_SPEED_UPDATE_SEC:
            self.timer_fall_freq_start = time()
            self.fall_freq += self.FALL_SPEED_FREQ_INC
            print('Speed updated.')

    def update_display(self):
        self.draw_whole_playing_field()
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
                    if event.key == py.K_SPACE:
                        self.drop_current_peice_to_bottom()
                    if event.key == py.K_DOWN:
                        if not self.is_collision_down_at_next_time_step():
                            self.move_current_piece_one_down()
                    if event.key == py.K_LEFT:
                        self.move_current_piece_one_left()
                    if event.key == py.K_RIGHT:
                        self.move_current_piece_one_right()
                    if event.key == py.K_UP:
                        self.rotate_peice()

            self.update_timers()
            self.update_display()

    def print_map(self):
        for row in range(0, self.NUM_OF_SQUARES_ROWS):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                print(int(self.game_grid[row][col].peice_id), end='')
            print('')

if __name__ == '__main__':
    print('Running Tetris UI file..')
    T = TetrisUI()
    print(T.POS_SQUARES_TOP_LEFT)
    print(T.POS_SQUARES_BUTTOM_RIGHT)
    T.run()
