from typing import Tuple, List, Set
from collections import defaultdict
from utils import parse_string_to_pos, parse_drop_to_string
from piece import *
from player import shogiPlayer

import copy
    
class shogiBoard:
    PIECES = {'K': King, 'R': Rook, 'B': Bishop, 'G': GGeneral, 'S': SGeneral, 'N': Knight, 'L': Lance, 'P': Pawn}

    OUR_PROMOTION_ZONE = [0, 1, 2]
    ENEMY_PROMOTION_ZONE = [6, 7, 8]
    
    OUR_NL_DROP_FORBIDDEN_ZONE = [7, 8]
    ENEMY_NL_DROP_FORBIDDEN_ZONE = [0, 1]

    OUR_P_DROP_FORBIDDEN_ZONE = 8
    ENEMY_P_DROP_FORBIDDEN_ZONE = 0

    OUR_PIECES_NAME = ['r', 'b', 'g', 's', 'n', 'l', 'p',
                       '+r', '+b', '+g', '+s', '+n', '+l', '+p']
    ENEMY_PIECES_NAME = ['R', 'B', 'G', 'S', 'N', 'L', 'P',
                         '+R', '+B', '+G', '+S', '+N', '+L', '+P']
    
    PAWN_PIECE_NAME = ['p', 'P']
    KINGHT_LANCE_PIECE_NAME = ['n', 'l', 'N', 'L']


    def __init__(self, player0: shogiPlayer, player1: shogiPlayer) -> None:
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.our_player = player0
        self.enemy_player = player1
        self.our_king_pos = (8, 4)
        self.enemy_king_pos = (0, 4)
        self.init_board()


    def init_board(self) -> None:
        '''
        Initial board
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
        # Enemy pieces (team = -1)
        self.board[0] = [Lance('L', -1), Knight('N', -1), SGeneral('S', -1), GGeneral('G', -1), King('K', -1), GGeneral('G', -1), SGeneral('S', -1), Knight('N', -1), Lance('L', -1)]
        self.board[1][1] = Rook('R', -1)
        self.board[1][7] = Bishop('B', -1)
        self.board[2] = [Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1)]

        # Our pieces (team = 1)
        self.board[6] = [Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1)]
        self.board[7][1] = Bishop('b', 1)
        self.board[7][7] = Rook('r', 1)
        self.board[8] = [Lance('l', 1), Knight('n', 1), SGeneral('s', 1), GGeneral('g', 1), King('k', 1), GGeneral('g', 1), SGeneral('s', 1), Knight('n', 1), Lance('l', 1)]


    def _has_piece(self, board, position: Tuple[int, int]) -> bool:
        if not in_board(position):
            raise Exception("Incorrect position!")

        r, c = position
        return True if board[r][c] else False
    

    def display_board(self) -> None:
        '''Print self.board'''
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
    
    
    def execute_move(self, move_command: str, player: shogiPlayer) -> None:
        '''
        實際的移動步

        Move ex: a3a4
        Promotion move ex: h6h7+

        Drops are written as a piece letter in upper case
        Drop ex: P*d4 or R*g5
        '''
        board = copy.deepcopy(self.board)

        if move_command[1] != '*':
            src_r, src_c, _ = parse_string_to_pos(move_command[:2])
            dst_r, dst_c, is_promoted = parse_string_to_pos(move_command[2:])

            # Execute move
            if not self._has_piece(board, (src_r, src_c)):
                raise Exception("No piece in the position")
            obj_piece = self.board[src_r][src_c]
            
            valid_moves = obj_piece.get_valid_moves((src_r, src_c), self.board)
            print(f"move_command: {move_command}")
            print(f"valid_moves: {valid_moves}")
            if move_command not in valid_moves:
                raise Exception("This move is invalid!")
            elif self.board[dst_r][dst_c] and self.board[dst_r][dst_c].team == -player.team:
                player.capture(self.board[dst_r][dst_c])
            
            # Promote!
            if is_promoted:
                if obj_piece.promoted or (player.team == 1 and dst_r not in self.OUR_PROMOTION_ZONE) or (player.team == -1 and dst_r not in self.ENEMY_PROMOTION_ZONE):
                    raise Exception("This move can't promote!")
                obj_piece.promoted = True
            
            self.board[src_r][src_c] = None
            self.board[dst_r][dst_c] = obj_piece

            if obj_piece.name == 'k':
                self.our_king_pos = (dst_r, dst_c)
            elif obj_piece.name == 'K':
                self.enemy_king_pos = (dst_r, dst_c)
        else:
            piece_name, _ = move_command[:2]
            dst_r, dst_c, _ = parse_string_to_pos(move_command[2:])  # Drop piece hasn't promotion.

            # Check the pos and piece could drop?
            if not self._can_drop_piece(piece_name, (dst_r, dst_c), player):
                raise Exception("Can't drop to the position!")
            
            if player.team == 1:
                obj_piece = self.PIECES[piece_name](piece_name.lower(), 1)
            else:
                obj_piece = self.PIECES[piece_name.upper()](piece_name.upper(), -1)

            player.drop(piece_name)
            self.board[dst_r][dst_c] = obj_piece


    def _can_drop_piece(self, piece_name: str, drop_pos: Tuple[int, int], player: shogiPlayer) -> bool:
        # 1. 檢查是否可以在指定位置打入棋子
        drop_r, drop_c = drop_pos
        board = copy.deepcopy(self.board)

        if self._has_piece(board, (drop_r, drop_c)):
            return False

        # 2. 禁止打入無法移動的棋子
        if piece_name in self.KINGHT_LANCE_PIECE_NAME:  # 檢查桂馬與香車
            if (player.team == 1 and drop_r in self.OUR_NL_DROP_FORBIDDEN_ZONE) or (player.team == -1 and drop_r in self.ENEMY_NL_DROP_FORBIDDEN_ZONE):
                return False
        elif piece_name in self.PAWN_PIECE_NAME:  # 檢查步兵
            if (player.team == 1 and drop_r == self.OUR_P_DROP_FORBIDDEN_ZONE) or (player.team == -1 and drop_r == self.ENEMY_P_DROP_FORBIDDEN_ZONE):
                return False

        if piece_name in self.PAWN_PIECE_NAME:
            # 3. 二步規則
            if (player.team == 1 and any(str(board[rol][drop_c]) == 'p' for rol in range(9))) or (player.team == -1 and any(str(board[rol][drop_c]) == 'P' for rol in range(9))):
                return False
            
            # 4. 打步詰規則
            if player.team == 1:
                obj_piece = self.PIECES[piece_name](piece_name.lower(), 1)
            else:
                obj_piece = self.PIECES[piece_name.upper()](piece_name.upper(), -1)

            board[drop_r][drop_c] = obj_piece
            if self.is_in_check(board, player) and len(self.get_all_evade_moves(board, player)) == 0:
                return False
            board[drop_r][drop_c] = None

        return True


    def is_in_check(self, board, player: shogiPlayer) -> bool:
        '''
        檢查王將/玉將是否被將軍
        '''
        king_pos = self.our_king_pos if player.team == 1 else self.enemy_king_pos
        all_enemy_pieces = self.ENEMY_PIECES_NAME if player.team == 1 else self.OUR_PIECES_NAME
        all_enemy_moves = []

        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell in all_enemy_pieces:
                    valid_moves = cell.get_valid_moves((r, c), board)
                    all_enemy_moves.append(valid_moves)

        return king_pos in all_enemy_moves
    

    def _get_king_evade_moves(self, board, king_pos: Tuple[int, int], player: shogiPlayer) -> List[str]:
        '''
        王將/玉將不會被將軍的移動
        '''
        all_enemy_pieces = self.ENEMY_PIECES_NAME if player.team == 1 else self.OUR_PIECES_NAME
        all_enemy_moves = []

        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell in all_enemy_pieces:
                    valid_moves = cell.get_valid_moves((r, c), self.board)
                    all_enemy_moves.append(valid_moves)
        
        king_r, king_c = king_pos
        king = self.board[king_r][king_c]
        king_valid_moves = king.get_valid_moves((king_r, king_c), self.board)
        
        king_safe_moves = list(set(king_valid_moves) - set(all_enemy_moves))
        return king_safe_moves


    def _get_piece_evade_moves(self, board, player: shogiPlayer) -> List[str]:
        '''
        檢查一般棋子移動後是否仍然被將軍，如果王將不再被將軍，則該移動是一個有效的閃避走步
        '''
        piece_evade_moves = []
        all_our_moves = []
        all_our_pieces = self.OUR_PIECES_NAME if player.team == 1 else self.ENEMY_PIECES_NAME

        for src_r, row in enumerate(board):
            for src_c, cell in enumerate(row):
                if cell in all_our_pieces:
                    valid_moves = cell.get_valid_moves((src_r, src_c), board)
                    all_our_moves.append(valid_moves)

        for move in all_our_moves:
            src_r, src_c, _ = parse_string_to_pos(move[:2])
            dst_r, dst_c, is_promoted = parse_string_to_pos(move[2:])

            # 先移動看看
            piece = board[src_r][src_c]
            board[src_r][src_c] = None
            if is_promoted:
                piece.promoted = True
            board[dst_r][dst_c] = piece

            if not self.is_in_check(board, player):  # 檢查移動後王將是否仍然被將軍
                piece_evade_moves.append(move)

            # 檢查後盤面需復原
            piece = board[dst_r][dst_c]
            board[dst_r][dst_c] = None
            if is_promoted:
                piece.promoted = False
            board[src_r][src_c] = piece

        return piece_evade_moves


    def _get_drop_evade_moves(self, board, player: shogiPlayer) -> List[str]:
        all_evade_drops = []
        all_our_captured = player.captured
        all_empty_cells = self._get_all_empty_cells()

        for piece_name in all_our_captured:
            for drop_pos in all_empty_cells:
                dst_r, dst_c = drop_pos

                # 先打入看看
                if self._can_drop_piece(piece_name, drop_pos, player):
                    board[dst_r][dst_c] = piece_name

                if not self.is_in_check(board, player):  # 檢查移動後王將是否仍然被將軍
                    move = parse_drop_to_string(piece_name, drop_pos)
                    all_evade_drops.append(move)

                # 檢查後盤面需復原
                board[dst_r][dst_c] = None

        return all_evade_drops


    def get_all_evade_moves(self, board, player: shogiPlayer):
        all_evade_moves = self._get_king_evade_moves(board, player)
        all_evade_moves.extend(self._get_piece_evade_moves(board, player))
        all_evade_moves.extend(self._get_drop_evade_moves(board, player))

        return all_evade_moves
    

    def _get_all_empty_cells(self) -> List[Tuple[int, int]]:
        all_empty_cells = []

        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if not cell:
                    all_empty_cells.append((r, c))

        return all_empty_cells
    

    def get_winner(self, our_player: shogiPlayer, enemy_player: shogiPlayer):
        '''
        Input:
            player: current player (1 or -1)

        Returns:
            winner: 0 if game has not ended. 1 if player won, -1 if player lost,
                    small non-zero value for draw.
        '''
        winner = 0
        board = copy.deepcopy(self.board)

        # 先檢查我方是否被將死
        is_our_king_check = self.is_in_check(board, our_player)
        all_evade_moves = self.get_all_evade_moves(board, our_player)
        if is_our_king_check and len(all_evade_moves) == 0:
            winner = enemy_player.team

        # 再檢查敵方是否被將死
        is_enemy_king_check = self.is_in_check(board, enemy_player)
        all_evade_moves = self.get_all_evade_moves(board, our_player)
        if is_enemy_king_check and len(all_evade_moves) == 0:
            winner = our_player.team

        return winner


if __name__ == '__main__':
    player1 = shogiPlayer(1)
    player2 = shogiPlayer(-1)
    board = shogiBoard(player0=player1, player1=player2)
    
    board.display_board()

    board.execute_move('a3a4', player1)
    board.execute_move('a4a5', player1)
    board.execute_move('a5a6', player1)
    board.execute_move('a6a7+', player1)
    board.execute_move('a7a8', player1)
    board.execute_move('a8b8', player1)
    board.display_board()
    
    board.execute_move('f7f6', player2)
    board.display_board()

    board.execute_move('P*a8', player1)
    board.display_board()

    board.execute_move('R*g5', player1)
    board.display_board()