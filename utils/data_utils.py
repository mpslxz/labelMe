import cv2
import numpy as np
from scipy.misc import imresize


def b8_to_ndarray(filename, resize_to=None):
    header_size = 19
    header = {}
    with open(filename, 'r') as b8_file:
        head_element = np.fromfile(b8_file, np.int32, header_size)
        header['file_type'] = head_element[0]
        header['nb_frames'] = head_element[1]
        header['width'] = head_element[2]
        header['height'] = head_element[3]
        width = resize_to[1] if resize_to is not None else header['width']
        height = resize_to[0] if resize_to is not None else header['height']
        frames = np.ndarray((header['nb_frames'], height, width))

        for frame in range(header['nb_frames']):
            f = np.fromfile(b8_file,
                            np.uint8, header['width'] * header['height']).reshape((header['height'], header['width']))
            f = f if resize_to is None else imresize(f, resize_to)
            frames[frame, :,:] = f
    return frames


def write_overlay(frames, results):
    review_frames = []
    for ind, frame in enumerate(frames):
        if results[ind] == 1:  # midline
            shape = np.zeros((75, 75))
            for i in range(75):
                for j in range(75):
                    if -j + i > 40 and -j + i < 50:
                        shape[i, j] = 1
                    if i + 1.5 * j > 115 and i + 1.5 * j < 126:
                        shape[i, j] = 1
        else:  # left
            shape = np.zeros((75, 75))
            for i in range(75):
                for j in range(75):
                    if -j + i > -5 and i - j < 5:
                        shape[i, j] = 1
                    if i + j > 70 and i + j < 80:
                        shape[i, j] = 1

        mask = np.zeros(frame.shape)
        mask[50:50 + shape.shape[0], 50:50 + shape.shape[1]] = shape
        mask_inv = (1 - mask).astype(np.uint8)
        mask = (255 * mask).astype(np.uint8)

        frame *= mask_inv
        frame += mask
        review_frames.append(frame)
    return np.asarray(review_frames)


def line_drawer(img, p1, p2):

    return cv2.line(img, p1, p2, (255, 0, 0))
