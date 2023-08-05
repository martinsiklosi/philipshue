from collections.abc import Iterable

import colour


def rgb_to_xy(rgb: Iterable[int]) -> tuple[int, int]:
    rgb_normalized = [x / 255.0 for x in rgb]
    xyz = colour.sRGB_to_XYZ(rgb_normalized)
    xy = colour.XYZ_to_xy(xyz)
    return tuple(xy)


def rgb_to_bri(rgb: Iterable[int]) -> int:
    return max(rgb)


def brighten_rgb(rgb: Iterable[int], factor: float) -> tuple[int, int, int]:
    # To fix color change due to my rgb_to_bri implementation
    max_factor = max(rgb) / 255
    factor = min(factor, max_factor)

    brightened_rgb = [round(factor*val)
                      for val in rgb]
    cut_rgb = [max(0, min(255, val))
               for val in brightened_rgb]
    return tuple(cut_rgb)
