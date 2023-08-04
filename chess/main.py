import pygame
from sys import exit
from consts import *
from game_ import Game
from square import Square
from move import Move
import os
from AI import Handle

class Main:
    def __init__(self):
        pygame.init()
        self.main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption("CHESS")
        self.clock = pygame.time.Clock()
        self.game = Game()
        self.dragger = self.game.dragger
        self.board = self.game.board
        self.ai = Handle(self.game)

        self.is_ai_calculating = False
        self.ai_move = None

    def main(self):
        screen = self.screen
        game = self.game
        dragger = self.dragger
        board = self.board

        while True:
            game.show_bg(screen)
            game.show_last_moves(screen)
            game.show_moves(screen)
            game.check_mate(screen)
            game.show_piece(screen)
            game.show_hover(screen)
            if dragger.isDragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_ms(event.pos)
                    pressed_row = dragger.mouse_y // SQSIZE
                    pressed_col = dragger.mouse_x // SQSIZE

                    if board.chess[pressed_row][pressed_col].has_piece():
                        piece_ = board.chess[pressed_row][pressed_col].piece
                        if piece_.color == game.next_player:
                            piece_.moves = []
                            board.construct_valid_moves(piece_, pressed_row, pressed_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece_)
                            game.show_bg(screen)
                            game.show_last_moves(screen)
                            game.show_moves(screen)
                            game.check_mate(screen)
                            game.show_piece(screen)

                elif event.type == pygame.MOUSEMOTION:
                    game.set_hover(event.pos[1] // SQSIZE, event.pos[0] // SQSIZE)
                    if dragger.isDragging:
                        dragger.update_ms(event.pos)
                        game.show_bg(screen)
                        game.show_last_moves(screen)
                        game.show_moves(screen)
                        game.check_mate(screen)
                        game.show_piece(screen)
                        if board.in_range_move(dragger.piece.moves, event.pos[1] // SQSIZE, event.pos[0] // SQSIZE): game.show_hover(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.isDragging:
                        dragger.update_ms(event.pos)
                        released_row = dragger.mouse_y // SQSIZE
                        released_col = dragger.mouse_x // SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.is_valid_move(dragger.piece, move):
                            board.make_move(dragger.piece, move, True)
                            game.show_bg(screen)
                            game.show_last_moves(screen)
                            game.show_piece(screen)
                            game.determine_player()
                            self.is_ai_calculating = True
                            pygame.time.set_timer(pygame.USEREVENT, 500)
                    dragger.un_drag()
                if event.type == pygame.USEREVENT:
                    if self.is_ai_calculating:
                        ai_move = self.ai.handle()
                        self.ai_move = ai_move
                        self.is_ai_calculating = False

                elif event.type == pygame.QUIT:
                    exit()

            if self.ai_move:
                board.make_move(self.ai_move[1], self.ai_move[0], True)
                game.show_bg(screen)
                game.show_last_moves(screen)
                game.check_mate(screen)
                game.show_piece(screen)
                game.determine_player()
                self.ai_move = None

            self.main_screen.blit(screen, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

root = Main()
root.main()
