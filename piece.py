from typing import Tuple, List
from abc import ABCMeta, abstractmethod
from utils import in_board

class shogiPiece:
    __metaclass__ = ABCMeta

    _GGeneral_pattern = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0)]

    def __init__(self, name: str, team: int, promoted: bool = False) -> None:
        self.name = name
        self.team = team          # 0: Our team, 1: Enemy team
        self.promoted = promoted

    def __str__(self):
        return self.name

    @abstractmethod
    def get_valid_moves(self):
        pass
    
    # Pattern provided to this function dictates the directions in which the piece may move
    def pattern_check(self, pattern: List[Tuple[int, int]], position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        src_r, src_c = position
        enemy_team = 1 - self.team
        possible_moves = []

        for pr, pc in pattern:
            dst_r, dst_c = src_r + pr, src_c + pc

            if in_board((dst_r, dst_c)):
                if not board[dst_r][dst_c] or board[dst_r][dst_c].team == enemy_team:
                    possible_moves.append((dst_r, dst_c))
        
        return possible_moves
    
    # Loop check diagonals or cardinal directions in the case of a rook or bishop that can move like this
    def loop_pattern_check(self, pattern: List[Tuple[int, int]], position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        src_r, src_c = position
        enemy_team = 1 - self.team
        possible_moves = []

        for pr, pc in pattern:
            dst_r, dst_c = src_r + pr, src_c + pc

            while in_board((dst_r, dst_c)):
                if not board[dst_r][dst_c]  or board[dst_r][dst_c].team == enemy_team:
                    possible_moves.append((dst_r, dst_c))
                else:
                    break

                dst_r += pr
                dst_c += pc
        
        return possible_moves
    

class King(shogiPiece):
    '''
    King mask:
    [D, D, D],
    [D, S, D],
    [D, D, D]
    '''
    _king_pattern = [(-1, -1), (-1, 0), (-1, -1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        moves = self.pattern_check(self._king_pattern, position, board)
        return moves


class Rook(shogiPiece):
    '''
    Rook mask:
    [D, E, D],
    [E, S, E],
    [D, E, D]
    '''
    _rook_pattern = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    _king_pattern = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Including promoted pattern.

    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        moves = self.loop_pattern_check(self._rook_pattern, position, board)
        if self.promoted:
            moves.extend(self.pattern_check(self._king_pattern, position, board))
        return moves


class Bishop(shogiPiece):
    '''
    Bishop mask:
    [D, E, D],
    [E, S, E],
    [D, E, D]
    '''
    _bishop_pattern = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    _king_pattern = [(-1, 0), (0, -1), (0, 1), (1, 0)]  # Including promoted pattern.

    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        moves = self.loop_pattern_check(self._bishop_pattern, position, board)
        if self.promoted:
            moves.extend(self.pattern_check(self._king_pattern, position, board))
        return moves


class GGeneral(shogiPiece):
    '''
    GGeneral mask:
    [D, D, D],
    [D, S, D],
    [E, D, E]
    '''
    _GGeneral_pattern = shogiPiece._GGeneral_pattern

    @property
    def _pattern(self):
        return self._GGeneral_pattern if self.team == 0 else [(-r, c) for r, c in self._GGeneral_pattern]

    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        moves = self.pattern_check(self._pattern, position, board)
        return moves


class SGeneral(shogiPiece):
    '''
    SGeneral mask:
    [D, D, D],
    [E, S, E],
    [D, E, D]
    '''
    _SGeneral_pattern = [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 1)]
    
    @property
    def _pattern(self):
        return self._SGeneral_pattern if self.team == 0 else [(-r, c) for r, c in self._SGeneral_pattern]
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern if self.team == 0 else [(-r, c) for r, c in self._GGeneral_pattern]
    
    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        pattern = self._pattern_promoted if self.promoted else self._pattern
        moves = self.pattern_check(pattern, position, board)
        return moves


class Knight(shogiPiece):
    '''
    Knight mask:
    [D, E, D],
    [E, E, E],
    [E, S, E]
    '''
    _Kinght_pattern = [(-2, -1), (-2, 1)]
    _GGeneral_pattern = shogiPiece._GGeneral_pattern
    
    @property
    def _pattern(self):
        return self._Kinght_pattern if self.team == 0 else [(-r, c) for r, c in self._Kinght_pattern]
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern if self.team == 0 else [(-r, c) for r, c in self._GGeneral_pattern]
    
    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        pattern = self._pattern_promoted if self.promoted else self._pattern
        moves = self.pattern_check(pattern, position, board)
        return moves


class Lance(shogiPiece):
    '''
    Lance mask:
    [E, D, E],
    [E, S, E],
    [E, E, E]
    '''
    _Lance_pattern = [(-1, 0)]
    _GGeneral_pattern = shogiPiece._GGeneral_pattern

    @property
    def _pattern(self):
        return self._Lance_pattern if self.team == 0 else [(-r, c) for r, c in self._Lance_pattern]
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern if self.team == 0 else [(-r, c) for r, c in self._GGeneral_pattern]
    
    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        pattern = self._pattern_promoted if self.promoted else self._pattern
        moves = self.loop_pattern_check(pattern, position, board)
        return moves


class Pawn(shogiPiece):
    '''
    Pawn mask:
    [E, D, E],
    [E, S, E],
    [E, E, E]
    '''
    _Pawn_pattern = [(-1, 0)]
    _GGeneral_pattern = shogiPiece._GGeneral_pattern

    @property
    def _pattern(self):
        return self._Pawn_pattern if self.team == 0 else [(-r, c) for r, c in self._Pawn_pattern]
    
    @property
    def _pattern_promoted(self):
        return self._GGeneral_pattern if self.team == 0 else [(-r, c) for r, c in self._GGeneral_pattern]
    
    def get_valid_moves(self, position: Tuple[int, int], board: List[List[int]]) -> List[Tuple[int, int]]:
        pattern = self._pattern_promoted if self.promoted else self._pattern
        moves = self.pattern_check(pattern, position, board)
        return moves