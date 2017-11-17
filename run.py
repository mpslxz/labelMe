from gui.gui_builder import UI
from utils.data_utils import b8_to_ndarray, write_overlay
import Tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    file_path = ['tamg_sweep.b8', 'tamb_sweep.b8']

    UI = UI(root, file_path, b8_to_ndarray, write_overlay)
    root.mainloop()
