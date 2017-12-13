import Tkinter as tk
from PIL import Image, ImageTk
import tkFont
import numpy as np
import tkMessageBox


class UI():

    def __init__(self, root, file_paths, reader_callback, overlay_callback):
        # Properties
        self.IMG_SIZE = IMAGE_SIZE
        self.root = root
        self.frame_idx = 0
        self.file_idx = 0
        self.file_paths = file_paths
        self.reader = reader_callback
        self.overlayer = overlay_callback
        self.curr_file = self.load_curr_b8()
        self.is_saved = False
        # Point initializer

        self.seq_points = np.zeros((len(self.curr_file), 2))
        self.init_top_point = self.curr_file.shape[2] / 2
        self.init_bottom_point = self.curr_file.shape[2] / 2
        self._set_seq_points(self.init_top_point, self.init_bottom_point)
        self.point_status = "Top"

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

        self.toggle_button = tk.Button(
            self.bottom_frame, text="Toggle Top/Bottom", font=self.button_font, command=self.toggle_callback)
        self.toggle_button.grid(row=1, column=1)

        self.point_status_label = tk.Label(
            self.bottom_frame, text="Top", font=self.label_font)
        self.status_label_color = 'blue'
        # Row three
        self.prev_scan_button = tk.Button(
            self.bottom_frame, text="<< Prev scan", font=self.button_font, command=self.prev_scan_callback)
        self.prev_scan_button.grid(row=2, column=0, padx=150, pady=20)

        self.save_label_button = tk.Button(
            self.bottom_frame, text="Save labels", font=self.button_font, command=self.save_label_callback)
        self.save_label_button.grid(row=2, column=1)

        self.clear_label_button = tk.Button(
            self.bottom_frame, text="Reset labels", font=self.button_font, command=self.clear_label_callback)
        self.clear_label_button.grid(row=2, column=2, padx=150, pady=20)

        self.bottom_frame.pack(side='top', fill='none', expand=True)

        # Key bindings
        self.root.bind('<Right>', self.next_frame_callback)
        self.root.bind('<Left>', self.prev_frame_callback)
        self.root.bind('<Up>', self.move_point_right_callback)
        self.root.bind('<Down>', self.move_point_left_callback)
        self.root.bind('<Control-Up>', self.move_point_right_fast_callback)
        self.root.bind('<Control-Down>', self.move_point_left_fast_callback)

        self.root.bind('<Shift-Right>', self.next_frame_override_callback)
        self.root.bind('<Shift-Left>', self.prev_frame_override_callback)
        self.root.bind('<F1>', self.help_generator_callback)
        self.refresh()

    def help_generator_callback(self, event):
        tkMessageBox.showinfo("Hotkey Help",
                              "Right/left:\tframe navigation\n" +
                              "Shift+(Right/left):\tframe navigation with\t\t\tlabel override\n" +
                              "Up/down:\tmove point\n" +
                              "CTRL+(up/down):\tmove point fast")

    def refresh(self):
        # Update image
        curr_frame = self.curr_file[self.frame_idx].astype('uint8')
        p1 = (int(self.seq_points[self.frame_idx][0]), 0)
        p2 = (int(self.seq_points[self.frame_idx][1]),
              int(curr_frame.shape[0]))
        curr_frame = self.overlayer(curr_frame, p1, p2)
        img = ImageTk.PhotoImage(
            Image.fromarray(curr_frame).resize(self.IMG_SIZE, Image.ANTIALIAS))
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
        # Update the toggle label
        self.point_status_label.config(
            text=self.point_status, foreground=self.status_label_color)
        self.point_status_label.grid(row=1, column=2)

    def prev_frame_override_callback(self, event):
        if self.frame_idx - 1 > -1:
            cached_idx = self.frame_idx
            self.frame_idx -= 1
            top = self.seq_points[cached_idx][0]
            bottom = self.seq_points[cached_idx][1]
            self._set_seq_points(top_point=top,
                                 bottom_point=bottom,
                                 start_idx=self.frame_idx,
                                 direction=-1)

    def next_frame_override_callback(self, event):
        if self.frame_idx + 1 < len(self.curr_file):
            cached_idx = self.frame_idx
            self.frame_idx += 1
            top = self.seq_points[cached_idx][0]
            bottom = self.seq_points[cached_idx][1]
            self._set_seq_points(top_point=top,
                                 bottom_point=bottom,
                                 start_idx=self.frame_idx,
                                 direction=1)
            self.refresh()

    def move_point_left_callback(self, event):
        if self.point_status == "Top":
            if self.seq_points[self.frame_idx][0] - 1 > -1:
                self.seq_points[self.frame_idx][0] -= 1
        if self.point_status == "Bottom":
            if self.seq_points[self.frame_idx][1] - 1 > -1:
                self.seq_points[self.frame_idx][1] -= 1
        self.refresh()

    def move_point_right_callback(self, event):
        if self.point_status == "Top":
            if self.seq_points[self.frame_idx][0] + 1 < self.curr_file[self.frame_idx].shape[1]:
                self.seq_points[self.frame_idx][0] += 1
        if self.point_status == "Bottom":
            if self.seq_points[self.frame_idx][1] + 1 < self.curr_file[self.frame_idx].shape[1]:
                self.seq_points[self.frame_idx][1] += 1
        self.refresh()

    def move_point_left_fast_callback(self, event):
        if self.point_status == "Top":
            if self.seq_points[self.frame_idx][0] - 10 > -1:
                self.seq_points[self.frame_idx][0] -= 10
        if self.point_status == "Bottom":
            if self.seq_points[self.frame_idx][1] - 10 > -1:
                self.seq_points[self.frame_idx][1] -= 10
        self.refresh()

    def move_point_right_fast_callback(self, event):
        if self.point_status == "Top":
            if self.seq_points[self.frame_idx][0] + 10 < self.curr_file[self.frame_idx].shape[1]:
                self.seq_points[self.frame_idx][0] += 10
        if self.point_status == "Bottom":
            if self.seq_points[self.frame_idx][1] + 10 < self.curr_file[self.frame_idx].shape[1]:
                self.seq_points[self.frame_idx][1] += 10
        self.refresh()

    def toggle_callback(self):
        if self.point_status == 'Top':
            self.point_status = 'Bottom'
            self.status_label_color = 'red'
        else:
            self.point_status = 'Top'
            self.status_label_color = 'blue'
        self.refresh()

    def next_frame_callback(self, event):
        if self.frame_idx + 1 < len(self.curr_file):
            self.frame_idx += 1
            self.refresh()

    def prev_frame_callback(self, event):
        if self.frame_idx - 1 > -1:
            self.frame_idx -= 1
            self.refresh()

    def next_scan_callback(self):
        var = True
        if not self.is_saved:
            var = tkMessageBox.askyesno(
                "Warning!", "The annotations were not saved. Do you want to proceed to the next sequence?")
        if var:
            if self.file_idx + 1 < len(self.file_paths):
                self.file_idx += 1
                self.frame_idx = 0
                self.curr_file = self.load_curr_b8()
                self.seq_points = np.zeros((len(self.curr_file), 2))
                self.init_top_point = self.curr_file.shape[2] / 2
                self.init_bottom_point = self.curr_file.shape[2] / 2
                self._set_seq_points(
                    self.init_top_point, self.init_bottom_point)
                self.is_saved = False
                self.refresh()

    def prev_scan_callback(self):
        var = True
        if not self.is_saved:
            var = tkMessageBox.askyesno(
                "Warning!", "The annotations were not saved. Do you want to proceed to the next sequence?")
        if var:
            if self.file_idx - 1 > -1:
                self.file_idx -= 1
                self.frame_idx = 0
                self.curr_file = self.load_curr_b8()
                self.seq_points = np.zeros((len(self.curr_file), 2))
                self.init_top_point = self.curr_file.shape[2] / 2
                self.init_bottom_point = self.curr_file.shape[2] / 2
                self._set_seq_points(
                    self.init_top_point, self.init_bottom_point)
                self.is_saved = False
                self.refresh()

    def start_midline_callback(self):
        self.start_idx = self.frame_idx

    def end_midline_callback(self):
        self.end_idx = self.frame_idx

    def clear_label_callback(self):
        self.curr_file = self.load_curr_b8()
        self.seq_points = np.zeros((len(self.curr_file), 2))
        self.init_top_point = self.curr_file.shape[2] / 2
        self.init_bottom_point = self.curr_file.shape[2] / 2
        self._set_seq_points(self.init_top_point, self.init_bottom_point)

        self.refresh()

    def save_label_callback(self):
        self.is_saved = True
        np.save(self.file_paths[self.file_idx].split('.')[0] +
                '_centerLines.npy', self.seq_points)
        print "{}".format(self.file_idx + 1) + " Saved " + self.file_paths[self.file_idx]

    def load_curr_b8(self):
        return self.reader(self.file_paths[self.file_idx])

    def _set_seq_points(self, top_point, bottom_point, start_idx=0, direction=1):
        if direction == 1:
            self.seq_points[start_idx:] = [top_point, bottom_point]
        else:
            self.seq_points[:start_idx] = [top_point, bottom_point]
