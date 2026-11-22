"""Generate the diagrams for the cells, DNA, and inheritance topic."""

from pathlib import Path

from svgkit import BLUE, BLUE_FILL, GREEN, GREEN_FILL, INK, MUTED, ORANGE, ORANGE_FILL, Fig


OUT = Path(__file__).resolve().parents[2] / "assets" / "S2"


def centre(fig, x, y, text, size=17):
    fig.text(x, y, text, size, weight="bold", anchor="middle")


def cell_types():
    fig = Fig(600, 262, "Typical leaf and cheek cells",
              "Both have a cell membrane and a nucleus. Only the leaf cell shown has a cell wall and chloroplasts.")
    centre(fig, 151, 34, "Green leaf cell")
    centre(fig, 451, 34, "Cheek cell")
    fig.rect(58, 82, 186, 126, "#fff", INK, 3, rx=22)
    fig.rect(68, 92, 166, 106, BLUE_FILL, BLUE, 3, rx=15)
    fig.path("M365 141 Q366 99 426 96 Q501 82 533 124 Q553 169 510 192 Q459 216 408 198 Q363 179 365 141 Z",
             BLUE_FILL, BLUE, 3)
    for x, y in ((145, 140), (449, 145)):
        fig.circle(x, y, 23, ORANGE_FILL, ORANGE, 2)
    for x, y in ((100, 118), (192, 116), (204, 162), (109, 170)):
        fig.circle(x, y, 10, GREEN_FILL, GREEN, 2)
        fig.line(x - 5, y, x + 5, y, GREEN, 1.5)
    fig.line(85, 68, 99, 82, MUTED)
    centre(fig, 69, 62, "Cell wall", 15)
    fig.line(206, 68, 206, 92, BLUE)
    centre(fig, 206, 62, "Cell membrane", 15)
    fig.line(495, 68, 509, 102, BLUE)
    centre(fig, 495, 62, "Cell membrane", 15)
    fig.line(65, 225, 102, 177, GREEN)
    centre(fig, 62, 245, "Chloroplast", 15)
    for x, y in ((145, 163), (449, 168)):
        fig.line(x, 225, x, y, ORANGE)
        centre(fig, x, 245, "Nucleus", 15)
    return fig


def hierarchy():
    fig = Fig(600, 213, "From a cell to a gene",
              "A typical cell contains a nucleus. The nucleus holds chromosomes. The enlarged chromosome contains DNA, and a gene is a stretch of that DNA.")
    centre(fig, 94, 37, "Cell")
    centre(fig, 274, 37, "Nucleus")
    centre(fig, 465, 37, "Chromosome")
    fig.circle(94, 114, 55, BLUE_FILL, BLUE, 3)
    fig.circle(106, 113, 24, ORANGE_FILL, ORANGE, 2)
    fig.circle(274, 113, 55, ORANGE_FILL, ORANGE, 3)
    fig.path("M245 113 q7 -13 20 -6 M263 82 q9 10 20 2 M278 109 q13 9 21 -2 M262 130 q7 13 17 9",
             stroke=ORANGE, sw=4)
    fig.path("M286 138 q12 6 18 -7", stroke=INK, sw=4)
    fig.line(155, 113, 206, 113, MUTED, arrow=True)
    fig.line(331, 113, 365, 113, MUTED, arrow=True)
    fig.rect(375, 72, 179, 79, "#fff", INK, 2, rx=14)
    fig.rect(441, 89, 45, 44, GREEN_FILL, GREEN, 1.5, rx=6)
    fig.path("M391 104 q12 -15 24 0 t24 0 t24 0 t24 0 t24 0 t24 0", stroke=BLUE, sw=3)
    fig.path("M391 118 q12 15 24 0 t24 0 t24 0 t24 0 t24 0 t24 0", stroke=BLUE, sw=3)
    fig.line(464, 136, 464, 171, GREEN, 1.5)
    centre(fig, 464, 190, "Gene")
    fig.line(525, 121, 549, 170, MUTED, 1.4)
    centre(fig, 551, 190, "DNA")
    return fig


def dna_ladder(top, bottom, title, numbered=False):
    width = 194 + 76 * len(top)
    fig = Fig(width, 167 if numbered else 138, title,
              f"From left to right, the top strand reads {', '.join(top)} and the bottom strand reads {', '.join(bottom)}.")
    y_top, y_bottom = (60, 113) if numbered else (41, 94)
    first_x = 190
    last_x = first_x + 76 * (len(top) - 1)
    for y, name in ((y_top, "Top strand"), (y_bottom, "Bottom strand")):
        fig.text(19, y + 6, name, 18, weight="bold")
        fig.line(first_x - 26, y, last_x + 26, y, BLUE, 3)
    for i, (above, below) in enumerate(zip(top, bottom)):
        x = first_x + 76 * i
        if numbered:
            centre(fig, x, 28, str(i + 1), 15)
        fig.line(x, y_top + 16, x, y_bottom - 16, MUTED, 2)
        for y, base in ((y_top, above), (y_bottom, below)):
            blank = base.startswith("Blank")
            fig.rect(x - 25, y - 17, 50, 34, "#fff" if blank else BLUE_FILL,
                     MUTED if blank else BLUE, 1.8, rx=6, dash="4 3" if blank else None)
            centre(fig, x, y + 6, base, 12 if blank else 20)
    return fig


def write_figures():
    OUT.mkdir(parents=True, exist_ok=True)
    figures = {
        "learn-cell-hierarchy.svg": hierarchy(),
        "learn-cell-types.svg": cell_types(),
        "learn-dna-pairs.svg": dna_ladder(("A", "C", "G"), ("T", "G", "C"), "DNA base pairs"),
        "q02-dna-pairs.svg": dna_ladder(("A", "Blank 2", "C", "T"), ("Blank 1", "G", "G", "A"), "A DNA ladder with two blanks"),
        "q27-pair-check.svg": dna_ladder(("A", "C", "G", "T"), ("T", "C", "C", "G"), "Four DNA base pairs to check", numbered=True),
    }
    for filename, figure in figures.items():
        figure.save(OUT / filename)


if __name__ == "__main__":
    write_figures()
