import Asym_Cryptographer
import Sym_Cryptographer
from tkinter import *

def switchSymmetric(root: Tk):
    Sym_Cryptographer.main(root)

def switchAsymmetric(root: Tk):
    Asym_Cryptographer.main(root)


def main():
    root = Tk()

    menubar = Menu(root)
    dropdownMenu = Menu(menubar, tearoff=0)
    dropdownMenu.add_command(label='Symmetric', command=lambda: switchSymmetric())
    dropdownMenu.add_command(label='Asymmetric', command=lambda: switchAsymmetric())
    menubar.add_cascade(label='Mode', menu=dropdownMenu)
    root.config(menu=menubar)

    root.mainloop()

if __name__ == '__main__':
    main()
