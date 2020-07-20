from tkinter import *
from loginpage import LoginPage
from config import Setting


root = Tk()
root.title("Fru edit")
root.iconbitmap(r".\tools\fru.ico")
config = Setting()
LoginPage(root, config)
root.mainloop()