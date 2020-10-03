#!/usr/bin/env python3

from grid_square import GridSquare as gsquare
from pieces import TetrisPiece as tpiece

from time import time
import random as rand
from math import cos, sin, pi

class TetrisGame(object):

    FALL_SPEED_UPDATE_SEC   = 30
    FALL_SPEED_INIT         = float(0.5)
    FALL_SPEED_FREQ_INC     = float(0.2)

    NUM_OF_SHAPES           = 7

    def __init__(self, num_of_rows=20, num_of_columns=10):
        self.num_of_rows = num_of_rows
        self.num_of_columns = num_of_columns
        self.grid = []

        self.current_piece_id = tpiece.PIECE_ID_EMPTY
        self.current_piece_rotation_center = (0, 0)
        self.current_shape_id = tpiece.SHAPE_ID_EMPTY
        self.next_shape_id = tpiece.SHAPE_ID_EMPTY

        self.running_game = False

        self.num_of_rows_cleared = 0
        self.num_of_holes = 0
        self.max_height_of_stacked_pieces = 0

        self.fall_freq = self.FALL_SPEED_INIT
        self.timer_speed_update_start = time()
        self.timer_speed_update_end = time()
        self.timer_piece_fall_start = time()
        self.timer_piece_fall_end = time()

    def setup_new_game(self):
        self.running_game = True
        self.empty_grid()
        self.current_piece_id = 1
        self.current_shape_id = rand.randint(0, self.NUM_OF_SHAPES - 1)
        self.next_shape_id = rand.randint(0, self.NUM_OF_SHAPES - 1)
        self.current_piece_rotation_center = tpiece.DEFAULT_ROTATION_CENTER_ALL[self.current_shape_id]
        self.place_new_current_piece()

    def empty_grid(self):
        self.grid = []
        for row in range(self.num_of_rows):
            temp_row = []
            for col in range(self.num_of_columns):        
                temp_row.append(gsquare(row, col))
            self.grid.append(temp_row)

    def select_new_current_piece(self):
        self.current_piece_id += 1
        self.current_shape_id = self.next_shape_id
        self.current_piece_rotation_center = tpiece.DEFAULT_ROTATION_CENTER_ALL[self.current_shape_id]
        self.next_shape_id = rand.randint(0, self.NUM_OF_SHAPES - 1)

    def can_new_piece_be_placed(self):
        for coordinate in tpiece.SPAWN_LOCATION_ALL[self.current_shape_id]:
            if not self.grid[coordinate[0]][coordinate[1]].piece_id == tpiece.PIECE_ID_EMPTY:
                return False
        return True
    
    def place_new_current_piece(self):
        for coordinate in tpiece.SPAWN_LOCATION_ALL[self.current_shape_id]:
            self.grid[coordinate[0]][coordinate[1]].empty = False
            self.grid[coordinate[0]][coordinate[1]].piece_id = self.current_piece_id
            self.grid[coordinate[0]][coordinate[1]].shape_id = self.current_shape_id
        self.current_piece_rotation_center = tpiece.DEFAULT_ROTATION_CENTER_ALL[self.current_shape_id]

    def can_current_piece_move_one_down(self):
        for row in range(self.num_of_rows - 1, -1, -1):
            for col in range(self.num_of_columns - 1, -1, -1):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    if row == self.num_of_rows - 1:
                        return False
                    elif not self.grid[row + 1][col].empty and not self.grid[row + 1][col].piece_id == self.current_piece_id:
                        return False
        return True
    
    def can_current_piece_move_one_left(self):
        for row in range(self.num_of_rows - 1, -1, -1):
            for col in range(0, self.num_of_columns):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    if col == 0:
                        return False
                    elif not self.grid[row][col - 1].empty and not self.grid[row][col - 1].piece_id == self.current_piece_id:
                        return False
        return True

    def can_current_piece_move_one_right(self):
        for row in range(self.num_of_rows - 1, -1, -1):
            for col in range(self.num_of_columns - 1, -1, -1):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    if col == self.num_of_columns - 1:
                        return False
                    elif not self.grid[row][col + 1].empty and not self.grid[row][col + 1].piece_id == self.current_piece_id:
                        return False
        return True

    def move_current_piece_one_down(self):
        for row in range(self.num_of_rows - 2, -1, -1):
            for col in range(self.num_of_columns - 1, -1, -1):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    self.grid[row + 1][col].empty = False
                    self.grid[row + 1][col].piece_id = self.current_piece_id
                    self.grid[row + 1][col].shape_id = self.current_shape_id
                    self.grid[row][col].empty = True
                    self.grid[row][col].piece_id = tpiece.PIECE_ID_EMPTY
                    self.grid[row][col].shape_id = tpiece.SHAPE_ID_EMPTY
        self.current_piece_rotation_center = (self.current_piece_rotation_center[0] + 1, self.current_piece_rotation_center[1])

    def move_current_piece_one_left(self):
        if not self.can_current_piece_move_one_left():
            return
        for row in range(self.num_of_rows - 1, -1, -1):
            for col in range(1, self.num_of_columns):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    self.grid[row][col - 1].empty = False
                    self.grid[row][col - 1].piece_id = self.current_piece_id
                    self.grid[row][col - 1].shape_id = self.current_shape_id
                    self.grid[row][col].empty = True
                    self.grid[row][col].piece_id = tpiece.PIECE_ID_EMPTY
                    self.grid[row][col].shape_id = tpiece.SHAPE_ID_EMPTY
        self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] - 1)

    def move_current_piece_one_right(self):
        if not self.can_current_piece_move_one_right():
            return
        for row in range(self.num_of_rows - 1, -1, -1):
            for col in range(self.num_of_columns - 2, -1, -1):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    self.grid[row][col + 1].empty = False
                    self.grid[row][col + 1].piece_id = self.current_piece_id
                    self.grid[row][col + 1].shape_id = self.current_shape_id
                    self.grid[row][col].empty = True
                    self.grid[row][col].piece_id = tpiece.PIECE_ID_EMPTY
                    self.grid[row][col].shape_id = tpiece.SHAPE_ID_EMPTY
        self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] + 1)    
    
    def rotate_piece_clock_wise(self):
        current_piece_location = []
        for row in range(self.num_of_rows):
            for col in range(self.num_of_columns):
                if self.grid[row][col].piece_id == self.current_piece_id:
                    current_piece_location.append(self.grid[row][col])

        rotated_piece = []
        for i in range(4):
            rotated_piece.append(self.rotate_single_square_around_rotation_point(current_piece_location[i], self.current_piece_rotation_center))

        # Check for boundry conditions:
        move_left = 0
        move_right = 0
        for i in range(len(rotated_piece)):
            if rotated_piece[i][0] < 0:
                move_right += 1
            elif rotated_piece[i][0] >= self.num_of_columns:
                move_left += 1
        
        if move_left > 0 and move_right > 0:
            print('Error: Can\'t move left and right at the same time....')
        elif move_left > 0:
            self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] - move_left)
            for i in range(len(rotated_piece)):
                rotated_piece[i][0] -= move_left
        elif move_right > 0:
            self.current_piece_rotation_center = (self.current_piece_rotation_center[0], self.current_piece_rotation_center[1] + move_right)
            for i in range(len(rotated_piece)):
                rotated_piece[i][0] += move_right

        can_be_rotated = True
        for i in range(len(rotated_piece)):
            if not self.grid[rotated_piece[i][1]][rotated_piece[i][0]].empty and not self.grid[rotated_piece[i][1]][rotated_piece[i][0]].piece_id == self.current_piece_id:
                can_be_rotated = False

        if can_be_rotated:
            for i in range(len(rotated_piece)):
                self.grid[current_piece_location[i].row][current_piece_location[i].col].empty = True
                self.grid[current_piece_location[i].row][current_piece_location[i].col].piece_id = tpiece.PIECE_ID_EMPTY
                self.grid[current_piece_location[i].row][current_piece_location[i].col].shape_id = tpiece.SHAPE_ID_EMPTY
            for i in range(len(rotated_piece)):
                self.grid[rotated_piece[i][1]][rotated_piece[i][0]].empty = False
                self.grid[rotated_piece[i][1]][rotated_piece[i][0]].piece_id = self.current_piece_id
                self.grid[rotated_piece[i][1]][rotated_piece[i][0]].shape_id = self.current_shape_id
        
    def rotate_single_square_around_rotation_point(self, square_location, rotation_point, angle_of_rotation=pi/2):
        rot_mat = [[cos(angle_of_rotation), -sin(angle_of_rotation)],
                   [sin(angle_of_rotation), cos(angle_of_rotation)]]
        original_point = [[float(square_location.col - rotation_point[1])], 
                          [float(square_location.row - rotation_point[0])]]

        result = [0, 0]
        if rotation_point[0] % 1 > 0.3 or rotation_point[1] % 1 > 0.3:
            for i in range(2):
                result[i] = round(rot_mat[i][0] * original_point[0][0] + rot_mat[i][1] * original_point[1][0], 3)
        else:
            for i in range(2):
                result[i] = round(rot_mat[i][0] * original_point[0][0] + rot_mat[i][1] * original_point[1][0])

        result[0] = int(result[0] + rotation_point[1])
        result[1] = int(result[1] + rotation_point[0])
        return result

    def drop_current_piece_to_bottom(self):
        while self.can_current_piece_move_one_down():
            self.move_current_piece_one_down()
        self.current_piece_has_reached_bottom()

    def current_piece_has_reached_bottom(self):
        self.remove_full_rows()
        self.count_num_of_holes()
        self.meassure_max_height()
        self.select_new_current_piece()
        if not self.can_new_piece_be_placed():
            self.running_game = False
        else:
            self.place_new_current_piece()

    def remove_full_rows(self):
        row = self.num_of_rows - 1
        while row > 0:
            row_has_no_pieces = True
            row_is_full = True
            for col in range(self.num_of_columns):
                if self.grid[row][col].empty:
                    row_is_full = False
                else:
                    row_has_no_pieces = False
            if row_has_no_pieces:
                return
            if row_is_full:
                for r in range(row, 0, -1):
                    for c in range(self.num_of_columns):
                        self.grid[r][c].empty      = self.grid[r - 1][c].empty
                        self.grid[r][c].piece_id   = self.grid[r - 1][c].piece_id
                        self.grid[r][c].shape_id   = self.grid[r - 1][c].shape_id
                row += 1
                self.num_of_rows_cleared += 1
            row -= 1

    def count_num_of_holes(self):
        self.num_of_holes = 0
        for col in range(self.num_of_columns):
            is_block_in_column = False
            for row in range(0, self.num_of_rows):
                if not self.grid[row][col].empty: # and not self.grid[row][col].piece_id == self.current_piece_id:
                    is_block_in_column = True
                if is_block_in_column and self.grid[row][col].empty:
                    self.num_of_holes += 1

    def meassure_max_height(self):
        self.max_height_of_stacked_pieces = 0
        height = 0
        for col in range(self.num_of_columns):
            for row in range(self.num_of_rows - 1, -1, -1):
                if not self.grid[row][col].empty: # and not self.grid[row][col].piece_id == self.current_piece_id:
                    height = row * (-1) + self.num_of_rows
            if self.max_height_of_stacked_pieces < height:
                self.max_height_of_stacked_pieces = height

    def update_timers(self):
        # Timer for dropping the current piece one down
        self.timer_piece_fall_end = time()
        if self.timer_piece_fall_end - self.timer_piece_fall_start > float(1 / self.fall_freq):
            self.timer_piece_fall_start = time()
            if self.can_current_piece_move_one_down():
                self.move_current_piece_one_down()
            else:
                self.current_piece_has_reached_bottom()
        
        # Timer for increasing the fall speed of the durrent piece
        self.timer_speed_update_end = time()
        if self.timer_speed_update_end - self.timer_speed_update_start > self.FALL_SPEED_UPDATE_SEC:
            self.timer_speed_update_start = time()
            self.fall_freq += self.FALL_SPEED_FREQ_INC
            # print('Speed updated.')

    def run(self):
        while self.running_game:
            self.update_timers()

    def print_map(self):
        for row in range(self.num_of_rows):
            for col in range(self.num_of_columns):
                print(int(self.grid[row][col].shape_id), end='')
            print('')


if __name__ == '__main__':
    pass
