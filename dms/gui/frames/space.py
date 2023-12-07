"""Module with frame for inputing time-space parameters of the monitored model"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from .consts import DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH, DEFAULT_FONT
from dms.model import ModelConfig


class SpaceInputFrame(tk.Frame):
    time_end: tk.DoubleVar
    space_start: tk.DoubleVar
    space_end: tk.DoubleVar

    config: ModelConfig

    DEFAULT_TIME_END_CHOICES = ["50", "60"]
    DEFAULT_SPACE_START_CHOICES = ["50"]
    DEFAULT_SPACE_END_CHOICES = ["60"]

    def __init__(self, config_ref: ModelConfig, parent=None) -> None:
        tk.Frame.__init__(
            self, parent, width=DEFAULT_FRAME_HEIGHT, height=DEFAULT_FRAME_WIDTH
        )

        self.parent = parent
        self.config = config_ref

        self.time_end = tk.DoubleVar()
        self.space_start = tk.DoubleVar()
        self.space_end = tk.DoubleVar()

        label = tk.Label(self, text= 'Функціонування процесу починається із нуля та є обмеженим.', font=DEFAULT_FONT, bg = 'white')
        label.grid(row=0, columnspan=2, padx=10, pady=10)


        label = tk.Label(self, text= 'Область одновимірна, то пропонується ввести точки, що є її границям.', font=DEFAULT_FONT, bg = 'white')
        label.grid(row=1, columnspan=2, padx=10, pady=10)
        
        self.__add_input_entry(
            row=2,
            column=10,
            text="Введіть час закінчення процесу T:",
            var=self.time_end,
            choices=self.DEFAULT_TIME_END_CHOICES,
        )

        self.__add_input_entry(
            row=3,
            column=10,
            text="Початок проміжку x",
            var=self.space_start,
            choices=self.DEFAULT_SPACE_START_CHOICES,
        )

        self.__add_input_entry(
            row=4,
            column=10,
            text="Кінець проміжку x",
            var=self.space_end,
            choices=self.DEFAULT_SPACE_END_CHOICES,
        )

        save_button = tk.Button(
            self,
            text="Зберегти та перейти далі",
            font=DEFAULT_FONT,
            bg="#E1FAE1",
            command=self.__update_config_callback,
        )
        save_button.grid(row=5, columnspan=20, padx=10, pady=10)

    def __add_input_entry(
        self,
        row: int,
        column: int,
        text: str,
        var: tk.DoubleVar,
        choices: Optional[List[str]] = None,
    ) -> None:
        """Add entry to the frame"""

        label = tk.Label(self, text=text, font=DEFAULT_FONT)
        label.grid(row=row, columnspan=2, padx=10, pady=10)

        entry = ttk.Combobox(
            self,
            values=choices if choices is not None else [],
            font=DEFAULT_FONT,
            height=5,
            textvariable=var,
        )
        entry.grid(row=row, column=column, padx=10, pady=10)

    def __update_config_callback(self) -> None:
        """Update config callback"""

        if (time_end := self.time_end.get()) != 0:
            self.config.T = time_end

        if (space_start := self.space_start.get()) != 0:
            self.config.A = space_start

        if (space_end := self.space_end.get()) != 0:
            self.config.B = space_end

        print(f"Updated config: {self.config}")

        if self.parent is not None:
            self.parent.forget(self)
