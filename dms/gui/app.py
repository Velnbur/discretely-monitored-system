import tkinter as tk
from tkinter import ttk
from dms.model import ModelConfig

from .frames.model_initialization import ModelInitializationFrame
from .frames.space import SpaceInputFrame
from .frames.monitor_points import MonitorInputPointsFrame
from .frames.results import ResultsFrame


class Application(tk.Frame):
    config: ModelConfig

    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.window = parent

        self.config = ModelConfig()

        self.notebook = ttk.Notebook(self.window)
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
