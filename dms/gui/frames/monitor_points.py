"""Frame for inputing monitor points in as lits of floats"""

import tkinter as tk
from tkinter import ttk
from typing import List, Tuple, Callable

from dms.model import ModelConfig

from .consts import DEFAULT_FONT, DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH


class MonitorInputPointsFrame(tk.Frame):
    """Tkinter frame for inputing monitor points in as lits of floats"""

    initial_points_number: tk.IntVar
    selected_initial_points_x: List[float]
    selected_initial_points_t: List[float]

    boundary_points_number: tk.IntVar
    selected_boundary_points_x: List[float]
    selected_boundary_points_t: List[float]

    config: ModelConfig

    def __init__(self, config_ref: ModelConfig, parent=None) -> None:
        tk.Frame.__init__(
            self, parent, width=DEFAULT_FRAME_HEIGHT, height=DEFAULT_FRAME_WIDTH
        )

        self.parent = parent
        self.config = config_ref

        self.initial_points_number = tk.IntVar()
        self.selected_initial_points_x = []
        self.selected_initial_points_t = []
        self.boundary_points_number = tk.IntVar()
        self.selected_boundary_points_x = []
        self.selected_boundary_points_t = []

        self.__add_input_entry(
            row=1,
            column=1,
            text="Кількість початкових точок:",
            var=self.initial_points_number,
            lists=(self.selected_initial_points_x, self.selected_initial_points_t),
        )

        self.__add_input_entry(
            row=10,
            column=1,
            text="Кількість крайових точок:",
            var=self.boundary_points_number,
            lists=(self.selected_boundary_points_x, self.selected_boundary_points_t),
        )

        save_button = tk.Button(
            self,
            text="Зберегти та перейти далі",
            font=DEFAULT_FONT,
            command=self.__store_initial_points,
        )
        save_button.grid(row=22, column=2)

    def __add_input_entry(
        self,
        row: int,
        column: int,
        text: str,
        var: tk.IntVar,
        lists: Tuple[List[float], List[float]],
    ) -> None:
        """Add entry to the frame"""

        label = tk.Label(self, text=text, font=DEFAULT_FONT)
        label.grid(row=row, columnspan=2, padx=10, pady=10)

        label_amount = tk.Label(self, text="Кількість:", font=DEFAULT_FONT)
        label_amount.grid(row=row + 1, column=column)

        amount_entry = ttk.Spinbox(
            self,
            from_=0,
            to=10,
            textvariable=var,
            font=DEFAULT_FONT,
        )
        amount_entry.grid(row=row + 1, column=column + 1, padx=10, pady=10)

        ok_button = tk.Button(
            self,
            text="Ok",
            command=self.__create_points_input_entries_callback(row, var, lists),
        )
        ok_button.grid(row=row + 1, column=column + 2)

    def __create_points_input_entries_callback(
        self, row: int, variable: tk.IntVar, lists: Tuple[List[float], List[float]]
    ) -> Callable[[], None]:
        """Create input entries for points"""

        def inner():
            points_number = variable.get()

            self.__create_column_list(
                text=f"x:",
                row_index=row + 3,
                column=0,
                rows=points_number,
                list=lists[0],
            )

            self.__create_column_list(
                text=f"t:",
                row_index=row + 3,
                column=2,
                rows=points_number,
                list=lists[1],
            )

        return inner

    def __create_column_list(
        self,
        text: str,
        row_index: int,
        column: int,
        rows: int,
        list: List[float],
    ) -> None:
        for index in range(rows):
            label = tk.Label(self, text=text, font=DEFAULT_FONT)
            label.grid(row=row_index + index, column=column)

            variable = tk.DoubleVar()

            entry = ttk.Entry(
                self,
                textvariable=variable,
                font=DEFAULT_FONT,
            )
            entry.grid(row=row_index + index, column=column + 1, padx=10, pady=10)
            entry.bind(
                "<Return>",
                func=MonitorInputPointsFrame.__store_point_in_list_callback(
                    index, variable, list
                ),
            )

    @staticmethod
    def __store_point_in_list_callback(
        index: int, value: tk.DoubleVar, list: List[float]
    ) -> Callable[[], None]:
        """Store point in list"""

        def inner():
            list[index] = value.get()

        return inner

    def __store_initial_points(self) -> None:
        """Store selected initial points into config"""

        if (num := self.initial_points_number.get()) != 0:
            self.config.M0 = num

        if (num := self.boundary_points_number.get()) != 0:
            self.config.Mg = self.boundary_points_number.get()

        if len(self.selected_initial_points_x) != 0:
            self.config.xi_m0 = self.selected_initial_points_x

        if len(self.selected_initial_points_t) != 0:
            self.config.ti_m0 = self.selected_initial_points_t

        if len(self.selected_boundary_points_x) != 0:
            self.config.xi_mg = self.selected_boundary_points_x

        if len(self.selected_boundary_points_t) != 0:
            self.config.ti_mg = self.selected_boundary_points_t

        print(f"Updated config: {self.config}")

        if self.parent is not None:
            self.parent.forget(self)
