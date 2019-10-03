from tkinter import *
from PIL import Image, ImageTk
from pieces import King, Queen, Rook, Bishop, Knight, Pawn
from chessy import GameState, minimax, convert_move
import random
'''
board = {
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
'''
pieces = {
    'wKing' : 'white_king.png',
    'wQueen' : 'white_queen.png',
    'wRook' : 'white_rook.png',
    'wBishop' : 'white_bishop.png',
    'wKnight' : 'white_knight.png',
    'wPawn' : 'white_pawn.png',
    'bKing' : 'black_king.png',
    'bQueen' : 'black_queen.png',
    'bRook' : 'black_rook.png',
    'bBishop' : 'black_bishop.png',
    'bKnight' : 'black_knight.png',
    'bPawn' : 'black_pawn.png'
}

class ChessEngine:
    def __init__(self):
        self.a = GameState()
        self.master = Tk(className='Chess Engine')
        self.canvas = Canvas(self.master, width=630, height=570)
        self.canvas.pack(side='top')

        self.var = IntVar()
        self.button = Button(master = self.master, text = 'Submit move', font = ('Helvetica', 20), command = self.do)
        self.button.pack(side='bottom')
        
        self.d = Entry(self.master)
        self.d.insert(0, "Destination")
        self.d.pack(side='bottom')

        self.p = Entry(self.master)
        self.p.insert(0, "Origin")
        self.p.pack(side='bottom')

    def do(self):
        self.var.set(1)
        
    def update_display(self, board):
        self.canvas.delete("all")
        square_color = 'bisque2'
        for x in range(8):
            if square_color == 'bisque2': square_color = 'bisque4'
            else                        : square_color = 'bisque2'
            for y in range(8):
                if square_color == 'bisque2': square_color = 'bisque4'
                else                        : square_color = 'bisque2'
                self.canvas.create_rectangle(65*x+55, 65*y, 65*(x+1)+55, 65*(y+1), fill=square_color)

        rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        for y in range(8):
            self.canvas.create_text(27.5, 32.5 + 65*y, text=rows[-1], font=("Times", 30, "bold"))
            rows.pop()

        cols = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        for x in range(8):
            self.canvas.create_text(87 + 65*x, 552.5, text=cols[-1], font=("Times", 30, "bold"))
            cols.pop()


        pieces_location = {}
        for coor, piece in board.items():
            if piece != None:
                photo = ImageTk.PhotoImage(Image.open(pieces[piece.side + piece.name]))
                image = self.canvas.create_image((87+65*coor[0], 32.5+65*(7-coor[1])), image=photo, anchor='center')
                pieces_location[(coor[0],coor[1])] = photo


        self.button.wait_variable(self.var)
        origin = convert_move(self.p.get().strip())
        destination = convert_move(self.d.get().strip())
        return origin, destination        

    def run(self):        
        while True:        
            if self.a.game_over():
                break
            
            while True:
                user_origin, user_destination = self.update_display(self.a.board)                                                   
                try:
                    if self.a.copy('w').make_move(user_origin, user_destination).in_check('w'):
                        print("You either put yourself in check or stayed in check. You must get out of check.")
                        raise AssertionError
                    self.a.make_move(user_origin, user_destination)
                    break
                except AssertionError:
                    pass
                

            if self.a.game_over():
                break
            print("The computer is thinking about its move. It will take up to a minute...")
            result = minimax(self.a, -99999, 99999, 3)
            origin, destination = result[0], result[1]
            origin = str(origin[0]) + str(origin[1])
            self.a.make_move(origin, destination)
            


if __name__ == '__main__':
    b = ChessEngine()
    b.run()
    b.master.mainloop()











