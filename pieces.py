class Pawn:
    def __init__(self, coor, side):
        self.coor = coor
        self.side = side
        self.moved = False

    def __str__(self):
        if self.side == 'w':
            return 'P'
        return 'p'

    def all_possible_moves(self, game_state):
        possible_moves = set()
        if self.side == 'w':
            if game_state[self.coor[0]][self.coor[1] + 1] == None:
                possible_moves.add(str(self.coor[0]) + str(self.coor[1] + 1))
                if game_state[self.coor[0]][self.coor[1] + 2] == None and self.moved == False:
                    possible_moves.add(str(self.coor[0]) + str(self.coor[1] + 2))

            if self.coor[0] - 1 >= 0:
                if game_state[self.coor[0] - 1][self.coor[1] + 1] != None and \
                game_state[self.coor[0] - 1][self.coor[1] + 1].side != self.side:
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] + 1))
                    game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] + 1)

            if self.coor[0] + 1 <= 7:
                if game_state[self.coor[0] + 1][self.coor[1] + 1] != None and \
                game_state[self.coor[0] + 1][self.coor[1] + 1].side != self.side:
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] + 1))
                    game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] + 1)
        else:
            if game_state[self.coor[0]][self.coor[1] - 1] == None:
                possible_moves.add(str(self.coor[0]) + str(self.coor[1] - 1))
                if game_state[self.coor[0]][self.coor[1] - 2] == None and self.moved == False:
                    possible_moves.add(str(self.coor[0]) + str(self.coor[1] - 2))

            if self.coor[0] - 1 >= 0:
                if game_state[self.coor[0] - 1][self.coor[1] - 1] != None and \
                game_state[self.coor[0] - 1][self.coor[1] - 1].side != self.side:
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] - 1))
                    game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] - 1)

            if self.coor[0] + 1 <= 7:
                if game_state[self.coor[0] + 1][self.coor[1] - 1] != None and \
                game_state[self.coor[0] + 1][self.coor[1] - 1].side != self.side:
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] - 1))
                    game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] - 1)
                            
        return possible_moves
                
        
class King:
    def __init__(self, coor, side):
        self.coor = coor
        self.side = side
        self.moved = False

    def __str__(self):
        if self.side == 'w':
            return 'K'
        return 'k'

    def update_attack_squares(self, game_state):
        if self.coor[0] - 1 >= 0:
            game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1])
            
            if self.coor[1] - 1 >= 0:
                game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] - 1)

            if self.coor[1] + 1 <= 7:
                game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1])
            
        if self.coor[0] + 1 <= 7:
            game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1])
            
            if self.coor[1] - 1 >= 0:
                game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] - 1)
                
            if self.coor[1] + 1 <= 7:
                game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] + 1)
                
        if self.coor[1] + 1 <= 7:
            game_state.attack_adder(self.side, self.coor[0], self.coor[1] + 1)
            
        if self.coor[1] - 1 >= 0:
            game_state.attack_adder(self.side, self.coor[0], self.coor[1] - 1)


    def all_possible_moves(self, game_state):
        possible_moves = set()
        
        opposite_turn = 'black'
        if self.side == 'b':
            opposite_turn = 'white'
        if self.coor[0] - 1 >= 0:
            if str(self.coor[0] - 1) + str(self.coor[1]) not in eval(f'game_state.{opposite_turn}_attack'):
                possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1]))
            
            if self.coor[1] - 1 >= 0:
                if str(self.coor[0] - 1) + str(self.coor[1] - 1) not in eval(f'game_state.{opposite_turn}_attack'):
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] - 1))

            if self.coor[1] + 1 <= 7:
                if str(self.coor[0] - 1) + str(self.coor[1] + 1) not in eval(f'game_state.{opposite_turn}_attack'):
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] + 1))
            
        if self.coor[0] + 1 <= 7:
            if str(self.coor[0] + 1) + str(self.coor[1]) not in eval(f'game_state.{opposite_turn}_attack'):
                possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1]))
            
            if self.coor[1] - 1 >= 0:
                if str(self.coor[0] + 1) + str(self.coor[1] - 1) not in eval(f'game_state.{opposite_turn}_attack'):
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] - 1))
                
            if self.coor[1] + 1 <= 7:
                if str(self.coor[0] + 1) + str(self.coor[1] + 1) not in eval(f'game_state.{opposite_turn}_attack'):
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] + 1))
                
        if self.coor[1] + 1 <= 7:
            if str(self.coor[0]) + str(self.coor[1] + 1) not in eval(f'game_state.{opposite_turn}_attack'):
                possible_moves.add(str(self.coor[0]) + str(self.coor[1] + 1))
            
        if self.coor[1] - 1 >= 0:
            if str(self.coor[0]) + str(self.coor[1] - 1) not in eval(f'game_state.{opposite_turn}_attack'):
                possible_moves.add(str(self.coor[0]) + str(self.coor[1] - 1))

        return possible_moves
                    
