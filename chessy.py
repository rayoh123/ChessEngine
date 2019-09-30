###################################################################################################
###   The gamestate of the chess game is represented in a set with all the pieces as elements.
###   Another set stores the White pieces, a set stores the Black pieces,
###   a set of all the squares White attacks, and a set of all the squares Black attacks.
###   Then after every move, these sets get updated to reflect the most current position.
###   


from pieces import King, Queen, Bishop, Knight, Rook, Pawn, update_attack_squares, all_possible_moves
from collections import defaultdict, namedtuple


class GameState():
    def __init__(self, board=None, turn='w', last_one=0, history=None, human='w', computer='b'):
        if board == None:
            self.board = {
             (0, 0) : Rook('Rook', (0,0), 'w', False), (0, 1) : Pawn('Pawn', (0,1), 'w', False),
             (0, 2) : None, (0, 3) : None, (0, 4) : None,(0, 5) : None,
             (0, 6) : Pawn('Pawn', (0,6), 'b', False), (0, 7) : Rook('Rook', (0,7), 'b', False), (1, 0) : Knight('Knight', (1,0), 'w'),
             (1, 1) : Pawn('Pawn', (1,1), 'w', False), (1, 2) : None, (1, 3) : None, (1, 4) : None, (1, 5) : None, (1, 6) : Pawn('Pawn', (1,6), 'b', False),
             (1, 7) : Knight('Knight', (1,7), 'b'), (2, 0) : Bishop('Bishop', (2,0), 'w'),
             (2, 1) : Pawn('Pawn', (2,1), 'w', False), (2, 2) : None, (2, 3) : None, (2, 4) : None, (2, 5) : None, (2, 6) : Pawn('Pawn', (2,6), 'b', False),
             (2, 7) : Bishop('Bishop', (2,7), 'b'), (3, 0) : Queen('Queen', (3,0), 'w'), (3, 1) : Pawn('Pawn', (3,1), 'w', False), (3, 2) : None, (3, 3) : None, (3, 4) : None,
             (3, 5) : None, (3, 6) : Pawn('Pawn', (3,6), 'b', False), (3, 7) : Queen('Queen', (3,7), 'b'), (4, 0) : King('King', (4,0), 'w', False),
             (4, 1) : Pawn('Pawn', (4,1), 'w', False), (4, 2) : None,
             (4, 3) : None, (4, 4) : None, (4, 5) : None, (4, 6) : Pawn('Pawn', (4,6), 'b', False), (4, 7) : King('King', (4,7), 'b', False),
             (5, 0) : Bishop('Bishop', (5,0), 'w'),
             (5, 1) : Pawn('Pawn', (5,1), 'w', False), (5, 2) : None, (5, 3) : None, (5, 4) : None, (5, 5) : None, (5, 6) : Pawn('Pawn', (5,6), 'b', False),
             (5, 7) : Bishop('Bishop', (5,7), 'b'), (6, 0) : Knight('Knight', (6,0), 'w'), (6, 1) : Pawn('Pawn', (6,1), 'w', False), (6, 2) : None, (6, 3) : None, (6, 4) : None,
             (6, 5) : None, (6, 6) : Pawn('Pawn', (6,6), 'b', False), (6, 7) : Knight('Knight', (6,7), 'b'), (7, 0) : Rook('Rook', (7,0), 'w', False),
             (7, 1) : Pawn('Pawn', (7,1), 'w', False), (7, 2) : None,
             (7, 3) : None, (7, 4) : None, (7, 5) : None, (7, 6) : Pawn('Pawn', (7,6), 'b', False), (7, 7) : Rook('Rook', (7,7), 'b', False)}

        else:
            self.board = board

        self.w_pieces = set()
        self.b_pieces = set()
        for piece in [i for i in self.board.values() if i != None]:
            if piece.side == 'w':
                self.w_pieces.add(piece)
            else:
                self.b_pieces.add(piece)

        self.w_attack = set()
        self.b_attack = set()
        
        self.computer = computer
        self.human = human
        self.player_turn = turn

        self.last_one = last_one
        
        self.game_history = ''
        if history == None: self.game_history = defaultdict(int)
        else              : self.game_history = history

    def __str__(self):
        row = 7
        final_string = ' -----------------\n'
        while row >= 0:
            final_string += '%d|' % (row + 1)
            for col in range(8):
                if self.board[(col,row)] == None:
                    final_string += ' |'
                elif self.board[(col,row)].name == 'Pawn':
                    if self.board[(col,row)].side == 'w': final_string += 'P|'
                    else: final_string += 'p|'
                elif self.board[(col,row)].name == 'Rook':
                    if self.board[(col,row)].side == 'w': final_string += 'R|'
                    else: final_string += 'r|'
                elif self.board[(col,row)].name == 'Queen':
                    if self.board[(col,row)].side == 'w': final_string += 'Q|'
                    else: final_string += 'q|'
                elif self.board[(col,row)].name == 'King':
                    if self.board[(col,row)].side == 'w': final_string += 'K|'
                    else: final_string += 'k|'
                elif self.board[(col,row)].name == 'Bishop':
                    if self.board[(col,row)].side == 'w': final_string += 'B|'
                    else: final_string += 'b|'
                elif self.board[(col,row)].name == 'Knight':
                    if self.board[(col,row)].side == 'w': final_string += 'N|'
                    else: final_string += 'n|'
            final_string += '\n -----------------\n a b c d e f g h'
            row -=1
        return final_string

    def __getitem__(self, idx):
        return self.board[tuple(idx)]

    def __setitem__(self, idx, value):
        self.board[idx] = value

    def __iter__(self):
        return iter([i for i in self.board.values() if i != None])

    def copy(self, turn=None):
        if turn == None: return GameState(self.board.copy(), self.player_turn, self.last_one, self.game_history.copy())
        else           : return GameState(self.board.copy(), turn, self.last_one, self.game_history.copy())

    def recalculate_w_attack_squares(self):
        self.w_attack = set()
        for piece in self.w_pieces:
            update_attack_squares(piece, self)        
        
    def recalculate_b_attack_squares(self):
        self.b_attack = set()
        for piece in self.b_pieces:
            update_attack_squares(piece, self)

    def remove_piece_set(self, target):
        self.board[target.coor] = None
        getattr(self, target.side + '_pieces').remove(target)

    def add_piece_set(self, added):
        self.board[added.coor] = added
        getattr(self, added.side + '_pieces').add(added)

    def make_move(self, origin, destination):
        self.past_board = self.board.copy()
        self.past_turn = self.player_turn
        self.past_last_one = self.last_one
        self.last_attacks = set()
        if self.player_turn == 'w': self.last_attacks = self.w_attack.copy()
        else                      : self.last_attacks = self.b_attack.copy()
        
        origin_piece = self[(int(origin[0]), int(origin[1]))]
        if not destination[0].isalpha(): destination_coor = (int(destination[0]), int(destination[1]))
        
        if origin_piece == None:
            print("No piece is at your origin.")
            raise AssertionError
        elif self.player_turn != origin_piece.side:
            if origin_piece.side == 'w':
                print(f"It is not White's turn")
                raise AssertionError
            else:
                print(f"It is not Black's turn")
                raise AssertionError
        
        possible_moves = all_possible_moves(origin_piece, self)                

        # Making a non-castling and non-pawn promotion move.
        if destination[0] not in ('C', 'Q', 'R', 'B', 'N'):
            if destination not in possible_moves:
                print("That is an illegal move.")
                raise AssertionError

            # Incrementing counter since last pawn move or capture if the current move isn't a
            # pawn move or capture.
            if origin_piece.name != 'Pawn' and self[destination_coor] == None:
                self.last_one += 1

            if self[destination_coor] != None:
                self.remove_piece_set(self[destination_coor])

            origin_piece = self[origin_piece.coor]._replace(coor=destination_coor)
            if origin_piece.name in ('Pawn', 'King', 'Rook'):
                origin_piece = origin_piece._replace(moved=True)
            self.add_piece_set(origin_piece)



            self.remove_piece_set(self[(int(origin[0]), int(origin[1]))])
                        
                
        # Castling
        elif destination[0] == 'C':
            if destination not in possible_moves:
                print("You either typed in the move wrong, or castling is not possible here.")
                raise AssertionError


            temp_king = self[(4, int(origin[1]))]._replace(coor=(int(destination[1:][0]), int(destination[1:][1])), moved=True)
            self.add_piece_set(temp_king)
            self.remove_piece_set(self[(4, int(origin[1]))])


            if destination[1:][0] == '2':
                temp_rook = self[(0, int(origin[1]))]._replace(coor=(3, int(origin[1])), moved=True)
                self.add_piece_set(temp_rook)
                self.remove_piece_set(self[(0, int(origin[1]))])
            elif destination[1:][0] == '6':
                temp_rook = self[(7, int(origin[1]))]._replace(coor=(5, int(origin[1])), moved=True)
                self.add_piece_set(temp_rook)
                self.remove_piece_set(self[(7, int(origin[1]))])

            # Incrementing counter since last pawn move or capture since castling
            # doesn't involve either.
            self.last_one += 1
            
        # Pawn promotion
        else:
            if destination not in possible_moves:
                print("Promotion is not possible here.")
                raise AssertionError

            origin_pawn_side = origin_piece.side
            promotion_square = (int(destination[1:][0]), int(destination[1:][1]))
            self.remove_piece_set(origin_piece)

            # If there's a piece on the promotion square, capture it.
            if self[promotion_square] != None:
                self.remove_piece_set(self[promotion_square])

            if   destination[0] == 'Q': self.add_piece_set(Queen('Queen', promotion_square, origin_pawn_side))
            elif destination[0] == 'R': self.add_piece_set(Rook('Rook', promotion_square, origin_pawn_side, False))
            elif destination[0] == 'B': self.add_piece_set(Bishop('Bishop', promotion_square, origin_pawn_side))
            else                      : self.add_piece_set(Knight('Knight', promotion_square, origin_pawn_side))                            

        self.game_history[tuple(self.board.items())] += 1

        if self.player_turn == 'w': self.player_turn = 'b'
        else                      : self.player_turn = 'w'
        
        return self

    def in_check(self, side):
        if side == 'w':
            opp_side = 'b'
            self.recalculate_b_attack_squares()
        else          :
            opp_side = 'w'
            self.recalculate_w_attack_squares()
        
        king_coor = ''
        for piece in getattr(self, side + '_pieces'):
            if piece.name == 'King':
                king_coor = str(piece.coor[0]) + str(piece.coor[1])
                break

        if king_coor in getattr(self, opp_side + '_attack'):
            return True
        
        return False

    def in_checkmate(self, side):    
        king_location = ''
        for piece in getattr(self, side + '_pieces'):
            if piece.name == 'King':
                king_location = str(piece.coor[0]) + str(piece.coor[1])
                break

        # Can the player block the attack, capture the attacking piece, or move away?
        if self.in_check(side):
            for piece in getattr(self, side + '_pieces'):
                for move in all_possible_moves(piece, self):
                    if self.copy(side).make_move(str(piece.coor[0]) + str(piece.coor[1]), move).in_check(side) == False:
                        return False
            return True
        else:
            return False
        
    def is_stalemate(self):
        for piece in getattr(self, self.player_turn + '_pieces'):
            if len(all_possible_moves(piece, self)) != 0:
                return False
        return True
        
    def evaluate(self):
        white_score = 0
        black_score = 0
        values = {
            'Queen': 9,
            'King': 9999,
            'Bishop': 3,
            'Knight': 3,
            'Pawn': 1,
            'Rook':5
            }
        global hash_store

        if self.in_checkmate('b'):
            return 9999999999999
        elif self.in_checkmate('w'):
            return -9999999999999
        elif 3 in self.game_history.values():
            return 0
        elif self.last_one == 50:
            return 0
        elif self.is_stalemate():
            return 0
        else:
            return sum([values[piece.name] for piece in self.w_pieces]) - sum([values[piece.name] for piece in self.b_pieces])
        
    def game_over(self):        
        if self.evaluate() == 9999999999999:
            print("White won")
            return True
        elif self.evaluate() == -9999999999999:
            print("Black won")
            return True
        elif 3 in self.game_history.values():
            print("Tie due to three-move-repetition.")
            return True
        elif self.last_one == 50:
            print("Tie by fifty move rule.")
            return True
        elif self.is_stalemate():
            print("Tie by stalemate.")
            return True

        return False

        
    def attack_adder(self, side, x, y):
        if side == 'w': self.w_attack.add(str(x) + str(y))
        else          : self.b_attack.add(str(x) + str(y))


