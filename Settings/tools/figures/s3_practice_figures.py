"""Draw the S3 learning, question setup, and worked-solution diagrams."""

from pathlib import Path

from svgkit import BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE, MUTED, ORANGE, ORANGE_FILL, Fig


ASSETS = Path(__file__).resolve().parents[2] / "assets" / "S3"


def card(width, height, title, description):
    fig = Fig(width, height, title, description)
    fig.text(24, 29, title, 18, weight="bold")
    return fig


def save(fig, filename):
    fig.save(ASSETS / f"{filename}.svg")


def cylinder(fig, center, reading, bottom=180, maximum=70):
    """Draw the same linear scale in every panel of one comparison."""
    left, right = center - 32, center + 32
    level = bottom - reading * 105 / maximum
    fig.rect(left, level, right - left, bottom - level, BLUE_FILL, "none")
    fig.path(f"M{left},{bottom - 115} V{bottom} H{right} V{bottom - 115}", sw=2)
    for mark in range(10, maximum + 1, 10):
        y = bottom - mark * 105 / maximum
        fig.line(right - 8, y, right, y, MUTED, 1)
    fig.line(left, level, right, level, BLUE, 2)
    fig.text(left - 10, level + 5, f"{reading} mL", 14, BLUE, "end")
    return level


def cube(fig, x, y, side, fill, stroke):
    depth = side * 0.32
    fig.path(f"M{x},{y} l{depth},{-depth} h{side} l{-depth},{depth} Z", fill, stroke)
    fig.path(f"M{x+side},{y} l{depth},{-depth} v{side} l{-depth},{depth} Z", fill, stroke)
    fig.rect(x, y, side, side, fill, stroke)


def displacement():
    fig = card(544, 258, "Measure only the rise",
               "Water reads 35 mL before and 50 mL with the cube submerged. The 15 mL rise is a volume of 15 cubic centimetres.")
    before = cylinder(fig, 174, 35, bottom=186, maximum=60)
    after = cylinder(fig, 376, 50, bottom=186, maximum=60)
    cube(fig, 365, 147, 21, ORANGE_FILL, ORANGE)
    fig.line(208, before, 413, before, MUTED, dash="4 4")
    fig.line(414, after, 449, after, BLUE, dash="4 4")
    fig.path(f"M449,{after} h8 V{before} h-8", stroke=MUTED)
    fig.text(468, (before + after) / 2 + 5, "15 mL", 14, GREEN, weight="bold")
    fig.text(174, 213, "Water alone", 15, anchor="middle")
    fig.text(376, 213, "Same water and cube", 15, anchor="middle")
    fig.text(272, 239, "50 mL − 35 mL = 15 mL, so the cube occupies 15 cm³.", 15, GREEN, "middle")
    save(fig, "learn-displacement")


def density_blocks():
    fig = card(544, 207, "Compare mass at the same volume",
               "Two 10-cubic-centimetre cubes have masses 20 g and 30 g, giving densities of 2 and 3 grams per cubic centimetre.")
    for x, mass, color, fill in ((138, 20, BLUE, BLUE_FILL), (406, 30, ORANGE, ORANGE_FILL)):
        cube(fig, x - 30, 78, 48, fill, color)
        fig.text(x, 152, f"{mass} g in 10 cm³", 16, anchor="middle", weight="bold")
        fig.text(x, 180, f"{mass} ÷ 10 = {mass // 10} g/cm³", 15, color, "middle")
    save(fig, "learn-equal-volume")

    fig = card(512, 209, "Blocks H and J",
               "H and J both occupy 12 cubic centimetres. H has a mass of 42 g; J has a mass of 30 g.")
    for x, name, mass, color, fill in ((144, "H", 42, BLUE, BLUE_FILL), (368, "J", 30, ORANGE, ORANGE_FILL)):
        cube(fig, x - 30, 76, 52, fill, color)
        fig.text(x - 4, 107, name, 19, color, "middle", "bold")
        fig.text(x, 157, f"Mass {mass} g", 16, anchor="middle")
        fig.text(x, 182, "Volume 12 cm³", 15, MUTED, "middle")
    save(fig, "q02-blocks")


def flotation():
    fig = card(560, 223, "Predict the first motion after release",
               "For a fully submerged object, density below the liquid gives rising, equal density allows suspension, and density above the liquid gives sinking.")
    for x, relation, action, direction in [
        (112, "Object less dense", "Rises", -1),
        (280, "Equal densities", "Stays suspended", 0),
        (448, "Object denser", "Sinks", 1),
    ]:
        fig.rect(x - 51, 77, 102, 86, BLUE_FILL, "none")
        fig.path(f"M{x - 51},60 V163 H{x + 51} V60", sw=2)
        fig.line(x - 51, 77, x + 51, 77, BLUE, 2)
        fig.circle(x - 10, 120, 13, ORANGE_FILL, ORANGE, 2)
        if direction:
            fig.line(x + 23, 120, x + 23, 120 + 31 * direction, MUTED, 2, arrow=True)
        else:
            fig.line(x + 15, 120, x + 31, 120, MUTED, 2)
        fig.text(x, 184, relation, 14, anchor="middle")
        fig.text(x, 205, action, 15, anchor="middle", weight="bold")
    save(fig, "learn-float-density")


