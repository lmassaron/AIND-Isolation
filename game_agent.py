"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")
    else:
        player1_moves = game.get_legal_moves(player)
        player2_moves = game.get_legal_moves(game.get_opponent(player))
        center_x, center_y = int(game.width / 2), int(game.height / 2)
        center1 = sum([1. / (abs(x - center_x) + abs(y - center_y) + 1.) for x, y in player1_moves])
        center2 = sum([1. / (abs(x - center_x) + abs(y - center_y) + 1.) for x, y in player2_moves])
        return center1 / (center2 + 1.0)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")
    else:
        player1 = game.get_legal_moves(player)
        player2 = game.get_legal_moves(game.get_opponent(player))
        common_moves = set(player1) & set(player2)
        player1_moves = len(player1)
        player2_moves = len(player2)
        unique_player1_moves = len(set(player1) - common_moves)
        unique_player2_moves = len(set(player2) - common_moves)
        return float((player1_moves + unique_player1_moves) - (player2_moves + unique_player2_moves)) / (player1_moves + unique_player1_moves + 1)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")
    elif game.is_winner(player):
        return float("inf")
    else:
        player1_moves = game.get_legal_moves(player)
        player2_moves = game.get_legal_moves(game.get_opponent(player))
        score = float(0)
        for x1, y1 in player1_moves:
            for x2, y2 in player2_moves:
                score += abs(x1 - x2) + abs(y1 - y2)
        return score


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax_search(self, game, depth):
        """Minimax search"""

        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Enumerate legal moves
        legal_moves = game.get_legal_moves(player=game.active_player)
        if not legal_moves:
            # Return empty move if no legal moves available
            return -1, -1

        # fixing the initial response values
        best_value = float("-inf")
        levels_left = depth - 1
        chosen_action = -1, -1
        # scanning through legal moves
        for action in legal_moves:
            project_next_game_state = game.forecast_move(action)
            minimum_value = self.min_value(project_next_game_state, levels_left)
            if best_value < minimum_value:
                chosen_action, best_value, = action, minimum_value
        return chosen_action

    def min_value(self, game, depth):
        """Return the minimum value"""

        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # if we reached the root level, we exit returning the actual utility
            return self.score(game, self)
        else:
            value = float("inf")
            # Scanning through legal moves
            for action in game.get_legal_moves(player=game.active_player):
                # Enumerating the next actions
                project_next_game_state = game.forecast_move(action)
                # Setting the levels left in the recursion
                levels_left = depth - 1
                # Setting the minimum value found up so far
                value = min(value, self.max_value(project_next_game_state, levels_left))

        return value

    def max_value(self, game, depth):
        """Return the maximum value"""

        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # if we reached the root level, we exit returning the actual utility
            return self.score(game, self)
        else:
            value = float("-inf")
            # Scanning through legal moves
            for action in game.get_legal_moves(player=game.active_player):
                # Enumerating the next actions
                project_next_game_state = game.forecast_move(action)
                # Setting the levels left in the recursion
                levels_left = depth - 1
                #  Setting the maximum value found up so far
                value = max(value, self.min_value(project_next_game_state, levels_left))

        return value

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        chosen_action = self.minimax_search(game, depth)
        return chosen_action

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        search_depth = 0

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is expired.
            while 1 == 1:
                best_move = self.alphabeta(game, search_depth)
                search_depth += 1
        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alfabeta_search(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Enumerate legal moves
        legal_moves = game.get_legal_moves(player=game.active_player)
        if not legal_moves:
            # Return empty move if no legal moves available
            return -1, -1
        else:
            value, chosen_action = self.max_value(game, depth, alpha, beta)
            return chosen_action

    def max_value(self, game, depth, alpha, beta):
        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # if we reached the root level, we exit returning the actual utility
            return self.score(game, self), (-1, -1)
        else:
            # fixing the initial response values
            best_value = float("-inf")
            best_move = (-1, -1)
            levels_left = depth - 1

            # Scanning through legal moves
            for action in game.get_legal_moves(player=game.active_player):
                value, move = self.min_value(game.forecast_move(action), levels_left, alpha, beta)
                if value > best_value:
                    best_value = value
                    best_move = action
                if best_value >= beta:
                    return best_value, best_move
                alpha = max(alpha, best_value)
            return best_value, best_move

    def min_value(self, game, depth, alpha, beta):
        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
            # if we reached the root level, we exit returning the actual utility
            return  self.score(game, self), (-1, -1)
        else:
            # fixing the initial response values
            best_value = float("inf")
            best_move = (-1, -1)
            levels_left = depth - 1

            # Scanning through legal moves
            for action in game.get_legal_moves(player=game.active_player):
                value, move = self.max_value(game.forecast_move(action), levels_left, alpha, beta)
                if value < best_value:
                    best_value = value
                    best_move = action
                if best_value <= alpha:
                    return best_value, best_move
                beta = min(beta, best_value)
            return best_value, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        # RaiseTimeout when the timer expires
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        chosen_action = self.alfabeta_search(game, depth, alpha, beta)
        return chosen_action