def minimax(game_state: GameState, alpha: int, beta: int, deep=2) -> str:
    def find_end(x) -> int:
        if type(x) == int:
            return x
        elif type(x[2]) == int:
            return x[2]
        else:
            return find_end(x[2])


    if deep == 0 or game_state.game_over():
        return game_state.evaluate()
    else:
        turn = game_state.player_turn
        
        if turn == 'w':
            max_val = -999999
            for piece in game_state.w_pieces:
                for move in all_possible_moves(piece, game_state):
                    if game_state.copy('w').make_move(str(piece.coor[0]) + str(piece.coor[1]), move).in_check('w'):
                        continue
                    temp = (tuple(piece.coor), move, minimax(game_state.copy().make_move(str(piece.coor[0]) + str(piece.coor[1]), move),
                                                             alpha, beta,
                                                             deep - 1))
                    max_val = max(max_val, temp, key=find_end)
                    alpha = max(alpha, max_val, key=find_end)
                    if find_end(beta) <= find_end(alpha):
                        break
                else:
                    continue
                break
            return max_val
        else:
            min_val = 999999
            for piece in game_state.b_pieces:
                for move in all_possible_moves(piece, game_state):
                    if game_state.copy('b').make_move(str(piece.coor[0]) + str(piece.coor[1]), move).in_check('b'):
                        continue
                    temp = (tuple(piece.coor), move, minimax(game_state.copy('b').make_move(str(piece.coor[0]) + str(piece.coor[1]), move),
                                                             alpha, beta,
                                                             deep - 1))
                    min_val = min(min_val, temp, key=find_end)
                    beta = min(beta, min_val, key=find_end)
                    if find_end(beta) <= find_end(alpha):
                        break
                else:
                    continue
                break
            return min_val

