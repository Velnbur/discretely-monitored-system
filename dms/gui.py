from tkinter import *
from tkinter import Button
from tkinter import ttk


class Interface:
    def __init__(self) -> None:
        self.window = Tk()
        self.selected_values = []

        self.window.geometry("700x700")

        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(pady=10, expand=True)

        self.frame1 = ttk.Frame(self.notebook, width=600, height=580)
        self.frame2 = ttk.Frame(self.notebook, width=600, height=580)
        self.frame3 = ttk.Frame(self.notebook, width=600, height=580)
        self.frame4 = ttk.Frame(self.notebook, width=600, height=580)

        label1 = Label(
            self.frame1,
            text="Оберіть диференціальний оператор L(x): ",
            font=("Arial", 14),
        )
        label1.grid(row=1, columnspan=2, padx=10, pady=10)

        l_choices = ["diff(diff(y,x), x) + diff(diff(y,t), t)"]
        l_entry = ttk.Combobox(
            self.frame1, values=l_choices, font=("Arial", 14), height=5
        )
        l_entry.grid(row=1, column=5, padx=10, pady=10)

        label2 = Label(
            self.frame1, text="Оберіть функцію Гріна G(x,t): ", font=("Arial", 14)
        )
        label2.grid(row=3, columnspan=2, padx=10, pady=10)

        g_choices = ["(1/(2*pi))*log(1/((x-x_)**2+(t-t_)**2))"]
        g_entry = ttk.Combobox(
            self.frame1, values=g_choices, font=("Arial", 14), height=5
        )
        g_entry.grid(row=3, column=5, padx=10, pady=10)

        label3 = Label(
            self.frame1, text="Оберіть функцію стану y(x,t): ", font=("Arial", 14)
        )
        label3.grid(row=5, columnspan=2, padx=10, pady=10)

        y_choices = ["5*sin(x/5)+ 4*cos(t/4)"]
        y_entry = ttk.Combobox(
            self.frame1, values=y_choices, font=("Arial", 14), height=5
        )
        y_entry.grid(row=5, column=5, padx=10, pady=10)

        label4 = Label(
            self.frame1,
            text="Оберіть зовнішньо-динамічне збурення u(x,t): ",
            font=("Arial", 14),
        )
        label4.grid(row=7, columnspan=2, padx=10, pady=10)

        u_choices = ["-0.2*sin(x/5) - 0.25*cos(t/4)"]
        u_entry = ttk.Combobox(
            self.frame1, values=u_choices, font=("Arial", 14), height=5
        )
        u_entry.grid(row=7, column=5, padx=10, pady=10)

        button = Button(
            self.frame1,
            text="Зберегти та перейти далі",
            font=("Arial", 14),
            bg="#E1FAE1",
        )
        button.grid(row=9, columnspan=20, padx=10, pady=10)

        # ''' Просторова область'''

        label_t = Label(
            self.frame2, text="Час закінчення процесу T:", font=("Arial", 14)
        )
        label_t.grid(row=0, column=0, padx=10, pady=10)

        t_choices = ["50", "60"]
        t_entry = ttk.Combobox(
            self.frame2, values=t_choices, font=("Arial", 14), height=5
        )
        t_entry.grid(row=0, column=10, padx=10, pady=10)

        label_x = Label(
            self.frame2, text="Проміжок, якому належить x", font=("Arial", 14)
        )
        label_x.grid(row=1, column=0)

        label_a = Label(self.frame2, text="Введіть A: ", font=("Arial", 14))
        label_a.grid(row=2, column=0)

        A_choices = ["50", "60"]
        A_entry = ttk.Combobox(
            self.frame2, values=A_choices, font=("Arial", 14), height=5
        )
        A_entry.grid(row=2, column=10, padx=10, pady=10)

        label_b = Label(self.frame2, text="Введіть B: ", font=("Arial", 14))
        label_b.grid(row=3, column=0)

        B_choices = ["50", "60"]
        B_entry = ttk.Combobox(
            self.frame2, values=B_choices, font=("Arial", 14), height=5
        )
        B_entry.grid(row=3, column=10, padx=10, pady=10)

        button2 = Button(
            self.frame2,
            text="Зберегти та перейти далі",
            font=("Arial", 14),
            bg="#E1FAE1",
        )
        button2.grid(row=4, columnspan=20, padx=10, pady=10)

        #''' Точки спостережень  '''
        label_init = Label(self.frame3, text="Початкові умови", font=("Agbalumo", 14))
        label_init.grid(row=0, column=0)

        label_iamount = Label(self.frame3, text="Кількість:", font=("Arial", 13))
        label_iamount.grid(row=1, column=0)

        self.initial_amount = StringVar()
        amount_entry = Spinbox(
            self.frame3,
            from_=0,
            to=5,
            textvariable=self.initial_amount,
            font=("Arial", 14),
        )
        amount_entry.grid(row=1, column=10, padx=10, pady=10)

        button_init = Button(self.frame3, text="Ok", command=self.initial_points)
        button_init.grid(row=1, column=14)

        # Краєві умови

        label_boundary = Label(self.frame3, text="Краєві умови", font=("Agbalumo", 14))
        label_boundary.grid(row=9, column=0)

        label_bamount = Label(self.frame3, text="Кількість:", font=("Arial", 13))
        label_bamount.grid(row=10, column=0)

        self.boundary_amount = StringVar()
        amount_entry = Spinbox(
            self.frame3,
            from_=0,
            to=5,
            textvariable=self.boundary_amount,
            font=("Arial", 14),
        )
        amount_entry.grid(row=10, column=10, padx=10, pady=10)

        button_bound = Button(self.frame3, text="Ok", command=self.boundary_points)
        button_bound.grid(row=10, column=14)

        save_button = Button(
            self.frame3, text="Зберегти та перейти далі", command=self.save_value
        )
        save_button.grid(row=17, columnspan=12, padx=10, pady=10)
        #''' Моделюючі функції '''

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack(fill="both", expand=True)
        self.frame3.pack(fill="both", expand=True)
        self.frame4.pack(fill="both", expand=True)

        self.notebook.add(self.frame1, text="Задати модель")
        self.notebook.add(self.frame2, text="Просторово-часова область")
        self.notebook.add(self.frame3, text="Точки спостережень")
        self.notebook.add(self.frame4, text="Моделюючі функції")

    def run(self) -> None:
        self.window.mainloop()

    def boundary_points(self) -> None:
        a = self.boundary_amount.get()
        label_x = Label(self.frame3, text="x: ", font=("Arial", 13))
        label_x.grid(row=11, column=3)
        for i in range(int(a)):
            b_choices = ["1", "2"]
            varb = StringVar()
            b_entry = ttk.Combobox(
                self.frame3,
                textvariable=varb,
                values=b_choices,
                font=("Arial", 14),
                height=5,
            )
            b_entry.grid(row=11 + i, column=10, padx=10, pady=10)

            varb.trace_add(
                "write",
                lambda *args, index=i, var=varb: self.save_value(
                    index, var.get(), *args
                ),
            )

    def initial_points(self):
        a = self.initial_amount.get()
        label_x = Label(self.frame3, text="x: ", font=("Arial", 13))
        label_x.grid(row=3, column=3)

        for i in range(int(a)):
            x_choices = ["1", "2"]
            var = StringVar()
            x_entry = ttk.Combobox(
                self.frame3,
                textvariable=var,
                values=x_choices,
                font=("Arial", 14),
                height=5,
            )
            x_entry.grid(row=3 + i, column=10, padx=10, pady=10)

            var.trace_add(
                "write",
                lambda *args, index=i, var=var: self.save_value(index, var.get()),
            )

    def save_value(self, index, value):
        self.selected_values.insert(index, value)
        print(self.selected_values)


if __name__ == "__main__":
    interface = Interface()
    interface.run()
