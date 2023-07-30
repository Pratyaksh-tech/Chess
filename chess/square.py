
class Square:
	def __init__(self, row, col, piece=None):
		self.row = row
		self.col = col
		self.piece = piece

	def __eq__(self, other):
		print(self.row, self.col)
		print(other.row, other.col)
		return self.row == other.row and self.col == other.col

	def has_piece(self):
		return self.piece != None

	def isEmpty(self):
		return not self.has_piece()

	def has_team_piece(self, color):
		return self.has_piece() and self.piece.color == color

	def has_rival_piece(self, color):
		return self.has_piece() and self.piece.color != color

	def isEmpty_or_rival(self, color):
		return self.isEmpty() or self.has_rival_piece(color)

	@staticmethod
	def in_range(*args):
		for arg in args:
			if arg < 0 or arg > 7:
				return False
		return True