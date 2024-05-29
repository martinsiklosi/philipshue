from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait

from lights import get_lights, Light, turn_on_all, turn_off_all
from screen import screen_rgb_stripes, screen_rgb_cubes
from rgb import brighten_rgb


TRANSITION_TIME_MS = 400
ADD_DELAY_MS = 400
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


def set_light_state(light: Light,
                    rgb_value: tuple[int, int, int],
                    brightness_factor: float,
                    trans_time_ms: int,
                    ) -> None:
    rgb_value = brighten_rgb(rgb=rgb_value, factor=brightness_factor)
    res = light.set_state(rgb=rgb_value, time_ms=trans_time_ms)
    print(res)


def main() -> None:
    suitible_lights, unsuitible_lights = get_suitible_and_unsuitible_lights()
    turn_on_all(suitible_lights)
    turn_off_all(unsuitible_lights)

    while True:
        rgb_values = screen_rgb_stripes(len(suitible_lights))
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for light, rgb_value in zip(suitible_lights, rgb_values):
                futures.append(executor.submit(set_light_state,
                                            light,
                                            rgb_value,
                                            BRIGHTNESS_FACTOR,
                                            TRANSITION_TIME_MS))
            wait(futures)
            sleep(ADD_DELAY_MS / 1000)

if __name__ == "__main__":
    main()
