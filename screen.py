from mss import mss
import numpy as np


def avg_screen_rgb(segments: int = 1) -> list[tuple[int, int, int]]:
    with mss() as sct:
        screen = np.array(sct.grab(sct.monitors[0]))
        # Dropping the alpha channel if present
        screen = screen[..., 2::-1]
        segment_width = screen.shape[1] // segments
        segment_rgb_list = []
        for i in range(segments):
            segment = screen[:, i * segment_width: (i + 1) * segment_width, :]
            average_color = segment.mean(axis=(0, 1))
            segment_rgb_list.append(tuple(map(int, average_color)))
        return segment_rgb_list