def convert_move(move):
    key = {'a': '0', 'b': '1', 'c': '2', 'd': '3', 'e': '4', 'f': '5', 'g': '6', 'h': '7',
           '1': '0', '2': '1', '3': '2', '4': '3', '5': '4', '6': '5', '7': '6', '8': '7'}

    try:
        if move[0] not in ('C', 'Q', 'R', 'B', 'N'): return key[move[0]] + key[move[1]]
        elif move[0] == 'C'                        : return 'C' + key[move[1]] + key[move[2]]
        elif move[0] == 'Q'                        : return 'Q' + key[move[1]] + key[move[2]]
        elif move[0] == 'R'                        : return 'R' + key[move[1]] + key[move[2]]
        elif move[0] == 'B'                        : return 'B' + key[move[1]] + key[move[2]]
        elif move[0] == 'N'                        : return 'N' + key[move[1]] + key[move[2]]
    except:
        print("You didn't type the move correctly.")
        raise AssertionError
        
'''
a = GameState()

def perft(game_state, nodes, counter):
    if nodes == 0:
        return 1
    internal_count = 0
    if game_state.player_turn == 'w':
        for piece in game_state.w_pieces:
            # I call .copy() after game_state because I don't want the set holding the pieces in 
            # game_state to change when I call all_possible_moves() on it. .copy() in GameState 
            # calls deepcopy on the internal sets and dicts in game_state. Every piece in the 
            # game_state set has a method called .all_possible_moves(GameState) that 
            # generates all the possible moves for that piece. 
            for move in all_possible_moves(piece, game_state):
                counter += perft(game_state.copy().make_move(piece.coor, move), nodes - 1, 0)
    else:
        for piece in game_state.b_pieces:
            for move in all_possible_moves(piece, game_state):
                counter += perft(game_state.copy().make_move(piece.coor, move), nodes - 1, 0)
    return counter

counter = perft(a, 5, 0)
print(counter)
'''



if __name__ == '__main__':
    a = GameState()
    print(a)
    
    while True:        
        if a.game_over():
            break

        while True:
            try:
                user_origin = convert_move(input("What piece do you want to move? Example: 'a1'. Origin: "))
                user_destination = convert_move(input("Where do you want to move this piece? Example: 'a1'. Destination: "))
                if a.copy('w').make_move(user_origin, user_destination).in_check('w'):
                    print("You either put yourself in check or stayed in check. You must get out of check.")
                    raise AssertionError
                a.make_move(user_origin, user_destination)
                break
            except AssertionError:
                pass
            
        print(a)
        
        if a.game_over():
            break
        print("The computer is thinking about its move. It will take up to two minutes...")
        result = minimax(a, -99999, 99999, 4)
        origin, destination = result[0], result[1]
        origin = str(origin[0]) + str(origin[1])
        a.make_move(origin, destination)
        print(a)

