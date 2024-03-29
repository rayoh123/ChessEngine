from collections import namedtuple

# The pieces will all be namedtuple objects
Pawn = namedtuple('Pawn', 'name coor side moved')
Knight = namedtuple('Knight', 'name coor side')
King = namedtuple('King', 'name coor side moved')
Bishop = namedtuple('Bishop', 'name coor side')
Rook = namedtuple('Rook', 'name coor side moved')
Queen = namedtuple('Queen', 'name coor side')


def all_possible_moves(piece: namedtuple, game_state) -> set:
    '''
    This function takes in a namedtuple that represents 
    a piece, and a GameState object that represents the 
    state of the game. The function then outputs a set 
    containing all the possible squares this piece can move to.
    '''
    
    possible_moves = set()
    
    # If piece is a pawn
    if piece.name == 'Pawn':
        
        # This helper function adds pawn promotion moves
        def _adding_promotion_options(possible_moves: set, x: str, y: str):
            possible_moves = possible_moves.union({'Q' + x + y, 'R' + x + y, 'B' + x + y, 'N' + x + y})
            return possible_moves
        
        # Different colored pawns need to be dealt with differently because 
        # white pawns move up the board and black pawns move down.
        if piece.side == 'w':
            
            # Checking if the white pawn can advance forwards by one or two squares, or both...
            if game_state[(piece.coor[0], piece.coor[1] + 1)] == None:                
                if piece.coor[1] + 1 == 7:
                    possible_moves = _adding_promotion_options(possible_moves, str(piece.coor[0]), str(piece.coor[1] + 1))
                else:
                    possible_moves.add(str(piece.coor[0]) + str(piece.coor[1] + 1))
                    
                if piece.moved == False and game_state[(piece.coor[0], piece.coor[1] + 2)] == None:
                    possible_moves.add(str(piece.coor[0]) + str(piece.coor[1] + 2))

            # Checking if the white pawn can capture to the left.
            if piece.coor[0] - 1 >= 0:
                if game_state[(piece.coor[0] - 1, piece.coor[1] + 1)] != None and \
                game_state[(piece.coor[0] - 1, piece.coor[1] + 1)].side != piece.side:
                    if piece.coor[1] + 1 == 7:
                        possible_moves = _adding_promotion_options(possible_moves, str(piece.coor[0] - 1), str(piece.coor[1] + 1))
                    else:
                        possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] + 1))

            # Checking if the white pawn can capture to the right.
            if piece.coor[0] + 1 <= 7:
                if game_state[(piece.coor[0] + 1, piece.coor[1] + 1)] != None and \
                game_state[(piece.coor[0] + 1, piece.coor[1] + 1)].side != piece.side:
                    if piece.coor[1] + 1 == 7:
                        possible_moves = _adding_promotion_options(possible_moves, str(piece.coor[0] + 1), str(piece.coor[1] + 1))
                    else:
                        possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] + 1))

        # Now do the same for if the pawn is a black pawn.
        else:
            if game_state[(piece.coor[0], piece.coor[1] - 1)] == None:
                if piece.coor[1] - 1 == 0:
                    possible_moves = _adding_promotion_options(possible_moves, str(piece.coor[0]), str(piece.coor[1] - 1))
                else:
                    possible_moves.add(str(piece.coor[0]) + str(piece.coor[1] - 1))
                if piece.moved == False and game_state[(piece.coor[0], piece.coor[1] - 2)] == None:
                    possible_moves.add(str(piece.coor[0]) + str(piece.coor[1] - 2))

            if piece.coor[0] - 1 >= 0:
                if game_state[(piece.coor[0] - 1, piece.coor[1] - 1)] != None and \
                game_state[(piece.coor[0] - 1, piece.coor[1] - 1)].side != piece.side:
                    if piece.coor[1] - 1 == 0:
                        possible_moves = _adding_promotion_options(possible_moves, str(piece.coor[0] - 1), str(piece.coor[1] - 1))
                    else:
                        possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] - 1))

            if piece.coor[0] + 1 <= 7:
                if game_state[(piece.coor[0] + 1, piece.coor[1] - 1)] != None and \
                game_state[(piece.coor[0] + 1, piece.coor[1] - 1)].side != piece.side:
                    if piece.coor[1] - 1 == 0:
                        possible_moves = _adding_promotion_options(possible_moves, str(piece.coor[0] + 1), str(piece.coor[1] - 1))
                    else:
                        possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] - 1))
        return possible_moves
                            
    elif piece.name == 'King':
        if piece.side == 'w':
            opposite_turn = 'b'
            game_state.recalculate_b_attack_squares()
        if piece.side == 'b':
            opposite_turn = 'w'
            game_state.recalculate_w_attack_squares()

        
        if piece.coor[0] - 1 >= 0:
            if str(piece.coor[0] - 1) + str(piece.coor[1]) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0] - 1, piece.coor[1])] == None or \
               game_state[(piece.coor[0] - 1, piece.coor[1])].side != piece.side):
                possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1]))
            
            if piece.coor[1] - 1 >= 0:
                if str(piece.coor[0] - 1) + str(piece.coor[1] - 1) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0] - 1, piece.coor[1] - 1)] == None or \
               game_state[(piece.coor[0] - 1, piece.coor[1] - 1)].side != piece.side):
                    possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] - 1))

            if piece.coor[1] + 1 <= 7:
                if str(piece.coor[0] - 1) + str(piece.coor[1] + 1) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0] - 1, piece.coor[1] + 1)] == None or \
               game_state[(piece.coor[0] - 1, piece.coor[1] + 1)].side != piece.side):
                    possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] + 1))
            
        if piece.coor[0] + 1 <= 7:
            if str(piece.coor[0] + 1) + str(piece.coor[1]) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0] + 1, piece.coor[1])] == None or \
               game_state[(piece.coor[0] + 1, piece.coor[1])].side != piece.side):
                possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1]))
            
            if piece.coor[1] - 1 >= 0:
                if str(piece.coor[0] + 1) + str(piece.coor[1] - 1) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0] + 1, piece.coor[1] - 1)] == None or \
               game_state[(piece.coor[0] + 1, piece.coor[1] - 1)].side != piece.side):
                    possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] - 1))
                
            if piece.coor[1] + 1 <= 7:
                if str(piece.coor[0] + 1) + str(piece.coor[1] + 1) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0] + 1, piece.coor[1] + 1)] == None or \
               game_state[(piece.coor[0] + 1, piece.coor[1] + 1)].side != piece.side):
                    possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] + 1))
                
        if piece.coor[1] + 1 <= 7:
            if str(piece.coor[0]) + str(piece.coor[1] + 1) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0], piece.coor[1] + 1)] == None or \
               game_state[(piece.coor[0], piece.coor[1] + 1)].side != piece.side):
                possible_moves.add(str(piece.coor[0]) + str(piece.coor[1] + 1))
            
        if piece.coor[1] - 1 >= 0:
            if str(piece.coor[0]) + str(piece.coor[1] - 1) not in getattr(game_state, opposite_turn + '_attack') and \
               (game_state[(piece.coor[0], piece.coor[1] - 1)] == None or \
               game_state[(piece.coor[0], piece.coor[1] - 1)].side != piece.side): 
                possible_moves.add(str(piece.coor[0]) + str(piece.coor[1] - 1))

        if piece.moved == False:
            if piece.side == 'w' and '40' not in game_state.b_attack:
                if type(game_state[(0, 0)]).__name__ == 'Rook' and game_state[(0, 0)].moved == False and \
                   game_state[(1, 0)] == None and '10' not in game_state.b_attack and \
                   game_state[(2, 0)] == None and '20' not in game_state.b_attack and \
                   game_state[(3, 0)] == None and '30' not in game_state.b_attack:
                    possible_moves.add('C20')
                if type(game_state[(7, 0)]).__name__ == 'Rook' and game_state[(7, 0)].moved == False and \
                   game_state[(5, 0)] == None and '50' not in game_state.b_attack and \
                   game_state[(6, 0)] == None and '60' not in game_state.b_attack:
                    possible_moves.add('C60')
            elif piece.side == 'b' and '47' not in game_state.w_attack:
                if type(game_state[(0, 7)]).__name__ == 'Rook' and game_state[(0, 7)].moved == False and \
                   game_state[(1, 7)] == None and '17' not in game_state.w_attack and \
                   game_state[(2, 7)] == None and '27' not in game_state.w_attack and \
                   game_state[(3, 7)] == None and '37' not in game_state.w_attack:
                    possible_moves.add('C27')
                if type(game_state[(7, 7)]).__name__ == 'Rook' and game_state[(7, 7)].moved == False and \
                   game_state[(5, 7)] == None and '57' not in game_state.w_attack and \
                   game_state[(6, 7)] == None and '67' not in game_state.w_attack:
                    possible_moves.add('C67')
        return possible_moves

    elif piece.name == 'Knight':
        if piece.coor[0] + 2 <= 7:
            if piece.coor[1] + 1 <= 7:
                if game_state[piece.coor[0] + 2, piece.coor[1] + 1] == None:
                    possible_moves.add(str(piece.coor[0] + 2) + str(piece.coor[1] + 1))
                elif game_state[piece.coor[0] + 2, piece.coor[1] + 1].side != piece.side:
                    possible_moves.add(str(piece.coor[0] + 2) + str(piece.coor[1] + 1))
                    
            if piece.coor[1] - 1 >= 0:
                if game_state[piece.coor[0] + 2, piece.coor[1] - 1] == None:
                    possible_moves.add(str(piece.coor[0] + 2) + str(piece.coor[1] - 1))
                elif game_state[piece.coor[0] + 2, piece.coor[1] - 1].side != piece.side:
                    possible_moves.add(str(piece.coor[0] + 2) + str(piece.coor[1] - 1))                 
                    
        if piece.coor[0] - 2 >= 0:
            if piece.coor[1] + 1 <= 7:
                if game_state[piece.coor[0] - 2, piece.coor[1] + 1] == None:
                    possible_moves.add(str(piece.coor[0] - 2) + str(piece.coor[1] + 1))
                elif game_state[piece.coor[0] - 2, piece.coor[1] + 1].side != piece.side:
                    possible_moves.add(str(piece.coor[0] - 2) + str(piece.coor[1] + 1))
                    
            if piece.coor[1] - 1 >= 0:
                if game_state[piece.coor[0] - 2, piece.coor[1] - 1] == None:
                    possible_moves.add(str(piece.coor[0] - 2) + str(piece.coor[1] - 1))
                elif game_state[piece.coor[0] - 2, piece.coor[1] - 1].side != piece.side:
                    possible_moves.add(str(piece.coor[0] - 2) + str(piece.coor[1] - 1))

        if piece.coor[0] + 1 <= 7:
            if piece.coor[1] + 2 <= 7:
                if game_state[piece.coor[0] + 1, piece.coor[1] + 2] == None:
                    possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] + 2))
                elif game_state[piece.coor[0] + 1, piece.coor[1] + 2].side != piece.side:
                    possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] + 2))

            if piece.coor[1] - 2 >= 0:
                if game_state[piece.coor[0] + 1, piece.coor[1] - 2] == None:
                    possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] - 2))
                elif game_state[piece.coor[0] + 1, piece.coor[1] - 2].side != piece.side:
                    possible_moves.add(str(piece.coor[0] + 1) + str(piece.coor[1] - 2))

        if piece.coor[0] - 1 >= 0:
            if piece.coor[1] + 2 <= 7:
                if game_state[piece.coor[0] - 1, piece.coor[1] + 2] == None:
                    possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] + 2))
                elif game_state[piece.coor[0] - 1, piece.coor[1] + 2].side != piece.side:
                    possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] + 2))

            if piece.coor[1] - 2 >= 0:
                if game_state[piece.coor[0] - 1, piece.coor[1] - 2] == None:
                    possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] - 2))
                elif game_state[piece.coor[0] - 1, piece.coor[1] - 2].side != piece.side:
                    possible_moves.add(str(piece.coor[0] - 1) + str(piece.coor[1] - 2))
        return possible_moves


    elif piece.name == 'Bishop':
        for i,j in zip(range(piece.coor[0] - 1, -1, -1), range(piece.coor[1] + 1, 8)):
            if game_state[i, j] == None:
                possible_moves.add(str(i) + str(j))
            elif game_state[i, j].side != piece.side:
                possible_moves.add(str(i) + str(j))
                break
            else:
                break
            
        for i,j in zip(range(piece.coor[0] - 1, -1, -1), range(piece.coor[1] - 1, -1, -1)):
            if game_state[i, j] == None:
                possible_moves.add(str(i) + str(j))
            elif game_state[i, j].side != piece.side:
                possible_moves.add(str(i) + str(j))
                break
            else:
                break

        for i,j in zip(range(piece.coor[0] + 1, 8), range(piece.coor[1] + 1, 8)):
            if game_state[i, j] == None:
                possible_moves.add(str(i) + str(j))
            elif game_state[i, j].side != piece.side:
                possible_moves.add(str(i) + str(j))
                break
            else:
                break
            
        for i,j in zip(range(piece.coor[0] + 1, 8), range(piece.coor[1] - 1, -1, -1)):
            if game_state[i, j] == None:
                possible_moves.add(str(i) + str(j))
            elif game_state[i, j].side != piece.side:
                possible_moves.add(str(i) + str(j))
                break
            else:
                break
        return possible_moves

    elif piece.name == 'Rook':
        possible_moves = set()
        for idx in range(piece.coor[1] - 1, -1, -1):
            if game_state[piece.coor[0], idx] == None:
                possible_moves.add(str(piece.coor[0]) + str(idx))
            elif game_state[piece.coor[0], idx].side != piece.side:
                possible_moves.add(str(piece.coor[0]) + str(idx))
                break
            else:
                break

        for idx in range(piece.coor[1] + 1, 8):
            if game_state[piece.coor[0], idx] == None:
                possible_moves.add(str(piece.coor[0]) + str(idx))
            elif game_state[piece.coor[0], idx].side != piece.side:
                possible_moves.add(str(piece.coor[0]) + str(idx))
                break
            else:
                break

        for i in range(piece.coor[0] - 1, -1, -1):
            if game_state[i, piece.coor[1]] == None:
                possible_moves.add(str(i) + str(piece.coor[1]))
            elif game_state[i, piece.coor[1]].side != piece.side:
                possible_moves.add(str(i) + str(piece.coor[1]))
                break
            else:
                break

        for i in range(piece.coor[0] + 1, 8):
            if game_state[i, piece.coor[1]] == None:
                possible_moves.add(str(i) + str(piece.coor[1]))
            elif game_state[i, piece.coor[1]].side != piece.side:
                possible_moves.add(str(i) + str(piece.coor[1]))
                break
            else:
                break
        return possible_moves

    elif piece.name == 'Queen':
        return all_possible_moves(Rook('Rook', piece.coor, piece.side, False), game_state).union(
            all_possible_moves(Bishop('Bishop', piece.coor, piece.side), game_state))

    else:
        raise AssertionError("A piece isn't being passed to all_possible_moves")



        