class Bishop:
    def __init__(self, coor, side):
        self.coor = coor
        self.side = side

    def __str__(self):
        if self.side == 'w':
            return 'B'
        return 'b'

    def all_possible_moves(self, game_state):
        possible_moves = set()

        if self.coor[0] > 0:
            for i,j in zip(range(self.coor[0] - 1, -1, -1), range(self.coor[1] + 1, 8)):
                if game_state[i][j] == None:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                elif game_state[i][j].side != self.side:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                    break
                else:
                    break
            for i,j in zip(range(self.coor[0] - 1, -1, -1), range(self.coor[1] - 1, -1, -1)):
                if game_state[i][j] == None:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                elif game_state[i][j].side != self.side:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                    break
                else:
                    break

        if self.coor[1] < 7:
            for i,j in zip(range(self.coor[0] - 1, -1, -1), range(self.coor[1] + 1, 8)):
                if game_state[i][j] == None:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                elif game_state[i][j].side != self.side:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                    break
                else:
                    break
                
            for i,j in zip(range(self.coor[0] + 1, 8), range(self.coor[1] - 1, -1, -1)):
                if game_state[i][j] == None:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                elif game_state[i][j].side != self.side:
                    possible_moves.add(str(i) + str(j))
                    game_state.attack_adder(self.side, i, j)
                    break
                else:
                    break

            
            
            
        '''
        if self.coor[0] > 0:
            for i in range(self.coor[0] - 1, -1, -1):
                if self.coor[1] > 0:
                    for idx in range(self.coor[1] - 1, -1, -1):
                        if game_state[i][idx] == None:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                        elif game_state[i][idx].side != self.side:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                            break
                        else:
                            break
                if self.coor[1] < 7:
                    for idx in range(self.coor[1] + 1, 8):
                        if game_state[i][idx] == None:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                        elif game_state[i][idx].side != self.side:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                            break
                        else:
                            break


        if self.coor[0] < 7:
            for i in range(self.coor[0] + 1, 8):
                if self.coor[1] > 0:
                    for idx in range(self.coor[1] - 1, -1, -1):
                        if game_state[i][idx] == None:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                        elif game_state[i][idx].side != self.side:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                            break
                        else:
                            break
                if self.coor[1] < 7:
                    for idx in range(self.coor[1] + 1, 8):
                        if game_state[i][idx] == None:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                        elif game_state[i][idx].side != self.side:
                            possible_moves.add(str(i) + str(idx))
                            game_state.attack_adder(self.side, i, idx)
                            break
                        else:
                            break
        '''
        return possible_moves
     
class Knight:
    def __init__(self, coor, side):
        self.coor = coor
        self.side = side

    def __str__(self):
        if self.side == 'w':
            return 'N'
        return 'n'

    def all_possible_moves(self, game_state):
        possible_moves = set()
        if self.coor[0] + 2 <= 7:
            if self.coor[1] + 1 <= 7:
                if game_state[self.coor[0] + 2][self.coor[1] + 1] == None:
                    possible_moves.add(str(self.coor[0] + 2) + str(self.coor[1] + 1))
                    game_state.attack_adder(self.side, self.coor[0] + 2, self.coor[1] + 1)
                elif game_state[self.coor[0] + 2][self.coor[1] + 1].side != self.side:
                    possible_moves.add(str(self.coor[0] + 2) + str(self.coor[1] + 1))
                    game_state.attack_adder(self.side, self.coor[0] + 2, self.coor[1] + 1)
                else:
                    print(self.coor[0] + 2, self.coor[1] + 1)
                    
            if self.coor[1] - 1 >= 0:
                if game_state[self.coor[0] + 2][self.coor[1] - 1] == None:
                    possible_moves.add(str(self.coor[0] + 2) + str(self.coor[1] - 1))
                    game_state.attack_adder(self.side, self.coor[0] + 2, self.coor[1] - 1)
                elif game_state[self.coor[0] + 2][self.coor[1] - 1].side != self.side:
                    possible_moves.add(str(self.coor[0] + 2) + str(self.coor[1] - 1))
                    game_state.attack_adder(self.side, self.coor[0] + 2, self.coor[1] - 1)
                else:
                    print(self.coor[0] + 2, self.coor[1] - 1)
                    
        if self.coor[0] - 2 >= 0:
            if self.coor[1] + 1 <= 7:
                if game_state[self.coor[0] - 2][self.coor[1] + 1] == None:
                    possible_moves.add(str(self.coor[0] - 2) + str(self.coor[1] + 1))
                    game_state.attack_adder(self.side, self.coor[0] - 2, self.coor[1] + 1)
                elif game_state[self.coor[0] - 2][self.coor[1] + 1].side != self.side:
                    possible_moves.add(str(self.coor[0] - 2) + str(self.coor[1] + 1))
                    game_state.attack_adder(self.side, self.coor[0] - 2, self.coor[1] + 1)
                else:
                    print(self.coor[0] - 2, self.coor[1] + 1)
                    
            if self.coor[1] - 1 >= 0:
                if game_state[self.coor[0] - 2][self.coor[1] - 1] == None:
                    possible_moves.add(str(self.coor[0] - 2) + str(self.coor[1] - 1))
                    game_state.attack_adder(self.side, self.coor[0] - 2, self.coor[1] - 1)
                elif game_state[self.coor[0] - 2][self.coor[1] - 1].side != self.side:
                    possible_moves.add(str(self.coor[0] - 2) + str(self.coor[1] - 1))
                    game_state.attack_adder(self.side, self.coor[0] - 2, self.coor[1] - 1)
                else:
                    print(self.coor[0] - 2, self.coor[1] - 1)

        if self.coor[0] + 1 <= 7:
            if self.coor[1] + 2 <= 7:
                if game_state[self.coor[0] + 1][self.coor[1] + 2] == None:
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] + 2))
                    game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] + 2)
                elif game_state[self.coor[0] + 1][self.coor[1] + 2].side != self.side:
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] + 2))
                    game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] + 2)
                else:
                    print(self.coor[0] + 1, self.coor[1] + 2)

            if self.coor[1] - 2 >= 0:
                if game_state[self.coor[0] + 1][self.coor[1] - 2] == None:
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] - 2))
                    game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] - 2)
                elif game_state[self.coor[0] + 1][self.coor[1] - 2].side != self.side:
                    possible_moves.add(str(self.coor[0] + 1) + str(self.coor[1] - 2))
                    game_state.attack_adder(self.side, self.coor[0] + 1, self.coor[1] - 2)
                else:
                    print(self.coor[0] + 1, self.coor[1] - 2)

        if self.coor[0] - 1 >= 0:
            if self.coor[1] + 2 <= 7:
                if game_state[self.coor[0] - 1][self.coor[1] + 2] == None:
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] + 2))
                    game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] + 2)
                elif game_state[self.coor[0] - 1][self.coor[1] + 2].side != self.side:
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] + 2))
                    game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] + 2)
                else:
                    print(self.coor[0] - 1, self.coor[1] + 2)
                    
            if self.coor[1] - 2 >= 0:
                if game_state[self.coor[0] - 1][self.coor[1] - 2] == None:
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] - 2))
                    game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] - 2)
                elif game_state[self.coor[0] - 1][self.coor[1] - 2].side != self.side:
                    possible_moves.add(str(self.coor[0] - 1) + str(self.coor[1] - 2))
                    game_state.attack_adder(self.side, self.coor[0] - 1, self.coor[1] - 2)
                else:
                    print(self.coor[0] - 1, self.coor[1] - 2)

        return possible_moves
                

        
