from tkinter import *


class CalcInterface:
    def __init__(self):
        window = Tk()
        window.title("Janela")
        window.geometry("500x600")

        # text1 = Label(window, text="Hello", font=("Arial Bold", 50)).grid(row=2, column=0)
        # Entry().grid(row=0, column=0)
        # Button(text="Olá").grid(row=1, column=0)
        def show():
            myLabel = Label(window, text=clicked.get())

        clicked = StringVar()
        clicked.set("Monday")
        drop = OptionMenu(window, clicked, "Monday", "Tuesday", "Wednesday")
        drop.config(width=20)
        drop.pack()

        myButton = Button(window, text="Show selection", command=show).pack()

        window.mainloop()



