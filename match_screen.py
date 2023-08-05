from time import sleep

from lights import get_lights
from screen import avg_screen_rgb
from rgb import brighten_rgb

# Get lights
lights = get_lights()
rgb_lights = []
white_lights = []
for light in lights:
    if light.supports_rgb:
        rgb_lights.append(light)
    else:
        white_lights.append(light)

# Turn on RGB lights
for light in white_lights:
    light.set_state(on=False)

for light in rgb_lights:
    light.set_state(on=True)

# Loop
trans_time_ms = 700
add_delay_ms = 100
brightness_factor = 2
while True:
    rgb_values = avg_screen_rgb(segments=len(rgb_lights))
    for light, rgb_value in zip(rgb_lights, rgb_values):
        rgb_value = brighten_rgb(rgb=rgb_value, factor=brightness_factor)
        light.set_state(rgb=rgb_value, time_ms=trans_time_ms)
        sleep(add_delay_ms / 1000)
