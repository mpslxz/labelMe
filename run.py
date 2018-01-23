import Tkinter as tk
import glob
import sys
import argparse
from gui.gui_builder import UI as CUI
from gui.line_drawer import UI as LUI
from utils.data_utils import b8_to_ndarray, write_overlay, line_drawer
from utils.logger import LogFactory

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-r', '--root_dir', nargs=1, required=True)
    ap.add_argument('-l', '--normal_line', action='store_true')
    opts = ap.parse_args()

    root = tk.Tk()
    log_engine = LogFactory(opts.root_dir[0])
    file_path = log_engine.get_pending_files_list()
    root.title(
        "labelMe: A simple python tool for labling b8 images")
    line_mode = 'vertical'
    if opts.normal_line:
        line_mode = 'normal'
    UI = LUI(root=root,
             file_paths=file_path,
             reader_callback=b8_to_ndarray,
             overlay_callback=line_drawer,
             logger=log_engine, line_mode=line_mode)
    root.mainloop()
