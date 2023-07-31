from consts import *
from game_ import Game

class Handle:
	def __init__(self, game):
		self.game = game
		self.board = self.game.board
		self.player = 'white'
		self.bot = 'black'

	def handle(self):
		best_Score = -1000000000
		best_move = None
		best_piece = None
		alpha = -1000000000
		beta = 1000000000
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

						score = self.minimax("black", 0, alpha, beta)
						self.board.undo_move(move, piece, opp)

						if score > best_Score:
							best_Score = score
							best_move = move
							best_piece = piece

						alpha = max(alpha, best_Score)
						if beta <= alpha:
							break

		print(f"best score is {best_Score} and piece is {best_piece.name}")
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

		return white_score - black_score

	def minimax(self, next_plyr, depth, alpha, beta):
		if depth == 1 or self.board.is_check:
			return self.static_evaluation()

		if next_plyr == "black":
			best_score = -1000000000
			for row in range(ROWS):
				for col in range(COLS):
					if not self.board.chess[row][col].isEmpty_or_rival(next_plyr):
						piece = self.board.chess[row][col].piece
						piece.moves = []
						self.board.calc_moves(piece, row, col)
						actual_moves = piece.moves
						for move in actual_moves:
							opp = move.final.piece
							self.board.make_move(piece, move)
							score = self.minimax("white", depth + 1, alpha, beta)
							self.board.undo_move(move, piece, opp)
							best_score = max(best_score, score)
							alpha = max(alpha, best_score)
							if beta <= alpha:
								break
			return best_score
		else:
			best_score = 1000000000
			for row in range(ROWS):
				for col in range(COLS):
					if not self.board.chess[row][col].isEmpty_or_rival(next_plyr):
						piece = self.board.chess[row][col].piece
						piece.moves = []
						self.board.calc_moves(piece, row, col)
						actual_moves = piece.moves
						for move in actual_moves:
							opp = move.final.piece
							self.board.make_move(piece, move)
							score = self.minimax("black", depth + 1, alpha, beta)
							self.board.undo_move(move, piece, opp)
							best_score = min(best_score, score)
							beta = min(beta, best_score)
							if beta <= alpha:
								break
			return best_score
