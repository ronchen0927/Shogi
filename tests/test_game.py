from game import *


def test_uchifuzume():
    uchifuzume_board = [[None for _ in range(9)] for _ in range(9)]  # 打步詰盤面測試
    uchifuzume_board[0] = [Lance('L', -1), None, None, None, None, None, None, Knight('N', -1), Lance('L', -1)]
    uchifuzume_board[1] = [None, None, None, Rook('r', 1), Bishop('b', 1, True), Knight('N', -1), King('K', -1), None, None]
    uchifuzume_board[2] = [None, GGeneral('G', -1), None, Pawn('p', 1), Pawn('P', -1), Pawn('P', -1), None, None, Pawn('P', -1)]
    uchifuzume_board[3] = [None, None, Pawn('P', -1), None, None, None, None, None, None]
    uchifuzume_board[4] = [None, None, None, None, SGeneral('S', -1), None, SGeneral('s', 1), SGeneral('S', -1), Pawn('p', 1)]
    uchifuzume_board[5] = [None, King('k', 1), Bishop('B', -1), Pawn('P', -1), None, None, None, None, Rook('r', 1)]
    uchifuzume_board[6] = [Pawn('p', 1), None, None, SGeneral('S', -1), Pawn('p', 1), Pawn('p', 1), Pawn('P', -1), None, None]
    uchifuzume_board[7] = [None, None, GGeneral('G', -1), None, None, None, None, Pawn('P', -1, True), None]
    uchifuzume_board[8] = [Lance('l', 1), None, None, None, None, None, None, Knight('n', 1), Lance('l', 1)]

    game = ShogiGame()
    game.board.insert_board(uchifuzume_board)
    game.players[0].captured = ['P', 'P', 'P', 'P', 'P', 'N', 'G', 'G']
    game.players[1].captured = ['p']
    game.board.our_king_pos = (5, 1)
    game.board.opponent_king_pos = (1, 6)

    game.board.execute_move('i1i3', game.players[0])
    game.board.execute_move('p*b5', game.players[1])

    assert game.get_game_ended(game.players[0], game.players[1]) == -1  # opponent player win