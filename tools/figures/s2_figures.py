"""Generate the S2 cells, inheritance, and evidence diagrams."""

from pathlib import Path
from math import pi, sin

from svgkit import (
    BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE, MUTED,
    ORANGE, ORANGE_FILL, Fig,
)


OUT = Path(__file__).resolve().parents[2] / "assets" / "S2"


def card(width, height, title, description):
    fig = Fig(width, height, title, description)
    fig.text(22, 28, title, 17, weight="bold")
    return fig


def label(fig, x, y, text, size=14, colour=INK, bold=False):
    fig.text(x, y, text, size, colour, anchor="middle", weight="bold" if bold else "normal")


def panel(fig, x, y, width, height, fill=GRAY_FILL):
    fig.rect(x, y, width, height, fill, LINE, rx=8)


def leaf_pattern(fig, cx, cy, radius=6):
    fig.circle(cx, cy, radius, GREEN_FILL, GREEN, 1.4)
    fig.line(cx - radius + 2, cy, cx + radius - 2, cy, GREEN, 1.2)


def strand(fig, x, y, width, height, colour=BLUE):
    points = [(x + width * step / 24, height * sin(step * pi / 6)) for step in range(25)]
    for step in range(0, 25, 2):
        px, py = points[step]
        fig.line(px, y - py, px, y + py, LINE)
    for sign in (1, -1):
        path = " ".join(f"{px:.1f},{y + sign * py:.1f}" for px, py in points)
        fig.path(f"M{path}", stroke=colour, sw=1.8)


def hierarchy():
    fig = card(646, 208, "From the whole cell to one gene",
               "The cell contains a nucleus. Its nucleus holds chromosomes. A chromosome contains packaged DNA, and a gene is a short stretch of that DNA.")
    centres = (83, 232, 381, 545)
    for x, title, subtitle in zip(
        centres,
        ("Cell", "Nucleus", "Chromosome", "DNA and gene"),
        ("Contains a nucleus", "Holds chromosomes", "Contains packaged DNA", "A gene is a short stretch"),
    ):
        panel(fig, x - 63, 48, 126, 135)
        label(fig, x, 149, title, bold=True)
        label(fig, x, 169, subtitle, 10, MUTED)
    for start, end in zip(centres, centres[1:]):
        fig.line(start + 67, 104, end - 67, 104, MUTED, arrow=True)

    fig.circle(83, 101, 34, BLUE_FILL, BLUE, 2)
    fig.circle(87, 99, 13, ORANGE_FILL, ORANGE, 2)
    fig.circle(232, 101, 31, ORANGE_FILL, ORANGE, 2)
    for x, y, dy in ((214, 99, 8), (225, 86, 10), (239, 103, -7)):
        fig.path(f"M{x},{y} q7,{dy * 2} 14,{dy}", stroke=INK, sw=3)
    fig.path("M350,115 q14,-42 26,-17 t34,-12", stroke=INK, sw=8)
    fig.rect(522, 80, 47, 43, ORANGE_FILL, ORANGE, rx=4)
    strand(fig, 496, 102, 98, 10)
    label(fig, 545, 75, "Gene", 11, ORANGE, True)
    return fig


def cell_types():
    fig = card(664, 257, "Compare typical cells from three tissues",
               "All three examples have a cell membrane and nucleus. The leaf and root cells have a wall. Only the photosynthetic leaf cell has chloroplasts.")
    for cx, name in ((120, "Photosynthetic leaf"), (332, "Underground root"), (544, "Animal cheek")):
        panel(fig, cx - 100, 44, 200, 161)
        label(fig, cx, 67, name, 14, bold=True)
        if name == "Animal cheek":
            fig.path(f"M{cx - 60},136 c-13,-35 72,-57 119,-24 c32,31 -25,71 -80,58 q-35,-8 -39,-34 Z",
                     BLUE_FILL, BLUE, 2.5)
        else:
            fig.rect(cx - 66, 86, 132, 91, "#ffffff", INK, 3, rx=11)
            fig.rect(cx - 58, 94, 116, 75, BLUE_FILL, BLUE, 2.4, rx=9)
        fig.circle(cx - 10, 131, 17, ORANGE_FILL, ORANGE, 2)
        if name == "Photosynthetic leaf":
            for dx, dy in ((-39, -22), (38, -18), (40, 15), (-37, 23)):
                leaf_pattern(fig, cx + dx, 130 + dy, 8)
    fig.line(28, 228, 46, 228, INK, 3)
    fig.text(54, 233, "Cell wall", 13)
    fig.line(156, 228, 174, 228, BLUE, 2.5)
    fig.text(182, 233, "Cell membrane", 13)
    fig.circle(328, 228, 7, ORANGE_FILL, ORANGE)
    fig.text(340, 233, "Nucleus", 13)
    leaf_pattern(fig, 452, 228, 7)
    fig.text(465, 233, "Chloroplast", 13)
    return fig


