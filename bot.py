import random
import time
import game_constants as gc
import move_functions

#Makes a random move
def get_random_move(options):
    moves_list = []     #In the form [[piece_index, move], ...]
    for i in range(len(options)):
        if options[i]:
            for j in options[i]:
                list = [i, j]
                moves_list.append(list)
    
    rand = random.choice(moves_list)
    piece_index = rand[0]
    random_move = rand[1]

    return piece_index, random_move

class engine:
    def __init__(self, white_pieces, black_pieces, white_locations, black_locations, w_check, b_check, white_ep, black_ep):
        self.new_white_pieces = white_pieces.copy()
        self.new_black_pieces = black_pieces.copy()
        self.new_white_locations = white_locations.copy()
        self.new_black_locations = black_locations.copy()
        self.w_check = w_check
        self.b_check = b_check
        self.white_ep = white_ep
        self.black_ep = black_ep

    def eval_function(self):
        w_points = 0
        b_points = 0
        for piece in self.new_white_pieces:
            w_points += self.points(piece)
        for piece in self.new_black_pieces:
            b_points += self.points(piece)

        total_eval = w_points - b_points
        return total_eval

    def points(self, piece):
        if piece == "pawn":
            return 100
        elif piece == "bishop":
            return 305
        elif piece == "knight":
            return 300
        elif piece == "rook":
            return 500
        elif piece == "queen":
            return 900
        elif piece == "king":
            return 999999
        
    #Minimax algorithm with alpha-beta pruning
    #Produces a tree of given maxDepth to check the best moves in the position
    def alpha_beta(self, alpha, beta, depth, color):
        if depth == 0:
            return self.eval_function()
        
        functions = move_functions.main(self.new_white_pieces, self.new_black_pieces, self.new_white_locations, self.new_black_locations, self.w_check, self.b_check, self.white_ep, self.black_ep)
        if color == "white":
            max_eval = -100000000
            white_options = functions.move_options(self.new_white_pieces, self.new_white_locations, "white")
            
            for i in range(len(white_options)):
                for move in white_options[i]:
                    w_pieces = self.new_white_pieces.copy()
                    w_locations = self.new_white_locations.copy()
                    b_pieces = self.new_black_pieces.copy()
                    b_locations = self.new_black_locations.copy()

                    self.new_white_locations[i] = move
                    if move in self.new_black_locations:
                        index = self.new_black_locations.index(move)
                        self.new_black_pieces.pop(index)
                        self.new_black_locations.pop(index)

                    eval = self.alpha_beta(alpha, beta, depth-1, "black")
                    if eval > max_eval:
                        max_eval = eval

                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                    
                    self.new_white_pieces = w_pieces.copy()
                    self.new_white_locations = w_locations.copy()
                    self.new_black_pieces = b_pieces.copy()
                    self.new_black_locations = b_locations.copy()    
                      
            return max_eval
        
        else:
            min_eval = 100000000
            black_options = functions.move_options(self.new_black_pieces, self.new_black_locations, "black")

            for i in range(len(black_options)):
                for move in black_options[i]:
                    w_pieces = self.new_white_pieces.copy()
                    w_locations = self.new_white_locations.copy()
                    b_pieces = self.new_black_pieces.copy()
                    b_locations = self.new_black_locations.copy()

                    self.new_black_locations[i] = move
                    if move in self.new_white_locations:
                        index = self.new_white_locations.index(move)
                        self.new_white_pieces.pop(index)
                        self.new_white_locations.pop(index)

                    eval = self.alpha_beta(alpha, beta, depth-1, "white")
                    if eval < min_eval:
                        min_eval = eval
                    
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                    
                    self.new_white_pieces = w_pieces.copy()
                    self.new_white_locations = w_locations.copy()
                    self.new_black_pieces = b_pieces.copy()
                    self.new_black_locations = b_locations.copy()
            
            return min_eval
        
    def get_best_move(self, depth, alpha, beta, color):
        piece_index = None
        best_move = None
        functions = move_functions.main(gc.white_pieces, gc.black_pieces, gc.white_locations, gc.black_locations, self.w_check, self.b_check, self.white_ep, self.black_ep)
        if color == "white":
            max_eval = -100000000
            white_options = functions.move_options(gc.white_pieces, gc.white_locations, "white")
            
            for i in range(len(white_options)):
                for move in white_options[i]:
                    self.new_white_locations[i] = move
                    if move in self.new_black_locations:
                        index = self.new_black_locations.index(move)
                        self.new_black_pieces.pop(index)
                        self.new_black_locations.pop(index)

                    eval = self.alpha_beta(alpha, beta, depth-1, "black")
                    if eval > max_eval:
                        max_eval = eval
                        best_move = move
                        piece_index = i
                    
                    #alpha = max(alpha, eval)
                    #if beta <= alpha:
                        #break

                    self.new_white_pieces = gc.white_pieces.copy()
                    self.new_white_locations = gc.white_locations.copy()
                    self.new_black_pieces = gc.black_pieces.copy()
                    self.new_black_locations = gc.black_locations.copy()
                        
        
        else:
            min_eval = 100000000
            black_options = functions.move_options(gc.black_pieces, gc.black_locations, "black")

            for i in range(len(black_options)):
                for move in black_options[i]:
                    self.new_black_locations[i] = move
                    if move in self.new_white_locations:
                        index = self.new_white_locations.index(move)
                        self.new_white_pieces.pop(index)
                        self.new_white_locations.pop(index)

                    eval = self.alpha_beta(alpha, beta, depth-1, "white")
                    if eval < min_eval:
                        min_eval = eval
                        best_move = move
                        piece_index = i
                    
                    #beta = min(beta, eval)
                    #if beta <= alpha:
                        #break

                    self.new_white_pieces = gc.white_pieces.copy()
                    self.new_white_locations = gc.white_locations.copy()
                    self.new_black_pieces = gc.black_pieces.copy()
                    self.new_black_locations = gc.black_locations.copy()
        
        if piece_index and best_move:
            return piece_index, best_move

        else:
            print("help")
            if color == "white":
                options = functions.move_options(gc.white_pieces, gc.white_locations, "white")
            else:
                options = functions.move_options(gc.black_pieces, gc.black_locations, "black")
            piece_index, best_move = get_random_move(options)
            return piece_index, best_move