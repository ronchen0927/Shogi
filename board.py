from typing import Tuple, List
from utils import parse_pos
from piece import *
from player import shogiPlayer
    
class shogiBoard:
    PIECES = {
        'K': King, 'R': Rook, 'B': Bishop, 'G': GGeneral,
        'S': SGeneral, 'N': Knight, 'L': Lance, 'P': Pawn
    }
    OUR_PROMOTION_ZONE = [0, 1, 2]
    ENEMY_PROMOTION_ZONE = [6, 7, 8]
    OUR_PIECES_NAME = ['r', 'b', 'g', 's', 'n', 'l', 'p',
                       '+r', '+b', '+g', '+s', '+n', '+l', '+p']
    ENEMY_PIECES_NAME = ['R', 'B', 'G', 'S', 'N', 'L', 'P',
                         '+R', '+B', '+G', '+S', '+N', '+L', '+P']

    def __init__(self, player0: shogiPlayer, player1: shogiPlayer) -> None:
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.our_player = player0
        self.enemy_player = player1
        self.our_king_pos = (8, 4)
        self.enemy_king_pos = (0, 4)
        self.init_board()


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


    def _has_piece(self, position: Tuple[int, int]) -> bool:
        if not in_board(position):
            raise Exception("Incorrect position!")

        r, c = position
        return True if self.board[r][c] else False
    
    
    def execute_move(self, move_command: str, player: shogiPlayer) -> None:
        '''
        Move ex: a3a4
        Promotion move ex: h6h7+

        Drops are written as a piece letter in upper case
        Drop ex: P*d4 or R*g5
        '''
        if move_command[1] != '*':
            src_r, src_c, _ = parse_pos(move_command[:2])
            dst_r, dst_c, is_promoted = parse_pos(move_command[2:])

            # print((src_r, src_c))
            # print((dst_r, dst_c))

            # Execute move
            if not self._has_piece((src_r, src_c)):
                raise Exception("No piece in the position")
            obj_piece = self.board[src_r][src_c]
            
            valid_moves = obj_piece.get_valid_moves((src_r, src_c), self.board)
            # print(f"valid_moves: {valid_moves}")
            if (dst_r, dst_c) not in valid_moves:
                raise Exception("This move is invalid!")
            elif self.board[dst_r][dst_c] and self.board[dst_r][dst_c].team == 1 - player.team:
                player.capture(self.board[dst_r][dst_c])
            
            if is_promoted:
                if obj_piece.promoted or (player.team == 0 and dst_r not in self.OUR_PROMOTION_ZONE) or (player.team == 1 and dst_r not in self.ENEMY_PROMOTION_ZONE):
                    raise Exception("This move can't promote!")
                obj_piece.promoted = True
            
            self.board[src_r][src_c] = None
            self.board[dst_r][dst_c] = obj_piece

            if obj_piece.name == 'k':
                self.our_king_pos = (dst_r, dst_c)
            elif obj_piece.name == 'K':
                self.enemy_king_pos = (dst_r, dst_c)
        else:
            piece, _ = move_command[:2]
            dst_r, dst_c, _ = parse_pos(move_command[2:])  # Drop piece hasn't promotion.

            if piece not in player.captured:
                raise Exception("Player capture isn't having the piece to drop!")
            
            if self._has_piece((dst_r, dst_c)):
                raise Exception("Has piece in the position or not in bound!")
            
            obj_piece = self.board[dst_r][dst_c]
            if obj_piece:
                raise Exception("Can't drop the position, because the position has piece!")
            
            if player.team == 0:
                obj_piece = self.PIECES[piece](piece.lower(), 1)
            else:
                obj_piece = self.PIECES[piece.upper()](piece.upper(), 0)

            player.drop(piece)
            self.board[dst_r][dst_c] = obj_piece
        

    def display_board(self) -> None:
        for idx, row in enumerate(self.board):
            row_content = []

            for piece in row:
                if piece:
                    if piece.promoted:
                        row_content.append(f"+{piece}|")
                    else:
                        row_content.append(f" {piece}|")
                else:
                    row_content.append("__|")

            print(f"{9 - idx} |{''.join(row_content)}")

        print("    " + "  ".join([chr(idx + 97) for idx in range(9)]))

        print("\n")

        print(f"Our Captures: {' '.join(self.our_player.captured)}")
        print(f"Enemy Captures: {' '.join(self.enemy_player.captured)}")

    
    def _check_two_pawn():
        '''
        檢查二步
        '''
        # TODO
        pass

    
    def _is_dropped_pawn_checkmate():
        '''
        檢查打步詰
        '''
        # TODO
        pass

    
    def _get_all_empty_position(self) -> List[Tuple[int, int]]:
        empty_cells = []

        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if not cell:
                    empty_cells.append((r, c))

        return empty_cells


    def _get_all_valid_drop(self, player: shogiPlayer):
        if not player.captured:
            return []
        
        empty_cells = self._get_all_empty_position()

        for piece in player.captured:
            if piece.name not in ['p', 'P']:
                return empty_cells
            else:
                self._check_two_pawn()
                self._is_dropped_pawn_checkmate()


    def is_in_check(self, is_for_enemy: bool = False) -> bool:
        '''
        is_for_enemy=False: 檢查我方王將是否被將軍
        is_for_enemy=True: 檢查敵方王將是否被將軍
        '''
        king_pos = self.enemy_king_pos if is_for_enemy else self.our_king_pos
        enemy_all_pieces_name = self.ENEMY_PIECES_NAME if is_for_enemy else self.OUR_PIECES_NAME
        enemy_all_moves = []

        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if cell in enemy_all_pieces_name:
                    valid_moves = cell.get_valid_moves((r, c), self.board)
                    enemy_all_moves.append(valid_moves)

        return set(king_pos) & set(enemy_all_moves)
    

    def find_avoidance_check_moves(self, is_for_enemy: bool = False):
        '''
        is_for_enemy=False: 找出我方王將被將軍時可以逃跑的走步
        is_for_enemy=True: 找出敵方王將被將軍時可以逃跑的走步
        '''
        king_pos = self.enemy_king_pos if is_for_enemy else self.our_king_pos
        enemy_all_pieces_name = self.ENEMY_PIECES_NAME if is_for_enemy else self.OUR_PIECES_NAME
        enemy_all_moves = []
        our_valid_drops = []

        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if cell in enemy_all_pieces_name:
                    valid_moves = cell.get_valid_moves((r, c), self.board)
                    enemy_all_moves.append(valid_moves)
        
        king_r, king_c = king_pos
        king = self.board[king_r][king_c]
        king_valid_moves = king.get_valid_moves((king_r, king_c), self.board)
        
        king_safe_moves = set(king_valid_moves) & set(enemy_all_moves)
        
        if is_for_enemy:
            our_valid_drops = self._get_all_valid_drop(self.enemy_player, self.board)
        else:
            our_valid_drops = self._get_all_valid_drop(self.our_player, self.board)


    def get_winner(self, player: shogiPlayer):
        '''
        Input:
            board: current board
            player: current player (player0 or player1)

        Returns:
            winner: -1 if game has not ended. 0 if our player won, 1 if enemy player won.
        '''
        winner = -1

        is_our_king_check = self.is_in_check()
        avoid_check_moves, avoid_check_drops = self.find_avoidance_check_moves()
        if is_our_king_check and len(avoid_check_moves) == 0 and len(avoid_check_drops) == 0:
            winner = 1 - player.team

        is_enemy_king_check, avoid_check_moves, avoid_check_drops = self.is_in_check(is_for_enemy=True)
        avoid_check_moves, avoid_check_drops = self.find_avoidance_check_moves(is_for_enemy=True)
        if is_enemy_king_check and len(avoid_check_moves) == 0 and len(avoid_check_drops) == 0:
            winner = player.team

        return winner


if __name__ == '__main__':
    player0 = shogiPlayer(0)
    player1 = shogiPlayer(1)
    board = shogiBoard(player0=player0, player1=player1)
    
    board.display_board()

    board.execute_move('a3a4', player0)
    board.execute_move('a4a5', player0)
    board.execute_move('a5a6', player0)
    board.execute_move('a6a7+', player0)
    board.execute_move('a7a8', player0)
    board.execute_move('a8b8', player0)
    board.display_board()
    
    board.execute_move('f7f6', player1)
    board.display_board()

    board.execute_move('P*a4', player0)
    board.display_board()

    board.execute_move('R*g5', player0)
    board.display_board()