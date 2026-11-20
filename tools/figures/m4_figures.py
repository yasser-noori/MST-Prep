"""Regenerate the M4 pattern and sequence enrichment figures."""

from math import sqrt
from pathlib import Path

from svgkit import BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE, MUTED, ORANGE, ORANGE_FILL, Fig


ASSETS = Path(__file__).resolve().parents[2] / "assets" / "M4"
WIDTH = 540
BLUE_TEXT = "#174ea6"
ORANGE_TEXT = "#93400d"


def card(height, title, description):
    figure = Fig(WIDTH, height, title, description)
    figure.text(22, 31, title, 20, weight="bold")
    return figure


def label(figure, x, y, text, size=15, fill=INK, weight="normal"):
    figure.text(x, y, text, size, fill, "middle", weight)


def token(figure, x, y, text, *, width=50, fill=GRAY_FILL, stroke=LINE):
    figure.rect(x - width / 2, y - 16, width, 32, fill, stroke, rx=6)
    label(figure, x, y + 6, text, 18, weight="bold")


def chain(figure, y, terms, gaps):
    step = 450 / (len(terms) - 1)
    for i, term in enumerate(terms):
        x = 45 + i * step
        token(figure, x, y, term, fill=BLUE_FILL if i + 1 == len(terms) else GRAY_FILL)
        if i < len(gaps):
            figure.line(x + 29, y, x + step - 29, y, MUTED, 1.5, arrow=True)
            label(figure, x + step / 2, y - 9, gaps[i], 14, BLUE_TEXT, "bold")


def count_gaps():
    figure = card(158, "Six positions have five gaps",
                  "Positions 1 to 6 read 19, 15, 11, 7, 3 and minus 1. Each of the five gaps subtracts 4.")
    terms = [19 - 4 * i for i in range(6)]
    for i in range(len(terms)):
        label(figure, 45 + i * 90, 61, f"Term {i + 1}", 13, MUTED)
    chain(figure, 92, [str(n).replace("-", "−") for n in terms], ["−4"] * 5)
    label(figure, 270, 137, "19 − 5 × 4 = −1", 17, BLUE_TEXT, "bold")
    return figure


def growing_jumps():
    figure = card(192, "Read the jumps between terms",
                  "Jumps of 3, 5, 7 and 9 take 2, 5, 10 and 17 to 26. Each jump is two larger than the last.")
    terms = [2]
    gaps = list(range(3, 10, 2))
    for gap in gaps:
        terms.append(terms[-1] + gap)
    chain(figure, 92, terms, [f"+{n}" for n in gaps])
    for i in range(len(gaps) - 1):
        x = 101.25 + i * 112.5
        figure.path(f"M{x},{114} v17 h112.5 v-17", stroke=ORANGE)
        label(figure, x + 56.25, 151, "+2", 14, ORANGE_TEXT, "bold")
    label(figure, 270, 175, "Each jump grows by 2.", 16, weight="bold")
    return figure


def repeat_slots():
    figure = card(199, "Find the slot inside the repeat",
                  "Five complete four-symbol blocks use positions 1 through 20. Position 23 is slot 3 of the sixth block.")
    for i in range(5):
        x = 70 + 100 * i
        token(figure, x, 76, f"Block {i + 1}", width=78)
        label(figure, x, 107, f"{1 + 4*i}–{4 + 4*i}", 14, MUTED)
    figure.line(22, 122, 518, 122, LINE)
    figure.text(26, 153, "Next block", 16, weight="bold")
    figure.text(26, 177, "23 = 5 × 4 + 3", 15, BLUE_TEXT, weight="bold")
    for slot in range(1, 5):
        x = 211 + (slot - 1) * 84
        token(figure, x, 149, 20 + slot, width=63,
              fill=BLUE_FILL if slot == 3 else GRAY_FILL, stroke=BLUE if slot == 3 else LINE)
        label(figure, x, 181, f"Slot {slot}", 14, BLUE_TEXT if slot == 3 else MUTED)
    return figure


