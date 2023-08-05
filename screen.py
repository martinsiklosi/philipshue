from mss import mss
import numpy as np


# def screen_rgb_stripes(n: int) -> list[tuple[int, int, int]]:
#     with mss() as sct:
#         screen = np.array(sct.grab(sct.monitors[0]))
#         # Dropping the alpha channel if present
#         screen = screen[..., 2::-1]
#         segment_width = screen.shape[1] // n
#         segment_rgb_list = []
#         for i in range(n):
#             segment = screen[:, i * segment_width: (i + 1) * segment_width, :]
#             average_color = segment.mean(axis=(0, 1))
#             segment_rgb_list.append(tuple(map(int, average_color)))
#         return segment_rgb_list


def screen_rgb_stripes(n: int) -> list[tuple[int, int, int]]:
    with mss() as sct:
        screen = np.array(sct.grab(sct.monitors[0]))
        # Dropping the alpha channel if present
        screen = screen[..., 2::-1]

        # Calculate the coordinates to crop to a 4:3 aspect ratio
        height, width, _ = screen.shape
        new_width = min(width, int(height * 4 / 3))
        new_height = min(height, int(width * 3 / 4))
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height

        # Crop the screen to the 4:3 ratio
        screen = screen[top:bottom, left:right, :]

        segment_width = screen.shape[1] // n
        segment_rgb_list = []
        for i in range(n):
            segment = screen[:, i * segment_width: (i + 1) * segment_width, :]
            average_color = segment.mean(axis=(0, 1))
            segment_rgb_list.append(tuple(map(int, average_color)))
        return segment_rgb_list


def screen_rgb_cubes(n: int) -> list[tuple[int, int, int]]:
    with mss() as sct:
        screen = np.array(sct.grab(sct.monitors[0]))
        screen = screen[..., 2::-1]
        h, w, _ = screen.shape
        cube_height, cube_width = h // 16, w // 8
        cubes = screen[:cube_height*16, :cube_width *
                       8].reshape(16, cube_height, 8, cube_width, 3)
        mean_colors = cubes.mean(axis=(1, 3)).astype(int)
        all_colors = [tuple(color) for color in mean_colors.reshape(-1, 3)]

        # Find the largest step that will return at least n colors
        step = len(all_colors) // n if len(all_colors) >= n else 1

        return all_colors[::step]
