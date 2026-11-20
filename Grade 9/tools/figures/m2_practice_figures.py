"""Regenerate the diagrams for the M2 practice questions and solutions."""

from m2_learning_figures import ASSETS, BLUE_TEXT, ORANGE_TEXT, WATER_TOP, card, centre, measure
from svgkit import BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE, MUTED, ORANGE, ORANGE_FILL


def tank(length, width, height, water_depth, *, thick=False):
    if thick:
        title = "Glass tank · front section"
        note = "The section shows the walls and base, each 1 cm thick."
        short_label = f"{water_depth} cm water depth"
    else:
        title = "Aquarium · front view"
        note = ""
        short_label = f"{height - water_depth} cm gap"
    fig = card(276 if thick else 244, title,
               f"Inside length {length} cm, inside width {width} cm, inside height {height} cm. "
               f"{short_label}. {note}".strip())
    x, top, w, h = 53, 62, 222, 124
    right, bottom = x + w, top + h
    level = bottom - h * water_depth / height
    if thick:
        fig.path(f"M{x-10},{top} H{x} V{bottom} H{right} V{top} H{right+10} V{bottom+10} H{x-10} Z",
                 GRAY_FILL, INK)
    else:
        fig.path(f"M{x},{top} V{bottom} H{right} V{top}", sw=2)
    fig.rect(x + 1, level, w - 2, bottom - level - 1, BLUE_FILL, "none")
    fig.line(x, level, right, level, BLUE, 2)
    centre(fig, x + w / 2, (level + bottom) / 2 + 5, "Water", 16, BLUE_TEXT, "bold")
    for y in (top, level, bottom):
        fig.line(right + 12, y, 316, y, LINE, dash="4 4")
    measure(fig, 315, top, 315, bottom)
    fig.text(326, 130, f"{height} cm inside height", 15, weight="bold")
    short_top, short_bottom = (level, bottom) if thick else (top, level)
    measure(fig, 295, short_top, 295, short_bottom)
    fig.text(326, (short_top + short_bottom) / 2 + (16 if thick else 5), short_label, 15,
             BLUE_TEXT, weight="bold")
    measure(fig, x, 206, right, 206)
    centre(fig, x + w / 2, 227, f"{length} cm inside length", 15, weight="bold")
    fig.text(326, 207, f"{width} cm inside width", 15)
    fig.text(326, 227, "Into the page", 13, MUTED)
    if thick:
        fig.text(43, 256, "Walls and base are each 1 cm thick.", 14, MUTED)
    return fig


def cylinder_body(fig, x, y, rx, h, *, water=0):
    """Draw a cylindrical vessel with an optional proportional water level."""
    ry = rx / 4
    if water:
        level = y + h * (1 - water)
        fig.path(f"M{x-rx},{level} V{y+h} a{rx},{ry} 0 0 0 {2*rx},0 V{level}",
                 BLUE_FILL, BLUE)
        fig.add(f'<ellipse cx="{x}" cy="{level}" rx="{rx}" ry="{ry}" '
                f'fill="{WATER_TOP}" stroke="{BLUE}"/>')
    fig.path(f"M{x-rx},{y} V{y+h} a{rx},{ry} 0 0 0 {2*rx},0 V{y}", sw=2)
    fig.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="2"/>')


def cup():
    fig = card(228, "Inside the cylindrical cup",
               "The circular base has inside radius 4 cm. The cup's inside height is 10 cm.")
    centre(fig, 136, 65, "Top view", 16, weight="bold")
    centre(fig, 350, 65, "Side view", 16, weight="bold")
    fig.line(252, 52, 252, 203, LINE)
    fig.circle(135, 131, 46, BLUE_FILL, INK, 2)
    fig.line(135, 131, 181, 131, BLUE, 2.5)
    fig.circle(135, 131, 3, INK, "none")
    centre(fig, 157, 121, "4 cm", 15, BLUE_TEXT, "bold")
    fig.rect(300, 83, 100, 115, GRAY_FILL, INK, sw=2)
    measure(fig, 420, 83, 420, 198)
    fig.text(432, 145, "10 cm", 15, weight="bold")
    return fig


