from typing import Tuple

def in_board(position: Tuple[int, int]) -> bool:
    r, c = position
    return 0 <= r <= 9 and 0 <= c <= 9

def parse_pos(notation: str) -> Tuple[int, int, bool]:
    row = 9 - int(notation[1])
    col = (ord(notation[0]) - 97)

    is_promoted = True if len(notation) == 3 else False
    return row, col, is_promoted