class Rook:
    def __init__(self, coor, side):
        self.coor = coor
        self.side = side
        self.moved = False

    def __str__(self):
        if self.side == 'w':
            return 'R'
        return 'r'

    def all_possible_moves(self, game_state):
        possible_moves = set()
        if self.coor[1] > 0:
            for idx in range(self.coor[1] - 1, -1, -1):
                if game_state.board[self.coor[0]][idx] == None:
                    possible_moves.add(str(self.coor[0]) + str(idx))
                    game_state.attack_adder(self.side, self.coor[0], idx)
                elif game_state.board[self.coor[0]][idx].side != self.side:
                    possible_moves.add(str(self.coor[0]) + str(idx))
                    game_state.attack_adder(self.side, self.coor[0], idx)
                    break
                else:
                    break

        if self.coor[1] < 7:
            for idx in range(self.coor[1] + 1, len(game_state[self.coor[0]])):
                if game_state.board[self.coor[0]][idx] == None:
                    possible_moves.add(str(self.coor[0]) + str(idx))
                    game_state.attack_adder(self.side, self.coor[0], idx)
                elif game_state.board[self.coor[0]][idx].side != self.side:
                    possible_moves.add(str(self.coor[0]) + str(idx))
                    game_state.attack_adder(self.side, self.coor[0], idx)
                    break
                else:
                    break

        if self.coor[0] > 0:
            for i in range(self.coor[0] - 1, -1, -1):
                if game_state[i][self.coor[1]] == None:
                    possible_moves.add(str(i) + str(self.coor[1]))
                    game_state.attack_adder(self.side, i, self.coor[1])
                elif game_state[i][self.coor[1]].side != self.side:
                    possible_moves.add(str(i) + str(self.coor[1]))
                    game_state.attack_adder(self.side, i, self.coor[1])
                    break
                else:
                    break

        if self.coor[0] < 7:
            for i in range(self.coor[0] + 1, 8):
                if game_state[i][self.coor[1]] == None:
                    possible_moves.add(str(i) + str(self.coor[1]))
                    game_state.attack_adder(self.side, i, self.coor[1])
                elif game_state[i][self.coor[1]].side != self.side:
                    possible_moves.add(str(i) + str(self.coor[1]))
                    game_state.attack_adder(self.side, i, self.coor[1])
                    break
                else:
                    break
                
        return possible_moves

class Queen:
    def __init__(self, coor, side):
        self.coor = coor
        self.side = side

    def __str__(self):
        if self.side == 'w':
            return 'Q'
        return 'q'

    def all_possible_moves(self, game_state):
        return Rook(self.coor, self.side).all_possible_moves(game_state).union(Bishop(self.coor, self.side).all_possible_moves(game_state))
