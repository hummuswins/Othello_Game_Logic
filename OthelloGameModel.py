import point
import OthelloGameLogic


def _convert_color(color: int) -> str:
    if color == OthelloGameLogic.BLACK:
        return '#000000'
    elif color == OthelloGameLogic.WHITE:
        return '#ffffff'
    elif color == OthelloGameLogic.NONE:
        return '#c0cde0'


class Disc:
    def __init__(self, center_point: point.Point, radius_frac: float, game_piece: OthelloGameLogic.Piece):
        self.center_point = center_point
        self.radius_frac = radius_frac

        self.game_piece = game_piece
        self.fill = _convert_color(self.game_piece.color)

    def contains(self, click_point: point.Point) -> bool:
        x, y = click_point.frac()
        center_x, center_y = self.center_point.frac()
        if (
            center_x - self.radius_frac <= x <= center_x + self.radius_frac and
            center_y - self.radius_frac <= y <= center_y + self.radius_frac
        ):
            return True
        else:
            return False

    def set_color(self, color: int):
        self.color = color
        self.fill = _convert_color(color)


def _create_lines_list(num: int):
    lines_list = []
    baseline = 0.0
    difference = 1.0 / float(num)

    for i in range(num - 1):
        baseline += difference
        lines_list.append(baseline)

    return lines_list


class ModelState:
    def __init__(self, rows: int, columns: int):
        self.discs = []
        self.rows = rows
        self.columns = columns
        self.row_lines = _create_lines_list(rows)
        self.col_lines = _create_lines_list(columns)
        self._radius_frac = 1.0 / float(rows * 2) - 0.005

    def add_disc(self, center_point: point.Point, game_piece: OthelloGameLogic.Piece):
        self.discs.append(Disc(center_point, self._radius_frac, game_piece))

    def handle_click(self, click_point: point.Point):
        for disc in self.discs:
            if disc.contains(click_point):
                return disc.game_piece.location
