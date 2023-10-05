from typing import Tuple, List
from piece import *
    
class shogiBoard:
    def __init__(self) -> None:
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.init_board()
        self.pieces = {
            'K': King, 'R': Rook, 'B': Bishop, 'G': GGeneral,
            'S': SGeneral, 'N': Knight, 'L': Lance, 'P': Pawn
        }

    def has_piece(self, position: Tuple[int, int]) -> bool:
        if not shogiPiece._in_bound(position):
            raise Exception("Incorrect position!")

        x, y = position
        return True if self.board[x][y] else False

    def init_board(self) -> None:
        '''
        # Initial board
        ---------------------
        a | L| N| S| G| K| G| S| N| L|
        b |__| R|__|__|__|__|__| B|__|
        c | P| P| P| P| P| P| P| P| P|
        d |__|__|__|__|__|__|__|__|__|
        e |__|__|__|__|__|__|__|__|__|
        f |__|__|__|__|__|__|__|__|__|
        g | p| p| p| p| p| p| p| p| p|
        h |__| b|__|__|__|__|__| r|__|
        i | l| n| s| g| k| g| s| n| l|
            9  8  7  6  5  4  3  2  1
        '''
        # 對方的棋子(後手)
        self.board[0] = [Lance('L', -1, (0, 0)), Knight('N', -1, (0, 1)), SGeneral('S', -1, (0, 2)), GGeneral('G', -1, (0, 3)), King('K', -1, (0, 4)), 
                         GGeneral('G', -1, (0, 5)), SGeneral('S', -1, (0, 6)), Knight('N', -1, (0, 7)), Lance('L', -1, (0, 8))]
        self.board[1][1] = Rook('R', -1, (1, 1))
        self.board[1][7] = Bishop('B', -1, (1, 7))
        self.board[2] = [Pawn('P', -1, (2, 0)), Pawn('P', -1, (2, 1)), Pawn('P', -1, (2, 2)), Pawn('P', -1, (2, 3)), Pawn('P', -1, (2, 4)), 
                         Pawn('P', -1, (2, 5)), Pawn('P', -1, (2, 6)), Pawn('P', -1, (2, 7)), Pawn('P', -1, (2, 8))]

        # 我方的棋子(先手)
        self.board[6] = [Pawn('p', 1, (6, 0)), Pawn('p', 1, (6, 1)), Pawn('p', 1, (6, 2)), Pawn('p', 1, (6, 3)), Pawn('p', 1, (6, 4)), 
                         Pawn('p', 1, (6, 5)), Pawn('p', 1, (6, 6)), Pawn('p', 1, (6, 7)), Pawn('p', 1, (6, 8))]
        self.board[7][1] = Bishop('b', 1, (7, 1))
        self.board[7][7] = Rook('r', 1, (7, 7))
        self.board[8] = [Lance('l', 1, (8, 0)), Knight('n', 1, (8, 1)), SGeneral('s', 1, (8, 2)), GGeneral('g', 1, (8, 3)), King('k', 1, (8, 4)), 
                         GGeneral('g', 1, (8, 5)), SGeneral('s', 1, (8, 6)), Knight('n', 1, (8, 7)), Lance('l', 1, (8, 8))]

    def display_board(self) -> None:
        for i, row in enumerate(self.board):
            row_content = []

            for piece in row:
                if piece:
                    row_content.append(f" {piece}|")
                else:
                    row_content.append("__|")

            print(f"{chr(i + 97)} |{''.join(row_content)}")

        print("    " + "  ".join(map(str, range(9, 0, -1))))

    def execute_move(self, move_command: str, player: int) -> None:
        # Move ex: 7g7f
        # Promotion move ex: 4e3c+
        # Drops are written as a piece letter in upper case
        # Drop ex: P*3d

        if move_command[1] != '*':
            sy, sx, _ = self._convert_shogi_notation(move_command[:2])
            ey, ex, promotion = self._convert_shogi_notation(move_command[2:])

            print((sx, sy))
            print((ex, ey))

            # Execute move
            obj_piece = self.board[sx][sy]
            if not obj_piece:
                raise Exception("No piece in the position")
            
            valid_moves = obj_piece.moves(self)
            print(valid_moves)
            if (ex, ey) not in valid_moves:
                raise Exception("This move is invalid!")
            
            if promotion:
                if player == 1 and ey not in [0, 1, 2] or player == -1 and ey not in [6, 7, 8]:
                    raise Exception("This move can't promote!")
                obj_piece.promoted = True
            
            self.board[sx][sy] = None
            obj_piece.position = (ex, ey)
        else:
            piece, _ = move_command[:2]
            ey, ex, _ = self._convert_shogi_notation(move_command[2:])  # Drop piece hasn't promotion.

            obj_piece = self.board[ex][ey]
            if obj_piece:
                raise Exception("Can't drop the position, because the position has piece!")
            
            if player == 1:
                obj_piece = self.pieces(piece.upper())(piece.lower(), 1, (ex, ey))
            else:
                obj_piece = self.pieces(piece.upper())(piece.upper(), -1, (ex, ey))

        self.board[ex][ey] = obj_piece

    def _convert_shogi_notation(self, notation: List[str]) -> Tuple[int, int, bool]:
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        col = 9 - col_map[notation[1]]
        row = int(notation[0])
        promotion = True if len(notation) == 3 else False
        return col, row, promotion

    # def get_winner(self):


if __name__ == '__main__':
    board = shogiBoard()
    board.display_board()
    board.execute_move('7g7f', 1)