#!/usr/bin/env python3

from dataclasses import dataclass

EMPTY_PEICE_ID = -1

@dataclass
class GridSquare:
    row: int
    col: int
    color: tuple
    empty: bool = True
    peice_id: int = EMPTY_PEICE_ID