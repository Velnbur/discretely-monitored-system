from tkinter import ttk

from dms.gui.state_widget import StateWidget


class CounterNotebook(ttk.Notebook):
    tabs_counter: int = 0
    master: StateWidget

    def __init__(self, master: StateWidget, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tabs_counter = 0
        self.master = master

    def add(self, child, **kw):
        super().add(child, **kw)
        self.tabs_counter += 1

    def forget(self, child):
        super().forget(child)
        self.tabs_counter -= 1

        if self.tabs_counter == 0:
            self.master.next_state()
