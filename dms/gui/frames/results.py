import tkinter as tk

from dms.model import ModelConfig, MonitoredModel

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
            text="Результати моделювання",
            font=DEFAULT_FONT,
        )
        results_label.grid(row=1, column=2)

        self.value_label = tk.Label(
            self,
            text="Значення",
            font=DEFAULT_FONT,
        )
        self.value_label.grid(row=2, column=1)

        show_button = tk.Button(
            self,
            text="Показати результати",
            font=DEFAULT_FONT,
            command=self.__show_results,
        )
        show_button.grid(row=22, column=2)

    def __show_results(self):
        print(f"Showing results: {self.config}")
        model = MonitoredModel(self.config)

        u = model.solve()
        self.value_label["text"] = f"Значення: {u}"
