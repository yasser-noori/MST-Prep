"""Generate the S5 forces and balance illustrations."""

from pathlib import Path

from svgkit import (
    BLUE, BLUE_FILL, GRAY_FILL, GREEN, INK, LINE, MUTED, ORANGE, ORANGE_FILL, Fig,
)


DESTINATION = Path(__file__).resolve().parents[2] / "assets" / "S5"


def save(name, fig):
    fig.save(DESTINATION / f"{name}.svg")


def arrow(fig, start, end, color=INK):
    """Draw an arrow with a head the same color as its shaft."""
    x1, y1 = start
    x2, y2 = end
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    bx, by = x2 - 10 * ux, y2 - 10 * uy
    fig.line(x1, y1, bx, by, color, 2.5)
    fig.path(
        f"M{x2},{y2} L{bx - 5 * uy},{by + 5 * ux} "
        f"L{bx + 5 * uy},{by - 5 * ux} Z",
        color, color, 0.5,
    )


def dimension(fig, x1, x2, y, label, color=MUTED):
    fig.line(x1, y, x2, y, color)
    for x in (x1, x2):
        fig.line(x, y - 5, x, y + 5, color)
    fig.text((x1 + x2) / 2, y + 20, label, 15, color, "middle")


def beam(name, marks, pivot, loads, *, arms=(), note=None):
    """Draw a numbered beam, with optional distance rulers used in explanations."""
    width = 560
    axis = 91
    lo, hi = marks.start, marks.stop - 1
    spacing = (width - 112) / (hi - lo)

    def position(mark):
        return 56 + (mark - lo) * spacing

    def label(mark):
        if lo >= 0 or mark == 0:
            return str(mark)
        side = "L" if mark < 0 else "R"
        return f"{side}{abs(mark)}"

    description = f"Beam with pivot at {label(pivot)}. "
    description += " ".join(f"{load} at {label(mark)}." for mark, load in loads)
    if arms:
        description += " " + " ".join(
            f"{reading} from {label(mark)} to the pivot." for mark, reading in arms
        )
    if note:
        description += f" {note}"
    height = 229 if note else 204 if arms else 164
    fig = Fig(width, height, "Loads on a beam", description)

    center = position(pivot)
    fig.rect(39, axis - 5, width - 78, 10, GRAY_FILL, INK, rx=4)
    fig.path(f"M{center},{axis + 5} l-10,14 h20 Z", GRAY_FILL, INK)
    for mark in marks:
        x = position(mark)
        fig.line(x, axis - 7, x, axis + 5, INK, 1.4)
        fig.text(x, axis + 40, label(mark), 15, INK, "middle", "bold" if mark == pivot else "normal")
    fig.text(center, axis + 59, "pivot", 13, MUTED, "middle")

    for mark, load in loads:
        x = position(mark)
        color = BLUE if mark < pivot else ORANGE if mark > pivot else INK
        fig.text(x, 43, load, 16, color, "middle", "bold")
        arrow(fig, (x, 53), (x, axis - 10), color)

    for mark, text in arms:
        color = BLUE if mark < pivot else ORANGE
        dimension(fig, position(mark), center, axis + 78, text, color)
    if note:
        fig.text(width / 2, 213, note, 16, GREEN, "middle", "bold")
    save(name, fig)


def scissors():
    fig = Fig(560, 183, "Parts of scissors",
              "In an overhead view, the two blades and two handles turn around the screw. "
              "Fingers press on the handles, and the material touches the blades.")
    fig.path("M78,48 Q162,59 256,84 L330,106 L309,116 L240,98 Q135,80 78,48 Z",
             GRAY_FILL, INK, 2)
    fig.path("M78,137 Q132,105 243,88 L310,67 L330,78 L257,101 Q159,123 78,137 Z",
             GRAY_FILL, INK, 2)
    for y, sign in [(50, -1), (134, 1)]:
        fig.path(f"M310,{92 + 20 * sign} L374,{y} L402,{y}", "none", BLUE, 10)
        fig.add(f'<ellipse cx="426" cy="{y}" rx="34" ry="20" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="4"/>')
        fig.add(f'<ellipse cx="426" cy="{y}" rx="23" ry="12" fill="#ffffff" stroke="{BLUE}" stroke-width="1.5"/>')
    fig.circle(253, 94, 10, ORANGE_FILL, INK, 2)
    fig.line(247, 94, 259, 94, INK, 2)

    fig.text(139, 26, "Blades", 16, INK, "middle", "bold")
    fig.line(139, 30, 139, 60, MUTED)
    fig.text(253, 156, "Screw (pivot)", 16, INK, "middle", "bold")
    fig.line(253, 106, 253, 137, MUTED)
    fig.text(401, 96, "Handles (effort)", 16, INK, "middle", "bold")
    save("learn-scissors", fig)