def garden(solution=False):
    title = "Trace all six outside edges" if solution else "L-shaped garden"
    description = ("Top 12 m, right 5 m, bottom 7 m, left 8 m. "
                   + ("The missing horizontal and vertical edges are 5 m and 3 m." if solution
                      else "The two edges of the inside step are unlabelled."))
    fig = card(238, title, description)
    x, y, scale = 129, 67, 17
    right, inner = x + 12 * scale, x + 7 * scale
    step, bottom = y + 5 * scale, y + 8 * scale
    fig.path(f"M{x},{y} H{right} V{step} H{inner} V{bottom} H{x} Z", BLUE_FILL, INK, 2)
    for px, py, value in (((x + right) / 2, y - 9, 12), (right + 26, (y + step) / 2 + 4, 5),
                          ((x + inner) / 2, bottom + 24, 7), (x - 28, (y + bottom) / 2 + 4, 8)):
        centre(fig, px, py, f"{value} m", 16, weight="bold")
    if solution:
        fig.path(f"M{right},{step} H{inner} V{bottom}", stroke=ORANGE, sw=3)
        fig.text(inner + 13, step + 22, "12 − 7 = 5 m", 16, ORANGE_TEXT, weight="bold")
        fig.text(inner + 13, bottom - 7, "8 − 5 = 3 m", 16, ORANGE_TEXT, weight="bold")
    return fig


def window(solution=False):
    title = "Follow the outside boundary" if solution else "Window and metal frame"
    fig = card(258, title,
               "A semicircle sits on top of an 8 cm wide and 10 cm tall rectangle. "
               + ("The outside boundary is the curved arc and three straight sides." if solution
                  else "The semicircle and rectangle share the rectangle's top side."))
    x, y, w, h = 104, 105, 96, 120
    fig.path(f"M{x},{y} a48,48 0 0 1 {w},0 V{y+h} H{x} Z", BLUE_FILL, INK, 2)
    if solution:
        fig.path(f"M{x},{y} a48,48 0 0 1 {w},0", stroke=ORANGE, sw=4)
        fig.path(f"M{x},{y} V{y+h} H{x+w} V{y}", stroke=BLUE, sw=4)
    fig.line(x, y, x + w, y, MUTED, 1.4, dash="5 4")
    measure(fig, 86, y, 86, y + h)
    centre(fig, 52, 168, "10 cm", 15, weight="bold")
    measure(fig, x, 232, x + w, 232)
    centre(fig, x + w / 2, 251, "8 cm", 15, weight="bold")
    if solution:
        fig.text(232, 88, "Curved arc  ·  3.14 × 8 ÷ 2 = 12.56 cm", 15, ORANGE_TEXT, weight="bold")
        fig.text(232, 122, "Straight sides  ·  10 + 8 + 10 = 28 cm", 15, BLUE_TEXT, weight="bold")
        fig.text(232, 154, "The dashed join is inside the frame.", 14, MUTED)
        fig.rect(229, 174, 259, 37, GREEN_FILL, "none", rx=6)
        centre(fig, 358, 198, "Frame length = 40.56 cm", 16, GREEN, "bold")
    else:
        fig.text(231, 81, "Semicircle", 16, weight="bold")
        fig.text(231, 154, "Rectangle", 16, weight="bold")
    return fig


def quarter_circle():
    fig = card(240, "Quarter circle",
               "O is the centre. Both straight sides OA and OB are 10 cm long.")
    x, y, r = 172, 187, 119
    fig.path(f"M{x},{y} v-{r} a{r},{r} 0 0 1 {r},{r} Z", BLUE_FILL, INK, 2)
    for px, py, label in ((x - 2, y - r - 9, "A"), (x - 13, y + 15, "O"), (x + r + 13, y + 4, "B")):
        centre(fig, px, py, label, 16, weight="bold")
    measure(fig, x - 25, y - r, x - 25, y)
    centre(fig, x - 59, y - r / 2 + 6, "10 cm", 15)
    measure(fig, x, y + 23, x + r, y + 23)
    centre(fig, x + r / 2, y + 45, "10 cm", 15)
    return fig