def temperature():
    fig = card(560, 204, "Temperature, temperature change and heat flow",
               "Sample A cools from 47 to 32 degrees Celsius, a 15 degree drop. At contact, energy flows from the warmer 47-degree object to the cooler 32-degree object.")
    fig.text(26, 59, "One sample, two times", 15, weight="bold")
    fig.text(265, 93, "47 °C  →  32 °C", 19, BLUE, "middle", "bold")
    fig.text(519, 93, "Drop 15 °C", 15, MUTED, "end")
    fig.line(26, 117, 534, 117, LINE)
    fig.text(26, 144, "Two touching objects, same instant", 15, weight="bold")
    fig.text(147, 178, "Warmer 47 °C", 16, ORANGE, "middle")
    fig.line(218, 174, 340, 174, MUTED, 2, arrow=True)
    fig.text(413, 178, "Cooler 32 °C", 16, BLUE, "middle")
    save(fig, "learn-temperature-heat")


def bubble():
    fig = card(552, 223, "Cylinder readings with a trapped bubble",
               "The water starts at 22 mL. With the bead and its attached air bubble fully underwater, the reading is 38 mL.")
    cylinder(fig, 165, 22, maximum=50)
    cylinder(fig, 350, 38, maximum=50)
    fig.circle(350, 157, 13, ORANGE_FILL, ORANGE, 2)
    fig.circle(360, 140, 7, "white", MUTED, 1.5)
    fig.path("M367,137 L407,112 H420", stroke=MUTED)
    fig.text(427, 116, "Air bubble", 14)
    fig.path("M362,159 L410,159 H420", stroke=MUTED)
    fig.text(427, 164, "Bead", 14)
    fig.text(165, 207, "Water alone", 15, anchor="middle")
    fig.text(350, 207, "With bead and bubble", 15, anchor="middle")
    save(fig, "q12-bubble")


def thermometer_cups():
    fig = card(566, 219, "Order in which the thermometer visits the cups",
               "The thermometer starts in 8-degree water, moves to 32-degree water and then moves to 18-degree water.")
    for x, temperature_value, step, color, fill in [
        (118, 8, "Starts here", BLUE, BLUE_FILL),
        (283, 32, "First move", ORANGE, ORANGE_FILL),
        (448, 18, "Second move", BLUE, BLUE_FILL),
    ]:
        fig.rect(x - 39, 103, 78, 56, fill, "none")
        fig.path(f"M{x - 39},87 V159 H{x + 39} V87", sw=2)
        fig.line(x - 39, 103, x + 39, 103, color, 2)
        fig.text(x, 138, f"{temperature_value} °C", 18, color, "middle", "bold")
        fig.text(x, 184, step, 15, anchor="middle")
    for start, end in ((166, 235), (331, 400)):
        fig.line(start, 125, end, 125, MUTED, 2, arrow=True)
    fig.text(283, 207, "Arrows show where the thermometer moves.", 14, MUTED, "middle")
    save(fig, "q17-cup-order")


def cooling_readings():
    minutes = [0, 2, 4, 6, 8, 10]
    readings = [76, 70, 58, 50, 45, 42]
    fig = card(556, 292, "Temperature readings every two minutes",
               "At minutes 0, 2, 4, 6, 8 and 10 the sample measures 76, 70, 58, 50, 45 and 42 degrees Celsius.")
    left, right, top, bottom = 95, 514, 66, 229

    def x(time):
        return left + (right - left) * time / 10

    def y(reading):
        return bottom - (bottom - top) * (reading - 40) / 40

    fig.text(24, 57, "°C", 15, weight="bold")
    for temperature_value in range(40, 81, 10):
        yy = y(temperature_value)
        fig.line(left, yy, right, yy, LINE, 1)
        fig.text(left - 10, yy + 5, temperature_value, 14, MUTED, "end")
    fig.path(f"M{left},{top} V{bottom} H{right}", sw=1.5)
    for minute, reading in zip(minutes, readings, strict=True):
        xx, yy = x(minute), y(reading)
        fig.circle(xx, yy, 5, BLUE, "white", 1.5)
        fig.text(xx + (8 if minute == 0 else 0), yy - 10, reading, 14, BLUE, "middle", "bold")
        fig.text(xx, 252, minute, 14, MUTED, "middle")
    fig.text((left + right) / 2, 275, "Time (minutes)", 15, anchor="middle")
    save(fig, "q18-cooling-readings")

    intervals = list(zip(minutes, minutes[1:]))
    drops = [start - end for start, end in zip(readings, readings[1:])]
    fig = card(530, 236, "Compare each two-minute drop",
               "Drops are 6, 12, 8, 5 and 3 degrees Celsius. The largest drop, 12 degrees Celsius, occurs from 2 to 4 minutes.")
    for index, ((start, end), drop) in enumerate(zip(intervals, drops, strict=True)):
        yy = 52 + index * 33
        largest = drop == max(drops)
        fig.text(26, yy + 16, f"{start}–{end} min", 14)
        fig.rect(119, yy, drop * 25, 22, GREEN_FILL if largest else BLUE_FILL, GREEN if largest else BLUE, rx=4)
        fig.text(130 + drop * 25, yy + 16, f"{drop} °C", 14, GREEN if largest else INK, weight="bold")
    save(fig, "sol18-temperature-drops")


