from pieces import King, Queen, Bishop, Knight, Rook, Pawn
import copy

class GameState():
    def __init__(self, board=None, turn='w'):
        if board == None:
            self.board = {
                0: [Rook([0,0], 'w'), Pawn([0,1], 'w'), None, None, None, None, Pawn([0,6], 'b'), Rook([0,7], 'b')],
                1: [Knight([1,0], 'w'), Pawn([1,1], 'w'), None, None, None, None, Pawn([1,6], 'b'), Knight([1,7], 'b')],
                2: [Bishop([2,0],'w'), Pawn([2,1], 'w'), None, None, None, None, Pawn([2,6], 'b'), Bishop([2,7],'b')],
                3: [Queen([3,0], 'w'), Pawn([3,1], 'w'), None, None, None, None, Pawn([3,6], 'b'), Queen([3,7], 'b')],
                4: [King([4,0], 'w'), Pawn([4,1], 'w'), None, None, None, None, Pawn([4,6], 'b'), King([4,7], 'b')],
                5: [Bishop([5,0], 'w'), Pawn([5,1], 'w'), None, None, None, None, Pawn([5,6], 'b'), Bishop([5,7],'b')],
                6: [Knight([6,0], 'w'), Pawn([6,1], 'w'), None, None, None, None, Pawn([6,6], 'b'), Knight([6,7], 'b')],
                7: [Rook([7,0], 'w'), Pawn([7,1], 'w'), None, None, None, None, Pawn([7,6], 'b'), Rook([7,7], 'b')]
            }
        else:
            self.board = board

        self.white_pieces = set()
        self.black_pieces = set()
        for col in self.board.values():
            for piece in col:
                if piece != None:
                    if piece.side == 'w':
                        self.white_pieces.add(piece)
                    else:
                        self.black_pieces.add(piece)

        self.black_attack = set()
        for piece in self.black_pieces:
            if type(piece) == King:
                piece.update_attack_squares(self)
            else:
                piece.all_possible_moves(self)

        self.white_attack = set()
        for piece in self.white_pieces:
            if type(piece) == King:
                piece.update_attack_squares(self)
            else:
                piece.all_possible_moves(self)

        self.possible_white_moves = set()
        self.update_white_moves()
        
        self.possible_black_moves = set()
        self.update_black_moves()
        
        self.pinned_pieces = set()
        self.computer = 'w'
        self.human = 'b'
        self.player_turn = turn

    def __str__(self):
        string = ' -----------------\n'
        row = 7
        for _ in range(8):
            string += str(row+1) + '|'
            for col in range(8):
                if self.board[col][row] != None: string += str(self.board[col][row]) + '|'
                else                            : string += ' |'
            string += '\n -----------------\n'
            row -=1
        return string + '  a b c d e f g h\n\n\n'

    def __getitem__(self, x):
        return self.board[x]

    def __iter__(self):
        iter(self.white_pieces.union(self.black_pieces))

    def copy(self):
        return GameState(copy.deepcopy(self.board), self.player_turn)

    def recalculate_attack_squares(self):
        self.black_attack = set()
        for piece in self.black_pieces:
            if type(piece) == King:
                piece.update_attack_squares(self)
            else:
                piece.all_possible_moves(self)

        self.white_attack = set()
        for piece in self.white_pieces:
            if type(piece) == King:
                piece.update_attack_squares(self)
            else:
                piece.all_possible_moves(self)

    def update_piece_set(self, side, target):
        if side == 'w':
            for piece in self.white_pieces:
                if piece == target:
                    self.white_pieces.remove(piece)
                    break
        else:
            for piece in self.black_pieces:
                if piece == target:
                    self.black_pieces.remove(piece)
                    break
            
        

    def update_white_moves(self):
        self.possible_white_moves = set()
        for piece in self.white_pieces:
            if type(piece) != King:
                self.possible_white_moves = self.possible_white_moves.union(piece.all_possible_moves(self))

        for piece in self.white_pieces:
            if type(piece) == King:
                self.possible_white_moves = self.possible_white_moves.union(piece.all_possible_moves(self))

    def update_black_moves(self):
        self.possible_black_moves = set()

        for piece in self.black_pieces:
            if type(piece) != King:
                self.possible_black_moves = self.possible_black_moves.union(piece.all_possible_moves(self))

        for piece in self.black_pieces:
            if type(piece) == King:
                self.possible_black_moves = self.possible_black_moves.union(piece.all_possible_moves(self))


    def make_move(self, origin, destination):
        piece = self[int(origin[0])][int(origin[1])]

        if piece == None:
            raise AssertionError("No piece is at your origin.")
        if self.player_turn != piece.side:
            if piece.side == 'w': raise AssertionError(f"It is not White's turn")
            else                : raise AssertionError(f"It is not Black's turn")

        possible_moves = piece.all_possible_moves(self)

        if destination[0] != 'C':
            if destination not in possible_moves:
                raise AssertionError("That is an illegal move.")

            self[int(origin[0])][int(origin[1])].coor = [int(destination[0]),int(destination[1])]                
            self[int(destination[0])][int(destination[1])] = piece
            if self[int(destination[0])][int(destination[1])] != None:
                self.update_piece_set(self[int(destination[0])][int(destination[1])].side, self[int(destination[0])][int(destination[1])])
            
            if type(piece) in (Pawn, King, Rook):
                self[int(origin[0])][int(origin[1])].moved = True
                
            self[int(origin[0])][int(origin[1])] = None

        else:
            if destination not in possible_moves:
                raise AssertionError("Castling is not possible here.")
            
            self[4][int(origin[1])].coor = [int(destination[1:][0]),int(destination[1:][1])]
            self[4][int(origin[1])].moved = True
            self[int(destination[1:][0])][int(destination[1:][1])] = self[4][int(origin[1])]
            self[4][int(origin[1])] = None
            

            if destination[1:][0] == '2':
                self[0][int(destination[1:][1])].coor = [3, int(destination[1:][1])]
                self[0][int(destination[1:][1])].moved = True
                self[3][int(destination[1:][1])] = self[0][int(destination[1:][1])]
                self[0][int(destination[1:][1])] = None
            elif destination[1:][0] == '6':
                self[7][int(destination[1:][1])].coor = [3, int(destination[1:][1])]
                self[7][int(destination[1:][1])].moved = True
                self[5][int(destination[1:][1])] = self[7][int(destination[1:][1])]
                self[7][int(destination[1:][1])] = None
                
                
            
        if self.player_turn == 'w': self.player_turn = 'b'
        else                      : self.player_turn = 'w'
        
        self.recalculate_attack_squares()
        return self

    def game_over(self):
        if self.evaluate() in (9999999999999, -9999999999999): return True
        
    def evaluate(self):
        white_score = 0
        black_score = 0
        values = {
            Queen: 9,
            King: 9999,
            Bishop: 3,
            Knight: 3,
            Pawn: 1,
            Rook:5
            }

        if sum([values[type(piece)] for piece in self.white_pieces]) - sum([values[type(piece)] for piece in self.black_pieces]) > 1000:
            return 9999999999999
        elif sum([values[type(piece)] for piece in self.white_pieces]) - sum([values[type(piece)] for piece in self.black_pieces]) < -1000:
            return -9999999999999
        return sum([values[type(piece)] for piece in self.white_pieces]) - sum([values[type(piece)] for piece in self.black_pieces])
        

    def attack_adder(self, side, x, y):
        if side == 'w'  : self.white_attack.add(str(x) + str(y))
        elif side == 'b': self.black_attack.add(str(x) + str(y))


