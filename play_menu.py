import pygame
import os
import time
import pvp as play1
import p_v_bot as play2
import game_constants as gc
from game_constants import *


pygame.init()

box_width, box_height = 375, 425
times = ["Unlimited", 10.0, 5.0, 2.0, 1.0]

#==Assets==#
white_image = pygame.image.load(os.path.join("chess assets", "colour_white.png"))
black_image = pygame.image.load(os.path.join("chess assets", "colour_black.png"))
random_image = pygame.image.load(os.path.join("chess assets", "colour_random.png"))
font0 = pygame.font.Font(montserrat, 55)
font1 = pygame.font.Font(montserrat, 50)
font2 = pygame.font.Font(montserrat, 27)
font3 = pygame.font.Font(montserrat, 23)
font4 = pygame.font.Font(montserrat, 15)
font5 = pygame.font.Font(tektur, 20)

screen = pygame.display.set_mode([width, height])  
pygame.display.set_caption("chess")

def draw_player_settings(time):
    pygame.draw.rect(screen, colors.dark_grey, pygame.Rect(50, 150, box_width, box_height), 0, 10)
    time_select = pygame.draw.rect(screen, colors.white, pygame.Rect(162, 250, 150, 50), 0, 40)
    play_button = pygame.draw.rect(screen, colors.blue, pygame.Rect(162, 500, 150, 50), 0, 15)

    mini_text = font2.render("Player vs Player", True, colors.white)
    text_time_choose = font4.render("time", True, colors.white)
    text_time = font5.render(time, True, colors.black)
    v = font4.render("v", True, colors.black)
    text_play = font3.render("PLAY", True, colors.white)
    screen.blit(mini_text, (123, 165))
    screen.blit(text_time_choose, (215, 230))
    screen.blit(text_time, (185, 262))
    screen.blit(v, (295,265))
    screen.blit(text_play, (205, 510))

    return play_button, time_select

def draw_bot_settings(time):
    pygame.draw.rect(screen, colors.dark_grey, pygame.Rect((100+box_width), 150, box_width, box_height), 0, 10)
    time_select = pygame.draw.rect(screen, colors.white, pygame.Rect(587, 250, 150, 50), 0, 40)
    color_white = pygame.draw.rect(screen, colors.light_blue, pygame.Rect(560, 350, 50, 50), 0, 15)
    color_black = pygame.draw.rect(screen, colors.light_blue, pygame.Rect(640, 350, 50, 50), 0, 15)
    color_random = pygame.draw.rect(screen, colors.light_blue, pygame.Rect(720, 350, 50, 50), 0, 15)

    play_button = pygame.draw.rect(screen, colors.blue, pygame.Rect(587, 500, 150, 50), 0, 15)

    mini_text = font2.render("Player vs Computer", True, colors.white)
    text_time_choose = font4.render("time", True, colors.white)
    text_time = font5.render(time, True, colors.black)
    v = font4.render("v", True, colors.black)
    text_color = font4.render("Choose a colour", True, colors.white)
    text_difficulty = font4.render("Difficulty", True, colors.white)
    text_play = font3.render("PLAY", True, colors.white)
    screen.blit(mini_text, (525, 165))
    screen.blit(text_time_choose, (640, 230))
    screen.blit(text_time, (610, 262))
    screen.blit(v, (720,265))
    screen.blit(text_color, (605, 330))
    screen.blit(text_play, (630, 510))
    screen.blit(white_image, (567, 355))
    screen.blit(black_image, (647, 355))
    screen.blit(random_image, (727, 355))

    return play_button, color_white, color_black, color_random, time_select

#Back button
def back():
    button = pygame.draw.rect(screen, colors.white, pygame.Rect(50, 50, 50, 50), 0, 15)
    arrow = font1.render("←", True, colors.black)
    screen.blit(arrow, (59,40))

    return button


