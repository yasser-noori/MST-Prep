"""Regenerate the M2–M5 and S1–S5 study figures."""

from pathlib import Path

from m2_learning_figures import generate as generate_m2_learning
from svgkit import (
    BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE, MUTED,
    ORANGE, ORANGE_FILL, Fig,
)

ASSETS = Path(__file__).resolve().parents[2] / "assets"


def save(category, name, figure):
    directory = ASSETS / category
    directory.mkdir(parents=True, exist_ok=True)
    figure.save(directory / f"{name}.svg")


def card(width, height, title, description):
    fig = Fig(width, height, title, description)
    fig.text(24, 27, title, 17, weight="bold")
    return fig


def box(fig, x, y, width, label, fill=GRAY_FILL):
    fig.rect(x, y, width, 38, fill, LINE, rx=7)
    fig.text(x + width / 2, y + 24, label, 14, anchor="middle", weight="bold")


def chain(fig, labels, y, fills=()):
    step = (fig.w - 36) / len(labels)
    for index, label in enumerate(labels):
        x = 18 + index * step
        fill = fills[index] if fills else GRAY_FILL
        box(fig, x, y, step - 22, label, fill)
        if index < len(labels) - 1:
            fig.line(x + step - 20, y + 19, x + step - 3, y + 19, MUTED, arrow=True)


def geometry():
    generate_m2_learning()

    fig = card(400, 213, "Circle with centre O",
               "A and B lie on opposite sides of the circle. AB passes through O and is 14 cm long.")
    fig.circle(200, 114, 61, BLUE_FILL, BLUE, 2)
    fig.line(139, 114, 261, 114, INK, 2)
    for x, label, tx in [(139, "A", 120), (200, "O", 200), (261, "B", 280)]:
        fig.circle(x, 114, 3.2, INK, "none")
        fig.text(tx, 106, label, 15, anchor="middle", weight="bold")
    fig.text(200, 197, "AB = 14 cm", 15, anchor="middle")
    save("M2", "q01-circle", fig)

    fig = card(520, 237, "Trace the six outside edges",
               "The missing horizontal and vertical steps are 12 minus 7, or 5 m, and 8 minus 5, or 3 m.")
    fig.path("M120,64 H390 V144 H278 V192 H120 Z", BLUE_FILL, BLUE, 2)
    for x, y, text in [(255, 56, "12 m"), (415, 109, "5 m"), (332, 134, "5 m"),
                       (303, 177, "3 m"), (198, 215, "7 m"), (92, 134, "8 m")]:
        fig.text(x, y, text, 15, anchor="middle")
    save("M2", "sol04-garden", fig)


def algebra():
    fig = card(520, 151, "Rebuild the starting pile",
               "Add the 36 bookmarks handed out to the 58 left, giving 94 at the start.")
    fig.rect(35, 56, 450 * 58 / 94, 38, BLUE_FILL, BLUE)
    left = 35 + 450 * 58 / 94
    fig.rect(left, 56, 450 * 36 / 94, 38, ORANGE_FILL, ORANGE)
    fig.text((35 + left) / 2, 80, "58 left", 15, anchor="middle")
    fig.text((left + 485) / 2, 80, "4 × 9 = 36 given away", 15, anchor="middle")
    fig.text(260, 122, "Starting pile = 58 + 36 = 94", 15, GREEN, "middle", "bold")
    save("M3", "learn-bookmarks", fig)

    fig = card(500, 165, "Photo and borders",
               "The left border is b cm, the right border is 2b cm, and the total width is 30 cm.")
    for x, width, label, fill in [
        (30, 65, "b cm", ORANGE_FILL), (95, 245, "Visible photo", BLUE_FILL),
        (340, 130, "2b cm", ORANGE_FILL)
    ]:
        fig.rect(x, 51, width, 53, fill, INK)
        fig.text(x + width / 2, 84, label, 15, anchor="middle")
    fig.path("M30,115 V125 H470 V115", stroke=MUTED)
    fig.text(250, 146, "30 cm total", 14, anchor="middle")
    save("M3", "q27-frame", fig)

    fig = card(530, 157, "Undo the transfer",
               "Mina had 22 and Dev had 14. Moving 4 makes both piles 18.")
    for y, label, left, right in [(65, "Before", 22, 14), (116, "After", 18, 18)]:
        fig.text(26, y + 4, label, 14, weight="bold")
        box(fig, 98, y - 19, 158, f"Mina: {left}", BLUE_FILL)
        box(fig, 365, y - 19, 138, f"Dev: {right}", ORANGE_FILL)
    fig.line(263, 65, 357, 65, MUTED, arrow=True)
    fig.text(310, 55, "Move 4", 13, anchor="middle")
    save("M3", "sol07-transfer", fig)


