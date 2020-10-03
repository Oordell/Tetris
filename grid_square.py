#!/usr/bin/env python3

from dataclasses import dataclass
from pieces import TetrisPiece as tpiece

@dataclass
class GridSquare:
    row: int
    col: int
    empty: bool = True
    piece_id: int = tpiece.PIECE_ID_EMPTY
    shape_id: int = tpiece.SHAPE_ID_EMPTY
