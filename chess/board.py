from consts import *
from piece import *
from square import Square
from move import Move
from sys import exit
from config import Config

class Board:
	def __init__(self):
		self.chess = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(ROWS)]
		self.last_move = Move(Square(-1, -1), Square(-1, -1))
		self.checkmate_pos = (-1, -1)
		self.is_check = (False, None)
		self.checkmate = False
		self.create()
		self.add_piece("white")
		self.add_piece("black")
		self.config = Config()

	def loc_of_king(self, color):
		for row in range(ROWS):
			for col in range(COLS):
				if not self.chess[row][col].isEmpty():
					if self.chess[row][col].piece.name == "king" and self.chess[row][col].piece.color == color:
						return (row, col)
	
	def calc_all_moves(self, color):
		if color == "white":
			pos = self.loc_of_king("black")
		else:
			pos = self.loc_of_king("white")
		if(pos == None): 
			return
		
		for row in range(ROWS):
			for col in range(COLS):
				if not self.chess[row][col].isEmpty():
					if self.chess[row][col].has_team_piece(color):
						self.calc_moves(self.chess[row][col].piece, row, col)
						for move in self.chess[row][col].piece.moves:
							if move.final.row == pos[0] and move.final.col == pos[1]:
								self.is_check = (True, self.chess[pos[0]][pos[1]].piece.color)
								self.checkmate_pos = pos
								self.checkmate = True
								return
		self.is_check = (False, None)
		self.checkmate_pos = (-1, -1)
		self.checkmate = False

	def construct_valid_moves(self, piece, row, col):
		piece.moves = []
		self.calc_moves(piece, row, col)
		moves = piece.moves
		to_be = []
		for move in moves:
			piece.moves = []
			self.make_move(piece, move)
			if piece.color == "white": self.calc_all_moves("black")
			else:  self.calc_all_moves("white")
			
			if self.checkmate:
				to_be.append(move)
			
			self.undo_move(move, piece, move.final.piece)
		for to in to_be:
			moves.remove(to)
		piece.moves = moves

	def make_move(self, piece, move, isSafe = False):
		initial = move.initial
		final = move.final
		captured = False
		if self.chess[final.row][final.col].piece != None:
			captured = True
		self.chess[initial.row][initial.col].piece = None
		self.chess[final.row][final.col].piece = piece
		piece.moves = []
		self.last_move = move
		self.calc_all_moves(piece.color)
		if isSafe:
			if captured: self.config.play_sound(self.config.capture_sound)
			else: self.config.play_sound(self.config.move_sound) 
			piece.moved = True
		
	def undo_move(self, move, piece, opp, isSafe = False):
		self.chess[move.initial.row][move.initial.col].piece = piece
		self.chess[move.final.row][move.final.col].piece = opp
		self.last_move = Move(Square(-1, -1), Square(-1, -1))
	
	def in_range_move(self, moves, row, col):
		for move in moves:
			if move.final.row == row and move.final.col == col: return True
		return False

	def is_valid_move(self, piece, move):
		return move in piece.moves
	
	def calc_moves(self, piece, row, col):
		piece.moves = []
		def knight_calc():
			possible_moves = [
				(row-2, col+1), (row-1, col+2), (row+1, col+2), (row+2, col+1), (row+2, col-1), (row+1, col-2), (row-1, col-2), (row-2, col-1)
			]
			for move in possible_moves:
				pos_move_row, pos_move_col = move
				if Square.in_range(pos_move_row, pos_move_col):
					if self.chess[pos_move_row][pos_move_col].isEmpty_or_rival(piece.color):
						initial = Square(row, col)
						final = Square(pos_move_row, pos_move_col, self.chess[pos_move_row][pos_move_col].piece)
						move = Move(initial, final)
						piece.add_move(move)
				
		def pawn_calc():
			steps = 1 if piece.moved else 2
			start = row + piece.dir
			end = row + (piece.dir * (1 + steps))
			for cur_row in range(start, end, piece.dir):
				if Square.in_range(cur_row):
					if self.chess[cur_row][col].isEmpty():
						initial = Square(row, col)
						final = Square(cur_row, col, self.chess[cur_row][col].piece)
						move = Move(initial, final)
						piece.add_move(move)
					else: break
				else: break

			diag_row = row + piece.dir
			dg_cols = [col+1, col-1]
			for dg_col in dg_cols:
				if Square.in_range(diag_row, dg_col):
					if self.chess[diag_row][dg_col].has_rival_piece(piece.color):
						initial = Square(row, col)
						final = Square(diag_row, dg_col, self.chess[diag_row][dg_col].piece)
						move = Move(initial, final)
						piece.add_move(move)

		def straight_line_moves(incrms):
			for inc in incrms:
				row_ic, col_ic = inc
				pos_move_row = row + row_ic
				pos_move_col = col + col_ic
				while True:
					if Square.in_range(pos_move_row, pos_move_col):
						initial = Square(row, col)
						final = Square(pos_move_row, pos_move_col, self.chess[pos_move_row][pos_move_col].piece)
						move = Move(initial, final)
							
						if self.chess[pos_move_row][pos_move_col].isEmpty():
							piece.add_move(move)
						
						if self.chess[pos_move_row][pos_move_col].has_rival_piece(piece.color):
							piece.add_move(move)
							break
						if self.chess[pos_move_row][pos_move_col].has_team_piece(piece.color):
							break

					else: break
					pos_move_row = pos_move_row + row_ic
					pos_move_col = pos_move_col + col_ic

		def king_moves():
			posb_moves = [
			(row-1, col), (row+1, col), (row, col+1), (row, col-1), (row+1, col+1), (row+1, col-1), (row-1, col-1), (row-1, col+1)]
			for amove in posb_moves:
				r, c = amove
				if Square.in_range(r, c):
					if self.chess[r][c].isEmpty_or_rival(piece.color):
						initial = Square(row, col)
						final = Square(r, c, self.chess[r][c].piece)
						move = Move(initial, final)	
						piece.add_move(move)


		if isinstance(piece, pawn):
			pawn_calc()

		if isinstance(piece, knight):
			knight_calc()

		if isinstance(piece, bishop):
			straight_line_moves(
				[(-1, 1), (-1, -1), (1, 1), (1, -1)])

		if isinstance(piece, rook):
			straight_line_moves(
				[(-1, 0), (0, 1), (1, 0), (0, -1)])

		if isinstance(piece, queen):
			straight_line_moves(
				[(-1, 1), (-1, -1), (1, 1), (1, -1), (-1, 0), (0, 1), (1, 0), (0, -1)])

		if isinstance(piece, king):
			king_moves()

	def create(self):
		for row in range(ROWS):
			for col in range(COLS):
				self.chess[row][col] = Square(row, col)

	def add_piece(self, color):
		if color == "white":
			row_pawn, row_remain = (6, 7)
		else:
			row_pawn, row_remain = (1, 0)

		for col in range(COLS):
			self.chess[row_pawn][col] = Square(row_pawn, col, pawn(color))

		# Knights
		self.chess[row_remain][1] = Square(row_remain, 1, knight(color))
		self.chess[row_remain][6] = Square(row_remain, 6, knight(color))

		# Bishops
		self.chess[row_remain][2] = Square(row_remain, 2, bishop(color))
		self.chess[row_remain][5] = Square(row_remain, 5, bishop(color))

		# Rooks
		self.chess[row_remain][0] = Square(row_remain, 0, rook(color))
		self.chess[row_remain][7] = Square(row_remain, 7, rook(color))

		# Queen
		self.chess[row_remain][3] = Square(row_remain, 3, queen(color))

		# King
		self.chess[row_remain][4] = Square(row_remain, 4, king(color))
