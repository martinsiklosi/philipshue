import os
import json
from collections.abc import Iterable


import colour
import requests
from dotenv import load_dotenv


load_dotenv()
BRIDGE_IP = os.getenv("BRIDGE_IP")
USERNAME = os.getenv("USERNAME")
BASE_URL = url = f"http://{BRIDGE_IP}/api/{USERNAME}"


class Light:
    def __init__(self, nr: int) -> None:
        self.nr = nr
        self.supports_rgb = self._supports_rgb()

    def _supports_rgb(self) -> bool:
        state = self.get_state()["state"]
        return "hue" in state

    def get_state(self) -> dict:
        url = BASE_URL + f"/lights/{self.nr}"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()

    def _convert_time_kwargs(self, kwargs: dict) -> dict:
        if "time_ms" in kwargs:
            kwargs["transitiontime"] = kwargs["time_ms"] // 100
            del kwargs["time_ms"]
        if "time_s" in kwargs:
            kwargs["transitiontime"] = round(kwargs["time_s"]*10)
            del kwargs["time_s"]
        return kwargs

    def _convert_color_kwargs(self, kwargs: dict) -> dict:
        if "rgb" in kwargs:
            kwargs["xy"] = rgb_to_xy(kwargs["rgb"])
            kwargs["bri"] = rgb_to_bri(kwargs["rgb"])
            del kwargs["rgb"]
        return kwargs

    def _convert_kwargs(self, kwargs: dict) -> dict:
        kwargs = self._convert_time_kwargs(kwargs)
        kwargs = self._convert_color_kwargs(kwargs)
        return kwargs

    def set_state(self, **kwargs) -> dict:
        kwargs = self._convert_kwargs(kwargs)
        url = BASE_URL + f"/lights/{self.nr}/state"
        res = requests.put(url, data=json.dumps(kwargs))
        res.raise_for_status()
        return res.json()


def get_bridge_state() -> dict:
    res = requests.get(BASE_URL)
    res.raise_for_status()
    return res.json()


def get_lights() -> list[Light]:
    bridge_state = get_bridge_state()
    light_items = bridge_state["lights"].items()
    lights = [Light(i)
              for i, light in light_items
              if light["state"]["reachable"]]
    return lights


def rgb_to_xy(rgb: Iterable) -> tuple[int, int]:
    rgb_normalized = [x / 255.0 for x in rgb]
    xyz = colour.sRGB_to_XYZ(rgb_normalized)
    xy = colour.XYZ_to_xy(xyz)
    return tuple(xy)


def rgb_to_bri(rgb: Iterable) -> int:
    return max(rgb)
