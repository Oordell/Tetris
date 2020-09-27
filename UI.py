#!/usr/bin/env python3

import pygame as py
from constants import *
from time import time
from grid_square import *
from dataclasses import dataclass
import random as rand
import numpy as np
from math import cos, sin, pi

#@dataclass
#class TetrisPiece:
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

    # Text:
    FONT_SIZE_SMALL         = 10
    FONT_SIZE_NORMAL        = 20
    FONT_SIZE_LARGE         = 30

    # Colors:
    COLOR_BACKGROUND        = (20, 20, 20)
    COLOR_GRID_BG           = (50, 50, 50)
    COLOR_GRID_LINES        = (100, 100, 100)
    COLOR_PIECE_L           = (250, 150, 10)
    COLOR_PIECE_J           = (10, 10, 250)
    COLOR_PIECE_5           = (10, 250, 10)
    COLOR_PIECE_Z           = (250, 10, 10)
    COLOR_PIECE_T           = (250, 10, 250)
    COLOR_PIECE_I           = (10, 250, 250)
    COLOR_PIECE_O           = (250, 250, 10)
    COLOR_PIECES            = [COLOR_PIECE_L, COLOR_PIECE_J, COLOR_PIECE_5, COLOR_PIECE_Z, COLOR_PIECE_T, COLOR_PIECE_I, COLOR_PIECE_O]
    COLOR_TEXT              = (200, 200, 200)

    FALL_SPEED_UPDATE_SEC   = 20
    FALL_SPEED_INIT         = float(0.5)
    FALL_SPEED_FREQ_INC     = float(0.2)

    # Pieces:
    NUM_OF_SHAPES           = 7
    SHAPE_ID                = [0, 1, 2, 3, 4, 5, 6]    # [L, J, 5, Z, T, |, 0]
    #######################################

    def __init__(self):
        self.game_grid = []

        self.current_piece_id = -1
        self.current_piece_rotation_center = (0, 0)
        self.next_piece_shape_id = EMPTY_PIECE_ID

        self.num_of_lines_cleared = 0
        self.num_of_holes = 0
        self.max_height_of_stacked_pieces = 0

        self.fall_freq = self.FALL_SPEED_INIT
        self.timer_fall_freq_start = time()
        self.timer_fall_freq_end = time()
        self.timer_piece_fall_start = time()
        self.timer_piece_fall_end = time()

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
        self.next_piece_shape_id = rand.randint(0, self.NUM_OF_SHAPES - 1)
        self.new_current_piece()
        self.draw_whole_playing_field()
        self.draw_game_data()

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
    
    def draw_game_data(self):
        # Draw game data:
        box_width = 220
        box_height = 200
        top_off_set = 100

        center_left_column = (self.SCREEN_WIDTH / 2 - (self.SIZE_OF_SQUARE * self.NUM_OF_SQUARES_COLUMS) / 2) / 2
        center_right_column = self.SCREEN_WIDTH - center_left_column
        py.draw.rect(self.screen_surface, 
                    self.COLOR_GRID_BG, 
                    (center_left_column - (box_width / 2), top_off_set, box_width, box_height) )

        self.draw_next_piece(center_right_column, top_off_set, box_width, box_height)

        font = py.font.Font('freesansbold.ttf', self.FONT_SIZE_LARGE)
        text = font.render("Game stats", True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_left_column , top_off_set - 30)
        self.screen_surface.blit(text, text_rect)

        font = py.font.Font('freesansbold.ttf', self.FONT_SIZE_NORMAL)
        text = font.render("Lines Cleared: " + str(self.num_of_lines_cleared), True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_left_column , 150)
        self.screen_surface.blit(text, text_rect)

        text = font.render("Height: " + str(self.max_height_of_stacked_pieces), True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_left_column , 200)
        self.screen_surface.blit(text, text_rect)

        text = font.render("Holes: " + str(self.num_of_holes), True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_left_column , 250)
        self.screen_surface.blit(text, text_rect)

    def draw_next_piece(self, center_right_column, top_off_set, box_width, box_height):
        py.draw.rect(self.screen_surface, 
                    self.COLOR_GRID_BG, 
                    (center_right_column - (box_width / 2), top_off_set, box_width, box_height))

        font = py.font.Font('freesansbold.ttf', self.FONT_SIZE_LARGE)

        text = font.render("Next piece", True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_right_column , top_off_set - 30)
        self.screen_surface.blit(text, text_rect)

        
        mini_grid = [[EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID],
                     [EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID],
                     [EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID],
                     [EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID, EMPTY_PIECE_ID]]
        top_left = (center_right_column - self.SIZE_OF_SQUARE * 1.5 , top_off_set + (box_height / 2) - self.SIZE_OF_SQUARE * 1.5)
        # buttom_right = ()
        # [0, 1, 2, 3, 4, 5, 6]
        # [L, J, 5, Z, T, |, O]
        if self.next_piece_shape_id == 0:
            mini_grid[0][1] = 0
            mini_grid[1][1] = 0
            mini_grid[2][1] = 0
            mini_grid[2][2] = 0
        elif self.next_piece_shape_id == 1:
            mini_grid[0][1] = 1
            mini_grid[1][1] = 1
            mini_grid[2][1] = 1
            mini_grid[2][0] = 1
        elif self.next_piece_shape_id == 2:
            mini_grid[1][1] = 2
            mini_grid[1][2] = 2
            mini_grid[2][0] = 2
            mini_grid[2][1] = 2
        elif self.next_piece_shape_id == 3:
            mini_grid[1][0] = 3
            mini_grid[1][1] = 3
            mini_grid[2][1] = 3
            mini_grid[2][2] = 3
        elif self.next_piece_shape_id == 4:
            mini_grid[0][1] = 4
            mini_grid[1][0] = 4
            mini_grid[1][1] = 4
            mini_grid[1][2] = 4
        elif self.next_piece_shape_id == 5:
            top_left = (center_right_column - self.SIZE_OF_SQUARE * 2 , top_off_set + (box_height / 2) - self.SIZE_OF_SQUARE * 2)
            mini_grid[0][1] = 5
            mini_grid[1][1] = 5
            mini_grid[2][1] = 5
            mini_grid[3][1] = 5
        elif self.next_piece_shape_id == 6:
            top_left = (center_right_column - self.SIZE_OF_SQUARE * 2 , top_off_set + (box_height / 2) - self.SIZE_OF_SQUARE * 2)
            mini_grid[1][1] = 6
            mini_grid[1][2] = 6
            mini_grid[2][1] = 6
            mini_grid[2][2] = 6
        else:
            print('Error: shape_id is incorrect')
        
        for row in range(len(mini_grid)):
            for col in range(len(mini_grid)):
                if not mini_grid[row][col] == -1:
                    py.draw.rect(self.screen_surface, 
                                self.COLOR_PIECES[mini_grid[row][col]], 
                                (top_left[0] + col * self.SIZE_OF_SQUARE, top_left[1] + row * self.SIZE_OF_SQUARE, self.SIZE_OF_SQUARE, self.SIZE_OF_SQUARE))

    def draw_whole_playing_field(self):
        for row in range(0, self.NUM_OF_SQUARES_ROWS):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                py.draw.rect(self.screen_surface, self.game_grid[row][col].color,
                    (self.POS_SQUARES_TOP_LEFT[1] + self.SIZE_OF_SQUARE * col, 
                    self.POS_SQUARES_TOP_LEFT[0] + self.SIZE_OF_SQUARE * row, 
                    self.SIZE_OF_SQUARE, self.SIZE_OF_SQUARE))
        self.draw_grid()

    def new_current_piece(self):
        self.check_and_remove_full_lines()
        self.count_num_of_holes()
        self.count_max_height()
        current_shape_id = self.next_piece_shape_id
        self.next_piece_shape_id = rand.randint(0, self.NUM_OF_SHAPES - 1)
        self.current_piece_id += 1
        # shape = self.current_piece_id - (int(self.current_piece_id / self.NUM_OF_SHAPES) * self.NUM_OF_SHAPES)
        self.place_new_piece(current_shape_id)
        self.draw_game_data()

    def place_new_piece(self, shape_id):
        # [0, 1, 2, 3, 4, 5, 6]
        # [L, J, 5, Z, T, |, O]
        if shape_id == 0:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[2][4] = GridSquare(2, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[2][5] = GridSquare(2, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (1, 4)
        elif shape_id == 1:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[2][4] = GridSquare(2, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[2][3] = GridSquare(2, 3, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (1, 4)
        elif shape_id == 2:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[0][5] = GridSquare(0, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][3] = GridSquare(1, 3, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (1, 4)
        elif shape_id == 3:
            self.game_grid[0][3] = GridSquare(0, 3, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (1, 4)
        elif shape_id == 4:
            self.game_grid[1][3] = GridSquare(1, 3, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (1, 4)
        elif shape_id == 5:
            self.game_grid[1][3] = GridSquare(1, 3, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][6] = GridSquare(1, 6, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (1.5, 4.5)
        elif shape_id == 6:
            self.game_grid[0][4] = GridSquare(0, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][4] = GridSquare(1, 4, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[0][5] = GridSquare(0, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.game_grid[1][5] = GridSquare(1, 5, self.COLOR_PIECES[shape_id], False, self.current_piece_id)
            self.current_piece_rotation_center = (0.5, 4.5)
        else:
            print('Error: shape_id is incorrect')

    def count_num_of_holes(self):
        self.num_of_holes = 0
        for col in range(0, self.NUM_OF_SQUARES_COLUMS):
            is_block_in_column = False
            for row in range(0, self.NUM_OF_SQUARES_ROWS):
                if not self.game_grid[row][col].empty: # and not self.game_grid[row][col].piece_id == self.current_piece_id:
                    is_block_in_column = True
                if is_block_in_column and self.game_grid[row][col].empty:
                    self.num_of_holes += 1

    def count_max_height(self):
        self.max_height_of_stacked_pieces = 0
        height = 0
        for col in range(0, self.NUM_OF_SQUARES_COLUMS):
            for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
                if not self.game_grid[row][col].empty: # and not self.game_grid[row][col].piece_id == self.current_piece_id:
                    height = row * (-1) + self.NUM_OF_SQUARES_ROWS
            if self.max_height_of_stacked_pieces < height:
                self.max_height_of_stacked_pieces = height

    def is_collision_down_at_next_time_step(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 1, -1, -1):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    if row == self.NUM_OF_SQUARES_ROWS - 1:
                        return True
                    elif not self.game_grid[row + 1][col].empty and not self.game_grid[row + 1][col].piece_id == self.current_piece_id:
                        return True
        return False

    def is_collision_left(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    if col == 0:
                        return True
                    elif not self.game_grid[row][col - 1].empty and not self.game_grid[row][col - 1].piece_id == self.current_piece_id:
                        return True
        return False

    def is_collision_right(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 1, -1, -1):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    if col == self.NUM_OF_SQUARES_COLUMS - 1:
                        return True
                    elif not self.game_grid[row][col + 1].empty and not self.game_grid[row][col + 1].piece_id == self.current_piece_id:
                        return True
        return False

    def move_current_piece_one_down(self):
        for row in range(self.NUM_OF_SQUARES_ROWS - 2, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 1, -1, -1):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    if self.game_grid[row + 1][col].empty:
                        self.game_grid[row + 1][col].empty = False
                        self.game_grid[row + 1][col].color = self.game_grid[row][col].color
                        self.game_grid[row + 1][col].piece_id = self.current_piece_id
                        self.game_grid[row][col].empty = True
                        self.game_grid[row][col].color = self.COLOR_GRID_BG
                        self.game_grid[row][col].piece_id = EMPTY_PIECE_ID
        self.current_piece_rotation_center = (self.current_piece_rotation_center[0] + 1, self.current_piece_rotation_center[1])

    def move_current_piece_one_left(self):
        if self.is_collision_left():
            return
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(1, self.NUM_OF_SQUARES_COLUMS):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    if self.game_grid[row][col - 1].empty:
                        self.game_grid[row][col - 1].empty = False
                        self.game_grid[row][col - 1].color = self.game_grid[row][col].color
                        self.game_grid[row][col - 1].piece_id = self.current_piece_id
                        self.game_grid[row][col].empty = True
                        self.game_grid[row][col].color = self.COLOR_GRID_BG
                        self.game_grid[row][col].piece_id = EMPTY_PIECE_ID
        self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] - 1)

    def move_current_piece_one_right(self):
        if self.is_collision_right():
            return
        for row in range(self.NUM_OF_SQUARES_ROWS - 1, -1, -1):
            for col in range(self.NUM_OF_SQUARES_COLUMS - 2, -1, -1):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    if self.game_grid[row][col + 1].empty:
                        self.game_grid[row][col + 1].empty = False
                        self.game_grid[row][col + 1].color = self.game_grid[row][col].color
                        self.game_grid[row][col + 1].piece_id = self.current_piece_id
                        self.game_grid[row][col].empty = True
                        self.game_grid[row][col].color = self.COLOR_GRID_BG
                        self.game_grid[row][col].piece_id = EMPTY_PIECE_ID
        self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] + 1)

    def drop_current_piece_to_bottom(self):
        while not self.is_collision_down_at_next_time_step():
            self.move_current_piece_one_down()
        self.new_current_piece()

    def check_and_remove_full_lines(self):
        row = self.NUM_OF_SQUARES_ROWS - 1
        while row > 0:
            row_has_no_pieces = True
            row_is_full = True
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                if self.game_grid[row][col].empty:
                    row_is_full = False
                else:
                    row_has_no_pieces = False
            if row_has_no_pieces:
                return
            if row_is_full:
                for r in range(row, 0, -1):
                    for c in range(0, self.NUM_OF_SQUARES_COLUMS):
                        self.game_grid[r][c].empty      = self.game_grid[r - 1][c].empty
                        self.game_grid[r][c].color      = self.game_grid[r - 1][c].color
                        self.game_grid[r][c].piece_id   = self.game_grid[r - 1][c].piece_id
                row += 1
                self.num_of_lines_cleared += 1
            row -= 1

    def rotate_piece_clock_wise(self):
        current_piece_location = []
        for row in range(0, self.NUM_OF_SQUARES_ROWS):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                if self.game_grid[row][col].piece_id == self.current_piece_id:
                    current_piece_location.append(self.game_grid[row][col])

        rotated_piece = []
        for i in range(0, 4):
            rotated_piece.append(self.rotate_single_square_around_rotation_point(current_piece_location[i], self.current_piece_rotation_center))

        # Check for boundry conditions:
        move_left = 0
        move_right = 0
        for i in range(len(rotated_piece)):
            if rotated_piece[i][0] < 0:
                move_right += 1
            elif rotated_piece[i][0] >= self.NUM_OF_SQUARES_COLUMS:
                move_left += 1
        
        if move_left > 0 and move_right > 0:
            print('Error: Can\'t move left and right at the same time....')
        elif move_left > 0:
            # print('moving left')
            self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] - move_left)
            for i in range(len(rotated_piece)):
                rotated_piece[i][0] -= move_left
        elif move_right > 0:
            # print('moving right')
            self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] + move_right)
            for i in range(len(rotated_piece)):
                rotated_piece[i][0] += move_right

        can_be_rotated = True
        for i in range(len(rotated_piece)):

            if not self.game_grid[rotated_piece[i][1]][rotated_piece[i][0]].empty and not self.game_grid[rotated_piece[i][1]][rotated_piece[i][0]].piece_id == self.current_piece_id:
                can_be_rotated = False
        
        # print('Rotation point: ', self.current_piece_rotation_center)
        # print('Old points: (', current_piece_location[0].row, ', ', current_piece_location[0].col, ')')
        # print('Old points: (', current_piece_location[1].row, ', ', current_piece_location[1].col, ')')
        # print('Old points: (', current_piece_location[2].row, ', ', current_piece_location[2].col, ')')
        # print('Old points: (', current_piece_location[3].row, ', ', current_piece_location[3].col, ')')
        # print('New points: (', rotated_piece[0][0], ', ', rotated_piece[0][1], ')')
        # print('New points: (', rotated_piece[1][0], ', ', rotated_piece[1][1], ')')
        # print('New points: (', rotated_piece[2][0], ', ', rotated_piece[2][1], ')')
        # print('New points: (', rotated_piece[3][0], ', ', rotated_piece[3][1], ')')

        if can_be_rotated:
            old_color = self.game_grid[current_piece_location[0].row][current_piece_location[0].col].color
            for i in range(len(rotated_piece)):
                self.game_grid[current_piece_location[i].row][current_piece_location[i].col].empty = True
                self.game_grid[current_piece_location[i].row][current_piece_location[i].col].color = self.COLOR_GRID_BG
                self.game_grid[current_piece_location[i].row][current_piece_location[i].col].piece_id = EMPTY_PIECE_ID
            for i in range(len(rotated_piece)):
                self.game_grid[rotated_piece[i][1]][rotated_piece[i][0]].empty = False
                self.game_grid[rotated_piece[i][1]][rotated_piece[i][0]].color = old_color
                self.game_grid[rotated_piece[i][1]][rotated_piece[i][0]].piece_id = self.current_piece_id
        
    def rotate_single_square_around_rotation_point(self, square_location, rotation_point, angle_of_rotation=pi/2):
        rot_mat = [[cos(angle_of_rotation), -sin(angle_of_rotation)],
                   [sin(angle_of_rotation), cos(angle_of_rotation)]]
        original_point = [[float(square_location.col - rotation_point[1])], 
                          [float(square_location.row - rotation_point[0])]]

        result = [0, 0]

        if rotation_point[0] % 1 > 0.3 or rotation_point[1] % 1 > 0.3:
            #print('half rot spot')
            for i in range(2):
                result[i] = round(rot_mat[i][0] * original_point[0][0] + rot_mat[i][1] * original_point[1][0], 3)
        else:
            #print('regular rot spot')
            for i in range(2):
                result[i] = round(rot_mat[i][0] * original_point[0][0] + rot_mat[i][1] * original_point[1][0])

        #print('Original Point (x, y): ', original_point)
        #print('Result (x, y): ', result)

        result[0] = int(result[0] + rotation_point[1])
        result[1] = int(result[1] + rotation_point[0])

        return result

    def update_timers(self):
        self.timer_piece_fall_end = time()
        if self.timer_piece_fall_end - self.timer_piece_fall_start > float(1 / self.fall_freq):
            self.timer_piece_fall_start = time()
            if not self.is_collision_down_at_next_time_step():
                self.move_current_piece_one_down()
            else:
                self.new_current_piece()
        
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
                        self.drop_current_piece_to_bottom()
                    if event.key == py.K_DOWN:
                        if not self.is_collision_down_at_next_time_step():
                            self.move_current_piece_one_down()
                    if event.key == py.K_LEFT:
                        self.move_current_piece_one_left()
                    if event.key == py.K_RIGHT:
                        self.move_current_piece_one_right()
                    if event.key == py.K_UP:
                        self.rotate_piece_clock_wise()

            self.update_timers()
            self.update_display()

    def print_map(self):
        for row in range(0, self.NUM_OF_SQUARES_ROWS):
            for col in range(0, self.NUM_OF_SQUARES_COLUMS):
                print(int(self.game_grid[row][col].piece_id), end='')
            print('')

if __name__ == '__main__':
    print('Running Tetris UI file..')
    T = TetrisUI()
    print(T.POS_SQUARES_TOP_LEFT)
    print(T.POS_SQUARES_BUTTOM_RIGHT)
    T.run()
