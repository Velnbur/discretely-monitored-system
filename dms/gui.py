from tkinter import *
from tkinter import Button
from tkinter import ttk


import tkinter as tk
from tkinter import ttk


class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.selected_values = []

        self.window.geometry("700x700")
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(pady=10, expand=True)

        self.create_frame(
            "Задати модель",
            [
                (
                    "Оберіть диференціальний оператор L(x): ",
                    ["diff(diff(y,x), x) + diff(diff(y,t), t)"],
                ),
                (
                    "Оберіть функцію Гріна G(x,t): ",
                    ["(1/(2*pi))*log(1/((x-x_)**2+(t-t_)**2))"],
                ),
                ("Оберіть функцію стану y(x,t): ", ["5*sin(x/5)+ 4*cos(t/4)"]),
                (
                    "Оберіть зовнішньо-динамічне збурення u(x,t): ",
                    ["-0.2*sin(x/5) - 0.25*cos(t/4)"],
                ),
            ],
            [("Зберегти та перейти далі", self.next_tab)],
        )

        self.create_frame(
            "Просторово-часова область",
            [
                ("Час закінчення процесу T:", ["50", "60"]),
                (
                    "Проміжок, якому належить x",
                    [("Введіть A: ", ["50", "60"]), ("Введіть B: ", ["50", "60"])],
                ),
            ],
            [("Зберегти та перейти далі", self.next_tab)],
        )

        self.create_frame(
            "Точки спостережень",
            [
                ("Початкові умови", [("Кількість:", "initial_points")]),
                ("Краєві умови", [("Кількість:", "boundary_points")]),
            ],
            [("Ok", "save_points"), ("Зберегти та перейти далі", self.next_tab)],
        )

    def create_frame(self, tab_name, labels_entries, buttons):
        frame = ttk.Frame(self.notebook, width=600, height=580)
        frame.pack(fill="both", expand=True)
        self.notebook.add(frame, text=tab_name)

        for i, (label_text, entry_choices) in enumerate(labels_entries):
            label = tk.Label(frame, text=label_text, font=("Arial", 14))
            label.grid(row=i * 2, columnspan=2, padx=10, pady=10)

            if isinstance(entry_choices, list):
                entry = ttk.Combobox(
                    frame, values=entry_choices, font=("Arial", 14), height=5
                )
                entry.grid(row=i * 2, column=5, padx=10, pady=10)
            else:
                entry = Spinbox(
                    frame, from_=0, to=5, textvariable=entry_choices, font=("Arial", 14)
                )
                entry.grid(row=i * 2, column=10, padx=10, pady=10)

        for button_text, command in buttons:
            button = tk.Button(
                frame,
                text=button_text,
                font=("Arial", 14),
                bg="#E1FAE1",
                command=command,
            )
            button.grid(row=len(labels_entries) * 2, columnspan=20, padx=10, pady=10)

    def next_tab(self):
        current_tab = self.notebook.index(tk.CURRENT)
        next_tab = current_tab + 1 if current_tab < 3 else 0
        self.notebook.select(next_tab)

    def boundary_points(self):
        self.create_points("x: ", "b_choices", "save_value")

    def initial_points(self):
        self.create_points("x: ", "x_choices", "save_value")

    def create_points(self, label_text, entry_choices_var, trace_command):
        a = tk.StringVar()
        label_x = tk.Label(
            self.notebook.winfo_children()[2], text=label_text, font=("Arial", 13)
        )
        label_x.grid(row=3, column=3)
        for i in range(int(a.get())):
            choices_var = tk.StringVar()
            entry = ttk.Combobox(
                self.notebook.winfo_children()[2],
                textvariable=choices_var,
                values=["1", "2"],
                font=("Arial", 14),
                height=5,
            )
            entry.grid(row=3 + i, column=10, padx=10, pady=10)

            choices_var.trace_add(
                "write",
                lambda *args, index=i, var=choices_var: self.save_value(
                    index, var.get(), *args
                ),
            )

    def save_value(self, index, value, *args):
        self.selected_values.insert(index, value)
        print(self.selected_values)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    interface = Interface()
    interface.run()


if __name__ == "__main__":
    interface = Interface()
    interface.run()
