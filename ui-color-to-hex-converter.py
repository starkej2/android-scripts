#!/usr/bin/env python3
#
# This script converts a UIColor to an equivalent HEX representation
# Expects input formatted like this: [UIColor colorWithRed:1.000 green:1.000 blue:1.000 alpha:1.000]

SPACE_CHAR = " "
MAX_COLOR_VALUE = 255
MAX_ALPHA_IN_HEX = "ff"

UI_COLOR_RED_PREFIX = "red:"
UI_COLOR_GREEN_PREFIX = "green:"
UI_COLOR_BLUE_PREFIX = "blue:"
UI_COLOR_ALPHA_PREFIX = "alpha:"


def _find_attribute(ui_color_string, prefix):
    start_index = ui_color_string.find(prefix) + len(prefix)
    end_index = ui_color_string.find(SPACE_CHAR, start_index)
    return ui_color_string[start_index: end_index]


def _get_red(ui_color_string):
    return float(_find_attribute(ui_color_string, UI_COLOR_RED_PREFIX))


def _get_green(ui_color_string):
    return float(_find_attribute(ui_color_string, UI_COLOR_GREEN_PREFIX))


def _get_blue(ui_color_string):
    return float(_find_attribute(ui_color_string, UI_COLOR_BLUE_PREFIX))


def _get_alpha(ui_color_string):
    return float(_find_attribute(ui_color_string, UI_COLOR_ALPHA_PREFIX))


def _convert_to_hex(ui_color_value):
    rgb_value = int(round(ui_color_value * MAX_COLOR_VALUE))
    return '{0:02x}'.format(rgb_value)


def main():
    while True:
        ui_color_input = input("Enter UIColor definition: ").lower()

        red_hex_value = _convert_to_hex(_get_red(ui_color_input))
        green_hex_value = _convert_to_hex(_get_green(ui_color_input))
        blue_hex_value = _convert_to_hex(_get_blue(ui_color_input))
        alpha_hex_value = _convert_to_hex(_get_alpha(ui_color_input))

        full_hex = red_hex_value + green_hex_value + blue_hex_value if alpha_hex_value == MAX_ALPHA_IN_HEX \
            else alpha_hex_value + red_hex_value + green_hex_value + blue_hex_value

        print("HEX representation: #{hex}".format(hex=full_hex))


main()