def inheritance():
    fig = card(630, 258, "Use one copy from each parent",
               "Rr supplies R or r. The rr parent supplies r in both rows. The four combinations are Rr, rr, Rr, and rr, making two red and two white possibilities.")
    label(fig, 196, 62, "Copies from the Rr parent", 14, bold=True)
    fig.text(30, 103, "Copies", 13, MUTED)
    fig.text(30, 120, "from the", 13, MUTED)
    fig.text(30, 137, "rr parent", 13, MUTED)
    for column, copy in enumerate(("R", "r")):
        label(fig, 155 + column * 91, 86, copy, 16, bold=True)
    for row in range(2):
        label(fig, 111, 122 + row * 44, "r", 16, bold=True)
        for column, (pair, colour, fill) in enumerate(
            (("Rr", "Red", ORANGE_FILL), ("rr", "White", GRAY_FILL))
        ):
            x = 121 + column * 91
            y = 95 + row * 44
            panel(fig, x, y, 68, 36, fill)
            label(fig, x + 34, y + 16, pair, 15, bold=True)
            label(fig, x + 34, y + 30, colour, 11, MUTED)
    panel(fig, 329, 71, 275, 123, BLUE_FILL)
    fig.text(352, 100, "Four equally likely combinations", 14, weight="bold")
    fig.text(352, 129, "2 of 4 have Rr → red", 15)
    fig.text(352, 156, "2 of 4 have rr → white", 15)
    fig.text(29, 226, "For the white offspring, both parents supplied r.", 15, fill=MUTED)
    return fig


def fair_comparison():
    fig = card(628, 240, "Design a comparison about water",
               "Randomly assign seedlings to groups. Where just water changes and light stays fixed, the comparison can test water. Where water and light both change, their effects are mixed.")
    panel(fig, 22, 52, 282, 162)
    panel(fig, 324, 52, 282, 162)
    for x, title, second_light, inference in (
        (34, "One factor varies", "Bright light", "Can test the effect of water"),
        (336, "Two factors vary", "Dim light", "Water and light are mixed"),
    ):
        fig.text(x + 8, 76, title, 15, weight="bold")
        for index, (water, light) in enumerate((("More water", "Bright light"), ("Less water", second_light))):
            cx = x + index * 131
            panel(fig, cx, 91, 122, 73, "#ffffff")
            label(fig, cx + 61, 110, f"Group {index + 1}", 12, MUTED)
            label(fig, cx + 61, 131, water, 14, BLUE, True)
            label(fig, cx + 61, 151, light, 13, ORANGE if light == "Dim light" else INK)
        fig.text(x + 8, 192, inference, 14, weight="bold")
    fig.text(23, 231, "Randomly assign seedlings in both comparisons.", 13, MUTED)
    return fig


def randomized_split():
    fig = card(620, 260, "Seedling groups after three weeks",
               "Sixty seeds from one parent are randomly assigned to two groups of 30. At the same soil, water and temperature, the bright group averages 12 cm and the dim group averages 7 cm.")
    panel(fig, 187, 46, 246, 43, GRAY_FILL)
    label(fig, 310, 64, "60 seeds from one parent", 15, bold=True)
    label(fig, 310, 80, "Random split", 11, MUTED)
    for x in (163, 457):
        fig.line(310, 91, x, 118, MUTED, arrow=True)
    for x, title, height, colour, fill in (
        (44, "Bright light · 30 seedlings", 12, BLUE, BLUE_FILL),
        (338, "Dim light · 30 seedlings", 7, ORANGE, ORANGE_FILL),
    ):
        panel(fig, x, 121, 238, 78)
        fig.text(x + 12, 145, title, 14, weight="bold")
        fig.rect(x + 12, 157, height * 13, 24, fill, colour, rx=3)
        fig.text(x + 18 + height * 13, 175, f"{height} cm", 14, colour, weight="bold")
    label(fig, 310, 231, "Shared conditions: soil, water, and temperature", 14, MUTED)
    return fig


