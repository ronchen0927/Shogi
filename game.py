from src.player import ShogiPlayer
from src.board import ShogiBoard
from src.piece import *

import copy

class ShogiGame:
    def __init__(self) -> None:
        self.players = [ShogiPlayer("Gojo Satoru", 1), ShogiPlayer("Geto Suguru", -1)]
        self.board = ShogiBoard(self.players[0], self.players[1])
        self.current_player = self.players[0]
        self.game_round = 0


    def get_game_ended(self, board: List[List[str]], our_player: ShogiPlayer, opponent_player: ShogiPlayer) -> int:            
        '''
        Input:
            board: 2D list of ShogiPiece objects
            our_player: 1
            opponent_player: -1

        Returns:
            result: 0 if game has not ended. 1 if player won, -1 if player lost,
                    small non-zero value for draw.
        '''
        result = 0

        # 先檢查我方是否被將死
        is_our_king_check = self.board.is_in_check(board, our_player)
        our_all_evade_moves = self.board.get_all_king_evade_moves(board, our_player)
        if 'k' in opponent_player.captured or (is_our_king_check and len(our_all_evade_moves) == 0):
            result = opponent_player.team

        # 再檢查敵方是否被將死
        is_opponent_king_check = self.board.is_in_check(board, opponent_player)
        opponent_all_evade_moves = self.board.get_all_king_evade_moves(board, opponent_player)
        if 'K' in our_player.captured or (is_opponent_king_check and len(opponent_all_evade_moves) == 0):
            result = our_player.team

        return result


    def play(self):
        while True:
            self.current_player = self.players[self.game_round % 2]

            print(f"Round: {self.game_round + 1}\nCurrent Player : {self.current_player.name}\n")
            print(self.board)

            input_move = input('Input your move: ').replace(" ", "")  # truncation all space

            try:
                self.board.execute_move(input_move, self.current_player)
                board = copy.deepcopy(self.board)
                result = self.get_game_ended(board, self.players[0], self.players[1])

                if result:
                    # Game over
                    winner = result
                    # Final board
                    print(self.board)

                    if winner == 1:
                        print(f"Winner is {self.players[0].name}")
                    else:
                        print(f"Winner is {self.players[1].name}")

                    break
                
                self.game_round += 1
                print('-' * 35)
            except Exception as e:
                print(f"Error message: {e}")
                print('-' * 35)
                continue


if __name__ == "__main__":
    game = ShogiGame()
    game.play()