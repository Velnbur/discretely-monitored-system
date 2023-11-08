from tkinter import *
from tkinter import Button
from tkinter import ttk

window = Tk()

window.geometry("700x700")

notebook = ttk.Notebook(window)
notebook.pack(pady=10, expand=True)

frame1 = ttk.Frame(notebook, width=600, height=580)
frame2 = ttk.Frame(notebook, width=600, height=580)
frame3 = ttk.Frame(notebook, width=600, height=580)
frame4 = ttk.Frame(notebook, width=600, height=580)

label1 = Label(frame1, text="Оберіть диференціальний оператор L(x): ", font=("Arial", 14))
label1.grid(row=1, columnspan=2, padx = 10, pady = 10)

l_choices = ['diff(diff(y,x), x) + diff(diff(y,t), t)']
l_entry = ttk.Combobox(frame1, values=l_choices, font=("Arial", 14), height=5)
l_entry.grid(row=1, column=5, padx = 10, pady = 10)

label2 = Label(frame1, text="Оберіть функцію Гріна G(x,t): ", font=("Arial", 14))
label2.grid(row=3, columnspan=2, padx = 10, pady = 10)

g_choices = ['(1/(2*pi))*log(1/((x-x_)**2+(t-t_)**2))']
g_entry = ttk.Combobox(frame1, values=g_choices, font=("Arial", 14), height=5)
g_entry.grid(row=3, column=5, padx = 10, pady = 10)

label3 = Label(frame1, text="Оберіть функцію стану y(x,t): ", font=("Arial", 14))
label3.grid(row=5, columnspan=2, padx = 10, pady = 10)

y_choices = ['5*sin(x/5)+ 4*cos(t/4)']
y_entry = ttk.Combobox(frame1, values=y_choices, font=("Arial", 14), height=5)
y_entry.grid(row=5, column=5, padx = 10, pady = 10)

label4 = Label(frame1, text="Оберіть зовнішньо-динамічне збурення u(x,t): ", font=("Arial", 14))
label4.grid(row=7, columnspan=2, padx = 10, pady = 10)

u_choices = ['-0.2*sin(x/5) - 0.25*cos(t/4)']
u_entry = ttk.Combobox(frame1, values=u_choices, font=("Arial", 14), height=5)
u_entry.grid(row=7, column = 5, padx = 10, pady = 10)

button = Button(frame1, text = 'Зберегти та перейти далі', font=("Arial", 14), bg = '#E1FAE1')
button.grid(row = 9, columnspan = 20, padx = 10, pady = 10)

#''' Просторова область'''

label_t = Label(frame2, text='Час закінчення процесу T:', font=("Arial", 14))
label_t.grid(row=0, column=0, padx = 10, pady = 10)

t_choices = ['50','60']
t_entry = ttk.Combobox(frame2, values = t_choices, font=("Arial", 14), height=5)
t_entry.grid(row = 0, column=10, padx = 10, pady = 10)

label_x = Label(frame2,text="Проміжок, якому належить x", font=("Arial", 14))
label_x.grid(row = 1,column=0)

label_a = Label(frame2,text="Введіть A: ", font=("Arial", 14))
label_a.grid(row=2,column=0)

A_choices = ['50','60']
A_entry = ttk.Combobox(frame2, values = A_choices, font=("Arial", 14), height=5)
A_entry.grid(row = 2, column=10, padx = 10, pady = 10)

label_b = Label(frame2,text="Введіть B: ", font=("Arial", 14))
label_b.grid(row=3,column=0)

B_choices = ['50','60']
B_entry = ttk.Combobox(frame2, values = B_choices, font=("Arial", 14), height=5)
B_entry.grid(row = 3, column=10, padx = 10, pady = 10)

button2 = Button(frame2, text = 'Зберегти та перейти далі', font=("Arial", 14), bg = '#E1FAE1')
button2.grid(row = 4, columnspan = 20, padx = 10, pady = 10)

#''' Точки спостережень  '''
label_init = Label(frame3, text = 'Початкові умови', font=("Arial", 14))
label_init.grid(row = 0, column=0)

label_iamount = Label(frame3, text = 'Кількість:', font=("Arial", 14))
label_iamount.grid(row = 1, column= 0)

amount_choices = ['1', '2', '3', '4', '5']
amount_entry = ttk.Combobox(frame3, values = amount_choices, font=("Arial", 14), height=5)
amount_entry.grid(row = 1, column=10, padx = 10, pady = 10)


#''' Моделюючі функції '''

frame1.pack(fill='both', expand=True)
frame2.pack(fill='both', expand=True)
frame3.pack(fill='both', expand=True)
frame4.pack(fill='both', expand=True)

notebook.add(frame1, text='Задати модель')
notebook.add(frame2, text='Просторово-часова область')
notebook.add(frame3, text='Точки спостережень')
notebook.add(frame4, text='Моделюючі функції')

window.mainloop()