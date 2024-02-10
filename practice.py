import pygame
import copy
import time
import move_functions
from game_constants import *

pygame.init()

screen = pygame.display.set_mode([width, height])  
pygame.display.set_caption("chess")

font1 = pygame.font.Font(montserrat, 23)
font2 = pygame.font.Font(montserrat, 15)


def draw_board():
        screen.fill(colors.grey)
        screen.blit(assets.background, (0,0))

def draw_pieces(white_pieces, black_pieces, white_locations, black_locations, turn_step, selection):
        for i in range(len(white_pieces)):
            index = piece_list.index(white_pieces[i])
            screen.blit(white_images[index], (white_locations[i][0] * 75, white_locations[i][1] * 75))
            if turn_step < 2:
                if selection == i:
                    pygame.draw.rect(screen, colors.red, [white_locations[i][0] * 75, white_locations[i][1] * 75,
                                                    75, 75], 3)

        for i in range(len(black_pieces)):
            index = piece_list.index(black_pieces[i])
            screen.blit(black_images[index], (black_locations[i][0] * 75, black_locations[i][1] * 75))
            if turn_step >= 2:
                if selection == i:
                    pygame.draw.rect(screen, colors.red, [black_locations[i][0] * 75, black_locations[i][1] * 75, 75, 75], 3)

#Checking the valid moves for a selected piece
def check_valid_moves(white_options, black_options, turn_step, selection):
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

#Check if the king is being attacked
def check(w_check, b_check, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, turn_step):
    #if black moved a piece
    if turn_step >= 2:
        if 'king' in white_pieces:   
            king_index = white_pieces.index('king')    
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    assets.check_sound.play()
                    w_check = True
                    break
                    
    #if white moved a piece
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    assets.check_sound.play()
                    b_check = True
                    break

    return w_check, b_check

#Displaying the valid moves for the selected piece
def draw_valid(moves):
    for i in range(len(moves)):
        pygame.draw.circle(screen, colors.red, (moves[i][0] * 75 + 37, moves[i][1] * 75 + 37), 5)

def back():
        button = pygame.draw.rect(screen, colors.blue, pygame.Rect(675, 540, 150, 50), 0, 15)
        text = font1.render("← Back", True, colors.white)
        screen.blit(text, (705, 550))

        return button

def next():
    button = pygame.draw.rect(screen, colors.white, pygame.Rect(650, 100, 200, 50), 0, 15)
    text = font1.render("Next example", True, colors.black)
    screen.blit(text, (665, 110))

    return button

def show_try():
    show_button = pygame.draw.rect(screen, colors.white, pygame.Rect(650, 25, 75, 50), 0, 15)
    text = font1.render("Show", True, colors.black)
    screen.blit(text, (654, 35))

    try_button = pygame.draw.rect(screen, colors.white, pygame.Rect(775, 25, 75, 50), 0, 15)
    text = font1.render("Try", True, colors.black)
    screen.blit(text, (793, 35))

    return show_button, try_button

def show(position, moved, turn_step):
    if moved < len(position[6]):
        piece_captured = False
        white_locations = position[0]
        black_locations = position[1]
        white_pieces = position[2]
        black_pieces = position[3]

        move = position[6][moved]
        if turn_step == 0:
            white_locations[move[0]] = move[1]

            #If a piece is captured
            if move[1] in black_locations:
                piece_captured = True
                black_piece = black_locations.index(move[1])
                black_pieces.pop(black_piece)
                black_locations.pop(black_piece)

            if piece_captured:
                assets.capture_sound.play()    #Play capture sound if a black piece is captured and black is not in check   
            elif not piece_captured:
                assets.move_sound.play()    #Play move sound if a piece is moved and the black king is not in check
                   
            #Reset the variables
            turn_step = 2
            moved += 1
        
        else:
            black_locations[move[0]] = move[1]

            #If a piece is captured
            if move[1] in white_locations:
                piece_captured = True
                white_piece = white_locations.index(move[1])                   
                white_pieces.pop(white_piece)
                white_locations.pop(white_piece) 
            
            if piece_captured and not w_check:
                assets.capture_sound.play()     #Play capture sound if a white piece is captured and white is not in check  
            elif not piece_captured and not w_check:
                assets.move_sound.play()    #Play move sound if a piece is moved and white  is not in check


            #Reset the variables
            turn_step = 0
            moved += 1

    return moved, turn_step, position


