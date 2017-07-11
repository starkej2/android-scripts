#!/usr/bin/env python
#
# This script converts a UIColor to an equivalent HEX representation
# Expects input formatted like this: [UIColor colorWithRed:1.000 green:1.000 blue:1.000 alpha:1.000]

SPACE_CHAR = " "
MAX_COLOR_VALUE = 255


def find_attribute(ui_color_string, prefix):
    start_index = ui_color_string.find(prefix) + len(prefix)
    end_index = ui_color_string.find(SPACE_CHAR, start_index)
    return ui_color_string[start_index: end_index]


def get_red(ui_color_string):
    return float(find_attribute(ui_color_string, "red:"))


def get_green(ui_color_string):
    return float(find_attribute(ui_color_string, "green:"))


def get_blue(ui_color_string):
    return float(find_attribute(ui_color_string, "blue:"))


def get_alpha(ui_color_string):
    return float(find_attribute(ui_color_string, "alpha:"))


def convert_to_hex(ui_color_value):
    rgb_value = int(round(ui_color_value * MAX_COLOR_VALUE))
    return '{0:02x}'.format(rgb_value)


while True:
    ui_color_input = raw_input("Enter UIColor definition: ").lower()

    red_hex_value = convert_to_hex(get_red(ui_color_input))
    green_hex_value = convert_to_hex(get_green(ui_color_input))
    blue_hex_value = convert_to_hex(get_blue(ui_color_input))
    alpha_hex_value = convert_to_hex(get_alpha(ui_color_input))

    print "HEX representation: #{hex}".format(
        hex=red_hex_value + green_hex_value + blue_hex_value if alpha_hex_value == "ff"
        else alpha_hex_value + red_hex_value + green_hex_value + blue_hex_value)