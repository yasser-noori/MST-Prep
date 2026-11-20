"""Build the supplementary M5 logic and constraints diagrams."""

from pathlib import Path

from svgkit import (
    BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE,
    MUTED, ORANGE, ORANGE_FILL, Fig,
)

ASSETS = Path(__file__).resolve().parents[2] / "assets" / "M5"


def card(width, height, title, description):
    fig = Fig(width, height, title, description)
    fig.text(24, 29, title, 18, weight="bold")
    return fig


def cell(fig, x, y, width, label, fill=GRAY_FILL, stroke=LINE, height=36):
    fig.rect(x, y, width, height, fill, stroke, rx=6)
    fig.text(x + width / 2, y + height / 2 + 5, label, 15, anchor="middle")


def table(fig, x, y, widths, headers, rows, fills=None):
    for index, (values, row_fills) in enumerate(zip(
        [headers] + rows,
        [None] + (fills or [None] * len(rows)),
        strict=True,
    )):
        left = x
        for j, (width, value) in enumerate(zip(widths, values, strict=True)):
            fill = row_fills[j] if row_fills else GRAY_FILL if index == 0 else "#ffffff"
            cell(fig, left, y + 38 * index, width - 4, value, fill, height=34)
            left += width


def learning_forward():
    fig = card(588, 208, "Test each rule with the same inputs",
               "At least one and exactly one both pass with one ON input. With two ON inputs, "
               "at least one and both pass, while exactly one fails.")
    table(fig, 24, 49, [110, 146, 145, 123],
          ("ON inputs", "At least one", "Exactly one", "Both"),
          [("0", "No", "No", "No"), ("1", "Yes", "Yes", "No"), ("2", "Yes", "No", "Yes")],
          [[GRAY_FILL] + ["#ffffff"] * 3,
           [GRAY_FILL, GREEN_FILL, GREEN_FILL, "#ffffff"],
           [GRAY_FILL, GREEN_FILL, ORANGE_FILL, GREEN_FILL]])
    return fig


def learning_backward():
    fig = card(542, 184, "Start with the observed light",
               "If the light comes on when inputs match, work backward to two possibilities: "
               "both ON or both OFF. Another clue is needed to distinguish them.")
    cell(fig, 26, 91, 167, "Matching light is on", BLUE_FILL, BLUE)
    cell(fig, 302, 56, 210, "ON and ON")
    cell(fig, 302, 126, 210, "OFF and OFF")
    for dest in (74, 144):
        fig.line(205, 109, 289, dest, MUTED, 1.5, arrow=True)
    return fig


def learning_order():
    fig = card(568, 211, "Draw extra space when the clue allows it",
               "Bea immediately before Kai means neighbouring positions; Bea before Kai "
               "allows either neighbouring positions or an intervening position.")
    fig.text(24, 68, "Immediately before", 15, weight="bold")
    fig.text(24, 155, "Before", 15, weight="bold")
    for x, y, labels in [(200, 50, ("Bea", "Kai")), (200, 137, ("Bea", "…", "Kai"))]:
        for i, label in enumerate(labels):
            fill = ORANGE_FILL if label == "…" else BLUE_FILL
            cell(fig, x + 108 * i, y, 103, label, fill)
    fig.text(200, 108, "The two places touch.", 14, MUTED)
    fig.text(200, 195, "Other places may lie between them.", 14, MUTED)
    return fig


def learning_proof():
    fig = card(606, 184, "Match your check to the question",
               "Could: find one valid arrangement. Must: check whether any valid arrangement breaks the claim. "
               "Enough information: check whether every valid arrangement gives the same answer.")
    for index, (kind, check) in enumerate([
        ("Could", "Find one arrangement that works."),
        ("Must", "Try to find an arrangement that breaks the claim."),
        ("Enough information?", "Compare the answer across all valid arrangements."),
    ]):
        y = 48 + 43 * index
        cell(fig, 24, y, 164, kind, BLUE_FILL)
        fig.text(205, y + 24, check, 15)
    return fig


def q04_calendar():
    fig = card(594, 133, "Mira’s half-hour slots",
               "From 9:00 through 11:30 in order: free, busy, free, free, busy, free.")
    slots = [("9:00", True), ("9:30", False), ("10:00", True),
             ("10:30", True), ("11:00", False), ("11:30", True)]
    for index, (time, free) in enumerate(slots):
        x = 25 + 92 * index
        cell(fig, x, 52, 88, "Free" if free else "Busy", BLUE_FILL if free else GRAY_FILL)
        fig.text(x + 44, 108, time, 15, anchor="middle")
    return fig


