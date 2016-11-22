# GameState.py
# James Nguyen 45298461
#
# This is the game logic, with some made exceptions
#
NONE = 0  # This is the game constants, setting colors to integer
BLACK = 1
WHITE = 2


class OddColRowNumber(Exception):
    """Raises whenever there is an invalid Column or Row number """
    pass


class InvalidMoveError(Exception):
    """Raises whenever there is an invalid move"""
    pass


class Piece:
    """
    This will be a single game piece in the game, with property of either NONE, WHITE or BLACK.
    """
    def __init__(self, color: int, location: [int]):
        self.color = color
        self.location = location

    def opposite_color(self) -> int:
        """
        What is the opposite color of the piece
        :return: opposite color of the piece
        """
        if self.color == BLACK:
            return WHITE
        elif self.color == WHITE:
            return BLACK
        else:
            return NONE


class GameBoard:
    """
    This is the board of the Othello Game State
    """
    def __init__(self, top_left_disc_color: str, rows: int, columns: int):
        self._top_left_disc_color = top_left_disc_color
        self.rows = rows
        self. columns = columns
        self.board = self._new_game_board()
        self.black_disc = 2
        self.white_disc = 2

    def _new_game_board(self) -> [[Piece]]:
        """
        Create a new game board using list
        :return: List of the list of boards and their colors inside
        """
        board = []

        # This is the code for creating the diagonal color pieces for the board
        if self._top_left_disc_color == 'B':
            diagonal1 = BLACK
            diagonal2 = WHITE
        else:
            diagonal1 = WHITE
            diagonal2 = BLACK

        turns = 0  # This will help make sure which important piece is going to be printed
        for row in range(self.rows):
            board.append([])
            for col in range(self.columns):
                condition1 = self.columns / 2 - col
                condition2 = self.rows / 2 - row

                if 0 <= condition1 <= 1 and 0 <= condition2 <= 1:
                    if turns == 0 or turns == 3:
                        board[-1].append(Piece(diagonal1, [row, col]))

                    elif turns == 1 or turns == 2:
                        board[-1].append(Piece(diagonal2, [row, col]))

                    turns += 1

                else:
                    board[-1].append(Piece(NONE, [row, col]))

        return board

    def place_piece(self, place: [int], color: int) -> None:
        """
        Place piece on the board
        :param place: Place on the board
        :param color: Color of piece to placed on the board
        """
        row, column = place
        before_piece_color = self.board[row][column].color
        self.board[row][column] = Piece(color, [row, column])
        self.adjust_piece_num(before_piece_color, color)

    def adjust_piece_num(self, before_color: int, after_color: int) -> None:
        """
        Adjust the number of pieces in game_board
        :param before_color: The color before placing down the piece
        :param after_color: The color after placing down the piece
        """
        if before_color == BLACK:
            self.black_disc -= 1
        elif before_color == WHITE:
            self.white_disc -= 1
        if after_color == BLACK:
            self.black_disc += 1
        elif after_color == WHITE:
            self.white_disc += 1

    def get_piece(self, place: [int]) -> Piece:
        row, column = place
        return self.board[row][column]

    def list_of_pieces(self) -> [Piece]:
        list_of_pieces = []
        for row in self.board:
            for piece in row:
                list_of_pieces.append(piece)
        return list_of_pieces


def _list_testing_places(move: [int]) -> [int]:
    """
    Testing pieces for piece
    :param move: piece
    :return: Testing pieces
    """
    list_of_testing_locations = []
    row, column = move
    for i in range(3):
        testing_row = row - 1 + i
        if testing_row < 0:
            continue
        for h in range(3):
            testing_column = column - 1 + h
            if testing_column < 0:
                continue
            testing_place = [testing_row, testing_column]
            if testing_place is move:
                continue
            list_of_testing_locations.append(testing_place)
    return list_of_testing_locations


def _list_of_locations(list_of_pieces: [Piece]) -> [int]:
    """
    With a list of pieces, return a list of the locations of those pieces
    :param list_of_pieces: List of pieces
    :return: List of locations of the pieces
    """
    list_of_locations = []
    for piece in list_of_pieces:
        list_of_locations.append(piece.location)
    return list_of_locations


