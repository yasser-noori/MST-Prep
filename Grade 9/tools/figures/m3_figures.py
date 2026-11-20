"""Regenerate the M3 learning and drill diagrams added to the algebra unit."""

from pathlib import Path

from svgkit import BLUE, BLUE_FILL, GREEN, GREEN_FILL, GRAY_FILL, INK, LINE, MUTED, ORANGE, ORANGE_FILL, RED, Fig

ASSETS = Path(__file__).resolve().parents[2] / "assets" / "M3"


def card(height, title, description):
    fig = Fig(520, height, title, description)
    fig.text(22, 31, title, 20, weight="bold")
    return fig


def center(fig, x, y, label, size=16, color=INK, weight="normal"):
    fig.text(x, y, label, size, color, "middle", weight)


def cell(fig, x, y, width, label, fill, *, height=36):
    fig.rect(x, y, width, height, fill, INK, rx=5)
    center(fig, x + width / 2, y + height / 2 + 5, label, weight="bold")


def span(fig, left, right, y, label):
    fig.path(f"M{left},{y - 7} v7 H{right} v-7", stroke=MUTED)
    center(fig, (left + right) / 2, y + 21, label)


def ribbon():
    fig = card(207, "Start with 18 m, then subtract per parcel",
               "A tape shows 18 metres at the start. The first parcel uses 2 metres and leaves 16 metres.")
    for i, (y, label) in enumerate(((78, "Before wrapping"), (126, "After 1 parcel"))):
        fig.text(24, y + 5, label, 15, weight="bold")
        fig.rect(166, y - 16, 324, 32, BLUE_FILL, BLUE, rx=5)
        if i:
            fig.rect(454, y - 16, 36, 32, ORANGE_FILL, ORANGE)
            center(fig, 472, y + 5, "2 m", 13, weight="bold")
        center(fig, 310 if i else 328, y + 5, "16 m left" if i else "18 m to start")
    center(fig, 260, 181, "After p parcels: 18 − 2p metres left", 17, weight="bold")
    return fig


def substitute():
    fig = card(212, "Put brackets around the negative input",
               "Replacing both x values with negative 3 gives 2 times negative 3 squared minus "
               "negative 3 plus 1 in brackets. The square is 9, and the second bracket is negative 2.")
    center(fig, 260, 66, "2x² − (x + 1)  with  x = −3", 20, weight="bold")
    cell(fig, 42, 84, 202, "2 × (−3)²", BLUE_FILL)
    center(fig, 260, 107, "−", 20, weight="bold")
    cell(fig, 277, 84, 201, "(−3 + 1)", ORANGE_FILL)
    center(fig, 143, 147, "(−3) × (−3) = 9", 16)
    center(fig, 378, 147, "Inside brackets: −2", 16)
    center(fig, 260, 191, "2 × 9 − (−2) = 20", 18, GREEN, "bold")
    return fig


def inverse():
    fig = card(244, "Undo operations on both sides",
               "The three equations keep both sides equal. Add 4 to both sides of 3n minus 4 equals 11, "
               "then divide both sides of 3n equals 15 by 3 to get n equals 5.")
    fig.text(322, 60, "Undo step", 15, MUTED, weight="bold")
    for i, (left, right, action) in enumerate((("3n − 4", "11", ""),
                                              ("3n", "15", "Add 4 to both"),
                                              ("n", "5", "Divide both by 3"))):
        y = 68 + i * 52
        fill = GREEN_FILL if i == 2 else BLUE_FILL
        cell(fig, 30, y, 115, left, fill)
        center(fig, 163, y + 23, "=", 20, weight="bold")
        cell(fig, 185, y, 115, right, fill)
        fig.text(322, y + 23, action, 16, weight="bold")
    return fig