def turning_totals():
    fig = Fig(560, 135, "Add the turning effects on each side",
              "Two loads on the left contribute 9 and 3 N-marks. Their sum, 12, "
              "matches a single 12 N-mark turn on the right.")
    fig.text(29, 37, "Left turns", 16, BLUE, weight="bold")
    fig.text(29, 99, "Right turn", 16, ORANGE, weight="bold")
    for x1, span, y, fill, color, text in [
        (135, 9, 21, BLUE_FILL, BLUE, "9 N-marks"),
        (369, 3, 21, BLUE_FILL, BLUE, "3 N-marks"),
        (135, 12, 83, ORANGE_FILL, ORANGE, "12 N-marks"),
    ]:
        width = 26 * span
        fig.rect(x1, y, width, 30, fill, color, rx=3)
        fig.text(x1 + width / 2, y + 20, text, 14, INK, "middle")
    fig.line(447, 52, 447, 82, MUTED, dash="3 4")
    fig.text(500, 72, "Equal", 15, GREEN, "middle", "bold")
    save("learn-turn-totals", fig)


def line_forces(name, body, left, right, *, motion=None):
    """Draw collinear forces above a central object, with motion on a separate row."""
    left_total, right_total = sum(left), sum(right)
    description = f"{body} with "
    description += ", ".join(f"{force} N left" for force in left)
    description += " and " + ", ".join(f"{force} N right" for force in right) + "."
    if motion:
        description += f" The {body.lower()} is moving right."
    fig = Fig(560, 157 if motion else 141, "Forces along one line", description)
    center = 280
    axis = 79
    fig.line(28, axis, 532, axis, LINE, dash="5 5")
    fig.rect(center - 33, 61, 66, 37, GRAY_FILL, INK, rx=8)
    fig.text(center, 85, body, 15, INK, "middle", "bold")

    scale = 142 / max(left_total, right_total)
    for direction, forces, color in [(-1, left, BLUE), (1, right, ORANGE)]:
        for i, force in enumerate(forces):
            start = center + direction * 39
            end = start + direction * force * scale
            y = axis if len(forces) == 1 else axis - 24 + 48 * i
            if len(forces) > 1:
                fig.path(f"M{center + direction * 33},{axis} H{start} V{y}", "none", LINE, 1.5)
            arrow(fig, (start, y), (end, y), color)
            side = (("west" if direction < 0 else "east") if body == "Puck"
                    else ("left" if direction < 0 else "right"))
            label = f"{force} N {side}"
            if len(forces) > 1:
                fig.text(start + direction * 8, y - 11, label, 15, color,
                         "start" if direction > 0 else "end", "bold")
            else:
                fig.text((start + end) / 2, y - 11, label, 15, color, "middle", "bold")

    if motion:
        fig.line(28, 108, 532, 108, LINE)
        arrow(fig, (260, 130), (375, 130), GREEN)
        fig.text(247, 135, motion, 15, GREEN, "end", "bold")
    save(name, fig)


def gate():
    fig = Fig(560, 204, "Two ways to push a gate, viewed from above",
              "Both 10 N pushes act at the same distance from the hinge. In the first panel the push "
              "points along the gate toward the hinge. In the second it points across the gate at a right angle.")
    fig.line(280, 23, 280, 180, LINE)
    for offset, label in [(0, "Along the gate"), (280, "Across the gate")]:
        x1, x2 = offset + 61, offset + 212
        y = 123
        fig.text(offset + 140, 37, label, 17, INK, "middle", "bold")
        fig.rect(x1, y - 6, x2 - x1, 12, GRAY_FILL, INK, rx=3)
        fig.circle(x1, y, 7, BLUE_FILL, BLUE, 2)
        fig.text(x1, 154, "Hinge", 14, MUTED, "middle")
        fig.circle(x2, y, 3, INK, INK)
        if offset:
            arrow(fig, (x2, y - 65), (x2, y), ORANGE)
            fig.text(x2 - 11, 78, "10 N", 15, ORANGE, "end", "bold")
        else:
            arrow(fig, (x2, y), (x2 - 65, y), ORANGE)
            fig.text(x2 - 32.5, y - 14, "10 N", 15, ORANGE, "middle", "bold")
        dimension(fig, x1, x2, 174, "Same distance")
    save("q24-gate-pushes", fig)