def overflow():
    fig = card(544, 233, "Overflow setup",
               "The chain is fully submerged in the full vessel. Water runs from the spout into a collecting cup marked 12 mL.")
    fig.rect(89, 107, 186, 74, BLUE_FILL, "none")
    fig.path("M89,66 V181 H275 V122 C315,122 337,138 354,157 M275,66 V105 C318,105 349,126 370,155", sw=2)
    fig.line(89, 107, 275, 107, BLUE, 2)
    fig.path("M275,112 C315,113 347,135 361,155", stroke=BLUE, sw=2)
    fig.line(361, 155, 376, 180, BLUE, 2, dash="3 3")
    for index in range(5):
        fig.circle(177 + (index % 2) * 10, 121 + index * 10, 7, "none", INK, 2)
    fig.rect(345, 190, 72, 15, BLUE_FILL, "none")
    fig.path("M345,165 V205 H417 V165", sw=2)
    fig.line(345, 190, 417, 190, BLUE, 2)
    fig.text(430, 194, "12 mL", 15, BLUE, weight="bold")
    fig.text(173, 220, "Full vessel", 15, anchor="middle")
    fig.text(381, 225, "Collecting cup", 14, anchor="middle")
    save(fig, "q20-overflow")


def marbles():
    fig = card(542, 224, "The same cylinder with one marble and with four",
               "One submerged marble takes the reading to 41 mL. Four submerged marbles take it to 56 mL.")
    cylinder(fig, 170, 41)
    cylinder(fig, 376, 56)
    fig.circle(170, 164, 8, ORANGE_FILL, ORANGE, 2)
    for x, y in ((367, 145), (385, 145), (367, 163), (385, 163)):
        fig.circle(x, y, 8, ORANGE_FILL, ORANGE, 2)
    fig.text(170, 209, "1 marble", 15, anchor="middle")
    fig.text(376, 209, "4 equal marbles", 15, anchor="middle")
    save(fig, "q26-marbles")

    fig = card(550, 169, "Recover the water-only reading in two steps",
               "Three extra marbles raise the reading by 15 mL, so one marble displaces 5 mL. Subtracting 5 mL from 41 mL gives 36 mL.")
    for x, width, heading, formula in [
        (24, 238, "1   Find one marble’s volume", "(56 − 41) ÷ 3 = 5 mL"),
        (288, 238, "2   Remove one marble’s rise", "41 − 5 = 36 mL"),
    ]:
        fig.rect(x, 55, width, 87, BLUE_FILL if x == 24 else GREEN_FILL, LINE, rx=9)
        fig.text(x + 13, 84, heading, 15, weight="bold")
        fig.text(x + 13, 114, formula, 17, BLUE if x == 24 else GREEN, weight="bold")
    save(fig, "sol26-marble-steps")


def two_part_float():
    fig = card(549, 207, "A sealed float with two compartments",
               "The smaller compartment occupies 30 cubic centimetres and has mass 36 g. The larger one occupies 70 cubic centimetres and has mass 49 g. The liquid density is 0.90 grams per cubic centimetre.")
    fig.rect(34, 52, 481, 117, BLUE_FILL, BLUE, rx=9)
    fig.text(53, 78, "Liquid density 0.90 g/cm³", 15, BLUE, weight="bold")
    for x, width, volume, mass, fill in [
        (69, 123, 30, 36, ORANGE_FILL),
        (192, 287, 70, 49, GRAY_FILL),
    ]:
        fig.rect(x, 95, width, 54, fill, INK, 1.5)
        fig.text(x + width / 2, 117, f"{volume} cm³", 16, anchor="middle", weight="bold")
        fig.text(x + width / 2, 139, f"{mass} g", 15, anchor="middle")
    fig.text(274, 192, "The two compartment volumes make up the whole outside volume.", 14, MUTED, "middle")
    save(fig, "q29-float-compartments")

    fig = card(560, 203, "Combine totals before taking the ratio",
               "The float has mass 85 g and volume 100 cubic centimetres, giving 0.85 grams per cubic centimetre; this is below the liquid density of 0.90, so the float rises.")
    fig.text(26, 71, "Mass", 15, weight="bold")
    fig.text(148, 71, "36 + 49 = 85 g", 16)
    fig.text(26, 108, "Volume", 15, weight="bold")
    fig.text(148, 108, "30 + 70 = 100 cm³", 16)
    fig.line(26, 126, 535, 126, LINE)
    fig.text(26, 155, "Float density", 15, weight="bold")
    fig.text(148, 155, "85 ÷ 100 = 0.85 g/cm³", 16, GREEN, weight="bold")
    fig.text(148, 181, "0.85 < 0.90 g/cm³, so the float rises.", 15)
    save(fig, "sol29-float-total")


