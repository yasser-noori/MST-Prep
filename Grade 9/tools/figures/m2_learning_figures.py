"""Draw the M2 learning figures. Run directly to regenerate them."""

from pathlib import Path

from svgkit import BLUE, BLUE_FILL, GRAY_FILL, INK, LINE, MUTED, ORANGE, ORANGE_FILL, Fig

ASSETS = Path(__file__).resolve().parents[2] / "assets" / "M2"
AIR = "#fff4df"
WATER_TOP = "#b9d6ff"
BLUE_TEXT = "#174ea6"
ORANGE_TEXT = "#93400d"


def card(height, title, description):
    fig = Fig(520, height, title, description)
    fig.text(22, 31, title, 20, weight="bold")
    return fig


def centre(fig, x, y, label, size=15, fill=INK, weight="normal"):
    fig.text(x, y, label, size, fill, "middle", weight)


def measure(fig, x1, y1, x2, y2):
    """Draw a dimension line with ticks perpendicular to its direction."""
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    dx, dy = 4 * (y2 - y1) / length, -4 * (x2 - x1) / length
    fig.line(x1, y1, x2, y2, MUTED)
    for x, y in ((x1, y1), (x2, y2)):
        fig.line(x - dx, y - dy, x + dx, y + dy, MUTED)


def circle_measurements():
    fig = card(244, "Two lengths, two measurements",
               "The diameter spans the whole circle through the centre and is twice the radius. "
               "The circumference follows the rim. Area covers the shaded interior.")
    centre(fig, 135, 62, "Radius and diameter", 16, weight="bold")
    centre(fig, 385, 62, "Circumference and area", 16, weight="bold")
    fig.line(260, 55, 260, 221, LINE)
    fig.circle(135, 128, 49, GRAY_FILL, MUTED)
    fig.line(86, 128, 184, 128, BLUE, 3)
    fig.line(135, 128, 135, 79, ORANGE, 3)
    for x, y in ((86, 128), (135, 128), (184, 128), (135, 79)):
        fig.circle(x, y, 3, INK, "none")
    fig.text(145, 108, "r", 17, ORANGE_TEXT, weight="bold")
    centre(fig, 135, 154, "d", 17, BLUE_TEXT, "bold")
    centre(fig, 135, 215, "d = 2 × r", 16, weight="bold")

    fig.circle(385, 128, 49, BLUE_FILL, INK, 4)
    centre(fig, 385, 134, "Area", 16, BLUE_TEXT, "bold")
    fig.path("M432,115 L451,99 H485", stroke=INK)
    fig.text(451, 92, "Rim", 14, weight="bold")
    centre(fig, 385, 201, "Around → cm", 15, weight="bold")
    centre(fig, 385, 224, "Inside → cm²", 15, BLUE_TEXT, "bold")
    return fig


def combined_shape():
    fig = card(184, "A rectangle with a round end",
               "A rectangle measures 8 centimetres by 6 centimetres. A semicircle with radius 3 "
               "centimetres shares the right-hand side. The shared side is dashed, and the solid "
               "outline follows the perimeter.")
    fig.rect(76, 61, 112, 84, BLUE_FILL, "none")
    fig.path("M188,61 A42,42 0 0 1 188,145 Z", ORANGE_FILL, "none")
    fig.path("M188,61 H76 V145 H188 A42,42 0 0 0 188,61", stroke=INK, sw=2.5)
    fig.line(188, 61, 188, 145, MUTED, 1.5, dash="5 4")
    centre(fig, 132, 166, "8 cm", 15)
    centre(fig, 49, 108, "6 cm", 15)
    fig.path("M188,103 H246", stroke=MUTED)
    fig.text(260, 97, "Shared side = diameter = 6 cm", 15, weight="bold")
    fig.text(260, 121, "Radius = 3 cm", 15)
    return fig


