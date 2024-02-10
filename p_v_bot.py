import pygame
import time
import random
import bot
import move_functions
import game_constants as gc
from game_constants import *

pygame.init()

#==Bugs==#
#Enpassant checks doesnt follow check_options()
#You can check the opponent even tho you are in check yourself (Not at the moment)

def main(player_color, time_limit):

    def draw_board():
        screen.fill(colors.grey)
        screen.blit(assets.background, (0,0))

    def draw_pieces():
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

    def draw_captured():
        pygame.draw.rect(screen, colors.light_grey, pygame.Rect(625, 20, 250, 150))     #Black captured
        pygame.draw.rect(screen, colors.light_grey, pygame.Rect(625, 190, 250, 150))     #White captured

        for i in range(len(captured_pieces_black)):
            piece = captured_pieces_black[i]
            piece_index = small_piece_list.index(piece)
            image = small_black_images[piece_index]
            if i < 5:
                scale = i
                screen.blit(image, ((scale*45)+627, 22))
            elif 5 <= i < 10:
                scale = i - 5
                screen.blit(image, ((scale*45)+627, 70))
            else:
                scale = i - 10
                screen.blit(image, ((scale*45)+627, 120))
        
        for i in range(len(captured_pieces_white)):
            piece = captured_pieces_white[i]
            piece_index = small_piece_list.index(piece)
            image = small_white_images[piece_index]
            if i < 5:
                scale = i
                screen.blit(image, ((scale*45)+627, 192))
            elif 5 <= i < 10:
                scale = i - 5
                screen.blit(image, ((scale*45)+627, 240))
            else:
                scale = i - 10
                screen.blit(image, ((scale*45)+627, 290))


    def back():
        button = pygame.draw.rect(screen, colors.blue, pygame.Rect(675, 540, 150, 50), 0, 15)
        text = font3.render("← Back", True, colors.white)
        screen.blit(text, (705, 550))

        return button
    
    #Shows the time both players have left
    def draw_time(limit, time_white, time_black):                  
        pygame.draw.rect(screen, colors.white, pygame.Rect(620, 450, 125, 50), 2, 15)
        pygame.draw.rect(screen, colors.white, pygame.Rect(755, 450, 125, 50), 2, 15)
        if limit:
            white = {
                "mins": time_white // 60,
                "sec": time_white % 60
            }
            black = {
                "mins": time_black // 60,
                "sec": time_black % 60 
            }
        else:
            white = black = {
                "mins": 0,
                "sec": 0
            }
        
        white_time = None
        if white["mins"] < 10:
            white_time = "0" + str(white["mins"]) + ":"
        else:
            white_time = str(white["mins"]) + ":"
        if white["sec"] < 10:
            white_time += "0" + str(white["sec"])
        else:
            white_time += str(white["sec"])

        black_time = None
        if black["mins"] < 10:
            black_time = "0" + str(black["mins"]) + ":"
        else:
            black_time = str(black["mins"]) + ":"
        if black["sec"] < 10:
            black_time += "0" + str(black["sec"])
        else:
            black_time += str(black["sec"])
        
        white_text = font2.render(white_time, True, colors.white)
        black_text = font2.render(black_time, True, colors.white)
        text1 = font4.render("white", True, colors.white)
        text2 = font4.render("black", True, colors.white)
        screen.blit(white_text, (650, 460))
        screen.blit(black_text, (785, 460))
        screen.blit(text1, (655, 505))
        screen.blit(text2, (795, 505))

    #Checks for en passant
    def en_passant(old_coords, new_coords):
        if turn_step <= 1:   #If white
            index = white_locations.index(old_coords)
            piece = white_pieces[index]
            moved = white_moved[index]
            if piece == "pawn" and new_coords[1] == 4 and not moved:      #If the pawn moved 2 squares
                ep_coords = (new_coords[0], new_coords[1] + 1)  #Stores the coordinates of the square directly below the pawn (The capturing square in en passant)
            else:
                ep_coords = ()
        
        else:   #If black
            index = black_locations.index(old_coords)
            piece = black_pieces[index]
            moved = black_moved[index]
            if piece == "pawn" and new_coords[1] == 3 and not moved:      #If the pawn moved 2 squares
                ep_coords = (new_coords[0], new_coords[1] - 1)  #Stores the coordinates of the square directly below the pawn (The capturing square in en passant)
            else:
                ep_coords = ()
        
        return ep_coords

    #Checks for promotion  
    def check_promotion(pieces, locations, turn):
        promotion = False
        if turn == "white" and player_color == "white":
            for i in range(len(pieces)):
                piece = pieces[i]
                position = locations[i]
                if piece == "pawn":
                    if position[1] == 0:
                        promotion = True
                        select_promotion(position, turn)

        elif turn == "black" and player_color == "black":
            for i in range(len(pieces)):
                piece = pieces[i]
                position = locations[i]
                if piece == "pawn":
                    if position[1] == 7:
                        promotion = True
                        select_promotion(position, turn)

        elif turn == "white" and player_color == "black":
            for i in range(len(pieces)):
                piece = pieces[i]
                position = locations[i]
                if piece == "pawn":
                    if position[1] == 0:
                        pieces[i] = "queen"
                        assets.promotion_sound.play()
        
        else:
            for i in range(len(pieces)):
                piece = pieces[i]
                position = locations[i]
                if piece == "pawn":
                    if position[1] == 7:
                        pieces[i] = "queen"
                        assets.promotion_sound.play()
                        
        
        return promotion

    #Handling promotions
    def select_promotion(position, color):
        def selecting_piece(queen_button, rook_button, knight_button, bishop_button, pieces):
            for event in pygame.event.get():            
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if queen_button.collidepoint(pos):
                        pieces[pawn_index] = "queen"
                        assets.promotion_sound.play()
                    if rook_button.collidepoint(pos):
                        pieces[pawn_index] = "rook"
                        assets.promotion_sound.play()
                    if knight_button.collidepoint(pos):
                        pieces[pawn_index] = "knight"
                        assets.promotion_sound.play()
                    if bishop_button.collidepoint(pos):
                        pieces[pawn_index] = "bishop"
                        assets.promotion_sound.play()
                

        if color == "white":
            pawn_index = white_locations.index(position)
            #Drawing the promotion screen
            for i in range(len(small_piece_list)):
                piece = small_piece_list[i]
                def draw_promotion(position, index, padding):
                    promote_square = pygame.draw.rect(screen, colors.white, [(position[0]*75) + 5, (position[1]*75) + 5 + padding, 59, 59])
                    pygame.draw.rect(screen, colors.black, [(position[0]*75) + 5, (position[1]*75) + 5 + padding, 59, 59], 2)
                    screen.blit(small_white_images[index], ((position[0] * 75) + 12, (position[1] * 75) + 12 + padding))
                    return promote_square
                
                if piece == "queen":
                    queen_button = draw_promotion(position, i, 0)
                elif piece == "rook":
                    rook_button = draw_promotion(position, i, 59)
                elif piece == "knight":
                    knight_button = draw_promotion(position, i, 59*2)
                elif piece == "bishop":
                    bishop_button = draw_promotion(position, i, 59*3)            
            selecting_piece(queen_button, rook_button, knight_button, bishop_button, white_pieces)

        else:
            pawn_index = black_locations.index(position)
            #Drawing the promotion screen
            for i in range(len(small_piece_list)):
                piece = small_piece_list[i]
                def draw_promotion(position, index, padding):
                    promote_square = pygame.draw.rect(screen, colors.white, [(position[0]*75) + 5, (position[1]*75) - 5 - padding, 59, 59])
                    pygame.draw.rect(screen, colors.black, [(position[0]*75) + 5, (position[1]*75) - 5 - padding, 59, 59], 2)
                    screen.blit(small_black_images[index], ((position[0] * 75) + 12, (position[1] * 75) - padding))
                    return promote_square
                
                if piece == "queen":
                    queen_button = draw_promotion(position, i, 0)
                elif piece == "rook":
                    rook_button = draw_promotion(position, i, 59)
                elif piece == "knight":
                    knight_button = draw_promotion(position, i, 59*2)
                elif piece == "bishop":
                    bishop_button = draw_promotion(position, i, 59*3)            
            selecting_piece(queen_button, rook_button, knight_button, bishop_button, black_pieces)

    #Checks for Castling
    def castling():
        #===Castling Rules===#
        #The king musn't be in check
        #The king or the rook shouldn't have moved
        #There shouldn't be any pieces between the rook and the king
        #The squares the king moves to must not be attacked by the enemy pieces (2 squares to left or right)

        castle_moves = []   #Stores each valid castle move in the form [((new_king_coords), (old_rook_coords, (new_rook_coords)))]
        rook_moved = []     #Stores if each rook has moved or not
        rook_locations = []
        king_index = 0
        k_position = ()
        if turn_step <= 1:   #when whites turn
            for i in range(len(white_pieces)):
                if white_pieces[i] == "rook":
                    rook_moved.append(white_moved[i])
                    rook_locations.append(white_locations[i])

                elif white_pieces[i] == "king":
                    king_index = i
                    k_position = white_locations[i]
            
            #If the king hasn't moved in the game and atleast one rook hasn't moved and the king isn't in check
            #Empty squares: the squares between the king and the respective rook
            if not white_moved[king_index] and False in rook_moved and not w_check:
                for i in range(len(rook_moved)):
                    castle = True
                    if rook_locations[i][0] > k_position[0]:    #The rook to the right of the king
                        empty_squares = [(k_position[0] + 1, k_position[1]), (k_position[0] + 2, k_position[1])]
                    else:   #The rook to left of the king
                        empty_squares = [(k_position[0] - 1, k_position[1]), (k_position[0] - 2, k_position[1]), (k_position[0] - 3, k_position[1])]
                    
                    for j in range(len(empty_squares)):
                        #The third square between the king and the rook when long castling can be attacked by the enemy pieces
                        if j != 2:
                            #If there are  pieces on the squares between the king or the rook and the squares are attacked or the rook has moved
                            if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                                any(empty_squares[j] in move for move in black_options) or rook_moved[i]:
                                castle = False
                        else:
                            if empty_squares[j] in white_locations or empty_squares[j] in black_locations or rook_moved[i]:
                                castle = False

                    if castle:
                        #King always moves into the second square of empty_squares and the rook always moves into the first square of empty_squares
                        castle_moves.append((empty_squares[1], rook_locations[i], empty_squares[0]))   #(new_king_coords, old_rook_coords, new_rook_coords)


        else:   #when blacks turn
            for i in range(len(black_pieces)):
                if black_pieces[i] == "rook":
                    rook_moved.append(black_moved[i])
                    rook_locations.append(black_locations[i])

                elif black_pieces[i] == "king":
                    king_index = i
                    k_position = black_locations[i]
            
            #If the king hasn't moved in the game and atleast one rook hasn't moved and the king isn't in check
            #Empty squares: the squares between the king and the respective rook
            if not black_moved[king_index] and False in rook_moved and not b_check:
                for i in range(len(rook_moved)):
                    castle = True
                    if rook_locations[i][0] > k_position[0]:    #The rook to the right of the king
                        empty_squares = [(k_position[0] + 1, k_position[1]), (k_position[0] + 2, k_position[1])]
                    else:   #The rook to left of the king
                        empty_squares = [(k_position[0] - 1, k_position[1]), (k_position[0] - 2, k_position[1]), (k_position[0] - 3, k_position[1])]
                    
                    for j in range(len(empty_squares)):
                        #The third square between the king and the rook when long castling can be attacked by the enemy pieces
                        if j != 2:
                            #If there are  pieces on the squares between the king or the rook and the squares are attacked or the rook has moved
                            if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                                any(empty_squares[j] in move for move in white_options) or rook_moved[i]:
                                castle = False
                        else:
                            if empty_squares[j] in white_locations or empty_squares[j] in black_locations or rook_moved[i]:
                                castle = False

                    if castle:
                        #King always moves into the second square of empty_squares and the rook always moves into the first square of empty_squares
                        castle_moves.append((empty_squares[1], rook_locations[i], empty_squares[0]))   #(new_king_coords, old_rook_coords, new_rook_coords)                

        return castle_moves

    #Checking for stalemates and other draws
    def draw(winner, game_over):
        draw = False
        draw_type = None

        #Draw by insufficient materials
        #1. King vs King
        #2. King vs King + kight/bishop
        #3. king + kinght/bishop vs king + kinght/bishop
        if len(white_pieces) <= 2 and len(black_pieces) <= 2:
            draw = True
            for piece in white_pieces:
                if piece == "queen" or piece == "rook" or piece == "pawn":
                    draw = False

            for piece in black_pieces:
                if piece == "queen" or piece == "rook" or piece == "pawn":
                    draw = False
            
            if draw:
                draw_type = "By insufficient material"
        
        #3-fold repetition
        #Draw if a position is repeated 3 times
        if not draw:
            w_position = white_locations.copy()
            b_position = black_locations.copy()
            position = (w_position, b_position)
            if position not in positions:
                positions.append(position)
                position_played.append(1)
            else:
                index = positions.index(position)
                if position_played[index] == 2:
                    draw = True
                    draw_type = "By three-fold repetition"
                else:
                    position_played[index] += 1
        
        #50-move rule
        #If no pawn moves or captures are made within 50 moves, it is considered a draw
        #A "move" consists of a player completing a turn followed by the opponent completing a turn
        if not draw:
            if pawn_move_counter <= 0:
                draw = True
                draw_type = "     By fifty-move rule"

        #Stalemate
        #Draw if the player is not in check and cannot move anywhere
        if not draw:
            if turn_step <= 1 and (not any(white_options) and not w_check):
                draw = True
                draw_type = "           Stalemate"
            
            elif turn_step > 1 and (not any(black_options) and not b_check):
                draw = True
                draw_type = "           Stalemate"


        if draw:
            winner = "draw"
            game_over = True

        return winner, game_over, draw_type

    #Checking the valid moves for a selected piece
    def check_valid_moves():
        if turn_step < 2:
            options_list = white_options
        else:
            options_list = black_options
        valid_options = options_list[selection]
        return valid_options

    #Displaying the valid moves for the selected piece
    def draw_valid(moves, pieces):
        for i in range(len(moves)):
            pygame.draw.circle(screen, colors.red, (moves[i][0] * 75 + 37, moves[i][1] * 75 + 37), 5)

        if castle_moves and pieces[selection] == "king":
            for i in range(len(castle_moves)):
                move = castle_moves[i][0]
                pygame.draw.circle(screen, colors.red, (move[0] * 75 + 37, move[1] * 75 + 37), 5)

    #Check if the king is being attacked
    def check(w_check, b_check):
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

    #draws a flashing square if being checked                  
    def draw_check():
        #if white's turn
        if turn_step < 2 and w_check:
            if 'king' in white_pieces:
                king_index = white_pieces.index('king')
                if flashing_counter < fps/2:
                    pygame.draw.rect(screen, colors.purple, [white_locations[king_index][0] * 75,
                                                    white_locations[king_index][1] * 75, 75, 75], 4)                    
                        
        #if black's turn
        elif turn_step >= 2 and b_check:
            if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                if flashing_counter < fps/2:
                        pygame.draw.rect(screen, colors.purple, [black_locations[king_index][0] * 75,
                                                        black_locations[king_index][1] * 75, 75, 75], 4)
    
    def get_move(color):
        engine = bot.engine(white_pieces, black_pieces, white_locations, black_locations, w_check, b_check, white_ep, black_ep)
        piece, move = engine.get_best_move(3, -100000000000, 100000000000, color)

        return piece, move

    #Game over message
    def draw_game_over(winner):
        pygame.draw.rect(screen, colors.grey, pygame.Rect(150, 225, 300, 150), 0, 10)
        if winner == "white" or winner == "black":
            text = winner + " won!"
        elif winner == "draw":
            text = "Draw!"
            draw_text = font4.render(draw_type, True, colors.white)

        display_text = font1.render(text, True, colors.white)
        if winner != "draw":
            screen.blit(display_text, (210, 240))
        else:
            screen.blit(display_text, (250, 240))
            screen.blit(draw_text, (210, 275))
            

        button = pygame.draw.rect(screen, colors.blue, pygame.Rect(245, 300, 100, 50), 0, 15)
        text_button = font3.render("Restart", True, colors.white)
        screen.blit(text_button, (252,310))

        return button

    #Resetting the variables
    def restart():
        gc.black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        gc.black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                        (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        gc.black_moved = [False, False, False, False, False, False, False, False,
                    False, False, False, False, False, False, False, False]     
        gc.white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                        'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        gc.white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                        (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
        gc.white_moved = [False, False, False, False, False, False, False, False,
                    False, False, False, False, False, False, False, False]  
        gc.captured_pieces_white = []
        gc.captured_pieces_black = []

        gc.turn_step = 0
        gc.selection = 100     
        gc.valid_moves = []    
        gc.piece_captured = False     
        gc.white_ep = ()
        gc.black_ep = ()
        gc.flashing_counter = 0 
        gc.sound_counter = 0  
        gc.winner = ''
        gc.w_check = False
        gc.b_check = False
        gc.game_over = False
        gc.w_promotion = False
        gc.b_promotion = False
        gc.time_white = None
        gc.time_black = None
        gc.positions = []
        gc.position_played = []
        gc.castle_moves = []
        gc.castled = False

    #===========Position arrays========#
    black_pieces = gc.black_pieces
    black_locations = gc.black_locations
    black_moved = gc.black_moved
    white_pieces = gc.white_pieces
    white_locations = gc.white_locations
    white_moved = gc.white_moved
    captured_pieces_white = gc.captured_pieces_white
    captured_pieces_black = gc.captured_pieces_black

    #=====Game Variables=====#
    turn_step = gc.turn_step
    selection = gc.selection    
    valid_moves = gc.valid_moves 
    piece_captured = gc.piece_captured   
    white_ep = gc.white_ep
    black_ep = gc.black_ep
    flashing_counter = gc.flashing_counter   
    sound_counter = gc.sound_counter   
    winner = gc.winner
    w_check = gc.w_check
    b_check = gc.b_check
    game_over = gc.game_over
    w_promotion = gc.w_promotion
    b_promotion = gc.b_promotion
    time_white = gc.time_white
    time_black = gc.time_black
    positions = gc.positions
    position_played = gc.position_played
    pawn_move_counter = gc.pawn_move_counter
    castle_moves = gc.castle_moves
    castled = gc.castled

    if player_color == "random":
        player_color = random.choice(random_colors)
    running = True    
    black_options = []
    white_options = []
    font1 = pygame.font.Font(montserrat, 30)
    font2 = pygame.font.Font(tektur, 23)
    font3 = pygame.font.Font(montserrat, 23)
    font4 = pygame.font.Font(montserrat, 15)
    start_time_white = time.time()
    start_time_black = time.time()
    elapsed_time_white = time.time() - start_time_white
    elapsed_time_black = time.time() - start_time_black
    time_white = time_limit
    time_black = time_limit

    while running:
        clock.tick(fps)

        functions = move_functions.main(white_pieces, black_pieces, white_locations, black_locations, w_check, b_check, white_ep, black_ep)
        draw_board()
        draw_pieces()
        draw_captured()
        back_button = back()
        castle_moves = castling()
        white_options = functions.move_options(white_pieces, white_locations, 'white')
        black_options = functions.move_options(black_pieces, black_locations, 'black')
        if selection != 100:        #Displays the valid moves for the selected piece
            valid_moves = check_valid_moves()
            if turn_step <= 1:
                draw_valid(valid_moves, white_pieces)
            else:
                draw_valid(valid_moves, black_pieces)

        #Checks for promotion
        w_promotion = check_promotion(white_pieces, white_locations, "white")
        b_promotion = check_promotion(black_pieces, black_locations, "black")

        if time_limit and not game_over:
            if not any([w_promotion, b_promotion]):
                if turn_step <= 1:
                    start_time_black = time.time() - elapsed_time_black
                    elapsed_time_white = time.time() - start_time_white
                    time_white = time_limit - elapsed_time_white
                else:
                    start_time_white = time.time() - elapsed_time_white
                    elapsed_time_black = time.time() - start_time_black
                    time_black = time_limit - elapsed_time_black
            else:
                start_time_white = time.time() - elapsed_time_white
                start_time_black = time.time() - elapsed_time_black


            if time_white <= 0:
                game_over = True
                winner = "black"
            if time_black <= 0:
                game_over = True
                winner = "white"

        elif not time_limit:
            time_white = 0
            time_black = 0

        draw_time(time_limit, int(time_white), int(time_black))

        #checks if the game ended
        if not any(white_options) and w_check:
            game_over = True
            winner = "black"
            
        elif not any(black_options) and b_check:
            game_over = True
            winner = "white"
            

        #Display check
        if flashing_counter < fps:
            flashing_counter += 1
        else:
            flashing_counter = 0
        draw_check()

        #changes the cursor when the cursor is within the button
        mouse_pos = pygame.mouse.get_pos()
        mouse_coords = (mouse_pos[0] // 75, mouse_pos[1] // 75)
        if (mouse_coords in white_locations or mouse_coords in black_locations) and not game_over:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif back_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif sound_counter == 1 and restart_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if back_button.collidepoint(pos):
                    restart()
                    running = False
            
            #If the game is over and the game over screen is displayed
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and sound_counter == 1:
                pos = event.pos
                if restart_button.collidepoint(pos):
                    restart()
                    main(player_color, time_limit)
                    running = False
                
            if not any([w_promotion, b_promotion]) and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x_coord = event.pos[0] // 75
                    y_coord = event.pos[1] // 75
                    click_coords = (x_coord, y_coord)

                    #If the player choosed white pieces and its white's turn
                    if player_color == "white" and turn_step <= 1:
                        if click_coords in white_locations:
                            selection = white_locations.index(click_coords)
                            #check if the king is selected(for castiling)
                            selected_piece = white_pieces[selection]
                            if turn_step == 0:
                                turn_step = 1  #Piece selected

                        if selection != 100 and (click_coords in valid_moves or (selected_piece == "king" and any(click_coords == move[0] for move in castle_moves))):
                            white_ep = en_passant(white_locations[selection], click_coords)
                            white_locations[selection] = click_coords
                            white_moved[selection] = True

                            if selected_piece == "king" and castle_moves:
                                for coords in castle_moves:
                                    if click_coords == coords[0]:
                                        rook_index = white_locations.index(coords[1])
                                        white_locations[rook_index] = coords[2]
                                        white_moved[rook_index] = True
                                        castled = True
                                        assets.castle_sound.play()

                            #If a piece is captured
                            if click_coords in black_locations:
                                piece_captured = True
                                black_piece = black_locations.index(click_coords)
                                captured_pieces_black.append(black_pieces[black_piece])

                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                                black_moved.pop(black_piece)

                            #If a pawn is captured using en passant
                            if selected_piece == "pawn" and click_coords == black_ep:
                                piece_captured = True
                                black_piece = black_locations.index((click_coords[0], click_coords[1] + 1) ) 
                                captured_pieces_black.append(black_pieces[black_piece])

                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                                black_moved.pop(black_piece)
                            
                            if selected_piece != "pawn" and piece_captured == False:
                                pawn_move_counter -= 1
                            else:
                                pawn_move_counter = 100

                            black_options = functions.move_options(black_pieces, black_locations, 'black')
                            white_options = functions.move_options(white_pieces, white_locations, 'white')
                            w_check, b_check = check(w_check, b_check)

                            if piece_captured and not b_check and not castled:
                                assets.capture_sound.play()    #Play capture sound if a black piece is captured and black is not in check   
                            elif not piece_captured and not b_check and not castled:
                                assets.move_sound.play()    #Play move sound if a piece is moved and the black king is not in check

                            #Reset the variables
                            w_check = False
                            castled = False
                            piece_captured = False
                            turn_step = 2
                            selection = 100
                            valid_moves = []
                            winner, game_over, draw_type = draw(winner, game_over)
                    
                    if player_color == "black" and turn_step > 1:
                        if click_coords in black_locations:
                            selection = black_locations.index(click_coords)
                            #check if the king is selected(for castiling and en passant)
                            selected_piece = black_pieces[selection]
                            if turn_step == 2:
                                turn_step = 3   #Piece selected

                        if selection != 100 and (click_coords in valid_moves or (selected_piece == "king" and any(click_coords == move[0] for move in castle_moves))):
                            black_ep = en_passant(black_locations[selection], click_coords)
                            black_locations[selection] = click_coords
                            black_moved[selection] = True

                            if selected_piece == "king" and castle_moves:
                                for coords in castle_moves:
                                    if click_coords == coords[0]:
                                        rook_index = black_locations.index(coords[1])
                                        black_locations[rook_index] = coords[2]
                                        black_moved[rook_index] = True
                                        castled = True
                                        assets.castle_sound.play()

                            #If a piece is captured
                            if click_coords in white_locations:
                                piece_captured = True
                                white_piece = white_locations.index(click_coords)
                                captured_pieces_white.append(white_pieces[white_piece])
                                
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                                white_moved.pop(white_piece)

                            #If a pawn is captured using en passant
                            if selected_piece == "pawn" and click_coords == white_ep:
                                piece_captured = True
                                white_piece = white_locations.index((click_coords[0], click_coords[1] - 1) ) 
                                captured_pieces_white.append(white_pieces[white_piece])

                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                                white_moved.pop(white_piece)                            

                            if selected_piece != "pawn" and piece_captured == False:
                                pawn_move_counter -= 1
                            else:
                                pawn_move_counter = 100

                            black_options = functions.move_options(black_pieces, black_locations, 'black')
                            white_options = functions.move_options(white_pieces, white_locations, 'white')
                            w_check, b_check = check(w_check, b_check)
                            if piece_captured and not w_check and not castled:
                                assets.capture_sound.play()     #Play capture sound if a white piece is captured and white is not in check  
                            elif not piece_captured and not w_check and not castled:
                                assets.move_sound.play()    #Play move sound if a piece is moved and white  is not in check

                            #Reset the variables
                            b_check = False
                            castled = False
                            piece_captured = False
                            turn_step = 0
                            selection = 100
                            valid_moves = [] 
                            winner, game_over, draw_type = draw(winner, game_over)          
                    
                    
                else:     #So you dont have to click the screen for the bot to make a move                    
                    if player_color == "white" and turn_step > 1:
                        black_options = functions.move_options(black_pieces, black_locations, 'black')
                        if any(black_options):
                            piece_selection, move_played = get_move("black")
                            #piece_selection, move_played = bot.get_move(black_options)
                            black_ep = en_passant(black_locations[piece_selection], move_played)
                            
                            selected_piece = black_pieces[piece_selection]
                            black_locations[piece_selection] = move_played
                            black_moved[piece_selection] = True

                            if selected_piece == "king" and castle_moves:
                                for coords in castle_moves:
                                    if click_coords == coords[0]:
                                        rook_index = black_locations.index(coords[1])
                                        black_locations[rook_index] = coords[2]
                                        black_moved[rook_index] = True
                                        castled = True
                                        assets.castle_sound.play()

                            #If a piece is captured
                            if move_played in white_locations:
                                piece_captured = True
                                white_piece = white_locations.index(move_played)
                                captured_pieces_white.append(white_pieces[white_piece])
                                
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                                white_moved.pop(white_piece)

                            #If a pawn is captured using en passant
                            if selected_piece == "pawn" and move_played == white_ep:
                                piece_captured = True
                                white_piece = white_locations.index((move_played[0], move_played[1] - 1) ) 
                                captured_pieces_white.append(white_pieces[white_piece])

                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                                white_moved.pop(white_piece)

                            if selected_piece != "pawn" and piece_captured == False:
                                pawn_move_counter -= 1
                            else:
                                pawn_move_counter = 100                                

                            black_options = functions.move_options(black_pieces, black_locations, 'black')
                            white_options = functions.move_options(white_pieces, white_locations, 'white')
                            w_check, b_check = check(w_check, b_check)
                            if piece_captured and not w_check and not castled:
                                assets.capture_sound.play()     #Play capture sound if a white piece is captured and white is not in check  
                            elif not piece_captured and not w_check and not castled:
                                assets.move_sound.play()    #Play move sound if a piece is moved and white  is not in check

                            #Reset the variables
                            b_check = False
                            castled = False
                            piece_captured = False
                            turn_step = 0
                            winner, game_over, draw_type = draw(winner, game_over)

                    if player_color == "black" and turn_step <= 1:
                        white_options = functions.move_options(white_pieces, white_locations, 'white')
                        if any(white_options):
                            piece_selection, move_played = get_move("white")
                            #piece_selection, move_played = bot.get_move(white_options)
                            white_ep = en_passant(white_locations[piece_selection], move_played)
                            selected_piece = white_pieces[piece_selection]
                            white_locations[piece_selection] = move_played
                            white_moved[piece_selection] = True

                            if selected_piece == "king" and castle_moves:
                                for coords in castle_moves:
                                    if click_coords == coords[0]:
                                        rook_index = white_locations.index(coords[1])
                                        white_locations[rook_index] = coords[2]
                                        white_moved[rook_index] = True
                                        castled = True
                                        assets.castle_sound.play()

                            #If a piece is captured
                            if move_played in black_locations:
                                piece_captured = True
                                black_piece = black_locations.index(move_played)
                                captured_pieces_black.append(black_pieces[black_piece])
                                
                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                                black_moved.pop(black_piece)

                            #If a pawn is captured using en passant
                            if move_played == black_ep:
                                piece_captured = True
                                black_piece = black_locations.index((click_coords[0], click_coords[1] + 1) ) 
                                captured_pieces_black.append(black_pieces[black_piece])

                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                                black_moved.pop(black_piece)
                            
                            if selected_piece != "pawn" and piece_captured == False:
                                pawn_move_counter -= 1
                            else:
                                pawn_move_counter = 100
                            
                            black_options = functions.move_options(black_pieces, black_locations, 'black')
                            white_options = functions.move_options(white_pieces, white_locations, 'white')
                            w_check, b_check = check(w_check, b_check)
                            if piece_captured and not b_check and not castled:
                                assets.capture_sound.play()     #Play capture sound if a white piece is captured and white is not in check  
                            elif not piece_captured and not b_check and not castled:
                                assets.move_sound.play()    #Play move sound if a piece is moved and white  is not in check

                            #Reset the variables
                            w_check = False
                            castled = False
                            piece_captured = False
                            turn_step = 2
                            winner, game_over, draw_type = draw(winner, game_over)

        if game_over:
            if sound_counter == 0:
                assets.mate_sound.play()
                sound_counter = 1
            restart_button = draw_game_over(winner)
        
        pygame.display.flip()