def rate():
    fig = card(205, "Compare the changes between two columns",
               "From input 1 to input 4 is a change of 3. From output 8 to output 20 is a change of 12. "
               "The output increases by 4 per input unit.")
    for y, label, first, second, step, fill in (
        (65, "Input", "1", "4", "+3", BLUE_FILL),
        (116, "Output", "8", "20", "+12", ORANGE_FILL),
    ):
        fig.text(30, y + 23, label, 16, weight="bold")
        cell(fig, 129, y, 75, first, fill)
        cell(fig, 389, y, 75, second, fill)
        fig.line(217, y + 18, 376, y + 18, MUTED, arrow=True)
        fig.rect(270, y + 4, 52, 27, "white", "none")
        center(fig, 296, y + 23, step, weight="bold")
    center(fig, 260, 181, "12 ÷ 3 = 4 output units per input unit", 17, weight="bold")
    return fig


def rectangle():
    fig = card(240, "Rectangle dimensions",
               "The rectangle has a perimeter of 50 cm. Its length is the width plus 3 cm.")
    fig.rect(96, 60, 268, 113, BLUE_FILL, INK, sw=2)
    center(fig, 230, 122, "Perimeter 50 cm", 18, weight="bold")
    fig.line(379, 60, 379, 173, MUTED)
    for y in (60, 173):
        fig.line(374, y, 384, y, MUTED)
    fig.text(391, 122, "Width", 16)
    span(fig, 96, 364, 189, "Width + 3 cm")
    return fig


def signed_height():
    fig = card(239, "The ledge marks zero height",
               "A climber starts at negative 6 metres relative to the ledge. Upward is positive "
               "and the climber rises at 2 metres per minute.")
    fig.line(104, 68, 104, 192, MUTED, sw=2)
    fig.line(104, 73, 104, 49, MUTED, sw=2, arrow=True)
    fig.line(83, 87, 260, 87, INK, sw=3)
    fig.text(280, 93, "Ledge · 0 m", 17, weight="bold")
    fig.line(104, 181, 269, 181, MUTED, dash="4 5")
    fig.circle(104, 181, 5, BLUE, "none")
    fig.text(280, 187, "Start · −6 m", 17, weight="bold")
    fig.line(194, 165, 194, 108, BLUE, 2, arrow=True)
    fig.text(213, 142, "Rises 2 m per minute", 16, weight="bold")
    fig.text(122, 60, "Positive direction", 15, MUTED)
    return fig


def trail(solution=False):
    title = "Split the trail at the meeting point" if solution else "Two walkers on the same trail"
    desc = ("Isha walks from marker 6 to marker 18, a distance of 12 km. Leo walks "
            "21 km from marker 39 to marker 18." if solution else "Isha walks from marker A at kilometre 6 "
            "toward Leo at 4 km/h. Leo walks from marker B at kilometre 39 toward Isha at 7 km/h.")
    fig = card(224 if solution else 178, title, desc)
    left, right, y = 65, 455, 109
    meeting = left + (right - left) * 12 / 33
    fig.line(left, y, right, y, INK, 2)
    for x, label in ((left, "A · km 6"), (right, "B · km 39")):
        fig.circle(x, y, 5, INK, "none")
        center(fig, x, y + 28, label, weight="bold")
    if solution:
        fig.line(left + 4, y, meeting - 4, y, BLUE, 4)
        fig.line(meeting + 4, y, right - 4, y, ORANGE, 4)
        fig.circle(meeting, y, 6, GREEN, "none")
        center(fig, meeting, y + 28, "Meet · km 18", color=GREEN, weight="bold")
        center(fig, (left + meeting) / 2, y - 17, "Isha: 12 km", weight="bold")
        center(fig, (meeting + right) / 2, y - 17, "Leo: 21 km", weight="bold")
        span(fig, left, right, 164, "33 km ÷ 11 km/h = 3 h")
    else:
        fig.line(left + 4, 88, 208, 88, BLUE, sw=2, arrow=True)
        fig.line(right - 4, 88, 310, 88, ORANGE, sw=2, arrow=True)
        center(fig, 135, 73, "Isha · 4 km/h", weight="bold")
        center(fig, 385, 73, "Leo · 7 km/h", weight="bold")
    return fig


