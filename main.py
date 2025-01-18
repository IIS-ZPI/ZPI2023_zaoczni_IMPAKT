import tkinter as tk
from interface import Interface
from action_handler import ActionHandler
from plotter import Plotter


def main():
    def on_closing():
        root.quit()
        root.destroy() 

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    plotter = Plotter()
    action_handler = ActionHandler(plotter)
    ui = Interface(root, action_handler)

    action_handler.set_interface(ui)

    root.mainloop()

if __name__ == "__main__":
    main()