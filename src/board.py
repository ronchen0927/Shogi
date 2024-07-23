from typing import Tuple, List, Set

from src.utils import parse_string_to_pos, parse_drop_to_string
from src.piece import *
from src.player import ShogiPlayer

import copy

class ShogiBoard:
    PIECES = {'K': King, 'R': Rook, 'B': Bishop, 'G': GGeneral, 'S': SGeneral, 'N': Knight, 'L': Lance, 'P': Pawn}

    OUR_PROMOTION_ZONE = [0, 1, 2]
    OPPONENT_PROMOTION_ZONE = [6, 7, 8]
    
    OUR_NL_DROP_FORBIDDEN_ZONE = [0, 1]
    OPPONENT_NL_DROP_FORBIDDEN_ZONE = [7, 8]

    OUR_P_DROP_FORBIDDEN_ZONE = 0
    OPPONENT_P_DROP_FORBIDDEN_ZONE = 8

    OUR_PIECES_NAME = ['k', 'r', 'b', 'g', 's', 'n', 'l', 'p', '+r', '+b', '+s', '+n', '+l', '+p']
    OPPONENT_PIECES_NAME = ['K', 'R', 'B', 'G', 'S', 'N', 'L', 'P', '+R', '+B', '+S', '+N', '+L', '+P']
    
    PAWN_PIECE_NAME = ['p', 'P']
    KINGHT_LANCE_PIECE_NAME = ['n', 'l', 'N', 'L']


    def __init__(self, our_player: ShogiPlayer, opponent_player: ShogiPlayer) -> None:
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self._our_player = our_player
        self._opponent_player = opponent_player
        self.init_board()


    @property
    def opponent_player(self):
        return self._opponent_player
    
    @opponent_player.setter
    def opponent_player(self, opponent_player):
        self._opponent_player = opponent_player


    def __repr__(self) -> str:
        '''Print board for human to see'''
        str_board = ""

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

            str_board += f"{9 - idx} |{''.join(row_content)}\n"

        str_board += "    " + "  ".join([chr(idx + 97) for idx in range(9)]) + "\n"
        str_board += "\n"
        str_board += f"Our Captures: {' '.join(self._our_player.captured)}\n"
        str_board += f"Opponent Captures: {' '.join(self._opponent_player.captured)}\n"
        str_board += "\n"
        str_board += f"我方玩家: {self._our_player}\n"
        str_board += f"敵方玩家: {self._opponent_player}\n"

        return str_board


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
        Opponent Captures:
        '''
        # Opponent pieces (team = -1)
        self.board[0] = [Lance('L', -1), Knight('N', -1), SGeneral('S', -1), GGeneral('G', -1), King('K', -1), GGeneral('G', -1), SGeneral('S', -1), Knight('N', -1), Lance('L', -1)]
        self.board[1][1] = Rook('R', -1)
        self.board[1][7] = Bishop('B', -1)
        self.board[2] = [Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1), Pawn('P', -1)]

        # Our pieces (team = 1)
        self.board[6] = [Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1), Pawn('p', 1)]
        self.board[7][1] = Bishop('b', 1)
        self.board[7][7] = Rook('r', 1)
        self.board[8] = [Lance('l', 1), Knight('n', 1), SGeneral('s', 1), GGeneral('g', 1), King('k', 1), GGeneral('g', 1), SGeneral('s', 1), Knight('n', 1), Lance('l', 1)]

    
    def insert_board(self, customization_board):
        self.board = customization_board


    def _has_piece(self, board, position: Tuple[int, int]) -> bool:
        if not is_in_board(position):
            raise Exception("Incorrect position!")

        r, c = position
        return True if board[r][c] else False
    
    
    def execute_move(self, move_command: str, player: ShogiPlayer) -> None:
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
                raise Exception("No piece in the position!")
            obj_piece = board[src_r][src_c]
            
            if obj_piece.team != player.team:
                raise Exception("You can't move opponent pieces!")
            
            valid_moves = obj_piece.get_valid_moves((src_r, src_c), board)

            if move_command not in valid_moves:
                raise Exception("This move is invalid!")
            elif board[dst_r][dst_c] and board[dst_r][dst_c].team == -player.team:
                player.capture(board[dst_r][dst_c])
            
            # Promote!
            if is_promoted:
                if obj_piece.promoted or (player.team == 1 and dst_r not in self.OUR_PROMOTION_ZONE) or (player.team == -1 and dst_r not in self.OPPONENT_PROMOTION_ZONE):
                    raise Exception("This move can't promote!")
                obj_piece.promoted = True
            
            board[src_r][src_c] = None
            board[dst_r][dst_c] = obj_piece
        else:
            piece_name, _ = move_command[:2]
            dst_r, dst_c, _ = parse_string_to_pos(move_command[2:])  # Drop piece hasn't promotion.

            # Check the pos and piece could drop?
            if not self._can_drop_piece(board, piece_name, (dst_r, dst_c), player):
                raise Exception("Can't drop to the position!")
            
            if player.team == 1:
                obj_piece = self.PIECES[piece_name.upper()](piece_name.lower(), player.team)
            else:
                obj_piece = self.PIECES[piece_name.upper()](piece_name.upper(), player.team)

            player.drop(piece_name)
            board[dst_r][dst_c] = obj_piece

        self.board = board
        

    def _find_both_king_pos(self, board: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        '''
        找尋目前王將/玉將的位置
        如果是 (-1, -1) 代表有一方的王將/玉將已經被吃掉了
        '''
        our_king_pos, opponent_king_pos = (-1, -1), (-1, -1)
        
        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell and cell.name == 'k':
                    our_king_pos = (r, c)
                elif cell and cell.name == 'K':
                    opponent_king_pos = (r, c)

        return our_king_pos, opponent_king_pos


    def _can_drop_piece(self, board: List[List[str]], piece_name: str, drop_pos: Tuple[int, int], player: ShogiPlayer, is_check_last_rule: bool = True) -> bool:
        # 1. 檢查是否可以在指定位置打入棋子
        drop_r, drop_c = drop_pos
        if self._has_piece(board, (drop_r, drop_c)):
            return False

        # 2. 禁止打入無法移動的棋子
        if piece_name in self.KINGHT_LANCE_PIECE_NAME:  # 檢查桂馬與香車
            if (player.team == 1 and drop_r in self.OUR_NL_DROP_FORBIDDEN_ZONE) or (player.team == -1 and drop_r in self.OPPONENT_NL_DROP_FORBIDDEN_ZONE):
                return False
        elif piece_name in self.PAWN_PIECE_NAME:  # 檢查步兵
            if (player.team == 1 and drop_r == self.OUR_P_DROP_FORBIDDEN_ZONE) or (player.team == -1 and drop_r == self.OPPONENT_P_DROP_FORBIDDEN_ZONE):
                return False

        if piece_name in self.PAWN_PIECE_NAME:
            # 3. 二步規則
            if (player.team == 1 and any(str(board[rol][drop_c]) == 'p' for rol in range(9))) or (player.team == -1 and any(str(board[rol][drop_c]) == 'P' for rol in range(9))):
                return False
            
            # 4. 打步詰規則
            if is_check_last_rule:
                if player.team == 1:
                    obj_piece = self.PIECES[piece_name.upper()](piece_name.lower(), player.team)
                else:
                    obj_piece = self.PIECES[piece_name.upper()](piece_name.upper(), player.team)

                board[drop_r][drop_c] = obj_piece

                # 如果打入後，王將/玉將會被將死，則不可打入
                if len(self.get_all_king_evade_moves(board, player)) == 0:
                    return False

        return True


    def is_in_check(self, board: List[List[str]], player: ShogiPlayer) -> bool:
        '''
        檢查王將/玉將是否被將軍
        '''
        all_opponent_pieces_name = self.OPPONENT_PIECES_NAME if player.team == 1 else self.OUR_PIECES_NAME
        all_opponent_moves = []

        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell and (cell.name in all_opponent_pieces_name):
                    valid_moves = cell.get_valid_moves((r, c), board)
                    all_opponent_moves.extend(valid_moves)

        king_r, king_c = self._find_both_king_pos(board)[0] if player.team == 1 else self._find_both_king_pos(board)[1]
        if (king_r, king_c) == (-1, -1):
            return False
        
        king = board[king_r][king_c]
        king_valid_moves = king.get_valid_moves((king_r, king_c), board)
        king_src_pos = king_valid_moves[-1][:2]  # 隨機取一個移動步，然後取前半段，即為當前位置(src)的 notation
        all_opponent_dst = [move[2:4] for move in all_opponent_moves]  # 取 dst 且不取升變步的 notation

        return king_src_pos in set(all_opponent_dst)
    

    def _get_king_evade_moves(self, board: List[List[str]], player: ShogiPlayer) -> Set[str]:
        '''
        得到王將/玉將不會被將軍的移動走步
        '''
        all_opponent_pieces_name = self.OPPONENT_PIECES_NAME if player.team == 1 else self.OUR_PIECES_NAME
        all_opponent_moves = []

        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell and (cell.name in all_opponent_pieces_name):
                    valid_moves = cell.get_valid_moves((r, c), board)
                    all_opponent_moves.extend(valid_moves)
        
        king_r, king_c = self._find_both_king_pos(board)[0] if player.team == 1 else self._find_both_king_pos(board)[1]
        if (king_r, king_c) == (-1, -1):
            return False
        
        king = board[king_r][king_c]
        king_valid_moves = king.get_valid_moves((king_r, king_c), board)
        king_src_pos = king_valid_moves[-1][:2]  # 隨機取一個移動步，然後取前半段，即為當前位置(src)的 notation
        all_king_dst = [king_src_pos] + [move[2:] for move in king_valid_moves]
        all_opponent_dst = [move[2:4] for move in all_opponent_moves]  # 取所有 dst 且不取升變步的 notation
        king_safe_pos = list(set(all_king_dst) - set(all_opponent_dst))

        king_evade_moves = set([king_src_pos + king_dst_pos for king_dst_pos in king_safe_pos])  # concate back to king evade move
        return king_evade_moves


    def _get_piece_evade_moves(self, board: List[List[str]], player: ShogiPlayer) -> Set[str]:
        '''
        檢查一般棋子移動後是否仍然被將軍，如果王將不再被將軍，則該移動是一個有效的閃避走步
        '''
        piece_evade_moves = []
        all_our_moves = []
        all_our_pieces_name = self.OUR_PIECES_NAME if player.team == 1 else self.OPPONENT_PIECES_NAME

        for src_r, row in enumerate(board):
            for src_c, cell in enumerate(row):
                if cell and (cell.name in all_our_pieces_name):
                    valid_moves = cell.get_valid_moves((src_r, src_c), board)
                    all_our_moves.extend(valid_moves)

        for move in all_our_moves:
            src_r, src_c, _ = parse_string_to_pos(move[:2])
            dst_r, dst_c, is_promoted = parse_string_to_pos(move[2:])

            # 先移動看看
            piece = board[src_r][src_c]
            temp = board[dst_r][dst_c]
            if is_promoted:
                piece.promoted = True
            board[src_r][src_c] = None
            board[dst_r][dst_c] = piece

            # 王將/玉將的位置
            our_king_pos, opponent_king_pos = self._find_both_king_pos(board)

            if our_king_pos != (-1, -1) and opponent_king_pos != (-1, -1) and not self.is_in_check(board, player):  # 王將/玉將存在，且王將/玉將是否仍然被將軍
                piece_evade_moves.append(move)

            # 檢查後盤面需復原
            piece = board[dst_r][dst_c]
            if is_promoted:
                piece.promoted = False
            board[dst_r][dst_c] = temp
            board[src_r][src_c] = piece

        return set(piece_evade_moves)


    def _get_drop_evade_moves(self, board: List[List[str]], player: ShogiPlayer) -> Set[str]:
        '''
        檢查一般棋子打入後是否仍然被將軍，如果王將不再被將軍，則該移動是一個有效的打躲避走步
        '''
        all_evade_drops = []
        all_our_captured = player.captured
        all_empty_cells = self._get_all_empty_cells()

        for piece_name in all_our_captured:
            for drop_pos in all_empty_cells:
                dst_r, dst_c = drop_pos

                # 打入，這邊只需檢查前三個規則
                if self._can_drop_piece(board, piece_name, drop_pos, player, is_check_last_rule=False):
                    board[dst_r][dst_c] = self.PIECES[piece_name.upper()](piece_name, player.team)

                if not self.is_in_check(board, player):  # 檢查打入後，王將是否仍然被將軍
                    move = parse_drop_to_string(piece_name, drop_pos)
                    all_evade_drops.append(move)

                # 檢查後盤面需復原
                board[dst_r][dst_c] = None

        return set(all_evade_drops)
    

    def _get_all_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get all empty cells on the board
        """
        all_empty_cells = []

        for r, row in enumerate(self.board):
            for c, cell in enumerate(row):
                if not cell:
                    all_empty_cells.append((r, c))

        return all_empty_cells


    def get_all_king_evade_moves(self, board: List[List[str]], player: ShogiPlayer) -> Set[str]:
        """
        Get all king evade moves
        """
        king_evade_moves = self._get_king_evade_moves(board, player)
        king_evade_moves &= self._get_piece_evade_moves(board, player)
        king_evade_moves |= self._get_drop_evade_moves(board, player)

        return king_evade_moves
    

    # 列出該玩家所有的合法走步與合法打入
    def get_all_valid_moves_and_drops(self, board: List[List[str]], player: ShogiPlayer) -> Tuple[Set[str], Set[str]]:
        all_valid_moves = set()
        all_valid_drops = set()
        all_our_pieces_name = self.OUR_PIECES_NAME if player.team == 1 else self.OPPONENT_PIECES_NAME

        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                if cell and cell.name in all_our_pieces_name:
                    valid_moves = cell.get_valid_moves((r, c), board)
                    all_valid_moves |= set(valid_moves)

        all_empty_cells = self._get_all_empty_cells()
        all_our_captured = player.captured

        for piece_name in all_our_captured:
            for drop_pos in all_empty_cells:
                if self._can_drop_piece(board, piece_name, drop_pos, player):
                    move = parse_drop_to_string(piece_name, drop_pos)
                    all_valid_drops.add(move)

        return all_valid_moves, all_valid_drops