def split_positions():
    figure = card(182, "Keep the original position numbers",
                  "Odd positions 1, 3 and 5 have values 2, 4 and 6. Even positions 2, 4 and 6 have values 12, 9 and 6.")
    for i in range(6):
        x = 139 + 65 * i
        label(figure, x, 64, i + 1, 15, MUTED)
        figure.line(x, 72, x, 152, LINE, dash="3 3")
    figure.text(22, 109, "Odd +2", 15, BLUE_TEXT, weight="bold")
    figure.text(22, 154, "Even −3", 15, ORANGE_TEXT, weight="bold")
    for i in range(3):
        token(figure, 139 + 130 * i, 103, 2 + 2 * i, fill=BLUE_FILL, stroke=BLUE)
        token(figure, 204 + 130 * i, 148, 12 - 3 * i, fill=ORANGE_FILL, stroke=ORANGE)
    return figure


def cross_growth():
    figure = card(244, "Grow four arms around one centre",
                  "Stage 1 is one tile. Stage 2 has a centre and four one-tile arms. Stage 3 has a centre and four two-tile arms.")
    step = 22
    for stage in range(1, 4):
        x = 93 + 177 * (stage - 1)
        y = 136
        label(figure, x, 62, f"Stage {stage}", 16, weight="bold")
        for distance in range(1, stage):
            for dx, dy in ((distance, 0), (-distance, 0), (0, distance), (0, -distance)):
                figure.rect(x + dx * step - 11, y + dy * step - 11, step, step, BLUE_FILL, BLUE)
        figure.rect(x - 11, y - 11, step, step, ORANGE_FILL, ORANGE, 2)
        label(figure, x, y + 5, "C", 13, ORANGE_TEXT, "bold")
        total = 1 + 4 * (stage - 1)
        label(figure, x, 219, f"1 + 4 × {stage - 1} = {total}", 16, weight="bold")
    return figure


def border_repeat():
    figure = card(151, "One repeat of the printed border",
                  "The five marks in order are leaf, star, wave, heart and dot.")
    marks = (
        ("Leaf", "M-13,8 Q-8,-14 13,-12 Q12,7 -9,10 Z", GREEN_FILL, GREEN),
        ("Star", "M0,-15 L4,-5 15,-5 7,2 10,13 0,7 -10,13 -7,2 -15,-5 -4,-5 Z", ORANGE_FILL, ORANGE),
        ("Wave", "M-16,3 Q-8,-9 0,3 Q8,15 16,3", "none", BLUE),
        ("Heart", "M0,13 C-23,-1 -10,-17 0,-7 C10,-17 23,-1 0,13 Z", ORANGE_FILL, ORANGE),
        ("Dot", "M-8,0 a8,8 0 1 0 16,0 a8,8 0 1 0 -16,0", INK, INK),
    )
    for i, (name, shape, fill, stroke) in enumerate(marks):
        x = 62 + 104 * i
        figure.rect(x - 40, 54, 80, 62, GRAY_FILL, LINE, rx=8)
        figure.add(f'<g transform="translate({x} 85)">')
        figure.path(shape, fill, stroke, 2)
        if name == "Leaf":
            figure.line(-13, 12, 7, -7, GREEN)
        figure.add("</g>")
        label(figure, x, 138, name, 15)
    return figure


def peg_frames():
    figure = card(204, "The first three peg frames",
                  "Figure 1 has one peg above two; figure 2 has two above three; figure 3 has three above four. Each has one separate handle peg.")
    for n in range(1, 4):
        x = 157 + 142 * (n - 1)
        label(figure, x, 63, f"Figure {n}", 16, weight="bold")
        figure.rect(x - 52, 76, 104, 107, GRAY_FILL, LINE, rx=8)
        for y, count in ((100, n), (129, n + 1)):
            for i in range(count):
                figure.circle(x + (i - (count - 1) / 2) * 21, y, 7, BLUE_FILL, BLUE, 2)
        figure.rect(x - 6, 152, 12, 12, ORANGE_FILL, ORANGE, 2, rx=2)
    for y, name in ((105, "Top"), (134, "Bottom"), (164, "Handle")):
        figure.text(21, y, name, 14, MUTED, weight="bold")
    return figure


def sticks():
    figure = card(183, "Use the shared stick once",
                  "A first square uses four sticks. Each added square keeps the existing shared side and adds three sticks.")
    side = 42
    for x, count in ((63, 1), (205, 2), (365, 3)):
        y = 70
        figure.rect(x, y, side, side, BLUE_FILL, BLUE, 3)
        for i in range(1, count):
            left = x + i * side
            figure.path(f"M{left},{y} h{side} v{side} h-{side}", stroke=ORANGE, sw=3)
        label(figure, x + count * side / 2, 137, "4" + " + 3" * (count - 1), 16, weight="bold")
    label(figure, 270, 165, "Eight squares use 4 + 7 × 3 = 25 sticks.", 16, BLUE_TEXT, "bold")
    return figure


