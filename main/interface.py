from tkinter import *


class CalcInterface:
    def __init__(self, message):
        window = Tk()
        window.title("Janela")
        window.geometry("500x600")

        label1 = Label(window, text="Hello", font=("Arial Bold", 50)).grid(row=2, column=0)
        Entry().grid(row=0, column=0)
        Button(text="Olá").grid(row=1, column=0)
        window.mainloop()
