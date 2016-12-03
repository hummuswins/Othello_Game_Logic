import point
import OthelloGameLogic


def _convert_color(color: int) -> str:
    """
    Convert color integer to the color hexadecimal
    :param color: Color integer from the Othello Game Logc
    :return: Hexadecimal of the color
    """
    if color == OthelloGameLogic.BLACK:
        return '#000000'
    elif color == OthelloGameLogic.WHITE:
        return '#ffffff'
    elif color == OthelloGameLogic.NONE:
        return '#c0cde0'


class Disc:
    def __init__(self, center_point: point.Point, x_distance: float, y_distance: float,
                 game_piece: OthelloGameLogic.Piece):
        """
        Disc is an object that contain the both the piece information and the color
        :param center_point: The fractional center point of the disc
        :param x_distance: The fractional x-distance from the center point that disc is contained in
        :param y_distance: The fraction y-distance from the center point the disc is contained in
        :param game_piece: The Game Piece the disc is portraying
        """
        self.center_point = center_point
        self.x_distance = x_distance
        self.y_distance = y_distance

        self.game_piece = game_piece
        self.fill = _convert_color(self.game_piece.color)

    def contains(self, click_point: point.Point) -> bool:
        """
        Whether the click point is inside the rectangle
        :param click_point: The x and y coordinates of the click point
        :return: Boolean on whether the click point is inside the the rectangle of the disc
        """
        x, y = click_point.frac()
        center_x, center_y = self.center_point.frac()
        if (
            center_x - self.x_distance <= x <= center_x + self.x_distance and
            center_y - self.y_distance <= y <= center_y + self.y_distance
        ):
            return True
        else:
            return False

    def set_color(self, color: int) -> None:
        """
        Set the color fill of the disc
        :param color: The integer of the color
        """
        self.fill = _convert_color(color)


def _create_lines_list(num: int):
    """
    Create a list of fractional lines point based on the numbers of lines
    :param num: Number of lines
    """
    lines_list = []
    baseline = 0.0
    difference = 1.0 / float(num)

    for i in range(num - 1):
        baseline += difference
        lines_list.append(baseline)

    return lines_list


class ModelState:
    def __init__(self, rows: int, columns: int):
        """
        Model state is the  the collections of information of all the different pieces
        :param rows: Rows of the game board
        :param columns: Columns of the game board
        """
        self.discs = []
        self.rows = rows
        self.columns = columns
        self.row_lines = _create_lines_list(rows)
        self.col_lines = _create_lines_list(columns)
        self.x_distance = 1.0 / float(columns * 2)
        self.y_distance = 1.0 / float(rows * 2)

    def add_disc(self, center_point: point.Point, game_piece: OthelloGameLogic.Piece) -> None:
        """
        Add disc to the list of discs
        :param center_point: Fractional center point of the disc
        :param game_piece: The game piece from Othello Game Logic
        """
        self.discs.append(Disc(center_point, self.x_distance, self.y_distance, game_piece))

    def handle_click(self, click_point: point.Point) -> [int]:
        """
        Handling click point by checking if every discs has contain the click point
        :param click_point: The x and y coordinate of the click point
        :return: The location of the game piece in the board e.g. [0,1]
        """
        for disc in self.discs:
            if disc.contains(click_point):
                return disc.game_piece.location
