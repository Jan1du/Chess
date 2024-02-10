class main:
    def __init__(self, white_pieces, black_pieces, white_locations, black_locations, w_check, b_check, white_ep, black_ep):
        self.white_pieces = white_pieces
        self.black_pieces = black_pieces
        self.white_locations = white_locations
        self.black_locations = black_locations
        self.w_check = w_check
        self.b_check = b_check
        self.white_ep = white_ep
        self.black_ep = black_ep


    def move_options(self, pieces, locations, turn):
        moves_list = []
        all_moves_list = []
        check = False
        if turn == 'white':
            e_pieces = self.black_pieces
            e_locations = self.black_locations
            check = self.w_check
            ep_coords = self.black_ep

        else:
            e_pieces = self.white_pieces
            e_locations = self.white_locations
            check = self.b_check
            ep_coords = self.white_ep

        if check == True:
            king_index = pieces.index('king')
            k_location = locations[king_index]
            all_moves_list = self.check_options(e_locations, locations, pieces, k_location, turn, ep_coords)
        else:
            for i in range(len(pieces)):
                location = locations[i]
                piece = pieces[i]

                if piece == 'pawn':
                    moves_list = self.moves_pawn(locations, e_locations, location, turn, ep_coords)
                elif piece == 'rook':
                    moves_list = self.moves_rook(locations, e_locations, location)
                elif piece == 'knight':
                    moves_list = self.moves_knight(locations, location)
                elif piece == 'bishop':
                    moves_list = self.moves_bishop(locations, e_locations, location)
                elif piece == 'queen':
                    moves_list = self.moves_queen(locations, e_locations, location)
                elif piece == 'king':
                    moves_list = self.moves_king(locations, location)

                # Check each potential legal move for the piece
                valid_moves = []
                for move in moves_list:
                    #Simulate the move temporarily
                    temp_e_pieces = e_pieces.copy()
                    temp_e_locations = e_locations.copy()
                    locations[i] = move

                    if move in temp_e_locations:
                        e_index = temp_e_locations.index(move)
                        temp_e_pieces.pop(e_index)
                        temp_e_locations.pop(e_index)

                    #Check if the move puts the own king in check
                    king_index = pieces.index('king')
                    k_location = locations[king_index]
                    if not self.is_in_check(k_location, turn, temp_e_pieces, temp_e_locations, locations):
                        valid_moves.append(move)
                    locations[i] = location

                all_moves_list.append(valid_moves)

        return all_moves_list

    #To get move list of the enemy pieces in check_options()
    def enemy_moves(self, pieces, locations, e_locations, turn):
        all_moves = []
        moves_list = []
        for i in range(len(pieces)):
            location = locations[i]
            piece = pieces[i]

            if piece == 'pawn':
                moves_list = self.moves_pawn(locations, e_locations, location, turn, ())        #no need to check for en passants
            elif piece == 'rook':
                moves_list = self.moves_rook(locations, e_locations, location)
            elif piece == 'knight':
                moves_list = self.moves_knight(locations, location)
            elif piece == 'bishop':
                moves_list = self.moves_bishop(locations, e_locations, location)
            elif piece == 'queen':
                moves_list = self.moves_queen(locations, e_locations, location)
            elif piece == 'king':
                moves_list = self.moves_king(locations, location)

            all_moves.append(moves_list)
        
        return all_moves

    #Pawn Movement
    def moves_pawn(self, friends_list, enemies_list, position, color, ep):
        moves_list = []
        if color == 'white':
            #Move 1 square
            if (position[0], position[1] - 1) not in enemies_list and \
                (position[0], position[1] - 1) not in friends_list and position[1] > 0:
                moves_list.append((position[0], position[1] - 1))
                #Move 2 squares
                if (position[0], position[1] - 2) not in enemies_list and \
                    (position[0], position[1] - 2) not in friends_list and position[1] == 6:
                    moves_list.append((position[0], position[1] - 2))
            #Capture a piece to the right
            if (position[0] + 1, position[1] - 1) in enemies_list:
                moves_list.append((position[0] + 1, position[1] - 1))
            #Capture a piece to the left
            if (position[0] - 1, position[1] - 1) in enemies_list:
                moves_list.append((position[0] - 1, position[1] - 1)) 

            #En Passant moves
            if (position[0] + 1, position[1] - 1) == ep:       #To the right
                moves_list.append((position[0] + 1, position[1] - 1))
            if (position[0] - 1, position[1] - 1) == ep:       #To the left
                moves_list.append((position[0] - 1, position[1] - 1)) 


        else:
            #Move 1 square
            if (position[0], position[1] + 1) not in friends_list and \
                (position[0], position[1] + 1) not in enemies_list and position[1] < 7:
                moves_list.append((position[0], position[1] + 1))
                #Move 2 squares
                if (position[0], position[1] + 2) not in friends_list and \
                    (position[0], position[1] + 2) not in enemies_list and position[1] == 1:
                    moves_list.append((position[0], position[1] + 2))
            #Capture a piece to the right
            if (position[0] + 1, position[1] + 1) in enemies_list:
                moves_list.append((position[0] + 1, position[1] + 1))
            #Capture a piece to the left
            if (position[0] - 1, position[1] + 1) in enemies_list:
                moves_list.append((position[0] - 1, position[1] + 1))

            #En Passant moves
            if (position[0] + 1, position[1] + 1) == ep:       #To the right
                moves_list.append((position[0] + 1, position[1] + 1))
            if (position[0] - 1, position[1] + 1) == ep:       #To the left
                moves_list.append((position[0] - 1, position[1] + 1)) 
            

        return moves_list

    #Rook Movement
    def moves_rook(self, friends_list, enemies_list, position): 
        moves_list = []
        direction_of_movement = [(0, 1), (0, -1), (1, 0), (-1, 0)] #right, left, down, up

        for i in range(len(direction_of_movement)): 
            path = True
            chain = 1

            x, y = direction_of_movement[i]

            while path:
                nextChainSpace = (position[0] + (chain * x), position[1] + (chain * y)) #the next space in the line of the rooks movement
                if nextChainSpace not in friends_list:
                    if 0 <= nextChainSpace[0] <= 7 and 0 <= nextChainSpace[1] <= 7:
                        moves_list.append(nextChainSpace)
                        if nextChainSpace in enemies_list:
                            path = False
                        chain += 1
                    else:
                        path = False
                else:
                    path = False
        return moves_list

    #Kight Movement
    def moves_knight(self, friends_list, position):
        moves_list = []

        # 8 squares to check for knights, they can go two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
                moves_list.append(target)
        return moves_list

    #Bishop Movement
    def moves_bishop(self, friends_list, enemies_list, position):
        moves_list = []
        direction_of_movement = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  #down-right, down-left, up-right, down-left

        for i in range(len(direction_of_movement)): 
            path = True
            chain = 1

            x, y = direction_of_movement[i]

            while path:
                nextChainSpace = (position[0] + (chain * x), position[1] + (chain * y))
                if nextChainSpace not in friends_list:
                    if 0 <= nextChainSpace[0] <= 7 and 0 <= nextChainSpace[1] <= 7:
                        moves_list.append(nextChainSpace)
                        if nextChainSpace in enemies_list:
                            path = False
                        chain += 1
                    else:
                        path = False
                else:
                    path = False
        return moves_list

    #Queen Movement
    def moves_queen(self, friends_list, enemies_list, position):
        moves_list = self.moves_bishop(friends_list, enemies_list, position)
        second_list = self.moves_rook(friends_list, enemies_list, position)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list

    #King Movement
    def moves_king(self, friends_list, position):
        moves_list = []

        #8 squares to check for kings, they can go one square any direction
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(len(targets)):
            target = (position[0] + targets[i][0], position[1] + targets[i][1])
            if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:  #If the move is not blacked by the edges of the board or the friendly pieces
                moves_list.append(target)

        return moves_list

    #Checks the valid moves when in check
    def check_options(self, e_locations, locations, pieces, k_position, color, ep):
        all_moves = []
        filtered_moves = []  #Used to temporary keep the opponent moves 
        for i in range(len(pieces)):
            piece = pieces[i]
            position = locations[i]
            if piece == "king":
                king_index = pieces.index(piece)
                moves_list = self.moves_king(locations, position)
                if color == 'white':
                    #Temporary removes the king's coords from white_locations so that new_black_options1 can consider all the moves not considering the king
                    #This used to detect the squares of a line of attack of a bishop, rook or queen, directly behind the king
                    locations[king_index] = ()
                    new_black_options1 = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black') 
                    locations[king_index] = position    #puts the king back into the list
                    
                    for b_piece in range(len(self.black_pieces)):
                        #Removes all the pawn move options from the list as the movement pattern and attack patterns are different for pawns
                        if self.black_pieces[b_piece] != "pawn":
                            filtered_moves.append(new_black_options1[b_piece]) 
                        #adds the attack options for the pawns into the list
                        else:
                            p_location = self.black_locations[b_piece]
                            filtered_moves.append([(p_location[0] + 1, p_location[1] + 1)])
                            filtered_moves.append([(p_location[0] - 1, p_location[1] + 1)])
                    new_black_options1 = filtered_moves
                    filtered_moves = []

                    for move in moves_list:
                        #Compares the moves in new_black_options1 and the moves in moves_list and removes any moves that overlaps
                        if not any(move in option for option in new_black_options1):
                            filtered_moves.append(move)

                        #Checks if the pieces can be taken or not
                        if move in self.black_locations:
                            move_index = self.black_locations.index(move)

                            #Temporary removes the piece coords and the name from black_location and black_pieces to see if the piece is protected
                            piece_capturing = self.black_pieces[move_index]
                            self.black_locations[move_index] = ()
                            self.black_pieces[move_index] = ""
                            locations[king_index] = ()
                            new_black_options2 = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black') 
                            self.black_locations[move_index] = move
                            self.black_pieces[move_index] = piece_capturing
                            locations[king_index] = position

                            #To remove pawn moves from protecting the piece
                            filtered_black_options = []
                            for b_piece in range(len(self.black_pieces)):
                                if self.black_pieces[b_piece] != "pawn":
                                    filtered_black_options.append(new_black_options2[b_piece])
                            
                            if any(move in option for option in filtered_black_options) and filtered_moves:
                                filtered_moves.pop()

                        
                    moves_list = filtered_moves
                    filtered_moves = []
                
                else:
                    #Temporary removes the king's coords from black_locations so that new_white_options1 can consider all the moves not considering the king
                    #This used to detect the squares of a line of attack of a bishop, rook or queen, directly behind the king
                    locations[king_index] = ()
                    new_white_options1 = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                    locations[king_index] = position    #puts the king back into the list
                    
                    for w_piece in range(len(self.white_pieces)):
                        #Removes all the pawn move options from the list as the movement pattern and attack patterns are different for pawns
                        if self.white_pieces[w_piece] != "pawn":
                            filtered_moves.append(new_white_options1[w_piece]) 
                        #adds the attack options for the pawns into the list   
                        else:
                            p_location = self.white_locations[w_piece]
                            filtered_moves.append([(p_location[0] + 1, p_location[1] - 1)])
                            filtered_moves.append([(p_location[0] - 1, p_location[1] - 1)])      
                    new_white_options1 = filtered_moves
                    filtered_moves = []
                    
                    #Checks if the pieces can be taken or not
                    for move in moves_list:
                        #Compares the moves in new_white_options1 and the moves in moves_list and removes any moves that overlaps
                        if not any(move in option for option in new_white_options1):
                            filtered_moves.append(move)
                        
                        if move in self.white_locations:
                            move_index = self.white_locations.index(move)

                            #Temporary removes the piece coords and the name from white_location and white_pieces to see if the piece is protected
                            piece_capturing = self.white_pieces[move_index]
                            self.white_locations[move_index] = ()
                            self.white_pieces[move_index] = ""
                            locations[king_index] = ()
                            new_white_options2 = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                            self.white_locations[move_index] = move
                            self.white_pieces[move_index] = piece_capturing
                            locations[king_index] = position

                            #To remove pawn moves from protecting the piece
                            filtered_white_options = []
                            for w_piece in range(len(self.white_pieces)):
                                if self.white_pieces[w_piece] != "pawn":
                                    filtered_white_options.append(new_white_options2[w_piece])

                            if any(move in option for option in filtered_white_options) and filtered_moves:
                                filtered_moves.pop()

                    moves_list = filtered_moves
                    filtered_moves = []
                all_moves.append(moves_list)

            elif piece == "pawn":
                moves_list = self.moves_pawn(locations, e_locations, position, color, ep)
                
                if color == "white":
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the pawn to check if this move blocks the check
                        
                        if move in self.black_locations:     #Temporary removes the black piece in case a capture is possible
                            captured = True
                            b_piece_index = self.black_locations.index(move)
                            piece_capturing = self.black_pieces[b_piece_index]
                            self.black_pieces[b_piece_index] = ""
                            self.black_locations[b_piece_index] = ()
                        
                        new_black_options = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black')
                        if not any(k_position in option for option in new_black_options):
                            filtered_moves.append(move)
                        
                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.black_locations[b_piece_index] = move
                            self.black_pieces[b_piece_index] = piece_capturing

                    moves_list = filtered_moves
                    filtered_moves = []
                
                else:
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the pawn to check if this move blocks the check

                        if move in self.white_locations:     #Temporary removes the white piece in case a capture is possible
                            captured = True
                            w_piece_index = self.white_locations.index(move)
                            piece_capturing = self.white_pieces[w_piece_index]
                            self.white_pieces[w_piece_index] = ""
                            self.white_locations[w_piece_index] = ()

                        new_white_options = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                        if not any(k_position in option for option in new_white_options):
                            filtered_moves.append(move)

                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.white_locations[w_piece_index] = move
                            self.white_pieces[w_piece_index] = piece_capturing 

                    moves_list = filtered_moves
                    filtered_moves = [] 

                all_moves.append(moves_list)
            
            elif piece == "knight":
                moves_list = self.moves_knight(locations, position)
                
                if color == "white":
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the knight to check if this move blocks the check
                        
                        if move in self.black_locations:     #Temporary removes the black piece in case a capture is possible
                            captured = True
                            b_piece_index = self.black_locations.index(move)
                            piece_capturing = self.black_pieces[b_piece_index]
                            self.black_pieces[b_piece_index] = ""
                            self.black_locations[b_piece_index] = ()
                        
                        new_black_options = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black')
                        if not any(k_position in option for option in new_black_options):
                            filtered_moves.append(move)
                        
                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.black_locations[b_piece_index] = move
                            self.black_pieces[b_piece_index] = piece_capturing

                    moves_list = filtered_moves
                    filtered_moves = []
                
                else:
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the knight to check if this move blocks the check

                        if move in self.white_locations:     #Temporary removes the white piece in case a capture is possible
                            captured = True
                            w_piece_index = self.white_locations.index(move)
                            piece_capturing = self.white_pieces[w_piece_index]
                            self.white_pieces[w_piece_index] = ""
                            self.white_locations[w_piece_index] = ()

                        new_white_options = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                        if not any(k_position in option for option in new_white_options):
                            filtered_moves.append(move)

                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.white_locations[w_piece_index] = move
                            self.white_pieces[w_piece_index] = piece_capturing 

                    moves_list = filtered_moves
                    filtered_moves = [] 

                all_moves.append(moves_list)
            
            elif piece == "bishop":
                moves_list = self.moves_bishop(locations, e_locations, position)
                
                if color == "white":
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the bishop to check if this move blocks the check
                        
                        if move in self.black_locations:     #Temporary removes the black piece in case a capture is possible
                            captured = True
                            b_piece_index = self.black_locations.index(move)
                            piece_capturing = self.black_pieces[b_piece_index]
                            self.black_pieces[b_piece_index] = ""
                            self.black_locations[b_piece_index] = ()
                        
                        new_black_options = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black')
                        if not any(k_position in option for option in new_black_options):
                            filtered_moves.append(move)
                        
                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.black_locations[b_piece_index] = move
                            self.black_pieces[b_piece_index] = piece_capturing

                    moves_list = filtered_moves
                    filtered_moves = []
                
                else:
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the pawn to check if this move blocks the check

                        if move in self.white_locations:     #Temporary removes the white piece in case a capture is possible
                            captured = True
                            w_piece_index = self.white_locations.index(move)
                            piece_capturing = self.white_pieces[w_piece_index]
                            self.white_pieces[w_piece_index] = ""
                            self.white_locations[w_piece_index] = ()

                        new_white_options = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                        if not any(k_position in option for option in new_white_options):
                            filtered_moves.append(move)

                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.white_locations[w_piece_index] = move
                            self.white_pieces[w_piece_index] = piece_capturing 

                    moves_list = filtered_moves
                    filtered_moves = [] 

                all_moves.append(moves_list)
            
            elif piece == "rook":
                moves_list = self.moves_rook(locations, e_locations, position)
                
                if color == "white":
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the rook to check if this move blocks the check
                        
                        if move in self.black_locations:     #Temporary removes the black piece in case a capture is possible
                            captured = True
                            b_piece_index = self.black_locations.index(move)
                            piece_capturing = self.black_pieces[b_piece_index]
                            self.black_pieces[b_piece_index] = ""
                            self.black_locations[b_piece_index] = ()
                        
                        new_black_options = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black')
                        if not any(k_position in option for option in new_black_options):
                            filtered_moves.append(move)
                        
                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.black_locations[b_piece_index] = move
                            self.black_pieces[b_piece_index] = piece_capturing

                    moves_list = filtered_moves
                    filtered_moves = []
                
                else:
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the pawn to check if this move blocks the check

                        if move in self.white_locations:     #Temporary removes the white piece in case a capture is possible
                            captured = True
                            w_piece_index = self.white_locations.index(move)
                            piece_capturing = self.white_pieces[w_piece_index]
                            self.white_pieces[w_piece_index] = ""
                            self.white_locations[w_piece_index] = ()

                        new_white_options = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                        if not any(k_position in option for option in new_white_options):
                            filtered_moves.append(move)

                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.white_locations[w_piece_index] = move
                            self.white_pieces[w_piece_index] = piece_capturing 

                    moves_list = filtered_moves
                    filtered_moves = [] 

                all_moves.append(moves_list)
            
            elif piece == "queen":
                moves_list = self.moves_queen(locations, e_locations, position)
                
                if color == "white":
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the queen to check if this move blocks the check
                        
                        if move in self.black_locations:     #Temporary removes the black piece in case a capture is possible
                            captured = True
                            b_piece_index = self.black_locations.index(move)
                            piece_capturing = self.black_pieces[b_piece_index]
                            self.black_pieces[b_piece_index] = ""
                            self.black_locations[b_piece_index] = ()
                        
                        new_black_options = self.enemy_moves(self.black_pieces, self.black_locations, self.white_locations, 'black')
                        if not any(k_position in option for option in new_black_options):
                            filtered_moves.append(move)
                        
                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.black_locations[b_piece_index] = move
                            self.black_pieces[b_piece_index] = piece_capturing

                    moves_list = filtered_moves
                    filtered_moves = []
                
                else:
                    for move in moves_list:
                        captured = False
                        locations[i] = move     #Temporary move the pawn to check if this move blocks the check

                        if move in self.white_locations:     #Temporary removes the white piece in case a capture is possible
                            captured = True
                            w_piece_index = self.white_locations.index(move)
                            piece_capturing = self.white_pieces[w_piece_index]
                            self.white_pieces[w_piece_index] = ""
                            self.white_locations[w_piece_index] = ()

                        new_white_options = self.enemy_moves(self.white_pieces, self.white_locations, self.black_locations, 'white')
                        if not any(k_position in option for option in new_white_options):
                            filtered_moves.append(move)

                        #Resetting the position
                        locations[i] = position
                        if captured == True:
                            self.white_locations[w_piece_index] = move
                            self.white_pieces[w_piece_index] = piece_capturing 

                    moves_list = filtered_moves
                    filtered_moves = [] 

                all_moves.append(moves_list)
        
        return all_moves


    #Check if the king is attacked in a temporary position
    #! King can still take pieces that leads to a check if not in check.
    def is_in_check(self, k_location, color, enemy_pieces, enemy_locations, friend_locations):
        enemy_moves = []
        in_check = False
        if color == "white":
            enemy_color = "black"
        else:
            enemy_color = "white"

        for i in range(len(enemy_pieces)):
            piece = enemy_pieces[i]
            location = enemy_locations[i]
            if piece == "pawn":
                enemy_moves = self.moves_pawn(enemy_locations, friend_locations, location, enemy_color, ())     #No need to check for en passants
            elif piece == "knight":
                enemy_moves = self.moves_knight(enemy_locations, location)
            elif piece == "bishop":
                enemy_moves = self.moves_bishop(enemy_locations, friend_locations, location)
            elif piece == "rook":
                enemy_moves = self.moves_rook(enemy_locations, friend_locations, location)
            elif piece == "queen":
                enemy_moves = self.moves_queen(enemy_locations, friend_locations, location)
            
            if k_location in enemy_moves:
                in_check = True
                break

        return in_check