def hexagons(show_joins=False):
    title = "Count each join once" if show_joins else "A straight row of touching hexagons"
    caption = ("Three hexagons have two shared sides. The separate count 18 counts two extra sides; the distinct count is 16."
               if show_joins else "Three hexagons in a row, with adjacent hexagons touching along an entire side.")
    figure = card(196 if show_joins else 152, title, caption)
    side = 30
    half_width = side * sqrt(3) / 2
    y = 95
    for i in range(3):
        x = 270 + 2 * half_width * (i - 1)
        figure.path(f"M{x},{y-side} L{x+half_width},{y-side/2} V{y+side/2} "
                    f"L{x},{y+side} L{x-half_width},{y+side/2} V{y-side/2} Z", BLUE_FILL, BLUE, 2)
    if show_joins:
        for direction in (-1, 1):
            x = 270 + direction * half_width
            figure.line(x, y - side / 2, x, y + side / 2, ORANGE, 4)
            figure.line(x, y + side / 2 + 3, x, 132, ORANGE)
        label(figure, 270, 151, "2 shared sides", 15, ORANGE_TEXT, "bold")
        label(figure, 270, 178, "3 × 6 − 2 = 16 distinct sides", 16, BLUE_TEXT, "bold")
    return figure


def matching_sums():
    figure = card(221, "Subtract the overlapping sums",
                  "The first four terms sum to 38. The last four sum to 54. Terms 2, 3 and 4 cancel; term 5 minus term 1 is 16.")
    for i, term in enumerate(("a₁", "a₂", "a₃", "a₄", "a₅")):
        x = 142 + i * 82
        label(figure, x, 66, f"Term {i + 1}", 13, MUTED)
        if i < 4:
            token(figure, x, 96, term, fill=GRAY_FILL if i else BLUE_FILL)
        if i > 0:
            token(figure, x, 143, term, fill=GRAY_FILL if i < 4 else ORANGE_FILL)
        if 0 < i < 4:
            figure.line(x, 113, x, 126, MUTED, dash="3 2")
    figure.text(24, 101, "Sum 38", 15, BLUE_TEXT, weight="bold")
    figure.text(24, 148, "Sum 54", 15, ORANGE_TEXT, weight="bold")
    label(figure, 270, 193, "Difference 16 across four gaps → 4 per gap", 16, weight="bold")
    return figure


def mirror_join():
    figure = card(210, "Look at the join after the second copy",
                  "The strip 12344321 is followed by its mirror copy, which also reads 12344321. Positions 8 and 9 are both 1.")
    seed = [1, 2, 3, 4]
    first_strip = seed + seed[::-1]
    full_strip = first_strip + first_strip[::-1]
    label(figure, 141, 64, "Strip after first copy", 15, BLUE_TEXT, "bold")
    label(figure, 399, 64, "Its mirror copy", 15, ORANGE_TEXT, "bold")
    figure.line(270, 75, 270, 164, MUTED, 1.4, dash="4 3")
    for i, value in enumerate(full_strip):
        x = 30 + i * 32
        at_join = i in (7, 8)
        fill = GREEN_FILL if at_join else BLUE_FILL if i < 8 else ORANGE_FILL
        token(figure, x, 102, value, width=28, fill=fill, stroke=GREEN if at_join else LINE)
        label(figure, x, 138, i + 1, 12, GREEN if at_join else MUTED, "bold" if at_join else "normal")
    label(figure, 270, 186, "Positions 8 and 9 are both 1.", 16, GREEN, "bold")
    return figure


def main():
    images = {
        "learn-count-gaps": count_gaps(),
        "learn-growing-jumps": growing_jumps(),
        "learn-repeat-slots": repeat_slots(),
        "learn-split-positions": split_positions(),
        "learn-cross-growth": cross_growth(),
        "q04-border-repeat": border_repeat(),
        "q13-peg-frames": peg_frames(),
        "q25-hexagons": hexagons(),
        "sol07-shared-stick": sticks(),
        "sol25-hexagon-joins": hexagons(show_joins=True),
        "sol27-matching-sums": matching_sums(),
        "sol29-mirror-join": mirror_join(),
    }
    for name, figure in images.items():
        figure.save(ASSETS / f"{name}.svg")


if __name__ == "__main__":
    main()
