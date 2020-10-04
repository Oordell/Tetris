#!/usr/bin/env python3

import pygame as py
import pygame.gfxdraw
from game import TetrisGame as tgame 
from pieces import TetrisPiece as tpiece

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
    LINE_WIDTH_2            = 2
    LINE_WIDTH_4            = 4
    LINE_WIDTH_5            = 5

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
    COLOR_PIECE_EMPTY       = (50, 50, 50)
    COLOR_PIECE_ALL         = [COLOR_PIECE_L, COLOR_PIECE_J, 
                               COLOR_PIECE_5, COLOR_PIECE_Z, 
                               COLOR_PIECE_T, COLOR_PIECE_I, 
                               COLOR_PIECE_O, COLOR_PIECE_EMPTY]
    COLOR_TEXT              = (200, 200, 200)
    COLOR_TEXT_START_MENU   = (10, 10, 10)
    COLOR_GHOST_PIECE_LINE  = (170, 170, 170)
    COLOR_GHOST_PIECE_BG    = (70, 70, 70)
    COLOR_START_MENU_BG     = (120, 120, 255)
    COLOR_START_MENU_BORDER = (70, 70, 200)
    COLOR_BTN_START_GAME_BG = (120, 210, 120)
    COLOR_BTN_START_GAME_BORDER = (30, 150, 30)

    BTN_OFFSET_Y            = 40
    BTN_WIDTH               = 150
    BTN_HEIGHT              = 60
    BTN_TOP_LEFT_X          = (SCREEN_WIDTH / 2) - (BTN_WIDTH / 2)
    BTN_TOP_LEFT_Y          = (SCREEN_HEIGHT / 2) - (BTN_HEIGHT / 2) + BTN_OFFSET_Y

    def __init__(self):
        self.game_logic = tgame(num_of_rows=self.NUM_OF_SQUARES_ROWS, num_of_columns=self.NUM_OF_SQUARES_COLUMS)
        self.new_game = True

        # Initialize PyGame:
        py.init()
        py.display.set_caption("Tetris")
        self.screen = py.display
        self.screen_surface = self.screen.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = py.time.Clock()
        self.fps = 25

    def init_game(self):
        self.game_logic.setup_new_game()
        self.draw_screen_layout()

    def draw_screen_layout(self):
        self.draw_background()
        self.draw_playing_field()
        self.draw_game_data()

    def draw_start_menu(self):
        self.draw_default_start_and_end_game_rect()
        self.draw_menu_text("NEW GAME", "START")
    
    def draw_game_over_menu(self):
        self.draw_default_start_and_end_game_rect()
        self.draw_menu_text("GAME OVER", "NEW GAME")

    def draw_menu_text(self, menu_text, btn_text):
        font = py.font.Font('freesansbold.ttf', self.FONT_SIZE_LARGE)
        text = font.render(menu_text, True, self.COLOR_TEXT_START_MENU)
        text_rect = text.get_rect()
        text_rect.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 40)
        self.screen_surface.blit(text, text_rect)

        font = py.font.Font('freesansbold.ttf', self.FONT_SIZE_NORMAL)
        text = font.render(btn_text, True, self.COLOR_TEXT_START_MENU)
        text_rect = text.get_rect()
        text_rect.center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 40)
        self.screen_surface.blit(text, text_rect)
    
    def draw_default_start_and_end_game_rect(self):
        rect_width = 300
        rect_height = 200
        top_left = ((self.SCREEN_WIDTH / 2) - (rect_width / 2), (self.SCREEN_HEIGHT / 2) - (rect_height / 2))
        corner_radius = 30
        border_thickness = 5
        rect = py.Rect(top_left[0], top_left[1], rect_width, rect_height)
        self.draw_bordered_rounded_rect(rect, self.COLOR_START_MENU_BG, self.COLOR_START_MENU_BORDER, corner_radius, border_thickness)

        corner_radius = 10
        border_thickness = 4
        rect = py.Rect(self.BTN_TOP_LEFT_X, self.BTN_TOP_LEFT_Y, self.BTN_WIDTH, self.BTN_HEIGHT)
        self.draw_bordered_rounded_rect(rect, self.COLOR_BTN_START_GAME_BG, self.COLOR_BTN_START_GAME_BORDER, corner_radius, border_thickness)

    def draw_rounded_rect(self, rect, color, corner_radius):
        py.gfxdraw.aacircle(self.screen_surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
        py.gfxdraw.aacircle(self.screen_surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
        py.gfxdraw.aacircle(self.screen_surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
        py.gfxdraw.aacircle(self.screen_surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

        py.gfxdraw.filled_circle(self.screen_surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
        py.gfxdraw.filled_circle(self.screen_surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
        py.gfxdraw.filled_circle(self.screen_surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
        py.gfxdraw.filled_circle(self.screen_surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)

        rect_tmp = py.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(self.screen_surface, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(self.screen_surface, color, rect_tmp)

    def draw_bordered_rounded_rect(self, rect, color, border_color, corner_radius, border_thickness):
        if corner_radius < 0:
            raise ValueError(f"border radius ({corner_radius}) must be >= 0")

        rect_tmp = pygame.Rect(rect)
        center = rect_tmp.center

        if border_thickness:
            if corner_radius <= 0:
                pygame.draw.rect(self.screen_surface, border_color, rect_tmp)
            else:
                self.draw_rounded_rect(rect_tmp, border_color, corner_radius)

            rect_tmp.inflate_ip(-2*border_thickness, -2*border_thickness)
            inner_radius = corner_radius - border_thickness + 1
        else:
            inner_radius = corner_radius

        if inner_radius <= 0:
            pygame.draw.rect(self.screen_surface, color, rect_tmp)
        else:
            self.draw_rounded_rect(rect_tmp, color, inner_radius)

    def draw_background(self):
        self.screen_surface.fill(self.COLOR_BACKGROUND)
    
    def draw_playing_grid(self):
        for col in range(0, self.NUM_OF_SQUARES_COLUMS + 1):
            py.draw.line(self.screen_surface, 
                        self.COLOR_GRID_LINES, 
                        (self.POS_SQUARES_TOP_LEFT[1] + (col * self.SIZE_OF_SQUARE), self.POS_SQUARES_TOP_LEFT[0]),
                        (self.POS_SQUARES_TOP_LEFT[1] + (col * self.SIZE_OF_SQUARE), self.POS_SQUARES_BUTTOM_RIGHT[0]),
                        self.LINE_WIDTH_2)
        for row in range(0, self.NUM_OF_SQUARES_ROWS + 1):
            py.draw.line(self.screen_surface, 
                        self.COLOR_GRID_LINES, 
                        (self.POS_SQUARES_TOP_LEFT[1], self.POS_SQUARES_TOP_LEFT[0] + (row * self.SIZE_OF_SQUARE)),
                        (self.POS_SQUARES_BUTTOM_RIGHT[1], self.POS_SQUARES_TOP_LEFT[0] + (row * self.SIZE_OF_SQUARE)),
                        self.LINE_WIDTH_2)

    def draw_border_on_playing_area(self):
        py.draw.rect(self.screen_surface, 
                     self.COLOR_GRID_LINES,
                     (self.POS_SQUARES_TOP_LEFT[1], self.POS_SQUARES_TOP_LEFT[0],
                     self.SIZE_OF_SQUARE * self.NUM_OF_SQUARES_COLUMS, 
                     self.SIZE_OF_SQUARE * self.NUM_OF_SQUARES_ROWS),
                     self.LINE_WIDTH_5)

    def draw_playing_field(self):
        for row in range(self.NUM_OF_SQUARES_ROWS):
            for col in range(self.NUM_OF_SQUARES_COLUMS):
                py.draw.rect(self.screen_surface, 
                    self.COLOR_PIECE_ALL[self.game_logic.grid[row][col].shape_id],
                    (self.POS_SQUARES_TOP_LEFT[1] + self.SIZE_OF_SQUARE * col, 
                    self.POS_SQUARES_TOP_LEFT[0] + self.SIZE_OF_SQUARE * row, 
                    self.SIZE_OF_SQUARE, self.SIZE_OF_SQUARE))
        self.draw_playing_grid()
        self.draw_ghost_location_if_piece_is_droped()
        self.draw_border_on_playing_area()

    def draw_game_data(self):
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
        text = font.render("Rows Cleared: " + str(self.game_logic.num_of_rows_cleared), True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_left_column , 150)
        self.screen_surface.blit(text, text_rect)

        text = font.render("Height: " + str(self.game_logic.max_height_of_stacked_pieces), True, self.COLOR_TEXT)
        text_rect = text.get_rect()
        text_rect.center = (center_left_column , 200)
        self.screen_surface.blit(text, text_rect)

        text = font.render("Holes: " + str(self.game_logic.num_of_holes), True, self.COLOR_TEXT)
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

        
        mini_grid = [[tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY],
                     [tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY],
                     [tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY],
                     [tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY, tpiece.SHAPE_ID_EMPTY]]
        top_left = (center_right_column - self.SIZE_OF_SQUARE * 1.5,
                    top_off_set + (box_height / 2) - self.SIZE_OF_SQUARE * 1.5)
        
        for coordinate in tpiece.SPAWN_LOCATION_ALL[self.game_logic.next_shape_id]:
            mini_grid[coordinate[0]][coordinate[1] - 3] = self.game_logic.next_shape_id
        
        for row in range(len(mini_grid)):
            for col in range(len(mini_grid)):
                if not mini_grid[row][col] == -1:
                    py.draw.rect(self.screen_surface, 
                                self.COLOR_PIECE_ALL[mini_grid[row][col]], 
                                (top_left[0] + col * self.SIZE_OF_SQUARE, 
                                top_left[1] + row * self.SIZE_OF_SQUARE, 
                                self.SIZE_OF_SQUARE, 
                                self.SIZE_OF_SQUARE))

    def get_num_of_squares_piece_can_drop_from_current_location(self):
        num_of_squares_to_drop_piece = 0
        buttom_reached = False
        i = 1
        while not buttom_reached and i < self.NUM_OF_SQUARES_ROWS:
            for row in range(self.NUM_OF_SQUARES_ROWS):
                for col in range(self.NUM_OF_SQUARES_COLUMS):
                    if self.game_logic.grid[row][col].piece_id == self.game_logic.current_piece_id:
                        if i + row >= self.NUM_OF_SQUARES_ROWS:
                            num_of_squares_to_drop_piece = i - 1
                            buttom_reached = True
                            break
                        if not self.game_logic.grid[row + i][col].empty and not \
                            self.game_logic.grid[row + i][col].piece_id == self.game_logic.current_piece_id:
                            num_of_squares_to_drop_piece = i - 1
                            buttom_reached = True
                            break
            i += 1
        if i == self.NUM_OF_SQUARES_ROWS:
            num_of_squares_to_drop_piece = self.NUM_OF_SQUARES_ROWS - 2
        return num_of_squares_to_drop_piece

    def draw_ghost_location_if_piece_is_droped(self):
        num_of_squares_to_drop_piece = self.get_num_of_squares_piece_can_drop_from_current_location()
        border_thickness = 4
        for row in range(self.NUM_OF_SQUARES_ROWS):
            for col in range(self.NUM_OF_SQUARES_COLUMS):
                if self.game_logic.grid[row][col].piece_id == self.game_logic.current_piece_id:
                    if not self.game_logic.grid[row + num_of_squares_to_drop_piece][col].piece_id == self.game_logic.current_piece_id:
                        py.draw.rect(self.screen_surface, 
                                     self.COLOR_GHOST_PIECE_LINE, 
                                    (self.POS_SQUARES_TOP_LEFT[1] + col * self.SIZE_OF_SQUARE, 
                                     self.POS_SQUARES_TOP_LEFT[0] + (row + num_of_squares_to_drop_piece) * self.SIZE_OF_SQUARE, 
                                     self.SIZE_OF_SQUARE, 
                                     self.SIZE_OF_SQUARE),
                                     border_thickness )

    def update_display(self):
        py.display.update()
        self.clock.tick(self.fps)

    def run(self):
        while True:
            for event in py.event.get():
                if self.new_game and not self.game_logic.running_game:
                    self.draw_screen_layout()
                    self.draw_start_menu()
                    if event.type == py.MOUSEBUTTONDOWN:
                        x, y = event.pos[0], event.pos[1]
                        if self.BTN_TOP_LEFT_X < x < self.BTN_TOP_LEFT_X + self.BTN_WIDTH and \
                            self.BTN_TOP_LEFT_Y < y < self.BTN_TOP_LEFT_Y + self.BTN_HEIGHT:
                            self.init_game()
                            self.new_game = False
                            self.game_logic.running_game = True
                elif not self.new_game and self.game_logic.running_game:
                    if event.type == py.KEYDOWN:
                        if event.key == py.K_SPACE:
                            self.game_logic.drop_current_piece_to_bottom()
                        if event.key == py.K_DOWN:
                            if self.game_logic.can_current_piece_move_one_down():
                                self.game_logic.move_current_piece_one_down()
                        if event.key == py.K_LEFT:
                            self.game_logic.move_current_piece_one_left()
                        if event.key == py.K_RIGHT:
                            self.game_logic.move_current_piece_one_right()
                        if event.key == py.K_UP:
                            self.game_logic.rotate_piece_clock_wise()
                elif not self.new_game and not self.game_logic.running_game:
                    if event.type == py.MOUSEBUTTONDOWN:
                        x, y = event.pos[0], event.pos[1]
                        if self.BTN_TOP_LEFT_X < x < self.BTN_TOP_LEFT_X + self.BTN_WIDTH and \
                            self.BTN_TOP_LEFT_Y < y < self.BTN_TOP_LEFT_Y + self.BTN_HEIGHT:
                            self.init_game()
                            self.new_game = False
                            self.game_logic.running_game = True

                if event.type == py.QUIT:
                    py.quit()
                    quit()
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        py.quit()
                        quit()
            
            if not self.new_game:
                self.game_logic.update_timers()
                self.draw_playing_field()
                self.draw_game_data()
                if not self.game_logic.running_game:
                    self.draw_game_over_menu()

            self.update_display()


if __name__ == '__main__':
    tetris = TetrisUI()
    tetris.run()