def cut_card():
    fig = card(246, "Card with a semicircle cut out",
               "The original sheet is 14 cm by 10 cm. A semicircle whose diameter is the right edge "
               "has been removed. The tinted area is the card remaining.")
    x, y, w, h = 109, 58, 203, 145
    right, bottom = x + w, y + h
    r = h / 2
    fig.path(f"M{x},{y} H{right} A{r},{r} 0 0 0 {right},{bottom} H{x} Z", BLUE_FILL, INK, 2)
    fig.line(right, y, right, bottom, MUTED, dash="5 4")
    centre(fig, 176, 135, "Card left", 16, BLUE_TEXT, "bold")
    centre(fig, 278, 135, "Cut out", 14, MUTED)
    measure(fig, 336, y, 336, bottom)
    fig.text(347, 136, "10 cm", 15, weight="bold")
    measure(fig, x, 217, right, 217)
    centre(fig, (x + right) / 2, 237, "14 cm", 15, weight="bold")
    return fig


def bottle():
    fig = card(264, "Water in the cylindrical bottle",
               "The inside diameter is 8 cm, the inside height is 20 cm, and the water is 12 cm deep.")
    x, top, rx, h = 178, 89, 43, 140
    level = top + h * (1 - 12 / 20)
    cylinder_body(fig, x, top, rx, h, water=12 / 20)
    measure(fig, x - rx, top, x + rx, top)
    centre(fig, x, 64, "8 cm inside diameter", 15, weight="bold")
    centre(fig, x, 196, "Water", 16, BLUE_TEXT, "bold")
    for y in (top, level, top + h):
        fig.line(x + rx + 4, y, 270, y, LINE, dash="4 4")
    measure(fig, 269, top, 269, top + h)
    fig.text(281, 121, "20 cm inside height", 15, weight="bold")
    measure(fig, 247, level, 247, top + h)
    fig.text(281, 192, "12 cm water depth", 15, BLUE_TEXT, weight="bold")
    return fig


def tray_shape(fig, x, y, w, h, dx, dy, fill=GRAY_FILL):
    """Draw a shallow tray from its front-left rim, with a visible inside floor."""
    fig.path(f"M{x},{y} l{dx},-{dy} h{w} l-{dx},{dy} Z", "white", INK)
    inset = h * dx / dy
    fig.path(f"M{x+inset},{y} L{x+dx},{y-dy+h} H{x+w+dx-inset} L{x+w},{y} Z",
             fill, LINE)
    fig.path(f"M{x},{y} H{x+w} v{h} h-{w} Z", BLUE_FILL, INK)
    fig.path(f"M{x+w},{y} l{dx},-{dy} v{h} l-{dx},{dy} Z", WATER_TOP, INK)


def transfer(solution=False):
    if solution:
        fig = card(246, "The same water covers a different base",
                   "The bottle contains 1130.4 cubic centimetres. The tray base is 376.8 square "
                   "centimetres, so the water reaches a depth of 3 cm.")
    else:
        fig = card(246, "Bottle-to-tray transfer",
                   "A full cylinder with radius 6 cm and inside height 10 cm is emptied into a "
                   "rectangular tray with inside base 24 cm by 15.7 cm.")
    cylinder_body(fig, 107, 88, 36, 83, water=1)
    tray_shape(fig, 295, 146, 119, 14, 37, 30, BLUE_FILL if solution else GRAY_FILL)
    fig.line(178, 117, 269, 117, MUTED, 2, arrow=True)
    centre(fig, 224, 103, "Pour", 15, weight="bold")
    centre(fig, 107, 61, "Full bottle", 16, weight="bold")
    centre(fig, 374, 89, "Water in tray" if solution else "Empty tray", 16, weight="bold")
    if solution:
        centre(fig, 107, 207, "Volume = 1130.4 cm³", 16, BLUE_TEXT, "bold")
        centre(fig, 374, 188, "Base area = 376.8 cm²", 16, BLUE_TEXT, "bold")
        centre(fig, 374, 222, "1130.4 ÷ 376.8 = 3 cm deep", 16, GREEN, "bold")
    else:
        centre(fig, 107, 202, "Radius 6 cm", 15)
        centre(fig, 107, 223, "Inside height 10 cm", 15)
        centre(fig, 374, 202, "Inside base 24 cm × 15.7 cm", 15)
    return fig


