import tkinter as tk
from tkinter import ttk
from gui import SistemaGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x350")    
    app = SistemaGUI(root)
    root.mainloop()
