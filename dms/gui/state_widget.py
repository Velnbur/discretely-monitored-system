from tkinter import ttk


class StateWidget(ttk.Widget):
    """Tkinter widget that has changeable state"""

    def next_state(self):
        """Change state to next one"""
        raise NotImplementedError()
