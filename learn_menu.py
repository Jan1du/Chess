import pygame
import os
import practice
from game_constants import *

pygame.init()

screen = pygame.display.set_mode([width, height])  
pygame.display.set_caption("chess")

button_width, button_height = 375, 100
img_width = img_height = 80
font0 = pygame.font.Font(montserrat, 55)
font1 = pygame.font.Font(montserrat, 50)
font2 = pygame.font.Font(montserrat, 25)
font3 = pygame.font.Font(montserrat, 17)
font4 = pygame.font.Font(montserrat, 15)

#==Assets==#
fork_img = pygame.image.load(os.path.join("chess assets", "fork_image.png"))
fork_img = pygame.transform.scale(fork_img, (img_width, img_height))
pin_img = pygame.image.load(os.path.join("chess assets", "pin_image.png"))
pin_img = pygame.transform.scale(pin_img, (img_width, img_height))
d_attack_img = pygame.image.load(os.path.join("chess assets", "d_attack.png"))
d_attack_img = pygame.transform.scale(d_attack_img, (img_width, img_height))

def positions(technique):
    #example: [white_locations, black_locations, white_pieces, black_pieces, color, num_0f_moves, next_moves]
    #next_moves = [piece_index, move]
    if technique == "fork":
        position = {
            1: [
                [(3,5), (4,2)], [(6,6), (6,4), (0,3)],
                ["rook", "king"], ["knight", "king", "pawn"], 
                "black", 3, [[0, (5,4)], [1, (3,2)], [0, (3,5)]]
                ],
                
            #https://thechessworld.com/articles/general-information/5-forks-every-chess-player-must-know/    
            2: [
                [(1,7), (3,7), (5,5), (6,7), (6,6), (7,6)], [(0,0), (3,3), (3,1), (6,0), (0,1), (6,1), (7,1)],
                ["rook", "rook", "bishop", "king", "pawn", "pawn"], ["rook", "bishop", "queen", "king", "pawn", "pawn", "pawn"], 
                "white", 3, [[2, (3,3)], [2, (7,0)], [2, (0,0)]]
                ],

            #https://chessfox.com/fork/#:~:text=Fork%20Tactic%3A%201.,unique%20movement%20in%20any%20direction).
            3: [
                [(0,7), (3,7), (6,7), (2,6), (5,6), (6,6), (7,6)], [(1,2), (2,0), (3,1), (6,0), (0,2), (3,3), (5,1), (6,1)],
                ["rook", "queen", "king", "pawn", "pawn", "pawn", "pawn"], ["rook", "bishop", "queen", "king", "pawn", "pawn", "pawn", "pawn"],
                "white", 3, [[1, (3,4)], [3, (5,0)], [1, (1,2)]]
                ],
            
            #https://lichess.org/practice/basic-tactics/the-fork/Qj281y1p/dpUCi7FF
            4: [
                [(3,6), (5,7), (2,7), (2,5), (3,4), (6,6), (7,6)], [(2,4), (4,4), (1,1), (2,1), (3,3), (6,4), (7,4)],
                ["bishop", "queen", "king", "pawn", "pawn", "pawn", "pawn"], ["knight", "queen", "king", "pawn", "pawn", "pawn", "pawn"],
                "black", 5, [[1, (1,7)], [2, (1,7)], [0, (3,6)], [1, (2,7)], [0, (5,7)]]
            ],

            #https://lichess.org/practice/basic-tactics/the-fork/Qj281y1p/dpUCi7FF
            5: [
                [(5,4), (6,3), (5,5), (7,5), (3,6), (2,5), (3,4), (4,3), (5,6), (7,3)], [(6,0), (7,0), (4,0), (7,2), (4,1), (2,4), (3,3), (4,2), (5,2), (6,1)],
                ["rook", "rook", "bishop", "knight", "king", "pawn", "pawn", "pawn", "pawn", "pawn"], ["rook", "rook", "bishop", "knight", "king", "pawn", "pawn", "pawn", "pawn", "pawn"],
                "white", 5, [[1, (6,1)], [0, (6,1)], [6, (5,2)], [4, (3,1)], [6, (6,1)]]
            ]
        }

    elif technique == "pin":
        position = {
            #https://chessfox.com/pins/
            1: [
                [(7,7), (5,5), (1,7), (0,5), (1,6),  (5,6), (6,5)], [(3,1), (1,0), (0,2), (1,1), (2,1), (6,1), (7,1)],
                ["rook", "knight", "king", "pawn", "pawn", "pawn", "pawn"], [ "bishop", "king", "pawn", "pawn", "pawn", "pawn", "pawn"],
                "black", 3, [[0, (2,2)], [0, (4,7)], [0, ((5,5))]]
            ],

            #https://chessfox.com/pins/
            2: [
                [(1,7), (3,7), (6,7), (6,6), (7,6)], [(3,3), (6,0), (2,2), (5,3)],
                ["rook", "bishop", "king", "pawn", "pawn"], ["queen", "king", "pawn", "pawn"],
                "white", 3, [[1, (1,5)], [0, (1,5)], [0, (1,5)]]
            ],

            #https://chessfox.com/pins/
            3: [
                [(5,7), (4,6), (6,7), (5,6), (6,6), (7,6)], [(0,0), (2,2), (6,0), (5,1), (6,1), (7,1)],
                ["rook", "bishop", "king", "pawn", "pawn", "pawn"], ["rook", "queen", "king", "pawn", "pawn", "pawn"],
                "white", 3, [[1, (5,5)], [1, (3,2)], [1, (0,0)]]
            ],
            
            #https://chessfox.com/pins/
            4: [
                [(5,7), (5,5), (7,6), (0,6), (5,6), (6,6), (7,5)], [(7,0), (2,5), (6,0), (4,2), (5,1), (6,1), (7,1)],
                ["rook", "knight", "king", "pawn", "pawn", "pawn", "pawn"], ["rook", "knight", "king", "pawn", "pawn", "pawn", "pawn"],
                "white", 3, [[0, (2,7)], [5, (6,2)], [0, (2,5)]]
            ],

            #https://chessfox.com/pins/
            5: [
                [(3,7), (4,6), (2,6), (6,7), (1,6), (2,4), (3,5), (6,6), (7,6)], [(1,0), (4,2), (5,4), (5,0), (2,3), (3,4), (5,1), (6,1), (7,2)],
                ["rook", "rook", "queen", "king", "pawn", "pawn", "pawn", "pawn", "pawn"], ["rook", "bishop", "queen", "king", "pawn", "pawn", "pawn", "pawn", "pawn"],
                "white", 3, [[0, (5,7)], [2, (6,3)], [1, (4,2)]]
            ]
        }
    
    elif technique == "discoverd attack":
        position = {
            #https://lichess.org/practice/basic-tactics/discovered-attacks/MnsJEWnI/vV50tWGB
            1: [
                [(5,7), (5,5), (6,7), (6,6), (7,6)], [(5,0), (3,1), (6,1), (7,1)],
                ["rook", "knight", "king", "pawn", "pawn"], ["queen", "king", "pawn", "pawn"],
                "white", 3, [[1, (4,3)], [1, (4,1)], [0, (5,0)]]
            ],

            #https://lichess.org/practice/basic-tactics/discovered-attacks/MnsJEWnI/n76eNBSa
            2: [
                [(4,7), (4,3), (2,4), (6,7), (5,6), (6,6), (7,6), (0,6), (1,5)], [(7,0), (1,2), (4,1), (3,2), (5,2), (6,1), (7,1), (0,1), (1,1)],
                ["rook", "knight", "bishop", "king", "pawn", "pawn", "pawn", "pawn", "pawn"], ["rook", "knight", "king", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
                "white", 3, [[1, (5,1)], [2, (3,1)], [1, (7,0)]]
            ],

            #https://lichess.org/practice/basic-tactics/discovered-attacks/MnsJEWnI/8NxoNQ25
            3: [
                [(4,7), (7,1), (7,5), (1,7), (0,6), (2,5), (3,2)], [(5,6), (6,5), (4,3), (3,0), (0,2), (2,3)],
                ["rook", "rook", "bishop", "king", "pawn", "pawn", "pawn"], ["rook", "rook", "bishop", "king", "pawn", "pawn"],
                "white", 5, [[1, (3,1)], [3, (2,0)], [1, (5,1)], [3, (3,0)], [1, (5,6)]]
            ]#,
            
        }
        """

            #
            4: [
                [], [],
                [], [],
                "black", 5, []
            ],

            #
            5: [
                [], [],
                [], [],
                "black", 5, []
            ],
            
"""

    return position


#Back button
def back():
    button = pygame.draw.rect(screen, colors.white, pygame.Rect(50, 50, 50, 50), 0, 15)
    arrow = font1.render("←", True, colors.black)
    screen.blit(arrow, (59,40))

    return button

def technique_buttons():
    technique_fork = pygame.draw.rect(screen, colors.grey, pygame.Rect(50, 150, button_width, button_height), 0, 15)
    text1 = font2.render("Forks", True, colors.white)
    text2 = font3.render("Level: Beginner", True, colors.green)
    screen.blit(text1, (90, 167))
    screen.blit(text2, (90, 207))
    screen.blit(fork_img, (335, 160))

    technique_pin = pygame.draw.rect(screen, colors.grey, pygame.Rect(475, 150, button_width, button_height), 0, 15)
    text1 = font2.render("Pins", True, colors.white)
    text2 = font3.render("Level: Beginner", True, colors.green)
    screen.blit(text1, (515, 167))
    screen.blit(text2, (515, 207))
    screen.blit(pin_img, (760, 160))

    technique_d_attack = pygame.draw.rect(screen, colors.grey, pygame.Rect(50, 280, button_width, button_height), 0, 15)
    text1 = font2.render("Discovered Attacks", True, colors.white)
    text2 = font3.render("Level: Intermediate", True, colors.amber)
    screen.blit(text1, (70, 297))
    screen.blit(text2, (90, 342))
    screen.blit(d_attack_img, (335, 290))

    return technique_fork, technique_pin, technique_d_attack

def main():
    running = True
    while running:
        screen.fill(colors.dark_grey)
        big_text = font0.render("LEARN", True, colors.white)
        screen.blit(big_text, (650,50))
        back_button = back()
        fork, pin, d_attack = technique_buttons()
        pygame.display.flip()

        #changes the cursor when the cursor is within the button
        mouse_pos = pygame.mouse.get_pos()
        if fork.collidepoint(mouse_pos) or pin.collidepoint(mouse_pos) or back_button.collidepoint(mouse_pos) \
            or d_attack.collidepoint(mouse_pos):
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

                if fork.collidepoint(pos):
                    position = positions("fork")
                    practice.main(position, 1)
                
                if pin.collidepoint(pos):
                    position = positions("pin")
                    practice.main(position, 1)

                if d_attack.collidepoint(pos):
                    position = positions("discoverd attack")
                    practice.main(position, 1)
