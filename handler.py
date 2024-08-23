import board as board_class
import piece as piece_class
import pygame
import os
import math

###
### Init
###

pygame.init()
pygame.display.set_caption("chess")

screen_size = (720, 720)
running = True
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

board_sprites = []
piece_sprites = {}

square_colors = [(233, 193, 131), (179, 133, 75)]
square_selected_color = (253, 213, 151)
square_move_color = (255, 100, 100)

for row in range(8):
    for col in range(8):
        sprite = pygame.Rect(
            row * screen_size[0] / 8,
            col * screen_size[1] / 8, 
            screen_size[0] / 8,
            screen_size[1] / 8
        )
        board_sprites.append(sprite)

for sprite_name in os.listdir("piece_image"):
    sprite = pygame.image.load("piece_image/" + sprite_name)
    scaled = pygame.transform.scale(sprite, (
        screen_size[0] / 8,
        screen_size[1] / 8
    ))
    piece_sprites[sprite_name] = scaled

###
### Inputs
###

square_selection = [0, 0]
selection_square_index = 0
selection_debounce = False
moves_generated = False
selection_move_square_indices = []

def draw(board):
    for row in range(8):
        for col in range(8):
            square_index = row * 8 + col
            color = (row + col) % 2 == 0 and square_colors[0] or square_colors[1]
            sprite = board_sprites[square_index]

            if square_index in selection_move_square_indices:
                color = square_move_color

            #color = (255 * (row + col) / 14, 255 * (row + col) / 14, 255 * (row + col) / 14)

            pygame.draw.rect(screen, color, sprite)

            ##########################################################################################

            piecetype = board.squares[square_index]

            if piecetype != piece_class.none:
                piece_color = piece_class.is_white(piecetype) and "w" or "b"
                piece_sprite_name = piece_color + piece_class.get_enum(piecetype)
                piece_sprite = piece_sprites[piece_sprite_name + ".png"]

                screen.blit(piece_sprite, (
                    row * screen_size[0] / 8,
                    col * screen_size[1] / 8
                ))

    pygame.display.flip()

###
###
###

board = board_class.board()
board.load_position(FEN=r"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

while running:
    if not moves_generated:
        board.generate_moves()
        moves_generated = True
    
    draw(board)
    clock.tick(60)

    moves = board.moves

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]

            row = math.floor(8 * x / screen_size[0])
            col = math.floor(8 * y / screen_size[1])
            square_index = row * 8 + col

            if not selection_debounce:
                # Select
                #print("a")
                selection_debounce = True
                square_selection[0] = row
                square_selection[1] = col
                selection_square_index = square_index
                selection_move_square_indices.clear()

                for move in moves:
                    if move[0] == selection_square_index:
                        selection_move_square_indices.append(move[1])
            else:
                #print("b")
                if square_index == selection_square_index:
                    # Unselect
                    pass
                else:
                    # Move
                    for move in moves:
                        if move[0] == selection_square_index and move[1] == square_index:
                            board.make_move(move)
                            moves_generated = False
                            break
                 
                selection_debounce = False
                selection_move_square_indices.clear()

pygame.quit()