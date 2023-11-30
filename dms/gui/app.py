import enum
import numpy as np
import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib import cm


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

        x = np.linspace(model.config.A, model.config.B, num=100)
        y = np.linspace(0, model.config.T, num=100)

        x, y = np.meshgrid(x, y)

        both_fig = plt.figure(0)
        both_axes = both_fig.add_subplot(111, projection="3d")

        found_fig = plt.figure(
            1,
        )
        axes = found_fig.add_subplot(111, projection="3d")

        z = np.array([model.y(x, t) for x, t in zip(x, y)])

        axes.plot_surface(x, y, z, label="Початкові точки", cmap=cm.coolwarm)
        both_axes.plot_surface(x, y, z, label="Початкові точки", cmap=cm.coolwarm)

        expected_fig = plt.figure(2)
        axes = expected_fig.add_subplot(111, projection="3d")

        z = np.array([model.y_xt(x, t) for x, t in zip(x, y)])

        axes.plot_surface(x, y, z, label="Крайові точки", cmap=cm.coolwarm)
        both_axes.plot_surface(x, y, z, label="Початкові точки", cmap=cm.coolwarm)

        plt.show()
