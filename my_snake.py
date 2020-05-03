# -*- coding: utf-8 -*-
"""
Created on Fri May  1 13:29:03 2020

@author: Numa Gout
"""
import numpy as np
from tkinter import *



class snake():
    ''' Class Snake, contains all the information on the snake.
    Attributes : - board : board where the snake will grow (class board)
                 - position : list of positions of the snake
                 - direction : where the snake is currently moving '''
    
    def sum_tuple(u, v):
        ''' Return sum of 2 tuples terms by terms '''
        return u[0]+v[0], u[1]+v[1]
    
    def neg_tuple(u):
        ''' Return the oppositive tuple term by term (-u) '''
        return -u[0], -u[1]
    
    def __init__(self, board):
        ''' Initialization method '''
        self.board = board
        self.position = [(board.x//2, board.y//2), (board.x//2-1, board.y//2)]
        self.direction = (1, 0)
        
        
    def move(self, eat = False):
        ''' Do one moving step of the snake, if the snake is eating it will grow '''
        if eat:
            self.position = [snake.sum_tuple(self.position[0],self.direction)]+self.position
        else:
            self.position = [snake.sum_tuple(self.position[0],self.direction)] + self.position[:-1]
        
        self.board.fen.move_snake(eat)  # call the move method of the tkinter class (graph)           
        
    def change_direction(self, u):
        ''' Change the direction of the snake (impossible to go backward) '''
        if u != snake.neg_tuple(self.direction):
            self.direction = u
            
        
    
class board():
    ''' Class board, contains all the information of the board and the progress of the game.
    Attributes : - x : width of the board
                 - y : height of the board
                 - snake : snake which is moving on the board
                 - fen : tkinter window linked to the board
                 - apple : coords of the apple'''
    
    def __init__(self, x, y, fen):
        ''' Initialization method '''
        self.x = x
        self.y = y
            
        self.snake = snake(self)
        
        # positioning the apple
        i, j = (np.random.randint(self.x), np.random.randint(self.y))
        while (i, j) in self.snake.position:
            i, j = (np.random.randint(self.x), np.random.randint(self.y))
        self.apple = i, j
        
        self.fen = fen # tkinter window
        self.fen.shortest_way = np.linalg.norm(snake.sum_tuple(self.apple, snake.neg_tuple(self.snake.position[0])), ord = 1) - 1
        
    def new_apple(self):
        ''' Create a new apple on random coords '''
        i, j = (np.random.randint(self.x), np.random.randint(self.y))
        while (i, j) in self.snake.position:
            i, j = (np.random.randint(self.x), np.random.randint(self.y))
        self.apple = i, j
        
        self.fen.move_apple() # refresh the tkinter windows
        
    def new_game(self):
        ''' Reset the board and start a new game '''
        self.snake = snake(self)
        
        # positioning the apple
        i, j = (np.random.randint(self.x), np.random.randint(self.y))
        while (i, j) in self.snake.position:
            i, j = (np.random.randint(self.x), np.random.randint(self.y))
        self.apple = i, j
        
        self.fen.shortest_way = np.linalg.norm(snake.sum_tuple(self.apple, snake.neg_tuple(self.snake.position[0])), ord = 1) - 1
        self.fen.id_apple = self.fen.Can.create_oval(i*10, j*10, (i+1)*10, (j+1)*10, fill = 'red') # show the apple on the canvas of the tkinter window
        
    def __str__(self):
        ''' Show the board on the python shell, use for debugging'''
        s = ''
        for i in range(self.y):
            for j in range(self.x):
                if i in [0, self.y] or j in [0, self.x]:
                    s += '*'
                elif (j, i) == self.nourriture:
                    s += '@'
                elif (j, i) in self.snake.position[1:]:
                    s += '.'
                elif (j, i) == self.snake.position[0]:
                    s += 'o'
                else:
                    s += ' '
            s += '\n'
        return s
    
    def colision(self):
        ''' Detect if there is a colision '''
        i, j = self.snake.position[0]
        if (i, j) in self.snake.position[1:]:
            return True
        elif i in [-1, self.x] or j in [-1, self.y]:
            return True
        else:
            return False
    

class Game(Tk):
    ''' Class Game, inheritate of Tk class, it's just the window of the game.
    Attributes : - frameControle : frame which contains all the control info and button
                 - score : Score of the current game
                 - highscore : highscore of the older games
                 - ad : label of defeat or victoiry
                 - Can : Canvas of the game
                 - id_snake : all of the id of the oval form of the snake
                 - grow : if the snake is going to eat next step
                 - start : if the game has already started
                 - end : if the game has ended
                 - move_speed : speed of the snake in ms
                 - nb_moves : numbers of moves before hitting an apple
                 - add_size : size add after eating one apple'''
                 
    def max_points_scored(self):
        ''' Maximum points scored at one speed, max_points_scored(100) = 100'''
        return 80*np.exp(-((np.log(18)-np.log(8))/90)*(self.move_speed-100))+20   
    
    def points_scored(self, min_moves, current_moves):
        ''' Points scored according to the shortest way to get the apple and the actuel way chosen '''
        return (self.max_points_scored()-20)*np.exp(-np.log(4)/(2.5*min_moves)*(current_moves-min_moves))+20
    
    def __init__(self, xboard, yboard):
        ''' Initialization method '''
        Tk.__init__(self)
        self.configure(bg = '#b666d2')
        self.title('Snake')

        # Frame of controle things
        self.frameControle = Frame(self, bg = '#b666d2')
        self.frameControle.pack(side = LEFT, padx = 5)
        
        # new game button
        Button(self.frameControle, text = "New Game", width = 15, command = self.newgame, bg = '#fee7f0').pack(side = TOP, padx = 5, pady = 5)
        
        # score label
        self.score = 0
        self.lscore = Label(self.frameControle, text = 'Score = '+str(self.score), bg = '#b666d2', font = 'Helvetica 18 bold')
        self.lscore.pack(side = TOP, padx = 5)
        
        # highscore label
        try:
            self.filehighscore = open('highscore.txt', 'r')
            string = self.filehighscore.read()
            if len(string) == 0:
                self.highscore = 0
            else:
                self.highscore = int(string)
        except:
            self.filehighscore = open('highscore.txt', 'w')
            self.highscore = 0
            
        self.lhighscore = Label(self.frameControle, text = 'Highscore = '+str(self.highscore), bg = '#b666d2', font = 'Helvetica 18 bold')
        self.lhighscore.pack(side = TOP, padx = 5)
        
        # ad label (victory or defeat)
        self.ad = Label(self.frameControle, text = '', fg = 'black', bg = '#b666d2', font = 'Helvetica 18 bold')
        self.ad.pack(side = TOP, padx = 5)
        
        # scale of parameter
        self.scale_move_speed = Scale(self.frameControle, from_ = 10, to = 1000, resolution = 10, label = 'Change move speed (ms)', orient = 'horizontal', length = 200, bg = '#fee7f0', relief = 'raised')
        self.scale_move_speed.bind('<Button-1>', self.clic)
        self.scale_move_speed.bind('<ButtonRelease-1>', self.change_move_speed)
        self.scale_move_speed.set(100)
        self.scale_move_speed.pack(side = TOP, padx = 5)

        self.scale_growsize = Scale(self.frameControle, from_ = 1, to = 10, resolution = 1, label = 'Change grow size', orient = 'horizontal', length = 200, bg = '#fee7f0', relief = 'raised')
        self.scale_growsize.bind('<Button-1>', self.clic)
        self.scale_growsize.bind('<ButtonRelease-1>', self.change_eat_grow)
        self.scale_growsize.set(3)
        self.scale_growsize.pack(side = TOP, padx = 5)
        
        self.scale_xdim = Scale(self.frameControle, from_ = 5, to = 100, resolution = 1, label = 'Change dimention', orient = 'horizontal', length = 200, bg = '#fee7f0', relief = 'raised')
        self.scale_ydim = Scale(self.frameControle, from_ = 5, to = 100, resolution = 1, orient = 'horizontal', length = 200, bg = '#fee7f0', relief = 'raised')
        self.scale_xdim.bind('<Button-1>', self.clic)
        self.scale_ydim.bind('<Button-1>', self.clic)
        self.scale_xdim.bind('<ButtonRelease-1>', self.change_board_size)
        self.scale_ydim.bind('<ButtonRelease-1>', self.change_board_size)
        self.scale_xdim.set(50)
        self.scale_ydim.set(50)
        self.scale_xdim.pack(side = TOP, padx = 5)
        self.scale_ydim.pack(side = TOP, padx = 5)
        
        # Canvas
        self.Can = Canvas(self, width = xboard*10 , height = yboard*10, bg = 'black')
        self.Can.pack(side = LEFT, padx = 5)
        
        self.board = board(xboard, yboard, self)
        self.grow = 0
        
        self.id_snake = []
        self.start_spot()
        
        self.end = False
        
        self.start = False
        
        self.move_speed = 100
        
        self.nb_moves = 0
        
        self.add_size = 3
        
    def clic(self, event):
        ''' Change the attribute of the clicked widget if the clic was on the good spot '''
        if event.widget.identify(event.x, event.y) == 'slider':
            event.widget.goodclic = True
        else:
            event.widget.godclic = False
        
    def change_move_speed(self, event):
        ''' Change move speed according to the scale '''
        if event.widget.goodclic:
            self.move_speed = self.scale_move_speed.get()
            self.newgame()
            event.widget.goodclic = False
        
        
    def change_board_size(self, event):
        ''' Change the board size according to the scale '''
        if event.widget.goodclic:
            self.Can.destroy()
            self.Can = Canvas(self, width = self.scale_xdim.get()*10 , height = self.scale_ydim.get()*10, bg = 'black')
            self.Can.pack(side = LEFT, padx = 5)
            self.board = board(self.scale_xdim.get(), self.scale_ydim.get(), self)
            self.newgame()
        
    def change_eat_grow(self, event):
        ''' Change the length earned by the snake after eating one apple '''
        if self.scale_growsize.goodclic:
            self.add_size = self.scale_growsize.get()
            self.newgame()
        
    
    def start_spot(self):
        ''' plot all the items on the canvas '''
        i, j = self.board.snake.position[0]
        self.id_snake.append(self.Can.create_oval(i*10, j*10, (i+1)*10, (j+1)*10, fill = '#000fff000'))
        for i, j in self.board.snake.position[1:]:
            self.id_snake.append(self.Can.create_oval(i*10, j*10, (i+1)*10, (j+1)*10, fill = 'green'))
        
        i, j = self.board.apple
        self.id_apple = self.Can.create_oval(i*10, j*10, (i+1)*10, (j+1)*10, fill = 'red')
        
    def move_apple(self):
        ''' move the apple '''
        [i0, j0] = self.Can.coords(self.id_apple)[:2]
        i, j = self.board.apple
        
        dx = i*10 - i0
        dy = j*10 - j0
        self.Can.move(self.id_apple, dx, dy)
        
    def move_snake(self, eat = False):
        ''' Do one step of the snake '''
        if eat:
            i, j = self.board.snake.position[0]
            self.id_snake = [self.Can.create_oval(i*10, j*10, (i+1)*10, (j+1)*10, fill = '#000fff000')] + self.id_snake
                                       
            self.Can.itemconfig(self.id_snake[1], fill = 'green')
                                       
        else:
            i, j = self.board.snake.position[0]
            self.id_snake = [self.Can.create_oval(i*10, j*10, (i+1)*10, (j+1)*10, fill = '#000fff000')] + self.id_snake
                                       
            self.Can.itemconfig(self.id_snake[1], fill = 'green')
            
            id_to_delete = self.id_snake.pop()
            self.Can.delete(id_to_delete)    
        if self.board.colision():
            self.end = True
            
        if self.board.apple == self.board.snake.position[0]:
            self.grow += self.add_size             
            self.board.new_apple()
            self.update_score()
            self.shortest_way = np.linalg.norm(snake.sum_tuple(self.board.apple, snake.neg_tuple(self.board.snake.position[0])), ord = 1) - 1
        else:
            if self.grow != 0:
                self.grow -= 1     
            self.nb_moves += 1
    
    def update_score(self):
        ''' Update the score on the frameControle '''
        self.score += int(round(self.points_scored(self.shortest_way, self.nb_moves)))
        self.nb_moves = 0
        self.lscore.config(text = 'Score = '+ str(self.score))
        
    def newgame(self):
        ''' Launch a new game, reset all the attributes '''
        self.board.new_game()
        self.Can.delete('all')
        if self.score > self.highscore:
            self.highscore = self.score
            self.lhighscore.config(text = 'Highcore = '+str(self.highscore))
        self.score = 0
        self.lscore.config(text = 'Score = '+ str(self.score))
        self.id_snake = []
        self.start_spot()
        self.start = False
        self.b = True
        self.grow = 0
        self.end = False
        self.ad.config(text = '')
        self.nb_moves = 0
        
        
    def press_key(self, event):
        ''' detect the event of pressing an arrow '''
        if self.b:
            if event.keysym == 'Down':
                self.board.snake.change_direction((0, 1))
                self.b = False
                self.start = True
            elif event.keysym == 'Up':
                self.board.snake.change_direction((0, -1))
                self.b = False
                self.start = True
            elif event.keysym == 'Left':
                self.board.snake.change_direction((-1, 0))
                self.b = False
                self.start = True
            elif event.keysym == 'Right':
                self.board.snake.change_direction((1, 0))
                self.b = False
                self.start = True
            elif event.keysym == 'space':
                self.start = False
            
    def play(self):
        ''' Start the game, the game start when an arrow is pressed '''
        self.b = True
        if self.start:
            if self.grow != 0:
                self.board.snake.move(eat = True)
            else:
                self.board.snake.move()

        if not self.end:
            self.bind('<Key>', self.press_key)
            self.after(self.move_speed, self.play)
        else:
            if len(self.board.snake.position) == self.board.x*self.board.y:
                self.ad.config(text = 'Victory !!')
            else:
                self.ad.config(text = '/!\ Defeat ..')
            if self.score > self.highscore:
                self.highscore = self.score
                self.lhighscore.config(text = 'Highcore = '+str(self.highscore))
            self.start = False
            self.end = True
            self.after(self.move_speed, self.play)
            self.unbind('<Key>')

                
        
def start_game():
    play = Game(50, 50)
    play.play()
    play.mainloop()
    play.filehighscore.close()
    play.filehighscore = open('highscore.txt', 'w')
    play.filehighscore.write(str(play.highscore))
    play.filehighscore.close()
    
if __name__ == '__main__':        
    start_game()