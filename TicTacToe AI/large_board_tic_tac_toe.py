"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
                                                                                 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""

import pygame
import numpy as np
import math
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys
import random
import copy

# defines the class for random Board tic tac toe game


class RandomBoardTicTacToe:
    def __init__(self, size=(600, 600)):

        self.size = self.width, self.height = size
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.PURPLE = (95, 75, 139)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (96, 118, 143)

        # Grid Size
        self.GRID_SIZE = 3
        self. OFFSET = 5

        self.CIRCLE_COLOR = (0, 0, 255)
        self.CROSS_COLOR = (255, 0, 0)

        # This sets the WIDTH and HEIGHT of each grid location
        self.WIDTH = self.size[0]/self.GRID_SIZE - self.OFFSET
        self.HEIGHT = self.size[1]/self.GRID_SIZE - self.OFFSET

        # Margin between cells
        self.MARGIN = 5

        # more variables
        self.board = []
        self.clicked = False
        self.pos = []
        self.player = 1  # X = 1, O = -1
        self.turn = 1
        self.ShowMenu = True
        # default mode for playing the game (player vs AI)
        self.mode = "minimax"

        # Initialize pygame
        pygame.init()
        self.font = pygame.font.SysFont(None, 30)
        self.button1 = pygame.Rect(self.width, self.height, 0, 0)
        self.button2 = pygame.Rect(self.width, self.height, 0, 0)
        self.button3 = pygame.Rect(self.width, self.height, 0, 0)
        self.button4 = pygame.Rect(self.width, self.height, 0, 0)
        self.game_reset()

    def draw_game(self):  # draws the game and everything else
        # Create a 2 dimensional array using the column and row variables
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tic Tac Toe Random Grid")
        self.screen.fill(self.BLACK)
        # Draw the grid
        """
        YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
        """
        for x in range(self.GRID_SIZE):
            pygame.draw.line(self.screen, self.WHITE, (0, x * (self.width / self.GRID_SIZE)),
                             (self.width, x * (self.width / self.GRID_SIZE)), 6)
            pygame.draw.line(self.screen, self.WHITE, (x * ((self.height) / self.GRID_SIZE),
                             0), (x * ((self.height) / self.GRID_SIZE), self.height), 6)

        pygame.display.update()

    def draw_menu(self):  # draw the menu screen
        new_background_color = (0, 0, 0)
        pygame.draw.rect(self.screen, new_background_color,
                         (0, 0, self.width, self.height))

        menu_color = self.WHITE
        menu_width = self.width * 0.9  # Adjust menu width to be 90% of the screen width
        menu_height = 550
        menu_x = (self.width - menu_width) // 2
        menu_y = 30

        pygame.draw.rect(self.screen, menu_color, (menu_x,
                                                   menu_y, menu_width, menu_height), border_radius=4)

        menu_title_color = (0, 0, 0)  # Menu title
        menu_img = self.font.render(
            "Tic Tac Toe Game Menu", True, menu_title_color)
        self.screen.blit(menu_img, (menu_x + 150, menu_y + 20))

        # Adjust button dimensions to fit two rows of buttons within the menu width
        button_width = (menu_width - 150) / 2  # Adjusted width
        button_height = 80  # Increased height
        row_spacing = 20  # Space between rows of buttons
        col_spacing = 50  # Space between columns of buttons

        # Calculate the start_x position to center the buttons within the menu
        start_x = menu_x + (menu_width - (2 * button_width + col_spacing)) / 2

        # Adjust the start_y position to better center the buttons vertically
        start_y = menu_y + 100

        # First row of buttons
        self.button1 = pygame.Rect(
            start_x, start_y, button_width, button_height)
        self.button2 = pygame.Rect(
            start_x + button_width + col_spacing, start_y, button_width, button_height)

        # Second row of buttons - Adjust the y position based on the first row's position and height
        self.button3 = pygame.Rect(
            start_x, start_y + button_height + row_spacing, button_width, button_height)
        self.button4 = pygame.Rect(start_x + button_width + col_spacing,
                                   start_y + button_height + row_spacing, button_width, button_height)

        button_color = (0, 0, 0)
        text_color = (255, 255, 255)

        def draw_button(button_rect, text, text_color, button_color, border_radius=1):
            pygame.draw.rect(self.screen, button_color,
                             button_rect, border_radius=border_radius)
            text_img = self.font.render(text, True, text_color)
            text_x = button_rect.x + \
                (button_rect.width - text_img.get_width()) // 2
            text_y = button_rect.y + \
                (button_rect.height - text_img.get_height()) // 2
            self.screen.blit(text_img, (text_x, text_y))

        # Button texts
        player_text = "X" if self.player == 1 else "O"
        draw_button(self.button1, player_text, text_color, button_color)
        mode_text = "P v MiniMax" if self.mode == "minimax" else "P v NegaMax" if self.mode == "negamax" else "P v P"
        draw_button(self.button2, mode_text, text_color, button_color)
        size_text = "3 x 3" if self.GRID_SIZE == 3 else "4 x 4" if self.GRID_SIZE == 4 else "5 x 5" if self.GRID_SIZE == 5 else "6 x 6"
        draw_button(self.button3, size_text, text_color, button_color)
        draw_button(self.button4, "Start", text_color,
                    (0, 128, 0), border_radius=30)

    def draw_button(self, button_rect, text, text_color, button_color, border_radius=50):
        pygame.draw.rect(self.screen, button_color,
                         button_rect, border_radius=border_radius)
        text_img = self.font.render(text, True, text_color)
        text_x = button_rect.x + \
            (button_rect.width - text_img.get_width()) // 2
        text_y = button_rect.y + \
            (button_rect.height - text_img.get_height()) // 2
        self.screen.blit(text_img, (text_x, text_y))

    def draw_winner(self, score):

        if score > 0:
            win_text = f"Player X Wins! Score: {score}"
        elif score < 0:
            win_text = f"Player O Wins! Score: {score}"
        else:
            win_text = "Draw! Score: 0"

        # Adjusting the menu size slightly
        menu_width = 410  # Adjusted width for a more proportional look
        menu_height = 520  # Adjusted height for a more proportional look
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2

        # Draw the menu background with adjusted size
        pygame.draw.rect(self.screen, self.WHITE,
                         (menu_x, menu_y, menu_width, menu_height))

        # Winner text
        win_img = self.font.render(win_text, True, self.BLACK)
        self.screen.blit(win_img, (self.width // 2 -
                         win_img.get_width() // 2, menu_y + 30))

        # Adjusting button positions and shapes
        # Starting Y position for buttons, adjusted for new layout
        button_y_start = menu_y + 120
        button_spacing = 100  # Spacing between buttons
        button_height = 70  # Slightly larger buttons for better interaction

        # Play Again button
        self.button1 = pygame.Rect(
            menu_x + 60, button_y_start, 300, button_height)
        self.draw_button(self.button1, "Play Again", self.WHITE, self.BLACK)

        # Menu button
        self.button2 = pygame.Rect(
            menu_x + 60, button_y_start + button_spacing, 300, button_height)
        self.draw_button(self.button2, "Menu", self.WHITE, self.BLACK)

        # Quit button
        self.button3 = pygame.Rect(
            menu_x + 60, button_y_start + 2 * button_spacing, 300, button_height)
        self.draw_button(self.button3, "Quit", self.RED, self.BLACK)

    def change_turn(self):

        if (self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - X's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - O's turn")

    def draw_circle(self, x, y):
        """
        YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
        """

        pygame.draw.circle(self.screen, self.CIRCLE_COLOR, (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) / 2),
                           y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) / 2)), (((self.width / self.GRID_SIZE) / 2) * .75), 6)

    def draw_cross(self, x, y):  # to draw the corss for the cross player
        """
        YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
        """
        pygame.draw.line(self.screen, self.CROSS_COLOR, (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15)), (x * (
            self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15)), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15))), 6)
        pygame.draw.line(self.screen, self.CROSS_COLOR, (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width /
                         self.GRID_SIZE) * .15))), (x * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) - ((self.width / self.GRID_SIZE) * .15)), y * (self.width / self.GRID_SIZE) + ((self.width / self.GRID_SIZE) * .15)), 6)

    def is_game_over(self):  # check if the game is over
        if self.game_state.is_terminal():
            return True
        else:
            return False
        """
        YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
        FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
        
        YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME 
        """

    def move(self, move):       # functions for make move
        self.game_state = self.game_state.get_new_state(move)
        print("board state: ", self.game_state.board_state)
        x, y = move[0], move[1]
        if (self.game_state.turn_O):
            self.draw_circle(x, y)
        else:
            self.draw_cross(x, y)
        self.change_turn()
        if self.is_game_over():
            self.draw_winner(self.game_state.get_scores(True))

    def play_ai(self):  # let the AI play so needs to call Minmax and negamax
        """
        YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
        ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
        ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)

        THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
        NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
        """

        if (self.mode == "minimax"):
            score, move = minimax(copy.deepcopy(self.game_state), 4, True)
        elif (self.mode == "negamax"):
            score, move = negamax(copy.deepcopy(self.game_state), 4, True)

        self.move(move)

        self.change_turn()
        pygame.display.update()     # upadate display and see if the game is over or not
        terminal = self.game_state.is_terminal()
        """ USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """
    # reset the game function

    def game_reset(self):
        self.draw_game()  # rests the board and game state
        self.board = []
        for x in range(self.GRID_SIZE):
            row = [0] * self.GRID_SIZE
            self.board.append(row)

        self.game_state = GameStatus(self.board, self.player)
        self.change_turn()

        pygame.display.update()

    def play_game(self):  # play the game function
        done = False

        clock = pygame.time.Clock()
        self.draw_menu()

        while not done:
            for event in pygame.event.get():  # checks if user clicked on grid or quit
                """
                YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
                """

                """
                YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
                THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
                """

                """
                YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
                IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
                DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
                PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
                """
                # Quits Game
                if event.type == pygame.QUIT:
                    done = True

                # Game Over
                if self.is_game_over():  # TO see if it handels game over situation

                    self.draw_winner(self.game_state.get_scores(True))
                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False
                        self.pos = pygame.mouse.get_pos()
                        if self.button1.collidepoint(self.pos):
                            print("Re-Play")
                            self.game_reset()
                        if self.button2.collidepoint(self.pos):
                            print("Menu")
                            self.ShowMenu = True
                            self.game_reset()
                            self.draw_menu()
                        if self.button3.collidepoint(self.pos):
                            print("Game Over")
                            done = True
                # play Turns
                if not self.is_game_over() and not self.ShowMenu:
                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False
                        self.pos = pygame.mouse.get_pos()
                        cell_x = self.pos[0]
                        cell_y = self.pos[1]
                        if self.board[math.floor(cell_x / (self.width / self.GRID_SIZE))][math.floor(cell_y / (self.height / self.GRID_SIZE))] == 0:
                            self.move([math.floor(cell_x / (self.width / self.GRID_SIZE))] + [
                                      math.floor(cell_y / (self.height / self.GRID_SIZE))])
                            if not self.mode == "human" and not self.is_game_over():
                                self.play_ai()
                                print("issue1?")

                if not self.is_game_over() and self.ShowMenu:

                    if event.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
                        self.clicked = True
                    if event.type == pygame.MOUSEBUTTONUP and self.clicked == True:
                        self.clicked = False
                        self.pos = pygame.mouse.get_pos()
                        if self.button1.collidepoint(self.pos):
                            # X or O
                            if (self.player == 1):
                                self.player = -1
                            else:
                                self.player = 1
                            print("Change Setting(player): ", self.player)
                            self.draw_menu()
                        if self.button2.collidepoint(self.pos):
                            # Human or AI
                            if (self.mode == "minimax"):
                                self.mode = "negamax"
                            elif (self.mode == "negamax"):
                                self.mode = "human"
                            elif (self.mode == "human"):
                                self.mode = "minimax"
                            print("Change Setting(mode): ", self.mode)
                            self.draw_menu()
                        if self.button3.collidepoint(self.pos):
                            # Board Size
                            if self.GRID_SIZE == 3:
                                self.GRID_SIZE = 4
                            elif self.GRID_SIZE == 4:
                                self.GRID_SIZE = 3

                            print("Change Setting(gridSize): ", self.GRID_SIZE)
                            self.draw_menu()
                        if self.button4.collidepoint(self.pos):
                            # Start game
                            self.ShowMenu = False
                            self.game_reset()
                            print("Start")
                            if (self.mode == "minimax" and self.player == -1 or self.mode == "negamax" and self.player == -1):
                                self.play_ai()
                                print("issue2?")
                                print("player: ", self.player)

            clock.tick(60)
            # Update the screen with what was drawn.
            pygame.display.update()

        pygame.quit()


# Start Game
tictactoegame = RandomBoardTicTacToe()
tictactoegame.play_game()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""