def labelled_sketch():
    fig = card(620, 252, "The student's labels",
               "The student points Gene at the entire chromosome set, Nucleus at the round enclosure, Chromosome at one thread, Cell membrane at the cell boundary, and DNA at an enlarged strand.")
    fig.circle(287, 139, 77, BLUE_FILL, BLUE, 2)
    fig.circle(287, 139, 44, ORANGE_FILL, ORANGE, 2)
    for x, y, dy in ((270, 130, -8), (285, 137, 8), (271, 153, 6)):
        fig.path(f"M{x},{y} q5,{dy * 2} 12,{dy}", stroke=INK, sw=2.8)
    fig.rect(261, 110, 49, 54, stroke=MUTED, dash="4 3", rx=4)
    fig.line(299, 152, 407, 194, MUTED, arrow=True)
    strand(fig, 420, 198, 103, 9)
    for x, y, string, end, px, py in (
        (30, 83, "Cell membrane", 145, 222, 98),
        (38, 140, "Nucleus", 120, 243, 139),
        (452, 88, "Gene", 442, 309, 111),
        (443, 151, "Chromosome", 433, 297, 145),
        (543, 220, "DNA", 536, 493, 204),
    ):
        fig.text(x, y, string, 15, weight="bold")
        fig.line(end, y - 5, px, py, MUTED, arrow=True)
    return fig


def cutting_trials():
    fig = card(632, 280, "Cuttings and soil trials",
               "The original supplies cutting 1 for Soil A, which flowers blue, and cutting 2 for Soil B, which flowers pink. A cutting from the blue plant also flowers pink in Soil B.")
    panel(fig, 21, 87, 148, 62, GRAY_FILL)
    label(fig, 95, 113, "Original plant", 15, bold=True)
    label(fig, 95, 133, "Source of both cuttings", 11, MUTED)
    trials = (
        (215, 58, "1  Cutting 1", "Soil A → blue", BLUE_FILL, BLUE),
        (215, 159, "2  Cutting 2", "Soil B → pink", ORANGE_FILL, ORANGE),
        (431, 58, "3  From Trial 1", "Soil B → pink", ORANGE_FILL, ORANGE),
    )
    for x, y, title, detail, fill, stroke in trials:
        panel(fig, x, y, 182, 62, fill)
        label(fig, x + 91, y + 26, title, 15, bold=True)
        label(fig, x + 91, y + 46, detail, 14, stroke)
    fig.line(172, 105, 210, 92, MUTED, arrow=True)
    fig.line(172, 132, 210, 184, MUTED, arrow=True)
    fig.line(400, 89, 427, 89, MUTED, arrow=True)
    label(fig, 316, 253, "Shared conditions: light, water, temperature, and growing time", 13, MUTED)
    return fig


def pink_parents():
    fig = card(626, 223, "Work backward from both flower colours",
               "A red RR offspring needs R from parent 1 and parent 2. A white WW offspring needs W from both. Each parent must have RW, which gives pink flowers under the stated rule.")
    for x, parent in ((225, "Parent 1"), (385, "Parent 2")):
        panel(fig, x - 67, 48, 134, 37)
        label(fig, x, 71, parent, 14, bold=True)
    for y, outcome, copy, fill, colour in (
        (101, "Red offspring (RR)", "R", ORANGE_FILL, ORANGE),
        (139, "White offspring (WW)", "W", GRAY_FILL, MUTED),
    ):
        fig.text(25, y + 16, outcome, 13)
        for x in (225, 385):
            panel(fig, x - 46, y, 92, 25, fill)
            label(fig, x, y + 17, copy, 15, colour, True)
    fig.text(26, 195, "Copies needed", 13, weight="bold")
    for x in (225, 385):
        label(fig, x, 196, "RW", 16, GREEN, True)
    fig.text(468, 195, "RW gives pink.", 15, GREEN, weight="bold")
    return fig


