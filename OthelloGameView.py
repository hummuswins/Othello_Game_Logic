import tkinter
import point
from OthelloGameLogic import GameState, InvalidMoveError
import OthelloGameModel

DEFAULT_FONT = ('Helvetica', 14)


def _place_widget(widget: tkinter.Widget, row: int, column: int, columnspan: int,  padx: int, pady: int, sticky: int):
    widget.grid(
        row=row, column=column, columnspan=columnspan, padx=padx, pady=pady,
        sticky=sticky)


class GameDialog:
    def __init__(self):
        self.dialog_window = tkinter.Toplevel()

        self._label_counter = 0
        self._create_label('Please set the game setting: ')

        labels = ['Rules: ', 'Rows: ', 'Columns: ', 'Starting Player: ',
                  'Top Left Corner Piece: ', 'Winning Condition: ',
                  '> is for one with more pieces wins, < is for one with less pieces wins']
        for label in labels:
            self._create_label(label)

        self._rules_var = self._create_vars()
        self._create_menu(self._rules_var, ['FULL', 'SIMPLE'], 1, 1)

        num_options = ['4', '6', '8', '10', '12', '14', '16']

        self._row_var = self._create_vars()
        self._create_menu(self._row_var, num_options, 2, 1)

        self._col_var = self._create_vars()
        self._create_menu(self._col_var, num_options, 3, 1)

        colors = ['Black', 'White']
        self._starting_var = self._create_vars()
        self._create_menu(self._starting_var, colors, 4, 1)

        self._top_left_var = self._create_vars()
        self._create_menu(self._top_left_var, colors, 5, 1)

        self._winning_var = self._create_vars()
        self._create_menu(self._winning_var, ['>', '<'], 6, 1)

        button_frame = tkinter.Frame(master=self.dialog_window)
        _place_widget(button_frame, 8, 0, 2, 10, 10, tkinter.E + tkinter.S)

        ok_button = tkinter.Button(
            master=button_frame, text='OK', font=DEFAULT_FONT,
            command=self._on_ok_button)
        _place_widget(ok_button, 0, 0, 1, 10, 10, tkinter.E)

        self.dialog_window.rowconfigure(3, weight=3)
        self.dialog_window.columnconfigure(1, weight=1)

        self._ok_clicked = False

    def show(self) -> None:
        self.dialog_window.grab_set()
        self.dialog_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def game_settings(self) -> []:
        rules = self._rules_var.get()
        rows = int(self._row_var.get())
        columns = int(self._col_var.get())
        starting = self._starting_var.get()
        top_left = self._top_left_var.get()

        if starting == 'Black':
            starting = 'B'
        else:
            starting = 'W'

        if top_left == 'Black':
            top_left = 'B'
        else:
            top_left = 'W'

        winning = self._winning_var.get()
        return [rules, rows, columns, starting, top_left, winning]

    def _on_ok_button(self) -> None:
        self._ok_clicked = True
        self.dialog_window.destroy()

    def _create_vars(self) -> tkinter.StringVar:
        return tkinter.StringVar(master=self.dialog_window)

    def _create_label(self, label: str) -> None:
        label = tkinter.Label(
            master=self.dialog_window, text=label,
            font=DEFAULT_FONT
        )
        _place_widget(label, self._label_counter, 0, 10, 1, 10, tkinter.W)
        self._label_counter += 1

    def _create_menu(self, var: tkinter.StringVar, menu_list: [str], row: int, col: int):
        var.set(menu_list[0])
        row_menu = tkinter.OptionMenu(
            self.dialog_window, var,
            *menu_list)
        _place_widget(row_menu, row, col, 10, 10, 1, tkinter.E)


class OthelloGameApplication:
    def __init__(self):
        self._root_window = tkinter.Tk()
        self._root_window.withdraw()

        dialog = GameDialog()
        dialog.show()
        while True:
            rules, rows, columns, starting, top_left, winning = dialog.game_settings()
            self._game_state = GameState(rules, rows, columns, starting, top_left, winning)
            if dialog.was_ok_clicked() is True:
                break

        self._model_state = OthelloGameModel.ModelState(
            self._game_state.board.rows, self._game_state.board.columns
        )

        self._canvas = tkinter.Canvas(
            master=self._root_window, width=400, height=400,
            background='#c0cde0'
        )

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)

        self._canvas.grid(
            row=0, column=0, columnspan=2, padx=0, pady=0,
            sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W
        )

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.columnconfigure(0, weight=1)

        self._ok_clicked = False

        self._root_window.update()
        self._root_window.deiconify()

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
            try:
                self._game_state.move(move)
                self._redraw()
            except InvalidMoveError:
                self._error_dialog()

        self._winner_dialog()

    def _redraw(self):
        rule = self._game_state.rule + ' '

        if self._game_state.turn == 1:
            turn = 'Turn: Black\n'
        else:
            turn = 'Turn: White\n'

        game_condition = 'B:' + str(self._game_state.board.black_disc) + \
                         ' W:' + str(self._game_state.board.white_disc)

        label = rule + turn + game_condition
        tk_label = tkinter.Label(master=self._root_window, text=label, font=DEFAULT_FONT)
        _place_widget(tk_label, 1, 0, 1, 0, 0, tkinter.S)

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

        x_distance = int(self._model_state.x_distance * canvas_width)
        y_distance = int(self._model_state.y_distance * canvas_height)

        self._canvas.create_oval(
            center_x - x_distance, center_y - y_distance,
            center_x + x_distance, center_y + y_distance,
            fill=disc.fill, outline='#c0cde0')

    def _load_discs(self):
        board = self._game_state.board
        for piece in board.list_of_pieces():
            row, col = piece.location
            row_frac = float(1 + row * 2) / float(board.rows * 2)
            col_frac = float(1 + col * 2) / float(board.columns * 2)
            center_point = point.from_frac(col_frac, row_frac)
            self._model_state.add_disc(center_point, piece)

    def _winner_dialog(self):
        if self._game_state.ending_condition_met():
            winner_dialog = tkinter.Toplevel()

            winner = tkinter.Label(master=winner_dialog, text='Winner is ' + self._game_state.winner, font=DEFAULT_FONT)
            _place_widget(winner, 0, 0, 1, 20, 20, tkinter.N + tkinter.W + tkinter.E + tkinter.S)

            button_frame = tkinter.Frame(master=winner_dialog)
            _place_widget(button_frame, 1, 0, 1, 10, 10, tkinter.E)

            ok_button = tkinter.Button(master=button_frame, text='OK',
                                       font=DEFAULT_FONT, command=self._root_window.destroy)
            _place_widget(ok_button, 0, 0, 1, 10, 10, tkinter.E)

    def _error_dialog(self):
        error_dialog = tkinter.Toplevel()

        winner = tkinter.Label(master=error_dialog, text='Invalid Move', font=DEFAULT_FONT)
        _place_widget(winner, 0, 0, 1, 20, 20, tkinter.N + tkinter.W + tkinter.E + tkinter.S)

        button_frame = tkinter.Frame(master=error_dialog)
        _place_widget(button_frame, 1, 0, 1, 10, 10, tkinter.E)

        ok_button = tkinter.Button(master=button_frame, text='OK',
                                   font=DEFAULT_FONT, command=error_dialog.destroy)
        _place_widget(ok_button, 0, 0, 1, 10, 10, tkinter.E)


def main():
    game = OthelloGameApplication()
    game.run()

if __name__ == '__main__':
    main()
