import tkinter as tk
from dms.model import ModelConfig

from .consts import DEFAULT_FONT, DEFAULT_FRAME_HEIGHT, DEFAULT_FRAME_WIDTH


class ResultsFrame(tk.Frame):
    """Tkinter frame for showing results of the model"""

    config: ModelConfig

    def __init__(self, config_ref: ModelConfig, parent=None) -> None:
        tk.Frame.__init__(
            self, parent, width=DEFAULT_FRAME_HEIGHT, height=DEFAULT_FRAME_WIDTH
        )

        self.parent = parent
        self.config = config_ref

        results_label = tk.Label(
            self,
            text="Результати моделювання:",
            font=DEFAULT_FONT,
            bg = 'white'
        )
        results_label.grid(row=0, column=0)

        self.value_label = tk.Label(
            self,
            text="Значення",
            font=DEFAULT_FONT,
        )
        self.value_label.grid(row=1, column=0)

        show_button = tk.Button(
            self,
            text="Показати результати",
            font=DEFAULT_FONT,
            bg="#E1FAE1",
            command=self.__show_results,
        )
        show_button.grid(row=2, column=0)
        
        
        label = tk.Label(self, text= 'Після натискання на "Показати результати" починається проведення розрахунків,\n після чого в новому вікні виводиться графік функції стану системи,\n а також початкові та крайові спостереження', font=DEFAULT_FONT, bg = 'white')
        label.grid(row=3, column=0, padx=10, pady=15)

    def __show_results(self):
        print(f"Showing results: {self.config}")

        if self.parent is not None:
            self.parent.forget(self)
