import Tkinter as tk
import glob
import sys
from gui.gui_builder import UI as CUI
from gui.line_drawer import UI as LUI
from utils.data_utils import b8_to_ndarray, write_overlay, line_drawer
from utils.logger import LogFactory

if __name__ == "__main__":
    try:
        assert len(sys.argv) > 1
    except AssertionError as e:
        raise(AssertionError("Give the root of the files as the input arg."))

    root = tk.Tk()
    log_engine = LogFactory(sys.argv[1])
    file_path = log_engine.get_pending_files_list()
    root.title(
        "labelMe: A simple python tool for labling b8 images")

    UI = LUI(root=root,
             file_paths=file_path,
             reader_callback=b8_to_ndarray,
             overlay_callback=line_drawer,
             logger=log_engine)
    root.mainloop()