def density_interval():
    fig = card(546, 171, "The density must lie strictly between the two",
               "The acceptable interval is above 0.80 and below 1.20 grams per cubic centimetre. The option 0.95 lies inside. Both endpoints are excluded.")
    left, right, y = 99, 464, 83
    candidate = left + (right - left) * (0.95 - 0.8) / (1.2 - 0.8)
    fig.line(51, y, 512, y, MUTED, 1.5)
    fig.line(left, y, right, y, GREEN, 5)
    for x, label, name in ((left, "0.80", "Liquid X"), (right, "1.20", "Liquid Y")):
        fig.circle(x, y, 5, "white", GREEN, 2)
        fig.text(x, 113, label, 15, anchor="middle", weight="bold")
        fig.text(x, 141, name, 14, MUTED, "middle")
    fig.circle(candidate, y, 6, GREEN, "white", 1.5)
    fig.text(candidate, 65, "0.95 g/cm³", 15, GREEN, "middle", "bold")
    fig.text(281, 151, "Sinks in X and rises in Y", 15, GREEN, "middle")
    save(fig, "sol07-density-range")


def temperature_offset():
    fig = card(560, 190, "Correct both readings by the same amount",
               "The display readings 24 and 38 degrees Celsius become 21 and 35 after correction. The change is 14 degrees Celsius in both rows.")
    for y, label, start, end in ((87, "Display", 24, 38), (144, "Actual", 21, 35)):
        fig.text(25, y + 5, label, 15, weight="bold")
        for x, value in ((169, start), (373, end)):
            fig.rect(x - 39, y - 18, 78, 36, BLUE_FILL if y == 87 else GREEN_FILL, LINE, rx=6)
            fig.text(x, y + 6, f"{value} °C", 15, anchor="middle", weight="bold")
        fig.line(216, y, 325, y, MUTED, 1.5, arrow=True)
        fig.text(270, y - 8, "+14 °C", 14, GREEN, "middle")
    fig.text(169, 56, "Before", 14, MUTED, "middle")
    fig.text(373, 56, "After", 14, MUTED, "middle")
    fig.text(435, 148, "Subtract 3 °C", 14, MUTED)
    save(fig, "sol09-offset")


def missing_temperature():
    fig = card(562, 255, "Different paths fit the same two readings",
               "Both example paths start at 19 degrees Celsius at minute 2 and end at 25 degrees at minute 6. One example is cooler than the other at minute 4.")
    x1, xm, x2, bottom = 110, 285, 460, 188
    fig.path(f"M72,58 V{bottom} H513", sw=1.5)
    fig.text(25, 66, "°C", 15, weight="bold")
    fig.line(xm, 60, xm, bottom, LINE, 1.2, dash="4 4")
    for y, value in ((151, 19), (84, 25)):
        fig.text(59, y + 5, value, 14, MUTED, "end")
        fig.line(69, y, 76, y, INK)
    fig.line(x1, 151, x2, 84, BLUE, 2.5)
    fig.line(x1, 151, xm, 151, ORANGE, 2.5, dash="6 3")
    fig.line(xm, 151, x2, 84, ORANGE, 2.5, dash="6 3")
    for x, y in ((x1, 151), (x2, 84)):
        fig.circle(x, y, 5.5, INK, "white", 1.5)
    for x, minute in ((x1, 2), (xm, 4), (x2, 6)):
        fig.text(x, 209, minute, 14, MUTED, "middle")
    fig.text(286, 233, "Time (minutes)", 15, anchor="middle")
    fig.text(363, 165, "Two possible paths", 14, weight="bold")
    save(fig, "sol30-two-paths")


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for draw in (
        displacement, density_blocks, flotation, temperature, bubble, thermometer_cups,
        cooling_readings, overflow, marbles, two_part_float, density_interval,
        temperature_offset, missing_temperature,
    ):
        draw()
