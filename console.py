# console.py
# James Nguyen 45298461
#
# This is the module that will get user inputs through console commands
#

import OthelloGameLogic
from OthelloGameLogic import GameState
from OthelloGameLogic import InvalidMoveError
from OthelloGameLogic import OddColRowNumber


def print_game_pieces(game_state: GameState) -> None:
    """
    Print the current number of black and white pieces
    :param game_state: The Othello Game State
    """
    first_line = 'B: '
    first_line += str(game_state.board.black_disc)

    first_line += ' W: '
    first_line += str(game_state.board.white_disc)
    print(first_line)


def print_game_board(game_state: GameState) -> None:
    """
    Print the board of the current game_state
    :param game_state: The Othello Game State
    """
    rows = game_state.board.rows
    columns = game_state.board.columns
    game_board = game_state.board

    result = ''
    counter = 1
    for row in range(rows):
        for column in range(columns):
            piece = game_board.get_piece([row, column])
            if piece.color == OthelloGameLogic.NONE:
                result += '. '
            elif piece.color == OthelloGameLogic.BLACK:
                result += 'B '
            elif piece.color == OthelloGameLogic.WHITE:
                result += 'W '
        if counter < rows:
            result += '\n'
            counter += 1

    print(result)


def print_turn(game_state: GameState) -> None:
    """
    Print the current turn
    :param game_state: The Othello Game State
    """
    turn = game_state.turn
    if turn == OthelloGameLogic.BLACK:
        print('TURN: B')
    elif turn == OthelloGameLogic.WHITE:
        print('TURN: W')


def start_game() -> GameState:
    """
    Ask user input to create a new game state
    :return: The Othello Game State
    """
    while True:
        try:
            rules = input()
            rows_on_boards = int(input())
            columns_of_board = int(input())
            starting_player = input()
            top_left_color_disc = input()
            winning_condition = input()

            game_state = GameState(rules, rows_on_boards, columns_of_board,
                                   starting_player, top_left_color_disc, winning_condition)

            return game_state
        except OddColRowNumber:
            print('ODD COLUMN OR ROW NUMBER')
        except TypeError:
            print('CAN ONLY BE INTEGER')


def input_piece(game_state: GameState) -> None:
    """
    Input user moves into the game state
    :param game_state: The Othello Game State
    """
    user_input = input()

    split = user_input.split()

    row = int(split[0]) - 1
    column = int(split[1]) - 1

    game_state.move([row, column])


def play_game(game_state: GameState) -> None:
    """
    Prints output for one turn of the game adn gets input from user
    :param game_state: Othello Game State
    """
    print_game_pieces(game_state)
    print_game_board(game_state)
    while True:
        try:
            print_turn(game_state)
            input_piece(game_state)
            print('VALID')
            break
        except InvalidMoveError:
            print('INVALID')


def main():
    game_state = start_game()
    while game_state.ending_condition_met() is False:
        play_game(game_state)

    print_game_pieces(game_state)
    print_game_board(game_state)
    print(game_state.winner)


if __name__ == '__main__':
    main()
