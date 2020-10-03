#!/usr/bin/env python3

class TetrisPiece(object):
    
    # [0, 1, 2, 3, 4, 5, 6]
    # [L, J, 5, Z, T, |, O] 
    SHAPE_ID_L          = 0
    SHAPE_ID_J          = 1
    SHAPE_ID_5          = 2
    SHAPE_ID_Z          = 3
    SHAPE_ID_T          = 4
    SHAPE_ID_I          = 5
    SHAPE_ID_O          = 6
    SHAPE_ID_EMPTY      = 7

    PIECE_ID_EMPTY      = 0

    # List of [y, x] = [row, col]
    SPAWN_LOCATION_EMPTY= [[0, 0], [0, 0], [0, 0], [0, 0]]
    SPAWN_LOCATION_L    = [[0, 4], [1, 4], [2, 4], [2, 5]]
    SPAWN_LOCATION_J    = [[0, 4], [1, 4], [2, 4], [2, 3]]
    SPAWN_LOCATION_5    = [[0, 4], [0, 5], [1, 3], [1, 4]]
    SPAWN_LOCATION_Z    = [[0, 3], [0, 4], [1, 4], [1, 5]]
    SPAWN_LOCATION_T    = [[1, 3], [1, 4], [1, 5], [0, 4]]
    SPAWN_LOCATION_I    = [[1, 3], [1, 4], [1, 5], [1, 6]]
    SPAWN_LOCATION_O    = [[0, 4], [1, 4], [0, 5], [1, 5]]
    SPAWN_LOCATION_ALL  = [SPAWN_LOCATION_L, SPAWN_LOCATION_J, 
                           SPAWN_LOCATION_5, SPAWN_LOCATION_Z, 
                           SPAWN_LOCATION_T, SPAWN_LOCATION_I, 
                           SPAWN_LOCATION_O, SPAWN_LOCATION_EMPTY]

    # Default rotation center (y, x) = (row, col)
    DEFAULT_ROTATION_CENTER_L   = (1, 4)
    DEFAULT_ROTATION_CENTER_J   = (1, 4)
    DEFAULT_ROTATION_CENTER_5   = (1, 4)
    DEFAULT_ROTATION_CENTER_Z   = (1, 4)
    DEFAULT_ROTATION_CENTER_T   = (1, 4)
    DEFAULT_ROTATION_CENTER_I   = (1.5, 4.5)
    DEFAULT_ROTATION_CENTER_O   = (0.5, 4.5)
    DEFAULT_ROTATION_CENTER_EMPTY = (0, 0)
    DEFAULT_ROTATION_CENTER_ALL = [DEFAULT_ROTATION_CENTER_L, DEFAULT_ROTATION_CENTER_J, 
                                   DEFAULT_ROTATION_CENTER_5, DEFAULT_ROTATION_CENTER_Z, 
                                   DEFAULT_ROTATION_CENTER_T, DEFAULT_ROTATION_CENTER_I, 
                                   DEFAULT_ROTATION_CENTER_O, DEFAULT_ROTATION_CENTER_EMPTY]

    def __init__(self):
        pass

if __name__ == '__main__':
    t = TetrisPiece()

    for coordinate in t.SPAWN_LOCATION_ALL[2]:
        print(coordinate[1])
