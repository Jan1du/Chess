import pygame
import os
pygame.init()


width, height = 900, 600
board_width, board_height = 600, 600
fps = 60
small_piece_width, small_piece_height = 45, 45
montserrat = os.path.join("fonts", "Montserrat", "Montserrat-Bold.ttf")
tektur = os.path.join("fonts", "Tektur", "Tektur-Bold.ttf")
random_colors = ["white", "black"]


#==========colors============#
class colors:
    black = (0,0,0)
    white = (255,255,255)
    dark_grey = (30,30,30)
    grey = (50,50,50)
    light_grey = (150,150,150)
    blue = (0, 158, 248)
    light_blue = (20, 157, 183)
    red = (255,0,0)
    green = (0, 255, 0)
    purple = (130,10,130)
    amber = (255, 191, 0)


#Setting up the screen
screen = pygame.display.set_mode([width,height])
clock = pygame.time.Clock()
pygame.display.set_caption("chess")

#=============Assets=============#
class assets:
    background = pygame.image.load(os.path.join("chess assets", "chess_board.png"))
    background = pygame.transform.scale(background, (board_width, board_height))

    move_sound = pygame.mixer.Sound("chess assets/move.wav")
    capture_sound = pygame.mixer.Sound("chess assets/capture.wav")
    check_sound = pygame.mixer.Sound("chess assets/check.wav")
    castle_sound = pygame.mixer.Sound("chess assets/castle.wav")
    mate_sound = pygame.mixer.Sound("chess assets/mate.wav")
    promotion_sound = pygame.mixer.Sound("chess assets/promote.wav")
    wrong_sound = pygame.mixer.Sound("chess assets/buzz.wav")

    w_king = pygame.image.load(os.path.join("chess assets", "w_king.png"))
    w_king = pygame.transform.scale(w_king, (board_width/8, board_height/8))
    b_king = pygame.image.load(os.path.join("chess assets", "b_king.png"))
    b_king = pygame.transform.scale(b_king, (board_width/8, board_height/8))
    w_queen = pygame.image.load(os.path.join("chess assets", "w_queen.png"))
    w_queen = pygame.transform.scale(w_queen, (board_width/8, board_height/8))
    w_queen_small = pygame.transform.scale(w_queen, (small_piece_width, small_piece_height))
    b_queen = pygame.image.load(os.path.join("chess assets", "b_queen.png"))
    b_queen = pygame.transform.scale(b_queen, (board_width/8, board_height/8))
    b_queen_small = pygame.transform.scale(b_queen, (small_piece_width, small_piece_height))
    w_rook = pygame.image.load(os.path.join("chess assets", "w_rook.png"))
    w_rook = pygame.transform.scale(w_rook, (board_width/8, board_height/8))
    w_rook_small = pygame.transform.scale(w_rook, (small_piece_width, small_piece_height))
    b_rook = pygame.image.load(os.path.join("chess assets", "b_rook.png"))
    b_rook = pygame.transform.scale(b_rook, (board_width/8, board_height/8))
    b_rook_small = pygame.transform.scale(b_rook, (small_piece_width, small_piece_height))
    w_bishop = pygame.image.load(os.path.join("chess assets", "w_bishop.png"))
    w_bishop = pygame.transform.scale(w_bishop, (board_width/8, board_height/8))
    w_bishop_small = pygame.transform.scale(w_bishop, (small_piece_width, small_piece_height))
    b_bishop = pygame.image.load(os.path.join("chess assets", "b_bishop.png"))
    b_bishop = pygame.transform.scale(b_bishop, (board_width/8, board_height/8))
    b_bishop_small = pygame.transform.scale(b_bishop, (small_piece_width, small_piece_height))
    w_knight = pygame.image.load(os.path.join("chess assets", "w_knight.png"))
    w_knight = pygame.transform.scale(w_knight, (board_width/8, board_height/8))
    w_knight_small = pygame.transform.scale(w_knight, (small_piece_width, small_piece_height))
    b_knight = pygame.image.load(os.path.join("chess assets", "b_knight.png"))
    b_knight = pygame.transform.scale(b_knight, (board_width/8, board_height/8))
    b_knight_small = pygame.transform.scale(b_knight, (small_piece_width, small_piece_height))
    w_pawn = pygame.image.load(os.path.join("chess assets", "w_pawn.png"))
    w_pawn = pygame.transform.scale(w_pawn, (board_width/8, board_height/8))
    w_pawn_small = pygame.transform.scale(w_pawn, (small_piece_width, small_piece_height))
    b_pawn = pygame.image.load(os.path.join("chess assets", "b_pawn.png"))
    b_pawn = pygame.transform.scale(b_pawn, (board_width/8, board_height/8))
    b_pawn_small = pygame.transform.scale(b_pawn, (small_piece_width, small_piece_height))

white_images = [assets.w_pawn, assets.w_queen, assets.w_king, assets.w_knight, assets.w_rook, assets.w_bishop]
black_images = [assets.b_pawn, assets.b_queen, assets.b_king, assets.b_knight, assets.b_rook, assets.b_bishop]
small_white_images = [assets.w_pawn_small, assets.w_queen_small, assets.w_knight_small, assets.w_rook_small, assets.w_bishop_small]
small_black_images = [assets.b_pawn_small, assets.b_queen_small, assets.b_knight_small, assets.b_rook_small, assets.b_bishop_small]

#The pieces in the following lists should be in order of the respective image lists
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop'] #To link the images with the black_pieces and white_pieces
small_piece_list = ['pawn', 'queen', 'knight', 'rook', 'bishop'] #To find the index of the respective pieces from small white and black image lists


#===========Position arrays========#
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_moved = [False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False]      #Check if piece has moved for castling
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
white_moved = [False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False]      #Check if piece has moved for castling
captured_pieces_white = []
captured_pieces_black = []


#=====Game Variables=====#
#0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
#Stores the index of the piece selected from black_pieces or white_pieces
#A large value for when no piece is selected. 
selection = 100     
valid_moves = []    #stores the valid moves for a selected piece
piece_captured = False      #Check if a piece is captured

#En Passant coordinates(variable)
white_ep = ()
black_ep = ()

flashing_counter = 0    #Used to flash the king square when in check
sound_counter = 0   #Used to make the winning sound 1 time

#check variables
winner = None
w_check = False
b_check = False
game_over = False

#promotion variables
w_promotion = False
b_promotion = False

#==Time variables==#
time_white = None
time_black = None

#==Draw variables==#
#Stores all the previous positions for 3-fold repetition
positions = []      #[(white_locations, black_locations)]
#Records how many times each position is played
position_played = []
#For 50-move rule
pawn_move_counter = 10


#For castling
castle_moves = [] #[(King_pos, rook_pos), ...]
castled = False #For the castle sound