def shed():
    fig = card(258, "Front of the shed",
               "The rectangle is 12 m wide and 7 m tall. The isosceles roof has sloping sides "
               "of 10 m and a perpendicular height of 8 m.")
    x, mx, right, peak, join, ground = 166, 232, 298, 51, 139, 216
    fig.rect(x, join, right - x, ground - join, BLUE_FILL, INK, 2)
    fig.path(f"M{x},{join} L{mx},{peak} L{right},{join} Z", ORANGE_FILL, INK, 2)
    fig.line(mx, peak, mx, join, MUTED, 1.8, dash="4 3")
    fig.path(f"M{mx},{join-10} h10 v10", stroke=MUTED)
    for px, py, label in ((180, 86, "10 m"), (284, 86, "10 m"), (254, 114, "8 m")):
        centre(fig, px, py, label, 15, weight="bold")
    measure(fig, 320, join, 320, ground)
    fig.text(333, 183, "7 m", 15, weight="bold")
    measure(fig, x, 230, right, 230)
    centre(fig, mx, 250, "12 m", 15, weight="bold")
    return fig


def inscribed_circle():
    fig = card(254, "Circle inside a square",
               "A circle touches all four sides of a 10 cm by 10 cm square. "
               "Only the four corners outside the circle are shaded.")
    x, y, side = 146, 53, 151
    midx, midy = x + side / 2, y + side / 2
    fig.rect(x, y, side, side, BLUE_FILL, INK, 2)
    fig.circle(midx, midy, side / 2, "white", INK, 1.8)
    for px, py in ((x, midy), (x + side, midy), (midx, y), (midx, y + side)):
        fig.circle(px, py, 3.2, INK, "none")
    measure(fig, 321, y, 321, y + side)
    fig.text(333, midy + 5, "10 cm", 15, weight="bold")
    measure(fig, x, 222, x + side, 222)
    centre(fig, midx, 243, "10 cm", 15, weight="bold")
    return fig


def pond():
    fig = card(251, "Pond and surrounding path",
               "Both circles share centre O. The pond radius is 6 m, and the path extends 1 m "
               "from the pond edge all the way around.")
    x, y, r = 175, 145, 91
    pond_r = r * 6 / 7
    fig.circle(x, y, r, ORANGE_FILL, INK, 2)
    fig.circle(x, y, pond_r, BLUE_FILL, INK, 2)
    fig.circle(x, y, 3, INK, "none")
    fig.text(x - 5, y - 9, "O", 15, weight="bold")
    measure(fig, x, y, x + pond_r, y)
    centre(fig, x + 37, y - 8, "6 m", 15, BLUE_TEXT, "bold")
    measure(fig, x + pond_r, y, x + r, y)
    fig.path(f"M{x+(pond_r+r)/2},{y} l36,-24 h20", stroke=ORANGE)
    fig.text(312, 116, "1 m path width", 15, ORANGE_TEXT, weight="bold")
    centre(fig, x, y + 33, "Pond", 15, BLUE_TEXT, "bold")
    return fig