def q20_matches():
    fig = card(563, 214, "One game for each pair of teams",
               "Ash beat Birch, Cedar and Dune. Birch beat Cedar and Cedar beat Dune. "
               "The Birch–Dune result has not been given.")
    table(fig, 24, 51, [98, 137, 137, 137], ("Match", "Birch", "Cedar", "Dune"), [
        ("Ash", "Ash won", "Ash won", "Ash won"),
        ("Birch", "—", "Birch won", "?"),
        ("Cedar", "—", "—", "Cedar won"),
    ])
    return fig


def q27_strip():
    fig = card(500, 143, "The strip after both presses",
               "Six squares are labelled 1 to 6. Squares 2, 3 and 4 are black, and squares 1, 5 and 6 are white.")
    for number in range(1, 7):
        x = 38 + (number - 1) * 71
        fig.rect(x, 52, 68, 49, INK if 2 <= number <= 4 else "#ffffff", INK, rx=3)
        fig.text(x + 34, 123, number, 15, anchor="middle")
    return fig


def sol03_filters():
    fig = card(576, 147, "Filter the rows by what each light shows",
               "A dark dot keeps only rows 3 and 4 because Y matches Z. "
               "A lit square then keeps only row 3 because X differs from Y.")
    for x, heading, label, fill in [
        (24, "Possible inputs", "Rows 1, 2, 3, 4, 5", GRAY_FILL),
        (218, "Dark dot: Y = Z", "Rows 3 and 4", BLUE_FILL),
        (412, "Lit square: X ≠ Y", "Row 3", GREEN_FILL),
    ]:
        fig.text(x, 68, heading, 14, weight="bold")
        cell(fig, x, 81, 138, label, fill)
    for x in (174, 368):
        fig.line(x, 99, x + 31, 99, MUTED, 1.5, arrow=True)
    return fig


def sol22_neighbours():
    fig = card(555, 206, "Check the three edge neighbours of X",
               "Cells a, b and d share an edge with X. Cell a shares Y’s column, "
               "cell b is in the rightmost column, and d passes both checks.")
    for row, labels in enumerate((("a", "X", "b"), ("c", "d", "e"), ("Y", "f", "g"))):
        for col, label in enumerate(labels):
            fill = (ORANGE_FILL if label in {"a", "b"} else GREEN_FILL if label == "d"
                    else BLUE_FILL if label in {"X", "Y"} else GRAY_FILL)
            cell(fig, 25 + 47 * col, 53 + 47 * row, 43, label, fill, height=43)
    for y, name, reason, fill in [
        (54, "a", "Shares Y’s column", ORANGE_FILL),
        (101, "b", "In the rightmost column", ORANGE_FILL),
        (148, "d", "Outside both excluded columns", GREEN_FILL),
    ]:
        cell(fig, 202, y, 38, name, fill, height=39)
        fig.text(253, y + 26, reason, 15)
    return fig


def sol26_overlap():
    fig = card(580, 289, "Count the overlap once",
               "Of nine metal objects, six are metal only and three are in both groups. "
               "Of seven objects from the 1800s, four are from the 1800s only. The total is 6 + 3 + 4 = 13.")
    fig.text(208, 62, "Metal · 9 total", 15, BLUE, "middle", "bold")
    fig.text(372, 62, "From the 1800s · 7 total", 15, ORANGE, "middle", "bold")
    fig.circle(235, 154, 87, BLUE_FILL, BLUE, 2)
    fig.circle(345, 154, 87, ORANGE_FILL, ORANGE, 2)
    fig.path("M290,86.6 A87,87 0 0 1 290,221.4 A87,87 0 0 1 290,86.6 Z",
             GREEN_FILL, GREEN, 1.3)
    for x, total, label in [(209, "6", "Metal only"), (290, "3", "Both"), (369, "4", "1800s only")]:
        fig.text(x, 153, total, 28, anchor="middle", weight="bold")
        fig.text(x, 178, label, 14, anchor="middle")
    fig.text(290, 268, "6 + 3 + 4 = 13 distinct objects", 17, GREEN, "middle", "bold")
    return fig