def bead_cartons():
    fig = card(203, "Beads in the two cartons",
               "The cartons have the same unknown number of red beads. Carton 1 adds 6 blue beads, "
               "and carton 2 adds 10 blue beads.")
    for x, name, blue in ((30, "Carton 1", 6), (267, "Carton 2", 10)):
        center(fig, x + 110, 66, name, weight="bold")
        fig.rect(x, 80, 220, 93, GRAY_FILL, LINE, rx=7)
        fig.rect(x + 13, 92, 194, 32, "white", RED, rx=5)
        center(fig, x + 110, 113, "Same red count", color=RED, weight="bold")
        center(fig, x + 110, 151, f"{blue} blue beads", 16, BLUE, "bold")
    return fig


def shelf():
    fig = card(215, "Floor, platform and shelf",
               "The shelf is h centimetres above the platform. The platform is 12 centimetres above the floor.")
    for y, label in ((67, "Shelf"), (121, "Platform"), (183, "Floor")):
        fig.line(58, y, 256, y, INK, 3)
        fig.text(68, y - 8, label, 16, weight="bold")
        fig.line(256, y, 293, y, MUTED, dash="4 4")
    for top, bottom, label in ((67, 121, "h cm"), (121, 183, "12 cm")):
        fig.path(f"M293,{top} h7 V{bottom} h-7", stroke=BLUE, sw=2)
        fig.text(315, (top + bottom) / 2 + 5, label, 17, weight="bold")
    return fig


def length_solution():
    fig = card(227, "Use one length and one width",
               "Half the perimeter is 25 cm. Removing the extra 3 cm from the length leaves "
               "two equal widths totalling 22 cm. Each width is 11 cm, so the length is 14 cm.")
    x, y, width, extra = 46, 78, 185, 58
    for offset, label, fill in ((0, "Width", BLUE_FILL), (width, "Width", BLUE_FILL),
                                (2 * width, "3 cm", ORANGE_FILL)):
        bar_width = extra if offset == 2 * width else width
        fig.rect(x + offset, y, bar_width, 43, fill, INK)
        center(fig, x + offset + bar_width / 2, y + 27, label, weight="bold")
    span(fig, x + width, x + 2 * width + extra, y - 9, "")
    center(fig, x + 1.5 * width + extra / 2, y - 18, "Length", weight="bold")
    span(fig, x, x + 2 * width + extra, y + 61, "25 cm = half the perimeter")
    center(fig, 260, 197, "Width = (25 − 3) ÷ 2 = 11 cm  ·  Length = 14 cm", 16, GREEN, "bold")
    return fig


def rental_solution():
    fig = card(290, "The rental prices cross at 4 hours",
               "Loop starts at 16 dollars and adds 2 per hour. Wheel starts at 4 dollars and adds 5 "
               "per hour. Their lines cross at four hours and 24 dollars.")
    left, bottom, dx, dy = 61, 236, 52, 4.5
    for dollars in (0, 4, 16, 24, 36):
        y = bottom - dollars * dy
        fig.line(left, y, 425, y, LINE)
        fig.text(left - 8, y + 5, str(dollars), 14, anchor="end")
    fig.line(left, bottom, 425, bottom, INK, 1.8)
    fig.line(left, bottom, left, 69, INK, 1.8)
    fig.text(43, 58, "$", 15, weight="bold")
    for hour in (0, 2, 4, 6):
        center(fig, left + hour * dx, 257, str(hour), 14)
    center(fig, 224, 281, "Hours", 16, weight="bold")
    for name, start, per_hour, color, label_y in (
        ("Loop", 16, 2, BLUE, 119), ("Wheel", 4, 5, ORANGE, 86)
    ):
        end = bottom - (start + 6 * per_hour) * dy
        fig.line(left, bottom - start * dy, left + 6 * dx, end, color, 3)
        fig.text(left + 6 * dx + 12, label_y, name, 16, weight="bold")
    cross_x, cross_y = left + 4 * dx, bottom - 24 * dy
    fig.line(cross_x, cross_y, cross_x, bottom, MUTED, dash="5 4")
    fig.circle(cross_x, cross_y, 5, GREEN, "white", 1)
    fig.text(cross_x - 10, cross_y - 18, "4 h, $24", 16, GREEN, anchor="end", weight="bold")
    return fig


