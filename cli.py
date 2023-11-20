from dms.gui.app import Application
import tkinter as tk


def main():
    root = tk.Tk()
    root.geometry("700x700")

    Application(root)

    root.mainloop()


if __name__ == "__main__":
    main()