def sol27_stencil():
    fig = card(562, 216, "The two presses share square 3",
               "One press covers squares 2 and 3. The other covers squares 3 and 4. "
               "Square 3 belongs to both pairs.")
    for index in range(6):
        x = 166 + 61 * index
        fig.text(x + 27, 63, index + 1, 14, MUTED, "middle")
    for y, first, fill, stroke in [
        (78, 2, BLUE_FILL, BLUE), (125, 3, ORANGE_FILL, ORANGE),
    ]:
        fig.text(25, y + 24, f"Cover {first} and {first + 1}", 15, weight="bold")
        for number in range(1, 7):
            x = 166 + 61 * (number - 1)
            active = number in (first, first + 1)
            fig.rect(x, y, 54, 36, fill if active else "#ffffff", stroke if active else LINE, rx=5)
            if active:
                fig.tick(x + 27, y + 18, 6, stroke, 2)
    x = 166 + 2 * 61
    fig.rect(x - 4, 73, 62, 93, "none", GREEN, 2, rx=7, dash="5 3")
    fig.text(x + 27, 192, "Painted twice", 15, GREEN, "middle", "bold")
    return fig


def sol29_tree():
    fig = card(635, 252, "Use the second test only after gold",
               "Start with the lamp test. Blue identifies L, and pink identifies M. "
               "For gold, use the drop test: fast identifies J and slow identifies K.")
    cell(fig, 24, 109, 115, "Lamp test", BLUE_FILL, BLUE)
    cell(fig, 277, 52, 137, "Fabric L", GREEN_FILL, GREEN)
    cell(fig, 277, 109, 137, "Drop test", ORANGE_FILL, ORANGE)
    cell(fig, 277, 166, 137, "Fabric M", GREEN_FILL, GREEN)
    for y, word, text_y in [(70, "Blue", 79), (127, "Gold", 117), (184, "Pink", 172)]:
        fig.line(148, 127, 266, y, MUTED, 1.5, arrow=True)
        fig.text(222 if word == "Gold" else 198, text_y, word, 14, anchor="middle")
    for y, word, letter in [(97, "Fast", "J"), (157, "Slow", "K")]:
        cell(fig, 522, y - 18, 88, f"Fabric {letter}", GREEN_FILL, GREEN)
        fig.line(422, 127, 511, y, MUTED, 1.5, arrow=True)
        fig.text(461, y - 7 if y < 127 else y + 16, word, 14, anchor="middle")
    fig.text(24, 229, "Worst case: two tests", 15, weight="bold")
    return fig


def sol30_trace():
    fig = card(610, 177, "Skip the card, including its instruction",
               "READ 4 adds four. The first SKIP steps over the second SKIP. READ 2 and READ 1 "
               "then run, bringing the total from four to six to seven.")
    for index, (label, total, fill) in enumerate([
        ("READ 4", "4", BLUE_FILL), ("SKIP", "4", ORANGE_FILL), ("SKIP", "Skipped", GRAY_FILL),
        ("READ 2", "6", BLUE_FILL), ("READ 1", "7", GREEN_FILL),
    ]):
        x = 116 + 94 * index
        cell(fig, x, 86, 89, label, fill)
        fig.text(x + 44, 148, total, 14, anchor="middle")
    fig.path("M255,81 V63 H443 V79", stroke=MUTED, sw=1.5)
    fig.line(443, 69, 443, 80, MUTED, 1.5, arrow=True)
    fig.text(349, 57, "Skip one card", 14, MUTED, "middle")
    fig.text(25, 148, "Total", 15, weight="bold")
    return fig


def main():
    figures = {
        "learn-forward-rules": learning_forward,
        "learn-backward-rules": learning_backward,
        "learn-neighbouring-slots": learning_order,
        "learn-proof": learning_proof,
        "q04-calendar": q04_calendar,
        "q20-matches": q20_matches,
        "q27-strip": q27_strip,
        "sol03-filters": sol03_filters,
        "sol22-neighbours": sol22_neighbours,
        "sol26-overlap": sol26_overlap,
        "sol27-stencil": sol27_stencil,
        "sol29-test-tree": sol29_tree,
        "sol30-card-trace": sol30_trace,
    }
    for filename, draw in figures.items():
        draw().save(ASSETS / f"{filename}.svg")


if __name__ == "__main__":
    main()
