from consts import *
from game_ import Game
import copy

class Handle:
    def __init__(self, game):
        self.game = game
        self.board = self.game.board
        self.player = 'white'
        self.bot = 'black'

    def handle(self):
        best_score = -float('inf')
        best_move = None
        best_piece = None
        for row in range(ROWS):
            for col in range(COLS):
                if not self.board.chess[row][col].isEmpty_or_rival(self.bot):
                    piece = self.board.chess[row][col].piece
                    piece.moves = []
                    self.board.calc_moves(piece, row, col)
                    actual_moves = piece.moves
                    for move in actual_moves:
                        opp = move.final.piece
                        self.board.make_move(piece, move)

                        score = self.minimax(2, False)
                        self.board.undo_move(move, piece, opp)

                        if score > best_score:
                            best_score = score
                            best_move = move
                            best_piece = piece

        print(f"best score is {best_score} and piece is {best_piece.name}")
        return (best_move, best_piece)

    def static_evaluation(self):
        white_score = 0
        black_score = 0

        for row in range(ROWS):
            for col in range(COLS):
                if not self.board.chess[row][col].isEmpty():
                    piece = self.board.chess[row][col].piece
                    if piece.color == "white":
                        white_score += piece.value
                    else:
                        black_score += piece.value

        return black_score - white_score

    def minimax(self, depth, maximizing_player):
        if depth == 0:
            return self.static_evaluation()

        if maximizing_player:
            max_eval = -float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if not self.board.chess[row][col].isEmpty_or_rival(self.bot):
                        piece = self.board.chess[row][col].piece
                        piece.moves = []
                        self.board.calc_moves(piece, row, col)
                        actual_moves = piece.moves
                        for move in actual_moves:
                            opp = move.final.piece
                            self.board.make_move(piece, move)
                            eval_ = self.minimax(depth - 1, False)
                            self.board.undo_move(move, piece, opp)
                            max_eval = max(max_eval, eval_)
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(ROWS):
                for col in range(COLS):
                    if not self.board.chess[row][col].isEmpty_or_rival(self.player):
                        piece = self.board.chess[row][col].piece
                        piece.moves = []
                        self.board.calc_moves(piece, row, col)
                        actual_moves = piece.moves
                        for move in actual_moves:
                            opp = move.final.piece
                            self.board.make_move(piece, move)
                            eval_ = self.minimax(depth - 1, True)
                            self.board.undo_move(move, piece, opp)
                            min_eval = min(min_eval, eval_)
            return min_eval
