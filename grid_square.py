#!/usr/bin/env python3

from dataclasses import dataclass

@dataclass
class GridSquare:
    row: int
    col: int
    color: tuple
    empty: bool = True
    peice_id: int = -1