from mss import mss
import numpy as np


def screen_locations(n: int, h: int, w: int, buffer: int) -> list[tuple[int, int]]:
    rng = np.random.default_rng(seed=n + h + w)
    random_h = rng.integers(low=buffer, high=h - buffer, size=n)
    random_w = rng.integers(low=buffer, high=w - buffer, size=n)
    coordinates = [(int(x), int(y)) for x, y in zip(random_h, random_w)]
    return coordinates


def sample_colors_from_screen(n: int) -> list[tuple[int, int, int]]:
    with mss() as sct:
        screen = np.array(sct.grab(sct.monitors[0]))
        screen = screen[..., 2::-1]

    h, w, _ = screen.shape
    radius = min(h, w) // 10
    coordinates = screen_locations(n=n, h=h, w=w, buffer=radius)

    colors = []
    for x, y in coordinates:
        pixels = screen[x - radius : x + radius, y - radius : y + radius]
        color = np.mean(pixels, axis=(0, 1))
        colors.append(color)

    return colors