def minimax(game_state: GameState, alpha: int, beta: int, deep=2) -> str:
    def find_end(x: (str, tuple)) -> int:
        if type(x[2]) == int:
            return x[2]
        else:
            return find_end(x[2])

    if deep == 0:
        return game_state.evaluate()
    else:
        turn = game_state.player_turn
        final = []
        
        if turn == game_state.computer:
            max_val = -99999
            for piece in game_state.white_pieces:
                for move in piece.all_possible_moves(game_state):
                    temp = (piece.coor, move, minimax(game_state.copy().make_move(str(piece.coor[0]) + str(piece.coor[1]), move), alpha, beta, deep - 1))
                    final.append(temp)
                    max_val = max(max_val, find_end(temp))
                    alpha = max(alpha, max_val)
                    if beta <= alpha:
                        break
                else:
                    continue
                break
            return max(final, key = lambda x:find_end(x))
        else:
            min_val = 99999
            for piece in game_state.black_pieces:
                for move in piece.all_possible_moves(game_state):
                    temp = (piece.coor, move, minimax(game_state.copy().make_move(str(piece.coor[0]) + str(piece.coor[1]), move), alpha, beta, deep - 1))
                    final.append(temp)
                    min_val = min(min_val, find_end(temp))
                    alpha = min(alpha, min_val)
                    if beta <= alpha:
                        break
                else:
                    continue
                break
            return min(final, key = lambda x:find_end(x))

a = GameState()
while not a.game_over():
    print("up here", a.player_turn)
    result = minimax(a, -99999, 99999, 2)
    print("FIRST", result)
    origin, destination = result[0], result[1]
    origin = str(origin[0]) + str(origin[1])
    a.make_move(origin, destination)
    print(a)
    # user_origin = input("What move do you want to make? Origin: ")
    # user_destination = input("To where? Destination: ")
    print("rightly so", a.player_turn)
    result = minimax(a, -99999, 99999, 2)
    print("SECOND", result)
    origin, destination = result[0], result[1]
    origin = str(origin[0]) + str(origin[1])
    a.make_move(origin, destination)
    print(a)
    print('passed here')

print(a.evaluate())
































'''
a = GameState()
print(a)
a.make_move('01','03')
print(a)
a.make_move('06', '04')
print(a)
a.make_move('00', '02')
print(a)
a.make_move('17', '25')
print(a)
a.make_move('41', '43')
print(a)
a.make_move('07', '05')
print(a)
a.make_move('50', '05')        
print(a)
a.make_move('16', '14')
print(a)
a.make_move('05', '27')
print(a)
a.make_move('37', '27')
print(a)
a.make_move('30', '74')
print(a)
a.make_move('27', '05')
print(a)
a.make_move('60', '72')
print(a)
a.make_move('14', '13')
print(a)
a.make_move('31', '32')
print(a)
a.make_move('67', '55')
print(a)
a.make_move('40', 'C60')
print(a)
a.make_move('66', '65')
print(a)
a.make_move('74', '14')
print(a)
a.make_move('57', '66')
print(a)
a.make_move('14', '16')
print(a)
a.make_move('47', 'C67')
print(a)






a = GameState()
print(a)
a.make_move('01','03')
print(a)
a.make_move('06', '04')
print(a)
a.make_move('00', '02')
print(a)
a.make_move('17', '25')
print(a)
a.make_move('41', '43')
print(a)
a.make_move('07', '05')
print(a)
a.make_move('50', '05')
print(a)
a.make_move('16', '14')
print(a)
a.make_move('05', '27')
print(a)
a.make_move('37', '27')
print(a)
a.make_move('30', '74')
print(a)
a.make_move('27', '05')
print(a)
a.make_move('60', '52')
print(a)
a.make_move('47', '37')
print(a)
a.make_move('40', 'C60')
print(a)
'''

