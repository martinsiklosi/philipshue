from time import sleep
from concurrent.futures import ThreadPoolExecutor, wait

from lights import get_lights, Light
from screen import screen_rgb_stripes, screen_rgb_cubes
from rgb import brighten_rgb

lights = get_lights()
rgb_lights = []
white_lights = []
for light in lights:
    if light.supports_rgb:
        rgb_lights.append(light)
    else:
        white_lights.append(light)

for light in white_lights:
    light.set_state(on=False)

for light in rgb_lights:
    light.set_state(on=True)

trans_time_ms = 2000
add_delay_ms = 0
brightness_factor = 1.5


def set_light_state(light: Light,
                    rgb_value: tuple[int, int, int],
                    brightness_factor: float,
                    trans_time_ms: int,
                    ) -> None:
    rgb_value = brighten_rgb(rgb=rgb_value, factor=brightness_factor)
    light.set_state(rgb=rgb_value, time_ms=trans_time_ms)


while True:
    rgb_values = screen_rgb_stripes(len(rgb_lights))
    with ThreadPoolExecutor() as executor:
        futures = []
        for light, rgb_value in zip(rgb_lights, rgb_values):
            futures.append(executor.submit(set_light_state,
                                           light,
                                           rgb_value,
                                           brightness_factor,
                                           trans_time_ms))
        wait(futures)
        sleep(add_delay_ms / 1000)
