from typing import List
from piece import shogiPiece

class shogiPlayer:
    def __init__(self, team: int, captured: List[str]) -> None:
        self.team = team
        self.captured = captured

    # Pieces that the player has captured, printed every turn
    def capture(self, piece: shogiPiece) -> None:
        self.captured.append(piece)

    # Piece that has been placed on to the board and removed from captured
    def drop(self, piece: shogiPiece) -> None:
        self.captured.remove(piece)