def tray_net(fig, x, y, cut):
    scale = 9
    w, h, c = 18 * scale, 12 * scale, cut * scale
    fig.rect(x, y, w, h, "none", MUTED, dash="3 4")
    fig.path(f"M{x+c},{y} H{x+w-c} v{c} h{c} V{y+h-c} h-{c} v{c} H{x+c} v-{c} H{x} V{y+c} h{c} Z",
             BLUE_FILL, INK, 1.8)
    fig.rect(x + c, y + c, w - 2 * c, h - 2 * c, "none", MUTED, dash="5 4")
    for xx in (x, x + w - c):
        for yy in (y, y + h - c):
            fig.rect(xx, yy, c, c, ORANGE_FILL, ORANGE, dash="3 3")
            fig.line(xx + 3, yy + 3, xx + c - 3, yy + c - 3, ORANGE)
            fig.line(xx + c - 3, yy + 3, xx + 3, yy + c - 3, ORANGE)
    measure(fig, x, y + h + 12, x + w, y + h + 12)
    centre(fig, x + w / 2, y + h + 32, "18 cm", 15)
    measure(fig, x - 11, y, x - 11, y + h)
    centre(fig, x - 31, y + h / 2 + 5, "12 cm", 14)


def trays(solution=False):
    if solution:
        fig = card(245, "Compare the folded trays",
                   "Ada's base is 14 cm by 8 cm and the sides are 2 cm high, giving 224 cubic centimetres. "
                   "Nico's base is 12 cm by 6 cm and the sides are 3 cm high, giving 216 cubic centimetres.")
        for x, name, length, width, height in ((37, "Ada", 14, 8, 2), (304, "Nico", 12, 6, 3)):
            volume = length * width * height
            tray_shape(fig, x, 127, 10 * length, 7 * height, 5 * width, 4 * width)
            centre(fig, x + 90, 65, name, 17, weight="bold")
            centre(fig, x + 90, 169, f"Base {length} × {width} cm · height {height} cm", 15)
            centre(fig, x + 90, 196, f"{length} × {width} × {height} = {volume} cm³", 16, BLUE_TEXT, "bold")
        centre(fig, 260, 227, "Ada’s holds 8 cm³ more.", 16, GREEN, "bold")
    else:
        fig = card(263, "Corner cuts and fold lines",
                   "Both sheets are 18 cm by 12 cm. Ada cuts a 2 cm square from each corner; "
                   "Nico cuts a 3 cm square from each corner. Dashed interior lines show where the sides fold.")
        for x, name, cut in ((65, "Ada", 2), (319, "Nico", 3)):
            centre(fig, x + 81, 68, f"{name} · {cut} cm corner cuts", 16, weight="bold")
            tray_net(fig, x, 87, cut)
        fig.line(107, 240, 131, 240, ORANGE, 2, dash="3 3")
        fig.text(139, 245, "Remove corner", 14)
        fig.line(294, 240, 318, 240, MUTED, 2, dash="5 4")
        fig.text(326, 245, "Fold line", 14)
    return fig


def generate():
    ASSETS.mkdir(parents=True, exist_ok=True)
    figures = {
        "q02-glass-tank": tank(20, 15, 25, 18, thick=True),
        "q03-cylindrical-cup": cup(),
        "q04-garden": garden(),
        "q06-window": window(),
        "q10-aquarium": tank(40, 25, 30, 26),
        "q11-quarter-circle": quarter_circle(),
        "q14-cut-card": cut_card(),
        "q15-bottle": bottle(),
        "q18-transfer": transfer(),
        "q19-shed": shed(),
        "q25-inscribed-circle": inscribed_circle(),
        "q27-pond": pond(),
        "q30-tray-nets": trays(),
        "sol04-garden": garden(solution=True),
        "sol06-window": window(solution=True),
        "sol18-transfer": transfer(solution=True),
        "sol30-trays": trays(solution=True),
    }
    for name, fig in figures.items():
        fig.save(ASSETS / f"{name}.svg")


if __name__ == "__main__":
    generate()