def parcel():
    fig = Fig(560, 232, "The shelf supplies an upward force while in contact",
              "Before the shelf moves, gravity acts down with 12 N and the shelf pushes up with 12 N. "
              "Once there is no contact, only the 12 N downward gravity force remains.")
    fig.line(280, 23, 280, 188, LINE)
    for x, title in [(140, "On the shelf"), (420, "After the shelf slides away")]:
        fig.text(x, 34, title, 16, INK, "middle", "bold")
        fig.rect(x - 32, 91, 64, 48, ORANGE_FILL, INK, rx=4)
        fig.line(x - 7, 91, x - 7, 139, MUTED, dash="4 3")
        if x == 140:
            fig.rect(x - 79, 139, 158, 11, GRAY_FILL, INK, rx=2)
            arrow(fig, (x, 112), (x, 56), BLUE)
            fig.text(x + 13, 71, "Shelf 12 N", 14, BLUE)
        arrow(fig, (x, 117), (x, 173), ORANGE)
        fig.text(x + 13, 164, "Gravity 12 N", 14, ORANGE)
    fig.text(280, 210, "Without contact, the shelf's push is gone.", 15, INK, "middle", "bold")
    save("sol27-contact-force", fig)


def sign(name, solved=False):
    description = ("A square sign in plan view has pivot O and edge labels T, R, B and L. "
                   "The first arrow at R points up the page.")
    if solved:
        description += " A second equal arrow points up at L and turns the sign the opposite way."
    fig = Fig(560, 250 if solved else 229, "Sign seen from above", description)
    cx, cy, half = 280, 120, 72
    fig.rect(cx - half, cy - half, 2 * half, 2 * half, GRAY_FILL, INK, rx=4)
    fig.line(cx - half, cy, cx + half, cy, LINE, dash="5 3")
    fig.line(cx, cy - half, cx, cy + half, LINE, dash="5 3")
    for x, y, label, dx, dy in [
        (cx, cy - half, "T", 0, -10), (cx, cy + half, "B", 0, 20),
        (cx - half, cy, "L", -19, 5), (cx + half, cy, "R", 20, 5),
        (cx, cy, "O", 0, 20),
    ]:
        fig.circle(x, y, 3, INK, INK)
        fig.text(x + dx, y + dy, label, 15, INK, "middle", "bold")
    arrow(fig, (cx + half, cy), (cx + half, cy - 59), BLUE)
    fig.text(cx + half + 18, cy - 52, "First push", 15, BLUE, weight="bold")
    if solved:
        arrow(fig, (cx - half, cy), (cx - half, cy - 59), ORANGE)
        fig.text(cx - half - 18, cy - 52, "Second push", 15, ORANGE, "end", "bold")
        fig.text(280, 235, "Equal distances and equal pushes give opposite turns.", 15, GREEN, "middle", "bold")
    save(name, fig)


def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    scissors()
    beam("learn-measure-from-pivot", range(9), 5, [(2, "4 N"), (7, "3 N")],
         arms=[(2, "3 marks"), (7, "2 marks")])
    turning_totals()
    line_forces("learn-cart-motion", "Cart", [6], [3], motion="Cart moves right")

    setups = [
        ("q03-beam", range(-4, 5), 0, [(-2, "5 N"), (4, "3 N")]),
        ("q05-beam", range(-3, 4), 0, [(-3, "Bag"), (2, "Two weights")]),
        ("q06-beam", range(-3, 3), 0, [(-3, "4 N"), (2, "? N")]),
        ("q09-beam", range(-3, 4), 0, [(-1, "Stone"), (3, "Stone")]),
        ("q10-beam", range(-4, 5), 0, [(-4, "3 N"), (-1, "2 N"), (2, "? N")]),
        ("q11-numbered-beam", range(9), 4, [(1, "2 N"), (6, "3 N")]),
        ("q13-beam", range(-3, 4), 0, [(-2, "Load"), (2, "Identical load")]),
        ("q16-beam", range(-4, 5), 0, [(-4, "2 N"), (-2, "2 N")]),
        ("q18-beam", range(-3, 4), 0, [(-2, "6 N"), (3, "4 N")]),
        ("q20-beam", range(-4, 5), 0, [(-4, "? N"), (2, "? N")]),
        ("q22-beam", range(-3, 5), 0, [(-2, "6 N")]),
        ("q25-beam", range(-3, 5), 0, [(-2, "8 N"), (4, "Two bags")]),
        ("q26-movable-pivot", range(7), 3, [(0, "2 N"), (6, "4 N")]),
    ]
    for setup in setups:
        beam(*setup)
    line_forces("q04-sled-pulls", "Sled", [8], [5])
    line_forces("q07-puck-forces", "Puck", [7], [3], motion="Puck moves east")
    line_forces("q12-crate-forces", "Crate", [4], [6, 3])
    gate()
    sign("q30-sign-pivot")

    beam("sol18-new-arms", range(-3, 4), 0, [(-1, "6 N"), (2, "4 N")],
         arms=[(-1, "1 mark"), (2, "2 marks")],
         note="Left 6 N-marks  |  Right 8 N-marks")
    beam("sol26-new-pivot", range(7), 4, [(0, "2 N"), (6, "4 N")],
         arms=[(0, "4 marks"), (6, "2 marks")],
         note="Left and right each produce 8 N-marks")
    parcel()
    sign("sol30-opposite-turns", solved=True)


if __name__ == "__main__":
    main()
