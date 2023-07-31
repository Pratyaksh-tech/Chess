from consts import *
from game_ import Game

class Handle:
	def __init__(self, game):
		self.game = game
		self.board = self.game.board
		self.player = 'white'
		self.bot = 'black'

	def handle(self):
		best_Score = -100000
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
						
						score = self.minimax("black", 0)
						self.board.undo_move(move, piece, opp)
						if score > best_Score:
							best_Score = score
							best_move = move
							best_piece = piece
		print(f"best score is {best_Score} and piece is { best_piece.name}")
		return (best_move, best_piece)
	
	def static_evaluation(self):
		white_score = 0
		for row in range(ROWS):
			for col in range(COLS):
				if not self.board.chess[row][col].isEmpty():
					if self.board.chess[row][col].piece.color == "white":
						white_score += self.board.chess[row][col].piece.value

		black_score = 0
		for row in range(ROWS):
			for col in range(COLS):
				if not self.board.chess[row][col].isEmpty():
					if self.board.chess[row][col].piece.color == "black":
						black_score += self.board.chess[row][col].piece.value
		return white_score - black_score

	def minimax(self, next_plyr, depth):
		if depth == 2 or self.board.is_check:
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
							score = self.minimax("white", depth+1)
							self.board.undo_move(move, piece, opp)
							if score > best_score:
								best_score = score
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
							score = self.minimax("black", depth+1)
							self.board.undo_move(move, piece, opp)
							
							if score < best_score:
								best_score = score			
			return best_score
