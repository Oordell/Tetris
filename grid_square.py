#!/usr/bin/env python3

from dataclasses import dataclass

EMPTY_PIECE_ID = -1

@dataclass
class GridSquare:
    row: int
    col: int
    color: tuple
    empty: bool = True
    piece_id: int = EMPTY_PIECE_ID
