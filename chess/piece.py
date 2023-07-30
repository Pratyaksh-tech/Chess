import os

class Piece:
	def __init__(self, name, color, value, texture = None, rect_obj = None):
		self.name = name
		self.color = color
		value_sign = -1 if color == "white" else 1
		self.value = value*value_sign
		self.texture = texture
		self.set_texture()
		self.rect_obj = rect_obj
		self.moved = False
		self.moves = []
		
	def set_texture(self, size=80):
		self.texture = os.path.join(
				f"assets/images/imgs-{size}px/{self.color}_{self.name}.png")

	def add_move(self, move):
		self.moves.append(move)

class pawn(Piece):
	def __init__(self, color):
		if color == "white":
			self.dir = -1
		else:
			self.dir = 1
		super().__init__('pawn', color, 1.0)

class knight(Piece):
	def __init__(self, color):
		super().__init__('knight', color, 3.0)

class bishop(Piece):
	def __init__(self, color):
		super().__init__('bishop', color, 3.5)

class rook(Piece):
	def __init__(self, color):
		super().__init__('rook', color, 5.0)

class queen(Piece):
	def __init__(self, color):
		super().__init__('queen', color, 10.0)

class king(Piece):
	def __init__(self, color):
		super().__init__('king', color, 10000.0)
