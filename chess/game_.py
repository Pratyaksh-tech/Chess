import pygame
from consts import *
from board import Board
from dragger import Dragger

class Game:
	def __init__(self):
		self.next_player = "white"
		self.board = Board()
		self.dragger = Dragger()
	
	def show_bg(self, screen):
		for i in range(ROWS):
			for j in range(COLS):
				if (i+j) % 2 == 0:
					color = (112,102,119)
				else:
					color = (204,183,174)
				rect = (j*SQSIZE, i*SQSIZE, SQSIZE, SQSIZE)
				pygame.draw.rect(screen, color, rect)

	def show_piece(self, screen):
		for row in range(ROWS):
			for col in range(COLS):
				if self.board.chess[row][col].has_piece():
					piece = self.board.chess[row][col].piece
					if piece is not self.dragger.piece:
						piece.set_texture()
						img = pygame.image.load(piece.texture)
						cntr = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
						piece.rect_obj = img.get_rect(center = cntr)
						screen.blit(img, piece.rect_obj)

	def show_moves(self, screen):
		if self.dragger.isDragging:
			piece = self.dragger.piece

			for move in piece.moves:
				color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
				rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
				pygame.draw.rect(screen, color, rect)


	def determine_player(self):
		self.next_player = "white" if self.next_player == "black" else "black"

	def show_last_moves(self, screen):
		initial = self.board.last_move.initial
		final = self.board.last_move.final

		for pos in [initial, final]:
			if(pos.row + pos.col) % 2 == 0:
				color = (244, 247, 116)
			else:
				color = (172, 195, 51)
			rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
			pygame.draw.rect(screen, color, rect)

	def check_mate(self, screen):
		i, j = self.board.checkmate_pos
		color = "red"
		rect = (j * SQSIZE, i * SQSIZE, SQSIZE, SQSIZE)
		pygame.draw.rect(screen, color, rect)