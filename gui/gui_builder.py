import Tkinter as tk
from PIL import Image, ImageTk
import tkFont
import numpy as np


class UI():

    def __init__(self, root, file_paths, reader_callback, overlay_callback):
        # Properties
        self.IMG_SIZE = (1000, 720)
        self.root = root
        self.frame_idx = 0
        self.file_idx = 0
        self.start_idx = 0
        self.end_idx = 0
        self.file_paths = file_paths
        self.reader = reader_callback
        self.overlayer = overlay_callback
        self.curr_file = self.load_curr_b8()

        # Top frame
        self.top_frame = tk.Frame(self.root)
        self.panel = tk.Label(self.top_frame)
        self.panel.grid(row=0)
        self.top_frame.pack(side='top', fill='none', expand=True)

        # Bottom frame
        self.bottom_frame = tk.Frame(root)
        self.label_font = tkFont.Font(family='Helvetica', size=15)

        # Row one
        self.sequence_idx_label = tk.Label(
            self.bottom_frame, text="Sequence NaN", font=self.label_font)

        self.frame_idx_label = tk.Label(
            self.bottom_frame, text="Frame: ", font=self.label_font)
        self.scan_name = tk.Label(
            self.bottom_frame, text="Scan name: ", font=self.label_font)

        # Row two
        self.button_font = tkFont.Font(family='Helvetica', size=13)
        self.next_scan_button = tk.Button(
            self.bottom_frame, text="Next scan >>", font=self.button_font, command=self.next_scan_callback)
        self.next_scan_button.grid(row=1, column=0, padx=150, pady=20)

        self.end_midline_button = tk.Button(
            self.bottom_frame, text="End Mid.", font=self.button_font, command=self.end_midline_callback)
        self.end_midline_button.grid(row=1, column=1)

        self.start_midline_button = tk.Button(
            self.bottom_frame, text="Start Mid.", font=self.button_font, command=self.start_midline_callback)
        self.start_midline_button.grid(row=1, column=2)

        # Row three
        self.prev_scan_button = tk.Button(
            self.bottom_frame, text="<< Prev scan", font=self.button_font, command=self.prev_scan_callback)
        self.prev_scan_button.grid(row=2, column=0, padx=150, pady=20)

        self.save_label_button = tk.Button(
            self.bottom_frame, text="Save labels", font=self.button_font, command=self.save_label_callback)
        self.save_label_button.grid(row=2, column=1)

        self.clear_label_button = tk.Button(
            self.bottom_frame, text="Clear labels", font=self.button_font, command=self.clear_label_callback)
        self.clear_label_button.grid(row=2, column=2, padx=150, pady=20)

        self.bottom_frame.pack(side='top', fill='none', expand=True)

        # Key bindings
        self.root.bind('<Right>', self.next_frame_callback)
        self.root.bind('<Left>', self.prev_frame_callback)
        self.refresh()

    def refresh(self):
        # Update image
        img = ImageTk.PhotoImage(
            Image.fromarray(self.curr_file[self.frame_idx].astype('uint8')).resize(self.IMG_SIZE, Image.ANTIALIAS))
        self.panel.configure(image=img)
        self.panel.image = img

        # Update the sequence label
        self.sequence_idx_label.config(
            text="Sequence {} / {}".format(self.file_idx + 1, len(self.file_paths)))
        self.sequence_idx_label.grid(row=0, column=0)

        # Update the frame label
        self.frame_idx_label.config(
            text="Frame: {} / {}".format(self.frame_idx + 1, len(self.curr_file)))
        self.frame_idx_label.grid(row=0, column=1)

        # Update the scan name
        self.scan_name.config(
            text="Scan name: " + self.file_paths[self.file_idx].split('/')[-1])
        self.scan_name.grid(row=0, column=2)

    def next_frame_callback(self, event):
        if self.frame_idx + 1 < len(self.curr_file):
            self.frame_idx += 1
            self.refresh()

    def prev_frame_callback(self, event):
        if self.frame_idx - 1 > -1:
            self.frame_idx -= 1
            self.refresh()

    def next_scan_callback(self):
        if self.file_idx + 1 < len(self.file_paths):
            self.file_idx += 1
            self.frame_idx = 0
            self.curr_file = self.load_curr_b8()
            self.refresh()

    def prev_scan_callback(self):
        if self.file_idx - 1 > -1:
            self.file_idx -= 1
            self.frame_idx = 0
            self.curr_file = self.load_curr_b8()
            self.refresh()

    def start_midline_callback(self):
        self.start_idx = self.frame_idx

    def end_midline_callback(self):
        self.end_idx = self.frame_idx

    def clear_label_callback(self):
        self.start_idx = 0
        self.end_idx = 0
        self.curr_file = self.load_curr_b8()
        self.refresh()

    def save_label_callback(self):
        labels = np.zeros(len(self.curr_file))

        labels[min(self.start_idx, self.end_idx):
               max(self.start_idx, self.end_idx) + 1] = 1
        np.save(self.file_paths[self.file_idx].split('.')[0] +
                '_midline_labels.npy', labels)
        self.curr_file = self.overlayer(self.curr_file, labels)
        self.refresh()

    def load_curr_b8(self):
        return self.reader(self.file_paths[self.file_idx])
