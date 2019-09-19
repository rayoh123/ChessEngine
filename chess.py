from pieces import King, Queen, Bishop, Knight, Rook, Pawn

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
                        
        self.pinned_pieces = set()

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
        return string + '  a b c d e f g h'

    def __getitem__(self, x):
        return self.board[x]

    def __iter__(self):
        iter(self.white_pieces.union(self.black_pieces))

    def recalculate_attack_squares(self):
        for piece in self.black_pieces:
            if type(piece) == King:
                piece.update_attack_squares(self)
            else:
                piece.all_possible_moves(self)

        for piece in self.white_pieces:
            if type(piece) == King:
                piece.update_attack_squares(self)
            else:
                piece.all_possible_moves(self)

    
    def make_move(self, origin, destination):
        piece = self[int(origin[0])][int(origin[1])]

        if piece == None:
            raise AssertionError("No piece is at your origin.")
        if self.player_turn != piece.side:
            if piece.side == 'w': raise AssertionError(f"It is not White's turn")
            else                : raise AssertionError(f"It is not Black's turn")

        possible_moves = piece.all_possible_moves(self)
        print(piece, piece.coor, piece.side)
        
        print("possible", possible_moves)
        if destination not in possible_moves:
            raise AssertionError("That is an illegal move.")

        self[int(origin[0])][int(origin[1])].coor = [int(destination[0]),int(destination[1])]
        self[int(destination[0])][int(destination[1])] = piece
        
        if type(piece) in (Pawn, King, Rook):
            self[int(origin[0])][int(origin[1])].moved = True
            
        self[int(origin[0])][int(origin[1])] = None
        
        if self.player_turn == 'w': self.player_turn = 'b'
        else                      : self.player_turn = 'w'
        self.recalculate_attack_squares()

    def attack_adder(self, side, x, y):
        if side == 'w'  : self.white_attack.add(str(x) + str(y))
        elif side == 'b': self.black_attack.add(str(x) + str(y))

        


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
a.make_move('05', '50')
print(a)