def update_attack_squares(piece, game_state):
    if piece.name == 'Pawn':
        if piece.side == 'w':
            if piece.coor[0] - 1 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1] + 1)

            if piece.coor[0] + 1 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1] + 1)
        else:
            if piece.coor[0] - 1 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1] - 1)

            if piece.coor[0] + 1 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1] - 1)

    elif piece.name == 'King':
        if piece.coor[0] - 1 >= 0:
            game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1])
            
            if piece.coor[1] - 1 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1] - 1)

            if piece.coor[1] + 1 <= 7:
                
                game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1] + 1)
            
        if piece.coor[0] + 1 <= 7:
            game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1])
            
            if piece.coor[1] - 1 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1] - 1)
                
            if piece.coor[1] + 1 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1] + 1)
                
        if piece.coor[1] + 1 <= 7:
            game_state.attack_adder(piece.side, piece.coor[0], piece.coor[1] + 1)
            
        if piece.coor[1] - 1 >= 0:
            game_state.attack_adder(piece.side, piece.coor[0], piece.coor[1] - 1)

    elif piece.name == 'Knight':
        if piece.coor[0] + 2 <= 7:
            if piece.coor[1] + 1 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] + 2, piece.coor[1] + 1)
                    
            if piece.coor[1] - 1 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] + 2, piece.coor[1] - 1)                    
                    
        if piece.coor[0] - 2 >= 0:
            if piece.coor[1] + 1 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] - 2, piece.coor[1] + 1)
                    
            if piece.coor[1] - 1 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] - 2, piece.coor[1] - 1)

        if piece.coor[0] + 1 <= 7:
            if piece.coor[1] + 2 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1] + 2)

            if piece.coor[1] - 2 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] + 1, piece.coor[1] - 2)

        if piece.coor[0] - 1 >= 0:
            if piece.coor[1] + 2 <= 7:
                game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1] + 2)
                    
            if piece.coor[1] - 2 >= 0:
                game_state.attack_adder(piece.side, piece.coor[0] - 1, piece.coor[1] - 2)

    elif piece.name == 'Bishop':
        for i,j in zip(range(piece.coor[0] - 1, -1, -1), range(piece.coor[1] + 1, 8)):
            if game_state[i, j] == None:
                game_state.attack_adder(piece.side, i, j)
            else:
                game_state.attack_adder(piece.side, i, j)
                break
            
        for i,j in zip(range(piece.coor[0] - 1, -1, -1), range(piece.coor[1] - 1, -1, -1)):
            if game_state[i, j] == None:
                game_state.attack_adder(piece.side, i, j)
            else:
                game_state.attack_adder(piece.side, i, j)
                break

        for i,j in zip(range(piece.coor[0] + 1, 8), range(piece.coor[1] + 1, 8)):
            if game_state[i, j] == None:
                game_state.attack_adder(piece.side, i, j)
            else:
                game_state.attack_adder(piece.side, i, j)
                break
            
        for i,j in zip(range(piece.coor[0] + 1, 8), range(piece.coor[1] - 1, -1, -1)):
            if game_state[i, j] == None:
                game_state.attack_adder(piece.side, i, j)
            else:
                game_state.attack_adder(piece.side, i, j)
                break

    elif piece.name == 'Rook':
        possible_moves = set()
        for idx in range(piece.coor[1] - 1, -1, -1):
            if game_state[piece.coor[0], idx] == None:
                game_state.attack_adder(piece.side, piece.coor[0], idx)
            else:
                game_state.attack_adder(piece.side, piece.coor[0], idx)
                break

        for idx in range(piece.coor[1] + 1, 8):
            if game_state[piece.coor[0], idx] == None:
                game_state.attack_adder(piece.side, piece.coor[0], idx)
            else:
                game_state.attack_adder(piece.side, piece.coor[0], idx)
                break

        for i in range(piece.coor[0] - 1, -1, -1):
            if game_state[i, piece.coor[1]] == None:
                game_state.attack_adder(piece.side, i, piece.coor[1])
            else:
                game_state.attack_adder(piece.side, i, piece.coor[1])
                break

        for i in range(piece.coor[0] + 1, 8):
            if game_state[i, piece.coor[1]] == None:
                game_state.attack_adder(piece.side, i, piece.coor[1])
            else:
                game_state.attack_adder(piece.side, i, piece.coor[1])
                break


    elif piece.name == 'Queen':
        update_attack_squares(Rook('Rook', piece.coor, piece.side, False), game_state)
        update_attack_squares(Bishop('Bishop', piece.coor, piece.side), game_state)

    else:
        raise AssertionError("A piece isn't being passed to update_attack_squares")
