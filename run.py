from gui.gui_builder import UI
from utils.data_utils import b8_to_ndarray, write_overlay
import Tkinter as tk
import glob
import sys

if __name__ == "__main__":
    try:
        assert len(sys.argv) > 1
    except AssertionError as e:
        raise(AssertionError("Give the root of the files as the input arg."))

    root = tk.Tk()
    file_path = glob.glob(sys.argv[1] + "/**/*.b8")
    root.title(
        "labelMe: A simple python tool for labling b8 images for classification")
    UI = UI(root, file_path, b8_to_ndarray, write_overlay)
    root.mainloop()