def tank_views():
    fig = card(236, "Same base, three heights",
               "The water depth reaches the surface, the gap runs from the surface to the rim, "
               "and the full inside height runs from the bottom to the rim.")
    x, top, w, bottom, level = 36, 66, 168, 193, 138
    fig.rect(x, top, w, level - top, AIR, "none")
    fig.rect(x, level, w, bottom - level, BLUE_FILL, "none")
    fig.path(f"M{x},{top} V{bottom} H{x+w} V{top}", sw=2)
    fig.line(x, level, x + w, level, BLUE, 2)
    centre(fig, 120, 109, "Empty space", 16, ORANGE_TEXT, "bold")
    centre(fig, 120, 171, "Water present", 16, BLUE_TEXT, "bold")
    for y in (top, level, bottom):
        fig.line(206, y, 274, y, LINE, dash="4 4")
    measure(fig, 221, top, 221, level)
    measure(fig, 221, level, 221, bottom)
    measure(fig, 274, top, 274, bottom)
    fig.text(230, 108, "Gap", 14, ORANGE_TEXT, weight="bold")
    fig.text(230, 169, "Depth", 14, BLUE_TEXT, weight="bold")
    fig.text(285, 126, "Full inside height", 15, weight="bold")
    fig.text(285, 147, "Use for total capacity", 14, MUTED)
    centre(fig, 260, 219, "Water present + empty space = total capacity", 15, weight="bold")
    return fig


def depth_from_volume():
    fig = card(228, "Spread the volume across the base",
               "A base of 8 cm by 5 cm has area 40 square centimetres. "
               "A volume of 120 cubic centimetres makes a layer 3 cm deep.")
    x, y, w, h, dx, dy = 48, 114, 126, 48, 45, 26
    fig.rect(x, y, w, h, BLUE_FILL, INK)
    fig.path(f"M{x},{y} l{dx},-{dy} h{w} l-{dx},{dy} Z", WATER_TOP, INK)
    fig.path(f"M{x+w},{y} l{dx},-{dy} v{h} l-{dx},{dy} Z", BLUE_FILL, INK)
    centre(fig, x + w / 2, 144, "120 cm³", 16, BLUE_TEXT, "bold")
    measure(fig, x, 175, x + w, 175)
    centre(fig, x + w / 2, 196, "8 cm", 15)
    measure(fig, x + w + 7, 173, x + w + dx + 7, 173 - dy)
    fig.text(213, 180, "5 cm", 15)
    measure(fig, 33, y, 33, y + h)
    centre(fig, 18, 143, "?", 17, BLUE_TEXT, "bold")
    fig.line(271, 65, 271, 196, LINE)
    fig.text(291, 91, "Base area = 8 × 5 = 40 cm²", 15)
    fig.text(291, 124, "Depth = volume ÷ base area", 15)
    fig.rect(289, 143, 201, 40, BLUE_FILL, "none", rx=6)
    centre(fig, 389, 169, "120 ÷ 40 = 3 cm", 17, BLUE_TEXT, "bold")
    return fig


def scaling():
    fig = card(250, "Double each edge",
               "Doubling each edge doubles length. A two-by-two square contains four unit squares, "
               "and a two-by-two-by-two cube contains eight unit cubes in two layers.")
    for x in (176, 344):
        fig.line(x, 61, x, 222, LINE)
    for x, title, result in ((92, "Length", "2 unit lengths"),
                              (260, "Area", "4 unit squares"),
                              (428, "Volume", "8 unit cubes")):
        centre(fig, x, 72, title, 16, weight="bold")
        centre(fig, x, 216, result, 15, weight="bold")
    for x in (40, 92):
        fig.line(x, 142, x + 52, 142, BLUE, 5)
    for x in (40, 92, 144):
        fig.line(x, 133, x, 151, INK, 2)
    fig.rect(222, 106, 76, 76, BLUE_FILL, INK, sw=1.6)
    fig.line(260, 106, 260, 182, INK)
    fig.line(222, 144, 298, 144, INK)
    for y, label in ((114, "Top"), (168, "Bottom")):
        fig.path(f"M373,{y} l28,-19 h56 l-28,19 Z", BLUE_FILL, INK)
        fig.path(f"M373,{y} h56 v22 h-56 Z", GRAY_FILL, INK)
        fig.path(f"M429,{y} l28,-19 v22 l-28,19 Z", WATER_TOP, INK)
        fig.line(401, y, 429, y - 19, INK)
        fig.line(387, y - 9.5, 443, y - 9.5, INK)
        fig.line(401, y, 401, y + 22, INK)
        fig.line(443, y - 9.5, 443, y + 12.5, INK)
        fig.text(464, y + 7, label, 13, MUTED)
    return fig