def main(positions, example):
    positions_copy = copy.deepcopy(positions)
    running = True
    w_check, b_check = False, False
    valid_moves = []
    selection = 100
    piece_captured = False
    moved = 0
    position = positions[example]
    position_copy = copy.deepcopy(position)
    num_moves = position[5] - 1
    game_over = False
    mode = 'try'
    if position[4] == "white":
        turn_step = 0
    else:
        turn_step = 2

    while running:
        white_locations, black_locations, white_pieces, black_pieces = position[0], position[1], position[2], position[3]
        if moved <= num_moves:
            move = position[6][moved]
        else:
            game_over = True
        
        functions = move_functions.main(white_pieces, black_pieces, white_locations, black_locations, w_check, b_check, (), ())
        
        draw_board()
        draw_pieces(white_pieces, black_pieces, white_locations, black_locations, turn_step, selection)
        black_options = functions.move_options(black_pieces, black_locations, 'black')
        white_options = functions.move_options(white_pieces, white_locations, 'white')
        if selection != 100:        #Displays the valid moves for the selected piece
            valid_moves = check_valid_moves(white_options, black_options, turn_step, selection)
            if turn_step <= 1:
                draw_valid(valid_moves)
            else:
                draw_valid(valid_moves)

        back_button = back()
        show_button, try_button = show_try()
        next_button = next()
        pygame.display.flip()


        if mode == 'show':
            time.sleep(1)
            moved, turn_step, position = show(position, moved, turn_step)

        #changes the cursor when the cursor is within the button
        mouse_pos = pygame.mouse.get_pos()
        mouse_coords = (mouse_pos[0] // 75, mouse_pos[1] // 75)
        if (mouse_coords in white_locations or mouse_coords in black_locations) and not game_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif back_button.collidepoint(mouse_pos) or show_button.collidepoint(mouse_pos) \
            or try_button.collidepoint(mouse_pos) or next_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if back_button.collidepoint(pos):
                    running = False
                
                if next_button.collidepoint(pos):
                    if example < len(positions):
                        example += 1
                        main(positions_copy, example)
                        running = False           
                    else:
                        example = 1
                        main(positions_copy, example)
                        running = False
                
                if show_button.collidepoint(pos):
                    mode = 'show'
                    position = copy.deepcopy(position_copy)
                    moved = 0
                    selection = 100
                    if position[4] == "white":
                        turn_step = 0
                    else:
                        turn_step = 2

                if try_button.collidepoint(pos):
                    mode = 'try'
                    game_over = False
                    position = copy.deepcopy(position_copy)
                    moved = 0
                    if position[4] == "white":
                        turn_step = 0
                    else:
                        turn_step = 2


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and mode == 'try':
                x_coord = event.pos[0] // 75
                y_coord = event.pos[1] // 75
                click_coords = (x_coord, y_coord)

                #If the player choosed white pieces and its white's turn
                if turn_step <= 1 and position[4] == "white":
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            turn_step = 1  #Piece selected

                    if click_coords in valid_moves and selection != 100:
                        if selection == move[0] and click_coords == move[1]:
                            white_locations[selection] = click_coords

                            #If a piece is captured
                            if click_coords in black_locations:
                                piece_captured = True
                                black_piece = black_locations.index(click_coords)
                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)

                            black_options = functions.move_options(black_pieces, black_locations, 'black')
                            white_options = functions.move_options(white_pieces, white_locations, 'white')
                            w_check, b_check = check(w_check, b_check, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, turn_step)

                            if piece_captured and not b_check:
                                assets.capture_sound.play()    #Play capture sound if a black piece is captured and black is not in check   
                            elif not piece_captured and not b_check:
                                assets.move_sound.play()    #Play move sound if a piece is moved and the black king is not in check

                            #Reset the variables
                            turn_step = 2
                            moved += 1
                            w_check = False
                            piece_captured = False
                            selection = 100
                            valid_moves = []
                        
                        else:
                            assets.wrong_sound.play()

                if turn_step > 1 and position[4] == "black":
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3   #Piece selected

                    if click_coords in valid_moves and selection != 100:
                        if selection == move[0] and click_coords == move[1]:
                            black_locations[selection] = click_coords

                            #If a piece is captured
                            if click_coords in white_locations:
                                piece_captured = True
                                white_piece = white_locations.index(click_coords)                   
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece) 
                        

                            black_options = functions.move_options(black_pieces, black_locations, 'black')
                            white_options = functions.move_options(white_pieces, white_locations, 'white')
                            w_check, b_check = check(w_check, b_check, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, turn_step)
                            if piece_captured and not w_check:
                                assets.capture_sound.play()     #Play capture sound if a white piece is captured and white is not in check  
                            elif not piece_captured and not w_check:
                                assets.move_sound.play()    #Play move sound if a piece is moved and white  is not in check

                            #Reset the variables
                            turn_step = 0
                            moved += 1
                            b_check = False
                            piece_captured = False
                            selection = 100
                            valid_moves = []
                    
                        else:
                            assets.wrong_sound.play()

                
            else:
                if turn_step <= 1 and position[4] == "black" and not game_over and mode == 'try':
                    white_locations[move[0]] = move[1]

                    #If a piece is captured
                    if move[1] in black_locations:
                        piece_captured = True
                        black_piece = black_locations.index(move[1])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                    black_options = functions.move_options(black_pieces, black_locations, 'black')
                    white_options = functions.move_options(white_pieces, white_locations, 'white')
                    w_check, b_check = check(w_check, b_check, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, turn_step)

                    if piece_captured and not b_check:
                        assets.capture_sound.play()    #Play capture sound if a black piece is captured and black is not in check   
                    elif not piece_captured and not b_check:
                        assets.move_sound.play()    #Play move sound if a piece is moved and the black king is not in check

                    #Reset the variables
                    turn_step = 2
                    moved += 1
                    w_check = False
                    piece_captured = False
                    selection = 100
                    valid_moves = []

                if turn_step > 1 and position[4] == "white" and not game_over and mode == 'try':
                    black_locations[move[0]] = move[1]

                    #If a piece is captured
                    if move[1] in white_locations:
                        piece_captured = True
                        white_piece = white_locations.index(move[1])                   
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece) 
                

                    black_options = functions.move_options(black_pieces, black_locations, 'black')
                    white_options = functions.move_options(white_pieces, white_locations, 'white')
                    w_check, b_check = check(w_check, b_check, white_pieces, black_pieces, white_locations, black_locations, white_options, black_options, turn_step)
                    if piece_captured and not w_check:
                        assets.capture_sound.play()     #Play capture sound if a white piece is captured and white is not in check  
                    elif not piece_captured and not w_check:
                        assets.move_sound.play()    #Play move sound if a piece is moved and white  is not in check

                    #Reset the variables
                    turn_step = 0
                    moved += 1
                    b_check = False
                    piece_captured = False
                    selection = 100
                    valid_moves = []
