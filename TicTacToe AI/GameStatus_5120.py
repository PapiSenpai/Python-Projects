class GameStatus:

    def __init__(self, board_state, turn_O):  
        #ses the board state and whos turn
        self.board_state = board_state
        self.turn_O = turn_O
        self.oldScores = 0

        self.winner = ""
    #check if the game reached the terminal
    def is_terminal(self): 
        """
        YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
        THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
        """
        # loop throught board and check
        terminal = True
        for x in self.board_state:
            for y in x:
                if y == 0:
                    terminal = False
        return terminal
    # calculates the scores to determine the game 
    def get_scores(self, terminal):
        """
    YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
    EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)

    YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
    NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)

    """
        # board dimesnions
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

        # check rows
        for i in range(rows):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i][j + 1] == self.board_state[i][j + 2] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        # Check cols
        for i in range(rows-2):
            for j in range(cols):
                if self.board_state[i][j] == self.board_state[i + 1][j] == self.board_state[i + 2][j] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        # Check diags (left to right)
        for i in range(rows - 2):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i + 1][j + 1] == self.board_state[i + 2][j + 2] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        # Check diagonals (right to left)
        for i in range(2, rows):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i - 1][j + 1] == self.board_state[i - 2][j + 2] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        return scores

    def get_negamax_scores(self, terminal):
        """
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        scores = 0
        check_point = 3 if terminal else 2

        # check rows
        for i in range(rows):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i][j + 1] == self.board_state[i][j + 2] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        # Check cols
        for i in range(rows - 2):
            for j in range(cols):
                if self.board_state[i][j] == self.board_state[i + 1][j] == self.board_state[i + 2][j] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        # Check diagonals (left to right)
        for i in range(rows - 2):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i + 1][j + 1] == self.board_state[i + 2][j + 2] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        # Check diagonals (right to left)
        for i in range(2, rows):
            for j in range(cols - 2):
                if self.board_state[i][j] == self.board_state[i - 1][j + 1] == self.board_state[i - 2][j + 2] and self.board_state[i][j] != 0:
                    scores += self.board_state[i][j]

        return scores
    # moves on board
    def get_moves(self):
        moves = []
        """
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
        # overall initalize the list to score and the dimensions
        rows = len(self.board_state)
        cols = len(self.board_state[0])
        # loop 
        for i in range(rows):
            for j in range(cols):
                if self.board_state[i][j] == 0:
                    moves.append((i, j))

        return moves
    
    # get a new game after making a move
    #updates the baord, gets cordinats and retunes to a new Gamestaus
    def get_new_state(self, move):
        new_board_state = self.board_state.copy()
        x, y = move[0], move[1]
        new_board_state[x][y] = 1 if self.turn_O else -1
        print("board state: ", new_board_state)
        return GameStatus(new_board_state, not self.turn_O)