from typing import Tuple, List
from abc import ABCMeta, abstractmethod
from board import shogiBoard

class shogiPiece:
    __metaclass__ = ABCMeta

    _GGeneral_pattern_up = [(0, 1), (1, 0), (0, -1), (-1, 0),
                            (1, 1), (-1, 1)]
    _GGeneral_pattern_dn = [(0, 1), (1, 0), (0, -1), (-1, 0),
                            (1, -1), (-1, -1)]

    def __init__(self, name: str, team: int, position: Tuple[int, int], promoted: bool = False) -> None:
        self.name = name
        self.team = team
        self.position = position
        self.promoted = promoted

    def __str__(self):
        return self.name.lower() if self.team == 1 else self.name.upper()

    @abstractmethod
    def moves(self):
        pass

    @abstractmethod
    def promote(self):
        pass

    @abstractmethod
    def unpromote(self):
        pass

    # Make sure that the position is inside the boundaries of the game board
    @classmethod
    def _in_bound(cls, position: Tuple[int, int]) -> bool:
        x, y = position
        return 0 <= x <= 9 and 0 <= y <= 9
    
    # Pattern provided to this function dictates the directions in which the piece may move
    def pattern_check(self, pattern: List[Tuple[int, int]], shogi_board: shogiBoard) -> List[Tuple[int, int]]:
        x, y = self.position
        opposite_team = -self.team
        possible_moves = []

        for dx, dy in pattern:
            nx, ny = x + dx, y + dy

            if shogiPiece._in_bound((nx, ny)):
                if not shogi_board.has_piece((nx, ny)) or shogi_board.board[nx][ny].team == opposite_team:
                    possible_moves.append((nx, ny))
                else:
                    break
        
        return possible_moves
    
    # Loop check diagonals or cardinal directions in the case of a rook or bishop that can move like this
    def loop_pattern_check(self, pattern: List[Tuple[int, int]], shogi_board: shogiBoard) -> List[Tuple[int, int]]:
        x, y = self.position
        opposite_team = -self.team
        possible_moves = []

        for dx, dy in pattern:
            nx, ny = x + dx, y + dy

            while shogiPiece._in_bound((nx, ny)):
                if not shogi_board.has_piece((nx, ny)) or shogi_board.board[nx][ny].team == opposite_team:
                    possible_moves.append((nx, ny))
                else:
                    break

                nx += dx
                ny += dy
        
        return possible_moves
    

class King(shogiPiece):
    _king_pattern = [(0, 1), (1, 0), (0, -1), (-1, 0),
                    (1, 1), (-1, 1), (1, -1), (-1, -1)]
    
    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        moves = self.pattern_check(self._king_pattern, board)
        return moves
    
    def promote(self):
        raise Exception('Illegal move, King cannot be promoted')

    def unpromote(self):
        raise Exception('Illegal move, King cannot be promoted')


class Rook(shogiPiece):
    _rook_pattern = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    _king_pattern = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # Including promoted pattern.

    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        moves = self.loop_pattern_check(self._rook_pattern, board)
        if self.promoted:
            moves.extend(self.pattern_check(self._king_pattern, board))
        return moves
    
    def promote(self):
        self.promoted = True

    def unpromote(self):
        self.promoted = False


class Bishop(shogiPiece):
    _bishop_pattern = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
    _king_pattern = [(1, 1), (-1, 1), (1, -1), (-1, -1)]  # Including promoted pattern.

    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        moves = self.loop_pattern_check(self._bishop_pattern, board)
        if self.promoted:
            moves.extend(self.pattern_check(self._king_pattern, board))
        return moves
    
    def promote(self):
        self.promoted = True

    def unpromote(self):
        self.promoted = False


class GGeneral(shogiPiece):
    _GGeneral_pattern_up = shogiPiece._GGeneral_pattern_up
    _GGeneral_pattern_dn = shogiPiece._GGeneral_pattern_dn

    @property
    def _pattern(self):
        return self._GGeneralPattern_up if self.team == 1 else self._GGeneralPattern_dn

    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        moves = self.pattern_check(self._pattern, board)
        return moves
    
    def promote(self):
        raise Exception('Illegal move, Golden General cannot be promoted')

    def unpromote(self):
        raise Exception('Illegal move, Golden General cannot be promoted')


class SGeneral(shogiPiece):
    _SGeneral_pattern_up = [(1, 1), (-1, 1), (1, -1), (-1, -1),
                            (0, 1)]
    _SGeneral_pattern_dn = [(1, 1), (-1, 1), (1, -1), (-1, -1),
                            (0, -1)]
    
    @property
    def _pattern(self):
        return self._SGeneral_pattern_up if self.team == 1 else self._SGeneral_pattern_dn
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern_up if self.team == 1 else self._GGeneral_pattern_dn
    
    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        if not self.promoted:
            pattern = self._pattern
        else:
            pattern = self._pattern_promoted
        
        moves = self.pattern_check(pattern, board)
        return moves
    
    def promote(self):
        self.promoted = True

    def unpromote(self):
        self.promoted = False


class Knight(shogiPiece):
    _Kinght_pattern_up = [(-1, 2), (1, 2)]
    _Kinght_pattern_dn = [(-1, -2), (1, -2)]
    _GGeneral_pattern_up = shogiPiece._GGeneral_pattern_up
    _GGeneral_pattern_dn = shogiPiece._GGeneral_pattern_dn
    
    @property
    def _pattern(self):
        return self._Kinght_pattern_dn if self.team == 1 else self._Kinght_pattern_dn
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern_up if self.team == 1 else self._GGeneral_pattern_dn
    
    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        if not self.promoted:
            pattern = self._pattern
        else:
            pattern = self._pattern_promoted

        moves = self.pattern_check(pattern, board)
        return moves
    
    def promote(self):
        self.promoted = True

    def unpromote(self):
        self.promoted = False


class Lance(shogiPiece):
    _Lance_pattern_up = [(0, 1)]
    _Lance_pattern_dn = [(0, -1)]
    _GGeneral_pattern_up = shogiPiece._GGeneral_pattern_up
    _GGeneral_pattern_dn = shogiPiece._GGeneral_pattern_dn

    @property
    def _pattern(self):
        return self._Lance_pattern_up if self.team == 1 else self._Lance_pattern_dn
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern_up if self.team == 1 else self._GGeneral_pattern_dn
    
    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        if not self.promoted:
            pattern = self._pattern
        else:
            pattern = self._pattern_promoted

        moves = self.loop_pattern_check(pattern, board)
        return moves
    
    def promote(self):
        self.promoted = True

    def unpromote(self):
        self.promoted = False


class Pawn(shogiPiece):
    _Pawn_pattern_up = [(0, 1)]
    _Pawn_pattern_dn = [(0, -1)]
    _GGeneral_pattern_up = shogiPiece._GGeneral_pattern_up
    _GGeneral_pattern_dn = shogiPiece._GGeneral_pattern_dn

    @property
    def _pattern(self):
        return self._Pawn_pattern_up if self.team == 1 else self._Pawn_pattern_dn
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern_up if self.team == 1 else self._GGeneral_pattern_dn
    
    def moves(self, board: shogiBoard) -> List[Tuple[int, int]]:
        if not self.promoted:
            pattern = self._pattern
        else:
            pattern = self._pattern_promoted

        print(pattern)
        moves = self.pattern_check(pattern, board)
        return moves
    
    def promote(self):
        self.promoted = True

    def unpromote(self):
        self.promoted = False