def sequences():
    fig = card(600, 151, "Count high notes on their own",
               "High notes at positions 1, 3, 5, 7 and 9 last 3, 5, 7, 9 and 11 beats. Each low note lasts 1 beat.")
    for index in range(9):
        x = 24 + 62 * index
        high = index % 2 == 0
        fill = BLUE_FILL if high else GRAY_FILL
        box(fig, x, 60, 54, f"{3 + index if high else 1} beats" if high else "1 beat", fill)
        fig.text(x + 27, 51, str(index + 1), 13, MUTED, "middle")
    fig.text(24, 127, "High notes occupy odd positions. Their lengths increase by 2 beats each time.", 14)
    save("M4", "learn-high-notes", fig)

    fig = card(480, 145, "First three stick figures",
               "One, two and three squares in a straight row, each neighbouring pair sharing its side.")
    for count, x in enumerate((49, 167, 313), 1):
        y, side = 58, 32
        fig.rect(x, y, side * count, side, BLUE_FILL, BLUE, 2)
        for index in range(1, count):
            edge = x + side * index
            fig.line(edge, y, edge, y + side, BLUE, 2)
        fig.text(x + side * count / 2, 116, f"{count} " + ("square" if count == 1 else "squares"), 14, anchor="middle")
    save("M4", "q07-squares", fig)

    fig = card(568, 158, "The fourth card separates the rules",
               "Both begin 4, 9, 17. Rule P then adds 11 to get 28, while Q adds 5 to get 22.")
    chain(fig, ["4", "9  (+5)", "17  (+8)", "P: 28  (+11)"], 47,
          [GRAY_FILL, GRAY_FILL, GRAY_FILL, GREEN_FILL])
    chain(fig, ["4", "9  (+5)", "17  (+8)", "Q: 22  (+5)"], 102,
          [GRAY_FILL, GRAY_FILL, GRAY_FILL, ORANGE_FILL])
    save("M4", "sol05-fourth-card", fig)


def logic():
    fig = card(620, 106, "Apply both rules to the same setting",
               "Star on means R off, leaving settings 1, 4 and 5. P and Q match only in setting 4.")
    chain(fig, ["All five settings", "R OFF: 1, 4, 5", "P = Q: setting 4"], 48,
          [GRAY_FILL, BLUE_FILL, GREEN_FILL])
    save("M5", "learn-settings", fig)

    fig = card(500, 177, "One-way shuttle links",
               "Hub leads to North and South. North leads to Hall. South leads to Park, which leads to Hall.")
    for x1, y1, x2, y2 in [(103, 100, 146, 70), (103, 107, 146, 132),
                           (239, 68, 391, 99), (239, 132, 269, 132),
                           (361, 132, 391, 112)]:
        fig.line(x1, y1, x2, y2, MUTED, arrow=True)
    for x, y, label in [(23, 84, "Hub"), (150, 49, "North"), (150, 114, "South"),
                        (273, 114, "Park"), (395, 84, "Hall")]:
        box(fig, x, y, 86, label, BLUE_FILL)
    save("M5", "q13-shuttle", fig)

    fig = card(540, 126, "One arrangement that satisfies every clue",
               "Chairs 1 to 5 hold Noor, Ivo, Kai, Bea and Val, respectively.")
    for index, name in enumerate(["Noor", "Ivo", "Kai", "Bea", "Val"]):
        x = 25 + index * 102
        box(fig, x, 62, 82, name, BLUE_FILL if name in {"Bea", "Val"} else GRAY_FILL)
        fig.text(x + 41, 52, str(index + 1), 14, MUTED, "middle")
    save("M5", "sol09-chairs", fig)