def gene_use():
    fig = card(570, 183, "Check presence and use separately",
               "The particular gene is present in both cells. The muscle cell uses its instructions. The skin result supporting Omar has the gene present with its instructions unused.")
    for x, name, use in ((22, "Muscle cell", "Instructions in use"), (298, "Skin cell", "Instructions unused")):
        panel(fig, x, 49, 250, 112)
        label(fig, x + 125, 75, name, 15, bold=True)
        fig.line(x + 29, 103, x + 221, 103, BLUE, 3)
        fig.rect(x + 99, 94, 52, 18, ORANGE_FILL, ORANGE, rx=3)
        label(fig, x + 125, 129, "Gene present", 13, ORANGE, True)
        label(fig, x + 125, 150, use, 13, MUTED)
    return fig


def cell_counts():
    fig = card(620, 245, "Count cells using the wall",
               "Six wall-bearing bean cells have chloroplasts and five wall-bearing bean cells lack them. Nine cells lack the wall. Adding the two wall-bearing groups gives 11 bean cells.")
    groups = (
        (24, 6, "Wall and chloroplasts", BLUE_FILL, True, True),
        (214, 5, "Wall only", BLUE_FILL, True, False),
        (404, 9, "Neither structure", GRAY_FILL, False, False),
    )
    for x, count, name, fill, wall, chloroplast in groups:
        panel(fig, x, 51, 183, 124, fill)
        label(fig, x + 91, 76, name, 14, bold=True)
        for index in range(count):
            cx = x + 30 + (index % 5) * 30
            cy = 104 + (index // 5) * 24
            if wall:
                fig.rect(cx - 9, cy - 7, 18, 14, "#ffffff", INK, rx=2)
            else:
                fig.circle(cx, cy, 7, "#ffffff", MUTED)
            if chloroplast:
                leaf_pattern(fig, cx, cy, 4)
        label(fig, x + 91, 157, f"{count} cells", 13, MUTED)
    fig.path("M24,186 v8 h373 v-8", stroke=GREEN, sw=2)
    label(fig, 210, 218, "6 + 5 = 11 bean cells", 15, GREEN, True)
    return fig


def independent_hatchlings():
    fig = card(614, 171, "The next hatchling follows its own chance rule",
               "The first four hatchlings are spotted. The fifth can be spotted or plain, with the same one-in-two chance for each possibility.")
    for index in range(4):
        x = 49 + index * 61
        fig.circle(x, 86, 20, ORANGE_FILL, ORANGE)
        for dx, dy in ((-7, -4), (5, -6), (3, 7)):
            fig.circle(x + dx, 86 + dy, 2.5, ORANGE, "none")
        label(fig, x, 122, index + 1, 13)
    fig.line(276, 51, 276, 137, LINE, dash="4 4")
    for y, name, fill, stroke in (
        (57, "Spotted: 1 in 2", ORANGE_FILL, ORANGE),
        (112, "Plain: 1 in 2", BLUE_FILL, BLUE),
    ):
        panel(fig, 441, y - 17, 151, 34, fill)
        label(fig, 516, y + 5, name, 14, stroke, True)
        fig.line(375, 85, 437, y, MUTED, arrow=True)
    label(fig, 329, 91, "Fifth", 16, bold=True)
    label(fig, 141, 147, "Earlier results", 13, MUTED)
    return fig


def main():
    figures = {
        "learn-cell-hierarchy": hierarchy,
        "learn-cell-types": cell_types,
        "learn-one-copy-grid": inheritance,
        "learn-fair-comparison": fair_comparison,
        "q07-seedling-groups": randomized_split,
        "q22-student-labels": labelled_sketch,
        "q28-cutting-trials": cutting_trials,
        "sol19-parent-copies": pink_parents,
        "sol25-gene-use": gene_use,
        "sol27-cell-counts": cell_counts,
        "sol30-independent-hatchlings": independent_hatchlings,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in figures.items():
        draw().save(OUT / f"{name}.svg")


if __name__ == "__main__":
    main()