#Draws a border around the selected colour
def color_selection(color):
    if color:
        text_color = font4.render(color, True, colors.white)

    if color == "white":
        pygame.draw.rect(screen, colors.blue, pygame.Rect(560, 350, 50, 50), 2, 15)
        screen.blit(text_color, (645, 410))

    if color == "black":
        pygame.draw.rect(screen, colors.blue, pygame.Rect(640, 350, 50, 50), 2, 15)
        screen.blit(text_color, (645, 410))

    if color == "random":
        pygame.draw.rect(screen, colors.blue, pygame.Rect(720, 350, 50, 50), 2, 15)
        screen.blit(text_color, (640, 410))

#Selecting the time options
def time_menu(x_pos, y_pos, clicked, time):
    rect_list = []
    for i in range(len(times)):
        rect = pygame.draw.rect(screen, colors.white, [x_pos, y_pos, 130, 50])
        pygame.draw.rect(screen, colors.black, [x_pos, y_pos, 130, 50], 2)
        text = font5.render(str(times[i]), True, colors.black)
        screen.blit(text, ((x_pos+10), (y_pos+10)))
        rect_list.append(rect)
        y_pos += 50

    for event in pygame.event.get():            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if rect_list[0].collidepoint(pos):
                    time = times[0]
                    clicked = False
                if rect_list[1].collidepoint(pos):
                    time = times[1]
                    clicked = False
                if rect_list[2].collidepoint(pos):
                    time = times[2]
                    clicked = False
                if rect_list[3].collidepoint(pos):
                    time = times[3]
                    clicked = False
                if rect_list[4].collidepoint(pos):
                    time = times[4]
                    clicked = False

    return clicked, time

def main():
    color = None
    time1 = times[0]
    time2 = times[0]
    time_button_clicked1 = False
    time_button_clicked2 = False
    running = True
    while running:
        button_clicked = [time_button_clicked1, time_button_clicked2]
        screen.fill(colors.grey)
        big_text = font0.render("PLAY", True, colors.white)
        screen.blit(big_text, (700,50))
        back_button = back()
        play_button1, time_button1 = draw_player_settings(str(time1))
        play_button2, color_white, color_black, color_random, time_button2 = draw_bot_settings(str(time2))
        color_selection(color)

        if any(button_clicked):
            if time_button_clicked2:
                time_button_clicked2, time2 = time_menu(600, 250, time_button_clicked2, time2)
            if time_button_clicked1:
                time_button_clicked1, time1 = time_menu(175, 250, time_button_clicked1, time1)

        pygame.display.flip()

        #changes the cursor when the cursor is within the button
        mouse_pos = pygame.mouse.get_pos()
        if play_button1.collidepoint(mouse_pos) or play_button2.collidepoint(mouse_pos) \
            or time_button1.collidepoint(mouse_pos) or time_button2.collidepoint(mouse_pos) \
            or color_white.collidepoint(mouse_pos) or color_black.collidepoint(mouse_pos) \
            or color_random.collidepoint(mouse_pos) or back_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)        
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not any(button_clicked):
                pos = event.pos
                if back_button.collidepoint(pos):
                    running = False

                if play_button1.collidepoint(pos):
                    if isinstance(time1, float):
                        time_limit = time1 * 60
                    else:
                        time_limit = None
                    play1.main(time_limit)
                
                if time_button1.collidepoint(pos):
                    time_button_clicked1 = True

                if color_white.collidepoint(pos):
                    color = "white"       

                if color_black.collidepoint(pos):
                    color = "black"

                if color_random.collidepoint(pos):
                    color = "random"

                if time_button2.collidepoint(pos):
                    time_button_clicked2 = True

                if play_button2.collidepoint(pos) and color:
                    if isinstance(time2, float):
                        time_limit = time2 * 60
                    else:
                        time_limit = None
                    play2.main(color, time_limit)

                elif play_button2.collidepoint(pos) and not color:
                    text_color = font4.render("Choose a colour", True, colors.red)
                    screen.blit(text_color, (605, 330))
                    pygame.display.flip()
                    time.sleep(0.1)

                    
                