def ecology():
    fig = card(555, 106, "Kelp forest food chain",
               "Kelp is eaten by sea urchins, which are eaten by sea otters. Arrows go from food to eater.")
    chain(fig, ["Kelp", "Sea urchin", "Sea otter"], 48, [GREEN_FILL, ORANGE_FILL, BLUE_FILL])
    save("S1", "learn-kelp-chain", fig)

    fig = card(520, 106, "Who eats whom in the field",
               "Seeds are eaten by mice, mice by snakes, and snakes by hawks.")
    chain(fig, ["Seeds", "Mouse", "Snake", "Hawk"], 48)
    save("S1", "q01-field-chain", fig)

    fig = card(590, 152, "Follow the indirect effect",
               "Fewer foxes can lead to more rabbits, less grass and less food for grasshoppers.")
    chain(fig, ["Fewer foxes", "More rabbits", "Less grass", "Less food"], 47,
          [BLUE_FILL, ORANGE_FILL, GREEN_FILL, GRAY_FILL])
    fig.text(24, 115, "Rabbits and grasshoppers use the same grass.", 15)
    fig.text(24, 136, "Grasshoppers may lose food even though foxes do not eat them.", 14, MUTED)
    save("S1", "sol06-shared-grass", fig)


def chromosomes(name, title, labels, nucleus, chromosome, neighbours=()):
    left_label, right_label = labels
    fig = card(584, 186, title,
               f"{nucleus}. The enlarged DNA strand marks two distinct segments: {left_label} and {right_label}.")
    fig.circle(89, 112, 56, BLUE_FILL, BLUE, 2)
    chromosome_labels = [(110, chromosome, ORANGE)]
    chromosome_labels.extend((y, label, MUTED) for y, label in zip((81, 139), neighbours))
    for y, label, color in chromosome_labels:
        fig.line(55, y, 105, y, color, 3)
        fig.text(118, y + 5, label, 14, anchor="middle")
    fig.text(89, 178, "Nucleus", 13, MUTED, "middle")
    fig.line(154, 110, 206, 110, MUTED, arrow=True)
    fig.text(180, 99, "Zoom", 13, MUTED, "middle")
    fig.line(225, 110, 554, 110, INK, 2)
    for x, label, fill in [(246, left_label, BLUE_FILL), (411, right_label, ORANGE_FILL)]:
        fig.rect(x, 100, 85, 20, fill, INK, rx=5)
        fig.line(x + 42.5, 120, x + 42.5, 136, MUTED)
        fig.text(x + 42.5, 153, label, 14, anchor="middle")
    save("S2", name, fig)


def cells():
    chromosomes("learn-gene-segments", "Two stretches on chromosome 3",
                ("K1: fur colour", "K2: claw length"), "Chromosome 3 inside a nucleus", "3")
    chromosomes("q02-chromosome-q", "Zoom in on chromosome Q",
                ("Scale pattern", "Claw protein"), "The nucleus contains chromosomes P, Q and R",
                "Q", ("P", "R"))

    fig = card(400, 206, "Four equally likely pairs",
               "A Bb parent contributes B or b. The four pairs are BB, Bb, bB and bb. Only bb gives brown.")
    for x, text in [(191, "B"), (309, "b")]:
        fig.text(x, 59, text, 16, anchor="middle", weight="bold")
    for y, row in [(73, "B"), (119, "b")]:
        fig.text(98, y + 25, row, 16, anchor="middle", weight="bold")
        for x, column in [(140, "B"), (258, "b")]:
            pair = row + column
            box(fig, x, y, 102, pair, GREEN_FILL if pair == "bb" else GRAY_FILL)
    fig.text(24, 184, "One brown outcome out of four equally likely pairs.", 14)
    save("S2", "sol09-pair-grid", fig)


