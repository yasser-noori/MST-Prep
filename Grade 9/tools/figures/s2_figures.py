"""Generate the base-pair diagrams used by the S2 practice questions."""

from pathlib import Path

from svgkit import BLUE, BLUE_FILL, MUTED, Fig


OUT = Path(__file__).resolve().parents[2] / "assets" / "S2"


def centre(fig, x, y, text, size=17):
    fig.text(x, y, text, size, weight="bold", anchor="middle")


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
        "q02-dna-pairs.svg": dna_ladder(("A", "Blank 2", "C", "T"), ("Blank 1", "G", "G", "A"), "A DNA ladder with two blanks"),
        "q27-pair-check.svg": dna_ladder(("A", "C", "G", "T"), ("T", "C", "C", "G"), "Four DNA base pairs to check", numbered=True),
    }
    for filename, figure in figures.items():
        figure.save(OUT / filename)


if __name__ == "__main__":
    write_figures()
