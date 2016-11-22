import tkinter
import point
from OthelloGameLogic import GameState
import OthelloGameModel


class OthelloGameApplication:
    def __init__(self, game_state: GameState,
                 model_state: OthelloGameModel.ModelState):
        self._root_window = tkinter.Tk()

        self._game_state = game_state
        self._model_state = model_state

        self._canvas = tkinter.Canvas(
            master=self._root_window, width=400, height=400,
            background='#c0cde0'
        )

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._canvas.grid(
            row=0, column=0, padx=10, pady=10,
            sticky=tkinter.N + tkinter.S + tkinter.W + tkinter.E
        )

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

    def run(self):
        self._root_window.mainloop()

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        self._redraw()

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        click_point = point.from_pixel(
            event.x, event.y, width, height)

        move = self._model_state.handle_click(click_point)
        if move is not None:
            self._game_state.move(move)
            self._redraw()

    def _redraw(self):
        self._canvas.delete(tkinter.ALL)
        self._load_discs()
        for disc in self._model_state.discs:
            self._draw_disc(disc)
        for line in self._model_state.row_lines:
            self._draw_line('H', line)
        for line in self._model_state.col_lines:
            self._draw_line('V', line)

    def _draw_line(self, orientation: str, line: int):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        if orientation == 'H':
            y = line * canvas_height
            self._canvas.create_line(0, y, canvas_width, y)
        elif orientation == 'V':
            x = line * canvas_width
            self._canvas.create_line(x, 0, x, canvas_height)

    def _draw_disc(self, disc: OthelloGameModel.Disc):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        center_x, center_y = disc.center_point.pixel(canvas_width, canvas_height)

        radius_x = disc.radius_frac * canvas_width
        radius_y = disc.radius_frac * canvas_height

        self._canvas.create_oval(
            center_x - radius_x, center_y - radius_y,
            center_x + radius_x, center_y + radius_y,
            fill=disc.fill, outline='#c0cde0')

    def _load_discs(self):
        board = self._game_state.board
        for piece in board.list_of_pieces():
            row, col = piece.location
            row_frac = float(1 + row * 2) / float(board.rows * 2)
            col_frac = float(1 + col * 2) / float(board.columns * 2)
            center_point = point.from_frac(row_frac, col_frac)
            self._model_state.add_disc(center_point, piece)


def main():
    game_state = GameState('FULL', 16, 16, 'B', 'B', '>')
    rows = game_state.board.rows
    columns = game_state.board.columns
    model_state = OthelloGameModel.ModelState(rows, columns)
    OthelloGameApplication(game_state, model_state).run()

if __name__ == '__main__':
    main()