def cylinders(name, title, readings, objects, note=None):
    description = "; ".join(f"{label}: {reading} mL" for label, reading in readings)
    fig = card(520, 221, title, description + (f". {note}" if note else "."))
    card_max = max(reading for _, reading in readings)
    for index, (label, reading) in enumerate(readings):
        x = 156 + index * 205
        level = 157 - 76 * reading / card_max
        fig.rect(x - 31, level, 62, 157 - level, BLUE_FILL, "none")
        fig.path(f"M{x - 31},66 V157 H{x + 31} V66", stroke=INK, sw=2)
        fig.line(x - 31, level, x + 31, level, BLUE, 2)
        sample = objects[index]
        if sample == "counter":
            fig.rect(x - 12, 132, 24, 12, ORANGE_FILL, ORANGE, 2, rx=3)
        elif sample == "pebble":
            fig.path(f"M{x - 11},146 q-4,-10 7,-15 q13,-4 16,10 q-5,10 -23,5 Z",
                     ORANGE_FILL, ORANGE, 2)
        elif sample in {"sinker", "cork and sinker"}:
            if sample == "cork and sinker":
                fig.line(x, 122, x, 140, MUTED, dash="3 2")
                fig.rect(x - 10, 110, 20, 12, ORANGE_FILL, ORANGE, 2, rx=3)
            fig.circle(x, 142, 8, GRAY_FILL, INK, 2)
        fig.text(x - 42, level + 4, f"{reading} mL", 14, anchor="end")
        fig.text(x, 179, label, 14, anchor="middle")
    if note:
        fig.text(260, 204, note, 14, GREEN, "middle", "bold")
    save("S3", name, fig)


def fluids():
    cylinders("learn-counter", "Compare the two cylinder readings",
              [("Water alone", 42), ("Counter submerged", 66)], [None, "counter"])
    cylinders("q01-pebble", "Water levels before and after",
              [("Water alone", 26), ("Pebble submerged", 39)], [None, "pebble"])
    cylinders("sol03-cork", "Measure the extra rise from the cork",
              [("Sinker already in", 46), ("Sinker and cork in", 62)], ["sinker", "cork and sinker"],
              "Cork volume = 62 − 46 = 16 cm³")


def lamp(fig, x, y, label):
    fig.circle(x, y, 13, ORANGE_FILL, INK)
    fig.line(x - 6, y - 6, x + 6, y + 6)
    fig.line(x - 6, y + 6, x + 6, y - 6)
    fig.text(x, y - 19, label, 14, anchor="middle")


def switch(fig, x, y, label, state=None):
    if state is None:
        fig.rect(x - 17, y - 10, 34, 20, BLUE_FILL, BLUE, rx=3)
        fig.text(x, y + 5, label, 13, anchor="middle", weight="bold")
    else:
        fig.circle(x - 17, y, 3.2, INK)
        fig.circle(x + 17, y, 3.2, INK)
        fig.line(x - 17, y, x + 17, y - (0 if state else 12), INK, 2)
        fig.text(x, y + 25, f"{label} {'closed' if state else 'open'}", 14, anchor="middle")


