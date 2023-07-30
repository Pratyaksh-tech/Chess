import pygame
from consts import *

class Dragger:
	def __init__(self):
		self.mouse_x = 0
		self.mouse_y = 0
		self.initial_row = 0
		self.initial_col = 0
		self.piece = None
		self.isDragging = False

	def update_blit(self, screen):
		self.piece.set_texture(size=128)
		img = pygame.image.load(self.piece.texture)
		img_cntr = (self.mouse_x, self.mouse_y)
		self.piece.rect_obj = img.get_rect(center = img_cntr)
		screen.blit(img, self.piece.rect_obj)

	def update_ms(self, pos):
		self.mouse_x, self.mouse_y = pos

	def save_initial(self, pos):
		self.initial_col = pos[0] // SQSIZE
		self.initial_row = pos[1] // SQSIZE

	def drag_piece(self, piece):
		self.piece = piece
		self.isDragging = True	

	def un_drag(self):
		self.piece = None
		self.isDragging = False
