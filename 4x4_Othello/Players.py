from OthelloBoard import OthelloBoard


class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        self.total_nodes_seen += 1
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """
    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        
        # Load in the parameters
        self.eval_type = str(eval_type)
        self.prune = str(prune)
        self.max_depth = int(max_depth)
        
        # Tracker variables
        self.max_depth_seen = 0
        self.total_nodes_seen = 0

        # Set the opponent's symbol
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'

    def terminal_state(self, board: OthelloBoard) -> bool:
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board: OthelloBoard) -> int:
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol: str) -> str:
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"


    def get_successors(self, board: OthelloBoard, player_symbol: str) -> list:
        # Write function that takes the current state and generates all successors obtained by legal moves
        # type:(board, player_symbol) -> (list)
        
        # Initialize the list of successors
        successors = []
        
        # Iterate over every position, the row and column
        for r in range(board.get_num_rows()):
            for c in range(board.get_num_cols()):
                # If the move is legal, clone the board and play the move, save as successor
                if board.is_legal_move(c, r, player_symbol):
                    new_board = board.cloneOBoard()
                    new_board.play_move(c, r, player_symbol)
                    new_board.last_move = (c, r)
                    successors.append(new_board)

        # If there are no successors, return the board as a "Pass" action
        if len(successors) == 0:
            return [board]
        
        # Return generated successors
        return successors


    def eval_board(self, board: OthelloBoard) -> float:
        # Write eval function here
        # type:(board) -> (float)

        # Check if terminal state
        if self.terminal_state(board):
            return self.terminal_value(board)

        # H0: Piece Difference - difference in number of pieces
        if self.eval_type == "0":
            return board.count_score(self.symbol) - board.count_score(self.oppSym)
        
        
        # H1: Mobility - difference in number of legal moves
        elif self.eval_type == "1":
            return len(self.get_successors(board, self.symbol)) - len(self.get_successors(board, self.oppSym))        
        
        
        # H2: Custom Heuristic - Of all successor states for each player, the difference in the sum of the number of 
        # symbols that would be flipped
        elif self.eval_type == "2":
            # Get the successors for each player
            successors = self.get_successors(board, self.symbol)
            opp_successors = self.get_successors(board, self.oppSym)
            
            # Initialize the total number of flipped pieces
            total = 0
            opp_total = 0
            
            # Calculate the total number of flipped pieces for each player of each action
            for s in successors:
                total += abs(board.count_score(self.symbol) - s.count_score(self.oppSym))
            for s in opp_successors:
                opp_total += abs(board.count_score(self.symbol) - s.count_score(self.oppSym))
                
            # Return the difference in the total number of flipped pieces each player can make
            return total - opp_total
        
        return 0.0
        

    def max_value(self, board: OthelloBoard, alpha: float, beta: float, depth: int):
        # Write max_value function here
        # type:(board, float, float, int) -> (float)
        
        self.max_depth_seen = max(self.max_depth_seen, depth)
        
        # Check if terminal state or max depth; if so, return the evaluation of the board
        if self.terminal_state(board) or depth == self.max_depth:
            return self.eval_board(board), (None, None)
        
        # Initialize the value and move for comparison
        v = float('-inf')
        move = self.get_successors(board, self.symbol)[0].last_move
        
        # Iterate over all successors
        for s in self.get_successors(board, self.symbol):
            # Increment the total number of nodes seen
            self.total_nodes_seen += 1
            
            # Get the min value of the successor (the move they would play if playing optimally)
            v2, _ = self.min_value(s, alpha, beta, depth + 1)
            
            # If the result of the action P2 takes is better than current best case scenario, update the value and move
            if v2 > v:
                v, move = v2, s.last_move
        
                # Alpha-beta pruning if enabled
                alpha = max(alpha, v)
                if self.prune == '1' and v >= beta:
                    return v, move
        
        # Return the optimal value and move
        return v, move
    
    
    def min_value(self, board: OthelloBoard, alpha: float, beta: float, depth: int):
        # Write min_value function here
        # type:(board, float, float, int) -> (float)
        
        self.max_depth_seen = max(self.max_depth_seen, depth)
        
        # Check if terminal state or max depth; if so, return the evaluation of the board
        if self.terminal_state(board) or depth == self.max_depth:
            return self.eval_board(board), (None, None)
        
        # Initialize the value and move for comparison
        v = float('inf')
        move = self.get_successors(board, self.oppSym)[0].last_move
        
        # Iterate over all successors
        for s in self.get_successors(board, self.oppSym):
            # Increment the total number of nodes seen
            self.total_nodes_seen += 1
            
            # Get the max value of the successor (the move they would play if playing optimally)
            v2, _ = self.max_value(s, alpha, beta, depth + 1)
            
            # If the result of the action P2 takes is better than current best case scenario, update the value and move
            if v2 < v:
                v, move = v2, s.last_move
                
                # Alpha-beta pruning if enabled
                beta = min(beta, v)
                if self.prune == '1' and v <= alpha:
                    return v, move
                
        # Return the optimal value and move
        return v, move

    
    def alphabeta(self, board: OthelloBoard) -> tuple:
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        
        # Use the max_value function to get the optimal move using minimax and alpha-beta pruning if enabled
        _, move = self.max_value(board, alpha=-float('inf'), beta=float('inf'), depth=1)
        
        # Parse the move
        col, row = move
    
        # Return the move
        return (col, row)
        

    def get_move(self, board: OthelloBoard) -> tuple:
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        
        # Use minimax with alpha-beta pruning (if enabled) to get the optimal move
        return self.alphabeta(board)