def worked_tank():
    fig = card(278, "Inside dimensions of the fish tank",
               "The rectangular tank is 10 cm long, 8 cm wide and 12 cm high inside. "
               "The water is 5 cm deep.")
    x, front, w, h, dx, dy = 81, 91, 160, 132, 63, 36
    bottom = front + h
    level = bottom - h * 5 / 12
    r = x + w
    fig.path(f"M{x},{front} l{dx},-{dy} h{w} l-{dx},{dy} Z", "none", INK)
    fig.path(f"M{r},{front} l{dx},-{dy} v{h} l-{dx},{dy} Z", "#f7f8fa", INK)
    fig.path(f"M{r},{level} l{dx},-{dy} V{bottom-dy} L{r},{bottom} Z", WATER_TOP, BLUE)
    fig.rect(x, level, w, bottom - level, BLUE_FILL, "none")
    fig.path(f"M{x},{level} l{dx},-{dy} h{w} l-{dx},{dy} Z", WATER_TOP, BLUE)
    fig.path(f"M{x},{front} V{bottom} H{r} V{front} H{x}", sw=2)
    fig.path(f"M{r},{front} l{dx},-{dy} v{h} l-{dx},{dy}", sw=2)
    fig.line(x, level, r, level, BLUE, 2)
    centre(fig, x + w / 2, 194, "Water", 16, BLUE_TEXT, "bold")
    measure(fig, 63, front, 63, bottom)
    centre(fig, 34, 152, "12 cm", 14, weight="bold")
    measure(fig, x, 241, r, 241)
    centre(fig, x + w / 2, 262, "10 cm", 15, weight="bold")
    measure(fig, r + 13, 241, r + dx + 13, 241 - dy)
    fig.text(291, 238, "8 cm", 15, weight="bold")
    measure(fig, 333, level - dy, 333, bottom - dy)
    for y in (level - dy, bottom - dy):
        fig.line(r + dx, y, 328, y, LINE, dash="4 4")
    fig.text(347, 155, "5 cm water depth", 15, BLUE_TEXT, weight="bold")
    return fig


def worked_gap():
    fig = card(239, "Fill the gap above the water",
               "The 12 cm full height minus the 5 cm water depth leaves 7 cm. "
               "An 80 square centimetre base times this gap gives 560 millilitres of room.")
    x, y, w, h = 29, 56, 130, 144
    level = y + h * 7 / 12
    fig.rect(x, y, w, level - y, ORANGE_FILL, "none")
    fig.rect(x, level, w, y + h - level, BLUE_FILL, "none")
    fig.path(f"M{x},{y} V{y+h} H{x+w} V{y}", sw=2)
    fig.line(x, level, x + w, level, BLUE, 2)
    centre(fig, 94, 105, "Room to fill", 16, ORANGE_TEXT, "bold")
    centre(fig, 94, 174, "Water", 16, BLUE_TEXT, "bold")
    measure(fig, 174, y, 174, level)
    fig.text(185, 105, "7 cm", 16, ORANGE_TEXT, weight="bold")
    measure(fig, 174, level, 174, y + h)
    fig.text(185, 174, "5 cm", 16, BLUE_TEXT, weight="bold")
    fig.line(228, 58, 228, 203, LINE)
    fig.text(249, 81, "Gap = 12 − 5 = 7 cm", 16)
    fig.text(249, 112, "Base = 10 × 8 = 80 cm²", 16)
    fig.text(249, 143, "Room = 80 × 7 = 560 cm³", 16)
    fig.rect(246, 157, 244, 42, ORANGE_FILL, "none", rx=6)
    centre(fig, 368, 184, "560 mL more can fit", 17, ORANGE_TEXT, "bold")
    return fig


def generate():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, draw in (
        ("learn-circle-measurements", circle_measurements),
        ("learn-combined-shape", combined_shape),
        ("learn-tank-heights", tank_views),
        ("learn-depth-from-volume", depth_from_volume),
        ("learn-scaling", scaling),
        ("learn-tank", worked_tank),
        ("learn-tank-gap", worked_gap),
    ):
        draw().save(ASSETS / f"{name}.svg")


if __name__ == "__main__":
    generate()
