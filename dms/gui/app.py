import enum
import tkinter as tk
from tkinter import ttk

import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from dms.gui.notebook import CounterNotebook
from dms.gui.state_widget import StateWidget
from dms.model import ModelConfig, MonitoredModel

from .frames.model_initialization import ModelInitializationFrame
from .frames.monitor_points import MonitorInputPointsFrame
from .frames.results import ResultsFrame
from .frames.space import SpaceInputFrame


class AppState(enum.Enum):
    DATA_INPUT = 1
    RESULTS = 2


class Application(tk.Frame, StateWidget):
    config: ModelConfig
    state: AppState

    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.config = ModelConfig()
        self.state = AppState.DATA_INPUT

        self.notebook = CounterNotebook(self)
        self.notebook.pack(pady=10, expand=True)

        # ''' Задати модель '''
        model_init_frame = ModelInitializationFrame(self.config, self.notebook)
        model_init_frame.pack(fill="both", expand=True)
        self.notebook.add(model_init_frame, text="Задати модель")

        # ''' Просторова область'''
        space_frame = SpaceInputFrame(self.config, self.notebook)
        space_frame.pack(fill="both", expand=True)
        self.notebook.add(space_frame, text="Просторова область")

        #''' Точки спостережень  '''
        monitor_inputs = MonitorInputPointsFrame(self.config, self.notebook)
        monitor_inputs.pack(fill="both", expand=True)
        self.notebook.add(monitor_inputs, text="Точки спостережень")

        #''' Моделюючі функції '''

        # ''' Результати '''
        results = ResultsFrame(self.config, self.notebook)
        results.pack(fill="both", expand=True)
        self.notebook.add(results, text="Результати")

    def next_state(self):
        if self.state == AppState.DATA_INPUT:
            self.state = AppState.RESULTS

            self.notebook.destroy()

            self.__plot_results()
        else:
            raise ValueError(f"Unknown state: {self.state}")

    def __plot_results(self):
        model = MonitoredModel(self.config)

        figure = Figure(figsize=(6, 4), dpi=100)

        # create FigureCanvasTkAgg object
        figure_canvas = FigureCanvasTkAgg(figure, self)

        # create the toolbar
        NavigationToolbar2Tk(figure_canvas, self)

        # create axes
        axes = figure.add_subplot(projection="3d")

        z = [model.y(x, t) for x, t in zip(model.xi_m0, model.ti_m0)]

        print(z)

        axes.scatter(
            model.xi_m0,
            model.ti_m0,
            z,
            label="Початкові точки",
        )
        axes.set_title("Top 5 Programming Languages")
        axes.set_ylabel("Popularity")

        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
