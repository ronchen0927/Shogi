from typing import Tuple, List
from piece import *
from utils import parse_pos
    
class shogiBoard:
    OUR_PROMOTION_ZONE = [0, 1, 2]
    ENEMY_PROMOTION_ZONE = [6, 7, 8]

    def __init__(self) -> None:
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.init_board()
        self.pieces = {
            'K': King, 'R': Rook, 'B': Bishop, 'G': GGeneral,
            'S': SGeneral, 'N': Knight, 'L': Lance, 'P': Pawn
        }

    def init_board(self) -> None:
        '''
        # Initial board
        ---------------------
        9 | L| N| S| G| K| G| S| N| L|
        8 |__| R|__|__|__|__|__| B|__|
        7 | P| P| P| P| P| P| P| P| P|
        6 |__|__|__|__|__|__|__|__|__|
        5 |__|__|__|__|__|__|__|__|__|
        4 |__|__|__|__|__|__|__|__|__|
        3 | p| p| p| p| p| p| p| p| p|
        2 |__| b|__|__|__|__|__| r|__|
        1 | l| n| s| g| k| g| s| n| l|
            a  b  c  d  e  f  g  h  i

        Our Captures:
        Enemy Captures:
        '''
        # Enemy pieces (team = 1)
        self.board[0] = [Lance('L', 1), Knight('N', 1), SGeneral('S', 1), GGeneral('G', 1), King('K', 1), GGeneral('G', 1), SGeneral('S', 1), Knight('N', 1), Lance('L', 1)]
        self.board[1][1] = Rook('R', 1)
        self.board[1][7] = Bishop('B', 1)
        self.board[2] = [Pawn('P', 1), Pawn('P', 1), Pawn('P', 1), Pawn('P', 1), Pawn('P', 1), Pawn('P', 1), Pawn('P', 1), Pawn('P', 1), Pawn('P', 1)]

        # Our pieces (team = 0)
        self.board[6] = [Pawn('p', 0), Pawn('p', 0), Pawn('p', 0), Pawn('p', 0), Pawn('p', 0), Pawn('p', 0), Pawn('p', 0), Pawn('p', 0), Pawn('p', 0)]
        self.board[7][1] = Bishop('b', 0)
        self.board[7][7] = Rook('r', 0)
        self.board[8] = [Lance('l', 0), Knight('n', 0), SGeneral('s', 0), GGeneral('g', 0), King('k', 0), GGeneral('g', 0), SGeneral('s', 0), Knight('n', 0), Lance('l', 0)]


    def has_piece(self, position: Tuple[int, int]) -> bool:
        if not in_board(position):
            raise Exception("Incorrect position!")

        r, c = position
        return True if self.board[r][c] else False
    
    
    def execute_move(self, move_command: str, player: int) -> None:
        '''
        Move ex: a3a4
        Promotion move ex: h6h7+

        Drops are written as a piece letter in upper case
        Drop ex: P*d3 or p*d3
        '''


        if move_command[1] != '*':
            src_c, src_r, _ = parse_pos(move_command[:2])
            dst_c, dst_r, is_promoted = parse_pos(move_command[2:])

            print((src_r, src_c))
            print((dst_r, dst_c))

            # Execute move
            if not self.has_piece((src_r, src_c)):
                raise Exception("No piece in the position")
            obj_piece = self.board[src_r][src_c]
            
            valid_moves = obj_piece.get_valid_moves((src_r, src_c), self.board)
            print(f"valid_moves: {valid_moves}")
            if (dst_r, dst_c) not in valid_moves:
                raise Exception("This move is invalid!")
            
            if is_promoted:
                if (player == 0 and dst_r not in self.OUR_PROMOTION_ZONE) or (player == 1 and dst_r not in self.ENEMY_PROMOTION_ZONE):
                    raise Exception("This move can't promote!")
                obj_piece.promoted = True
            
            self.board[src_r][src_c] = None
        else:
            piece, _ = move_command[:2]
            dst_r, dst_c, _ = parse_pos(move_command[2:])  # Drop piece hasn't promotion.

            obj_piece = self.board[dst_r][dst_c]
            if obj_piece:
                raise Exception("Can't drop the position, because the position has piece!")
            
            if player:
                obj_piece = self.pieces[piece](piece.lower(), 1)
            else:
                obj_piece = self.pieces[piece.upper()](piece.upper(), 0)

        self.board[dst_r][dst_c] = obj_piece
        

    def display_board(self) -> None:
        for i, row in enumerate(self.board):
            row_content = []

            for piece in row:
                if piece:
                    row_content.append(f" {piece}|")
                else:
                    row_content.append("__|")

            print(f"{9 - i} |{''.join(row_content)}")

        print("    " + "  ".join([chr(i + 97) for i in range(9)]))

    # def get_winner(self):
    


if __name__ == '__main__':
    board = shogiBoard()
    board.display_board()

    board.execute_move('a3a4', 0)
    board.display_board()
    
    board.execute_move('b2a3', 0)
    board.display_board()