def circuits():
    fig = card(550, 192, "Two branches share one switch",
               "Positive terminal to M, then a split. The upper branch has P and Desk, the lower Q and Shelf. They rejoin at the negative terminal.")
    fig.path("M49,91 H112 M146,91 H266 M300,91 H364 M390,91 H501 M217,91 V155 H266 M300,155 H364 M390,155 H445 V91",
             stroke=INK, sw=2)
    for x, label in [(37, "+"), (516, "−")]:
        fig.circle(x, 91, 11, GRAY_FILL, INK)
        fig.text(x, 96, label, 16, anchor="middle")
    for x in (217, 445):
        fig.circle(x, 91, 4, INK, "none")
    for x, y, label in [(129, 91, "M"), (283, 91, "P"), (283, 155, "Q")]:
        switch(fig, x, y, label)
    lamp(fig, 377, 91, "Desk")
    lamp(fig, 377, 155, "Shelf")
    save("S4", "learn-reading-lamp", fig)

    fig = card(525, 145, "Battery, two switches and a lamp",
               "In order from positive to negative: P closed, lamp, Q open.")
    fig.path("M48,85 H118 M152,85 H250 M276,85 H371 M405,85 H474", stroke=INK, sw=2)
    for x, label in [(36, "+"), (486, "−")]:
        fig.circle(x, 85, 11, GRAY_FILL, INK)
        fig.text(x, 90, label, 16, anchor="middle")
    switch(fig, 135, 85, "P", True)
    lamp(fig, 263, 85, "Lamp")
    switch(fig, 388, 85, "Q", False)
    save("S4", "q01-series-break", fig)

    s = {2, 3, 6, 8}
    t = set(range(3, 8))
    fig = card(590, 197, "The beacon needs both contacts closed",
               "S closes at seconds 2, 3, 6 and 8. T closes at 3 through 7. The beacon lights at 3 and 6.")
    for second in range(1, 9):
        x = 155 + 54 * (second - 1)
        fig.text(x, 58, str(second), 14, anchor="middle")
        for y, closed in [(80, s), (120, t), (160, s & t)]:
            yes = second in closed
            fill = GREEN_FILL if y == 160 and yes else BLUE_FILL if yes else GRAY_FILL
            fig.rect(x - 22, y - 14, 44, 29, fill, LINE, rx=4)
            fig.text(x, y + 5, "Yes" if yes else "–", 13, anchor="middle")
    for y, label in [(58, "Second"), (85, "S closed"), (125, "T closed"), (165, "Beacon lit")]:
        fig.text(25, y, label, 14, weight="bold")
    save("S4", "sol26-contact-timing", fig)


def beam(name, title, loads, endpoints, note=None):
    lo, hi = endpoints
    description = ", ".join(f"{force} N at {mark_label(pos)}" for pos, force, _ in loads)
    fig = card(558, 190, title, f"Pivot at 0, with {description}." + (f" {note}" if note else ""))
    interval = 454 / (hi - lo)
    def x_at(position):
        return 52 + (position - lo) * interval

    fig.line(x_at(lo) - 13, 104, x_at(hi) + 13, 104, INK, 3)
    for index in range(lo, hi + 1):
        x = x_at(index)
        fig.line(x, 99, x, 110, INK, 2)
        fig.text(x, 127, mark_label(index), 14, anchor="middle")
    for pos, force, color in loads:
        x = x_at(pos)
        fig.line(x, 72, x, 96, color, 2, arrow=True)
        fig.text(x, 64, f"{force} N", 15, color, "middle", "bold")
    pivot = x_at(0)
    fig.path(f"M{pivot},132 l-9,15 h18 Z", GRAY_FILL, INK)
    fig.text(pivot, 165, "Pivot", 13, MUTED, "middle")
    if note:
        fig.text(24, 181, note, 14, GREEN, weight="bold")
    save("S5", name, fig)


def mark_label(position):
    return f"L{-position}" if position < 0 else f"R{position}" if position > 0 else "0"


def forces():
    beam("learn-beam", "Compare both turns around the pivot",
         [(-2, 6, BLUE), (3, 2, ORANGE)], (-3, 3))
    beam("q01-beam", "Starting load on the beam",
         [(-3, 4, BLUE)], (-3, 4))
    beam("sol01-balanced-beam", "Equal turning effects",
         [(-3, 4, BLUE), (2, 6, ORANGE)], (-3, 4),
         "Left: 4 × 3 = 12 N-marks  |  Right: 6 × 2 = 12 N-marks")


if __name__ == "__main__":
    for draw in (geometry, algebra, sequences, logic, ecology, cells, fluids, circuits, forces):
        draw()