def ages_solution():
    fig = card(240, "Line up their current ages",
               "Their current ages total 28 years. Arun has Beth's age plus 4 years. After removing the "
               "4 extra years, the two equal portions total 24 years. Beth is 12.")
    for y, name, extra in ((75, "Beth", False), (126, "Arun", True)):
        fig.text(42, y + 24, name, 16, weight="bold")
        fig.rect(111, y, 210, 39, BLUE_FILL, BLUE)
        center(fig, 216, y + 25, "Beth’s age", weight="bold")
        if extra:
            fig.rect(321, y, 70, 39, ORANGE_FILL, ORANGE)
            center(fig, 356, y + 25, "4 years", 15, weight="bold")
    center(fig, 260, 193, "Ages now total 34 − 6 = 28 years", 16)
    center(fig, 260, 220, "Beth’s age = (28 − 4) ÷ 2 = 12", 17, GREEN, "bold")
    return fig


def half_batches():
    fig = card(194, "Count in half-batches",
               "The first and second full batches each contain two half-batches. The final half-batch "
               "makes five equal parts, and 450 grams divided by five is 90 grams.")
    for i in range(5):
        cell(fig, 36 + 91 * i, 80, 84, "½ batch", BLUE_FILL if i < 4 else ORANGE_FILL, height=38)
    for x, label in ((123, "Batch 1"), (305, "Batch 2"), (442, "Extra ½")):
        center(fig, x, 68, label, 15, weight="bold")
    span(fig, 36, 484, 136, "450 g across five equal parts")
    return fig


def scores_solution():
    fig = card(218, "Which third marks leave 8 and 11?",
               "The two kept marks total 19. The whole numbers 0 through 8 let the kept marks "
               "remain 8 and 11. From 9 through 20, the third mark is kept instead of 8.")
    x, step, y = 37, 22, 113
    fig.rect(x - 9, y - 20, 9 * step, 40, GREEN_FILL, "none", rx=6)
    fig.line(x, y, x + 20 * step, y, INK, 2)
    for i in range(21):
        xx = x + i * step
        fig.line(xx, y - 4, xx, y + 4, INK)
        if i in (0, 4, 8, 9, 14, 20):
            center(fig, xx, y + 34, str(i), 14, weight="bold" if i in (8, 9) else "normal")
    center(fig, 121, 73, "0–8: kept total is 19", 16, GREEN, "bold")
    center(fig, 354, 73, "9–20: kept total exceeds 19", 16, weight="bold")
    center(fig, 260, 193, "At 8, either tied 8 can be dropped.", 16)
    return fig


def generate():
    figures = {
        "learn-ribbon-rule": ribbon(),
        "learn-substitution": substitute(),
        "learn-inverse-operations": inverse(),
        "learn-table-rate": rate(),
        "q03-rectangle": rectangle(),
        "q11-signed-height": signed_height(),
        "q17-trail": trail(),
        "q25-cartons": bead_cartons(),
        "q28-shelf": shelf(),
        "sol03-rectangle": length_solution(),
        "sol05-rentals": rental_solution(),
        "sol17-trail": trail(solution=True),
        "sol21-ages": ages_solution(),
        "sol29-half-batches": half_batches(),
        "sol30-score-range": scores_solution(),
    }
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, figure in figures.items():
        figure.save(ASSETS / f"{name}.svg")


if __name__ == "__main__":
    generate()
