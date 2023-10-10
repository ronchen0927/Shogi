from typing import List, Optional
from piece import shogiPiece

class shogiPlayer:
    def __init__(self, team: int, captured: Optional[List[str]] = None) -> None:
        self.team = team
        self.captured = captured if captured else []

    # Pieces that the player has captured, printed every turn
    def capture(self, piece: shogiPiece) -> None:
        self.captured.append(piece.name)

    # Piece that has been placed on to the board and removed from captured
    def drop(self, piece: shogiPiece) -> None:
        self.captured.remove(piece)