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
        self.eval_type = str(eval_type)
        self.prune = str(prune)
        self.max_depth = int(max_depth)
        
        self.max_depth_seen = 0
        self.total_nodes_seen = 0

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
        successors = []
        
        for r in range(board.get_num_rows()):
            for c in range(board.get_num_cols()):
                if board.is_legal_move(c, r, player_symbol):
                    new_board = board.cloneOBoard()
                    new_board.play_move(c, r, player_symbol)
                    new_board.last_move = (c, r)
                    successors.append(new_board)

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
        
        # H2: Custom Heuristic - Of all successor states for each player, the difference in the sum of the number of symbols that would be flipped
        elif self.eval_type == "2":
            successors = self.get_successors(board, self.symbol)
            opp_successors = self.get_successors(board, self.oppSym)
            total = 0
            opp_total = 0
            for s in successors:
                total += abs(board.count_score(self.symbol) - s.count_score(self.oppSym))
            for s in opp_successors:
                opp_total += abs(board.count_score(self.symbol) - s.count_score(self.oppSym))
            return total - opp_total
        
        return 0.0
        

    def max_value(self, board: OthelloBoard, alpha: float, beta: float, depth: int):
        # Write max_value function here
        # type:(board, float, float, int) -> (float)
        self.max_depth_seen = max(self.max_depth_seen, depth)
        
        if self.terminal_state(board) or depth == self.max_depth:
            return self.eval_board(board), (None, None)
        
        v = float('-inf')
        move = (None, None)
        
        for s in self.get_successors(board, self.symbol):
            self.total_nodes_seen += 1
            v2, _ = self.min_value(s, alpha, beta, depth + 1)
            if v2 >= v:
                v, move = v2, s.last_move
                alpha = max(alpha, v)
                if self.prune == '1' and v >= beta:
                    return v, move
        return v, move
    
    
    def min_value(self, board: OthelloBoard, alpha: float, beta: float, depth: int):
        # Write min_value function here
        # type:(board, float, float, int) -> (float)
        self.max_depth_seen = max(self.max_depth_seen, depth)
        
        if self.terminal_state(board) or depth == self.max_depth:
            return self.eval_board(board), (None, None)
        
        v = float('inf')
        move = (None, None)
        
        for s in self.get_successors(board, self.oppSym):
            self.total_nodes_seen += 1
            
            v2, _ = self.max_value(s, alpha, beta, depth + 1)
            if v2 <= v:
                v, move = v2, s.last_move
                beta = min(beta, v)
                if self.prune == '1' and v <= alpha:
                    return v, move
        return v, move

    
    def alphabeta(self, board: OthelloBoard) -> tuple:
        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        _, move = self.max_value(board, alpha=-float('inf'), beta=float('inf'), depth=1)
        col, row = move
    
        return (col, row)
        

    def get_move(self, board: OthelloBoard) -> tuple:
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        return self.alphabeta(board)