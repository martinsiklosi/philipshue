import os
import platform
from time import sleep
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, wait

from lights import get_lights, Light, turn_on_all, turn_off_all
from screen import sample_colors_from_screen
from rgb import brighten_rgb


TRANSITION_TIME_MS = 800
BRIGHTNESS_FACTOR = 1.2
MAX_WORKERS = 16


def get_suitible_and_unsuitible_lights() -> tuple[list[Light], list[Light]]:
    lights = get_lights()
    suitible_lights = []
    unsuitible_lights = []
    for light in lights:
        if light.is_from_ikea or not light.supports_rgb:
            unsuitible_lights.append(light)
        else:
            suitible_lights.append(light)
    return suitible_lights, unsuitible_lights


def set_light_state(
    light: Light,
    rgb_value: tuple[int, int, int],
    trans_time_ms: int,
) -> None:
    light.set_state(rgb=rgb_value, time_ms=trans_time_ms)


def clear_terminal() -> None:
    current_os = platform.system()
    if current_os == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def print_state(lights: list[Light], rgb_values: list[tuple[int, int, int]]) -> None:
    clear_terminal()
    print(f"{TRANSITION_TIME_MS = }")
    print(f"{BRIGHTNESS_FACTOR = }")
    print(f"{MAX_WORKERS = }")
    print()
    for light, rgb_value in zip(lights, rgb_values):
        print(f"{light.name.lower()} = {rgb_value}")


@contextmanager
def restore_original_state():
    all_lights = get_lights()
    all_states = [light.get_state()["state"] for light in all_lights]
    try:
        yield
    finally:
        for light, state in zip(all_lights, all_states):
            light.set_state(**state)


def main() -> None:
    with restore_original_state():
        suitible_lights, unsuitible_lights = get_suitible_and_unsuitible_lights()
        turn_on_all(suitible_lights)
        turn_off_all(unsuitible_lights)

        while True:
            rgb_values = sample_colors_from_screen(len(suitible_lights))
            rgb_values = [
                brighten_rgb(rgb_value, BRIGHTNESS_FACTOR) for rgb_value in rgb_values
            ]
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = []
                for light, rgb_value in zip(suitible_lights, rgb_values):
                    futures.append(
                        executor.submit(
                            set_light_state, light, rgb_value, TRANSITION_TIME_MS
                        )
                    )
                wait(futures)
            print_state(suitible_lights, rgb_values)
            sleep(TRANSITION_TIME_MS / 1000)


if __name__ == "__main__":
    main()