class GameState:
    """
    This is the Othello Game State, full with the game logic
    """

    def __init__(self, rule: str, rows: int, columns: int,
                 starting_player: str, top_left_disc_color: str, winning_condition: str):
        """
        :param rule: Rules for the game, either simple or full othello rules
        :param rows: How many rows there are in the game
        :param columns: How many columns there are in the game
        :param starting_player: Which color is the starting player
        :param top_left_disc_color: Which color will the top left disc be
        :param winning_condition: The winning condition, > for largest number of discs, < for smallest number of discs
        """
        self.rule = rule

        if not (4 <= rows <= 16 and rows % 2 == 0) or not (4 <= columns <= 16 and columns % 2 == 0):
            raise OddColRowNumber

        if starting_player == 'B':
            self.turn = BLACK
        elif starting_player == 'W':
            self.turn = WHITE

        self.winning_condition = winning_condition

        self.board = GameBoard(top_left_disc_color, rows, columns)
        self.winner = None

    def move(self, move: [int]) -> None:
        """
        How a move will affect the game state depending on the rule
        :param move: The piece that the player will place on the game _state
        """
        if self.rule == 'SIMPLE':
            if move in self.simple_possible_moves():
                self.board.place_piece(move, self.turn)

                for piece in self._directly_affected_pieces(move):
                    self.board.place_piece(piece.location, self.turn)

                self._new_turn()

            else:
                raise InvalidMoveError

        if self.rule == 'FULL':
            if move in self.full_possible_moves():
                self.board.place_piece(move, self.turn)

                for directly_affected_piece in self._directly_affected_pieces(move):
                    if self._full_affected_pieces(move, directly_affected_piece) is None:
                        'This means that there are no affected pieces going in the direction of this directly'
                        'affected piece.'
                        continue

                    for affected_piece in self._full_affected_pieces(move, directly_affected_piece):
                        self.board.place_piece(affected_piece.location, self.turn)

                self._new_turn()

            else:
                raise InvalidMoveError

    def ending_condition_met(self) -> bool:
        """
        Depending upon the rules, return whether the game is ending.
        :return: Boolean on whether the ending condition is met
        """
        if self.rule == 'SIMPLE':
            if len(self.simple_possible_moves()) == 0:
                self._winner()
                return True
            else:
                return False

        elif self.rule == 'FULL':
            # This has to deal with the possibilities that there could be no moves for one side
            if len(self.full_possible_moves()) == 0:
                self._new_turn()
                if len(self.simple_possible_moves()) == 0:
                    self._winner()
                    return True
            return False

    def _winner(self) -> int:
        """
        Initialize the winner of the game state
        :return: winner of the game
        """
        if self.winning_condition == '>':
            if self.board.black_disc > self.board.white_disc:
                self.winner = 'BLACK'
            elif self.board.black_disc < self.board.white_disc:
                self.winner = 'WHITE'
            else:
                self.winner = 'NONE'
        else:
            if self.board.black_disc > self.board.white_disc:
                self.winner = 'WHITE'
            elif self.board.black_disc < self.board.white_disc:
                self.winner = 'BLACK'
            else:
                self.winner = 'NONE'

    def _new_turn(self) -> None:
        """ Make a new turn """
        self.turn = self._opposite_turn_color()

    def _opposite_turn_color(self) -> int:
        """
        Return the opposite color opposed to the current turn color
        :return: Opposite turn color
        """
        if self.turn == BLACK:
            return WHITE
        else:
            return BLACK

    def _list_of_non_empty_pieces(self) -> [Piece]:
        """
        List of pieces on the board
        :return: list of pieces on the board
        """
        list_of_non_empty_pieces = []
        for piece in self.board.list_of_pieces():
            if piece.color > 0:
                list_of_non_empty_pieces.append(piece)
        return list_of_non_empty_pieces

    def _list_of_color_pieces(self, color: int) -> [Piece]:
        """
        List of a places of a certain color pieces
        :param color: The color of pieces we are looking for
        :return: The pieces of that specific color
        """
        list_of_color_pieces = []
        for piece in self.board.list_of_pieces():
            if piece.color is color:
                list_of_color_pieces.append(piece)
        return list_of_color_pieces

    def simple_possible_moves(self) -> [[int]]:
        """
        Return the possible moves of simple rules
        :return: Possible moves of simple rules
        """
        list_of_empty_pieces = self._list_of_color_pieces(NONE)
        list_of_opposite_turn_pieces = self._list_of_color_pieces(self._opposite_turn_color())

        list_of_possible_moves_locations = []
        for piece in list_of_opposite_turn_pieces:
            for testing_place in _list_testing_places(piece.location):
                list_of_locations = _list_of_locations(list_of_empty_pieces)
                if testing_place in list_of_locations and testing_place not in list_of_possible_moves_locations:
                    list_of_possible_moves_locations.append(testing_place)

        return list_of_possible_moves_locations

    def _directly_affected_pieces(self, move: [int]) -> [Piece]:
        """
        Return the directly affected pieces around the move
        :param move: The move we are returning affected pieces around
        :return: The affected pieces around the move
        """
        list_of_opposite_pieces = self._list_of_color_pieces(self._opposite_turn_color())
        list_of_affected_pieces = []
        for testing_place in _list_testing_places(move):
            if testing_place in _list_of_locations(list_of_opposite_pieces):
                testing_piece = self.board.get_piece(testing_place)
                list_of_affected_pieces.append(testing_piece)

        return list_of_affected_pieces

    def full_possible_moves(self) -> [[int]]:
        """
        Possible moves for the full Othello rule
        :return: possible moves for the full Othello rule
        """
        list_of_move = []
        for move in self.simple_possible_moves():
            for piece in self._directly_affected_pieces(move):
                if self._full_affected_pieces(move, piece) is not None:
                    if move not in list_of_move:
                        list_of_move.append(move)
        return list_of_move

    def _full_affected_pieces(self, move: [int], piece: Piece) -> [Piece]:
        """
        Affected pieces in the full rule depending on the move and the directly affected piece
        :param move: The move
        :param piece: The directly affected piece
        :return: List of affected pieces
        """
        list_of_affected_pieces = []
        row_difference = piece.location[0] - move[0]
        column_difference = piece.location[1] - move[1]
        try:
            for i in range(16):
                testing_row = piece.location[0] + i * row_difference
                testing_column = piece.location[1] + i * column_difference
                testing_place = [testing_row, testing_column]
                testing_piece = self.board.get_piece(testing_place)
                if (
                        testing_row < 0 or testing_column < 0 or testing_piece.color == NONE or
                        testing_row > self.board.rows or testing_column > self.board.columns
                ):
                    return None
                elif testing_piece in self._list_of_color_pieces(self.turn):
                    break
                elif testing_piece in self._list_of_color_pieces(self._opposite_turn_color()):
                    list_of_affected_pieces.append(testing_piece)

            return list_of_affected_pieces
        except IndexError:
            pass
