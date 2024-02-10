import pygame
import os
import time
import play_menu as play
import learn_menu as learn
from game_constants import *

pygame.init()


#--Constants--#
img_width = img_height = 425
button_width, button_height = 250, 75

#--assets--#
font = pygame.font.Font(montserrat, 37)
font_time = pygame.font.Font(tektur, 37)
arc = pygame.image.load(os.path.join("chess assets", "arc.png"))
arc = pygame.transform.scale(arc, (180, 200))
image = pygame.image.load(os.path.join("chess assets", "chess_image.png"))
image = pygame.transform.scale(image, (img_width, img_height))

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("chess")

def display_time(time):
  mins_played = font_time.render(str(time), True, colors.white)
  mins = font.render("mins", True, colors.white)
  screen.blit(mins_played, (145,150))
  screen.blit(mins, (145, 185))

def draw_buttons():
    play_button = pygame.draw.rect(screen, colors.blue, pygame.Rect(75, 350, button_width, button_height), 0, 10)
    learn_button = pygame.draw.rect(screen, colors.blue, pygame.Rect(75, 450, button_width, button_height), 0, 10)
    text_play = font.render("PLAY", True, colors.white)
    text_learn = font.render("LEARN", True, colors.white)
    screen.blit(text_play, (148,365))
    screen.blit(text_learn, (137,465))
    return play_button, learn_button


def main():   
    running = True
    Time = time.time()
    if os.path.isfile("files/time"):
        with open("files/time", "r") as f:
            startTime = int(f.read())
    else:
        startTime = 0

    while running:
        gametime = time.time() - Time
        play_time = int(round(gametime/60, 3) + startTime) 

        screen.fill(colors.grey)
        play_button, learn_button = draw_buttons() 
        screen.blit(arc, (90,90))
        screen.blit(image, (415,95))
        display_time(play_time)
        pygame.display.flip()

        #changes the cursor when the cursor is within the button
        mouse_pos = pygame.mouse.get_pos()
        if play_button.collidepoint(mouse_pos) or learn_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)        

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if play_button.collidepoint(pos):
                    play.main()     #Play window is accessed from here
                   

                if learn_button.collidepoint(pos):
                    learn.main()     #Learn window is accessed from here

    else:
        f = open("files/time", "w")
        f.write(str(play_time))
        f.close()
main()
