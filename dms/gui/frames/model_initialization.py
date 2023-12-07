"""Module that describes tkinter frame for initialization of monitored model parameters"""

import tkinter as tk
from tkinter import ttk
from typing import List, Optional

from dms.model import ModelConfig

from .consts import DEFAULT_FONT, DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH


class ModelInitializationFrame(tk.Frame):
    """Tkinter frame for initialization of monitored model parameters"""

    l_operator: tk.StringVar

    g_function: tk.StringVar
    y_function: tk.StringVar
    u_function: tk.StringVar

    config: ModelConfig

    DEFAULT_L_OPERATOR_CHOICES = ["diff(diff(y,x), x) + diff(diff(y,t), t)"]
    DEFAULT_G_FUNCTION_CHOICES = ["(1/(2*pi))*log(1/((x)**2+(t)**2))"]
    DEFAULT_Y_FUNCTION_CHOICES = ["5*sin(x/5)+ 4*cos(t/4)"]

    def __init__(self, config_ref: ModelConfig, parent=None) -> None:
        tk.Frame.__init__(
            self, parent, width=DEFAULT_FRAME_HEIGHT, height=DEFAULT_FRAME_WIDTH
        )
        label = tk.Label(
            self,
            text="Визначимо математичну модель процесу:",
            font=DEFAULT_FONT,
            bg="white",
        )
        label.grid(row=1, column=0, padx=10, pady=10)

        self.parent = parent
        self.config = config_ref
        self.l_operator = tk.StringVar()
        self.g_function = tk.StringVar()
        self.y_function = tk.StringVar()

        self.__add_input_entry(
            row=3,
            column=5,
            text="Оберіть функцію Гріна G(x,t): ",
            var=self.g_function,
            choices=self.DEFAULT_G_FUNCTION_CHOICES,
        )

        label1 = tk.Label(
            self, text="Введемо функцію стану системи:", font=DEFAULT_FONT, bg="white"
        )
        label1.grid(row=4, column=0, padx=10, pady=10)

        self.__add_input_entry(
            row=5,
            column=5,
            text="Оберіть функцію y(x,t): ",
            var=self.y_function,
            choices=self.DEFAULT_Y_FUNCTION_CHOICES,
        )

        label2 = tk.Label(
            self,
            text="Спостереження за системою та моделюючі функції є дискретними",
            font=DEFAULT_FONT,
            bg="white",
        )
        label2.grid(row=8, column=0, columnspan=5, padx=1, pady=10)

        self.__add_input_entry(
            row=7,
            column=5,
            text="Оберіть оператор L(y): ",
            var=self.l_operator,
            choices=self.DEFAULT_L_OPERATOR_CHOICES,
        )

        save_button = tk.Button(
            self,
            text="Зберегти та перейти далі",
            font=DEFAULT_FONT,
            bg="#E1FAE1",
            command=self.__update_config_callback,
        )
        save_button.grid(row=9, columnspan=20, padx=10, pady=10)

    def __add_input_entry(
        self,
        row: int,
        column: int,
        text: str,
        var: tk.StringVar,
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

        # def inner(entry):
        #     var.set(entry.get())

        # entry.bind("<Return>", lambda event, entry=entry: inner(entry))

    def __update_config_callback(self) -> None:
        """Update config callback"""

        if self.y_function.get() != "":
            self.config.y = self.y_function.get()

        if self.g_function.get() != "":
            self.config.g = self.g_function.get()

        print(f"Updating config: {self.config}")

        if self.parent is not None:
            self.parent.forget(self)
