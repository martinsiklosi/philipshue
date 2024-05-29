import os
import platform
from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait

from lights import get_lights, Light, turn_on_all, turn_off_all
from screen import screen_rgb_stripes, screen_rgb_cubes
from rgb import brighten_rgb


TRANSITION_TIME_MS = 400
BRIGHTNESS_FACTOR = 1.5
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


def main() -> None:
    suitible_lights, unsuitible_lights = get_suitible_and_unsuitible_lights()
    turn_on_all(suitible_lights)
    turn_off_all(unsuitible_lights)

    while True:
        rgb_values = screen_rgb_stripes(len(suitible_lights))
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
