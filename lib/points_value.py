# coding=utf-8


def points_value(points_value):
    try:
        points_value = str(points_value)
        points_value = points_value.split("last", 1)[1]
        points_value = points_value.split(":")[1]
        points_value = points_value.split("}")[0]
        points_value = float(points_value)
        points_value = "%.2f" % points_value
        return points_value
    except (ValueError, IndexError):
        return "Brak danych"


def pins(pin):
    if float(pin) >= 100:
        font_colour = "red"
        icon = "remove-sign"
    elif 50 < float(pin) < 100:
        font_colour = "orange"
        icon = "ok-sign"
    elif 1 < float(pin) < 50:
        font_colour = "green"
        icon = "ok-sign"
    elif float(pin) == 0.0:
        font_colour = "red"
        icon = "exclamation-sign"
    else:
        font_colour = "green"
        icon = "ok-sign"
    return font_colour, icon


def map_pins(value1, value2):
    if float(value1) >= 100 or float(value2) >= 100:
        icon = "remove-sign"
        icon_colour = "red"
    elif 50 < float(value1) < 100 or 50 < float(value2) < 100:
        icon = "ok-sign"
        icon_colour = "orange"
    elif float(value1) == 0.0 and float(value2) == 0.0:
        icon_colour = "red"
        icon = "exclamation-sign"
    else:
        icon = "ok-sign"
        icon_colour = "green"
    return icon, icon_colour
