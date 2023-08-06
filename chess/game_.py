import pygame
from consts import *
from board import Board
from dragger import Dragger

class Game:
	def __init__(self):
		self.next_player = "white"
		self.board = Board()
		self.dragger = Dragger()
		self.hov = (-1, -1)
		self.noMore = False
	
	def show_bg(self, screen):
		for i in range(ROWS):
			for j in range(COLS):
				if (i+j) % 2 == 0:
					color = "#613c00"
				else:
					color = "#ffd28874"
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

	def show_hover(self, screen):
		color = (180, 180, 180)
		rect = (self.hov[1] * SQSIZE, self.hov[0] * SQSIZE, SQSIZE, SQSIZE)
		pygame.draw.rect(screen, color, rect, width=3)		
	
	def set_hover(self, row, col):
		self.hov = (row, col)

	def end_game(self, screen):
		font = pygame.font.Font(None, 120)
		text_s = font.render("GAME OVER", True, (255, 255, 255))
		if self.noMore:
			cntr = (WIDTH // 2, HEIGHT // 2)
			hide = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
			hide.fill((170, 130, 90, 128))
			screen.blit(hide, (0, 0))
			btn_new = (WIDTH // 2 - 100, (HEIGHT // 2 - 90) + 60, 120, 50)
			pygame.draw.rect(screen, (150, 200, 90), btn_new, width=5)
		else: 
			cntr = (-200, -200)
		if self.board.is_check[0] == True:
			if self.board.is_game_over("white") or self.board.is_game_over("black"):
				cntr = (WIDTH // 2, HEIGHT // 2)
				self.noMore = True
		text_rect = text_s.get_rect(center = cntr)
		screen.blit(text_s, text_rect)
