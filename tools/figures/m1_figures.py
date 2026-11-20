"""Generate every M1 (number theory) figure into assets/M1/.

Run from the repository root:  python3 tools/figures/m1_figures.py
All positions and labels are computed from the numbers in the questions, so a
figure cannot drift out of step with its question if the script is re-run.

Naming:  learn-*.svg  learning page
         qNN-*.svg    question stem (shows the set-up only, never the answer)
         solNN-*.svg  full solution (may show the answer)
"""

import calendar
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from svgkit import (Fig, INK, MUTED, LINE, BLUE, BLUE_FILL, ORANGE, ORANGE_FILL,
                    GREEN, GREEN_FILL, RED, GRAY_FILL)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "M1")


def save(fig, name):
    fig.save(os.path.join(OUT, name))
    print("wrote", name)


# ---------------------------------------------------------------- helpers
RED_FILL = "#ffe1e1"
STYLE = {"a": (RED, RED_FILL), "b": (BLUE, BLUE_FILL)}


def tile(f, x, y, s, kind):
    """kind 'a' = square, 'b' = circle, so the two kinds differ in shape as well as colour."""
    col, fill = STYLE[kind]
    if kind == "a":
        f.rect(x, y, s, s, fill, col, 1.5, rx=2)
    else:
        f.circle(x + s / 2, y + s / 2, s / 2, fill, col, 1.5)


def groups_figure(name, title, a_total, b_total, a_label, b_label, groups, per_row, foot,
                  a_style=None, b_style=None):
    if a_style: STYLE["a"] = a_style
    if b_style: STYLE["b"] = b_style
    a_each, b_each = a_total // groups, b_total // groups
    s, gap = 13, 4
    rows_needed = math.ceil(groups / per_row)
    box_w = max(a_each, b_each) * (s + gap) + 16
    box_h = 2 * (s + gap) + 30
    width = max(640, per_row * (box_w + 12) + 40)
    height = 150 + rows_needed * (box_h + 12) + 50
    f = Fig(width, height, title,
            f"{a_total} {a_label} and {b_total} {b_label} sorted into {groups} identical groups, "
            f"each with {a_each} {a_label} and {b_each} {b_label}.")
    f.text(20, 30, title, 17, weight="bold")
    # the loose items
    y = 52
    for label, total, kind in ((a_label, a_total, "a"), (b_label, b_total, "b")):
        f.text(20, y + 11, f"{total} {label}", 14, STYLE[kind][0], weight="bold")
        x0 = 130
        pitch = min(s + 2, (width - x0 - 20) / total)
        size = min(s, pitch - 1)
        for i in range(total):
            tile(f, x0 + i * pitch, y, size, kind)
        y += s + 12
    f.line(width / 2, y + 2, width / 2, y + 24, MUTED, 1.5, arrow=True)
    f.text(width / 2 + 12, y + 18, f"GCF({a_total}, {b_total}) = {groups} identical groups", 14, GREEN, weight="bold")
    y += 34
    for g in range(groups):
        r, c = divmod(g, per_row)
        bx = 20 + c * (box_w + 12)
        by = y + r * (box_h + 12)
        f.rect(bx, by, box_w, box_h, GRAY_FILL, LINE, 1.5, rx=8)
        f.text(bx + 8, by + 16, f"group {g + 1}", 11, MUTED)
        for i in range(a_each):
            tile(f, bx + 8 + i * (s + gap), by + 22, s, "a")
        for i in range(b_each):
            tile(f, bx + 8 + i * (s + gap), by + 22 + s + gap, s, "b")
    f.text(20, height - 20, foot, 14)
    return f


def number_line(f, x0, x1, y, vmax, step_label=None, ticks=()):
    f.line(x0, y, x1, y, MUTED, 1.5)
    for v in ticks:
        x = x0 + (x1 - x0) * v / vmax
        f.line(x, y - 4, x, y + 4, MUTED, 1)
        f.text(x, y + 20, v, 12, MUTED, "middle")


def multiples_rows(name, title, desc, steps, labels, vmax, unit, foot, highlight_all=True, start=0):
    """Rows of multiples of each step on a shared line, common values highlighted."""
    width, x0, x1 = 680, 150, 650
    rows = len(steps)
    height = 98 + rows * 46 + 70
    f = Fig(width, height, title, desc)
    f.text(20, 30, title, 17, weight="bold")
    colours = [(BLUE, BLUE_FILL), (ORANGE, ORANGE_FILL), (MUTED, GRAY_FILL)]
    sets = [set(range(start, vmax + 1, st)) for st in steps]
    common = set.intersection(*sets)
    if not highlight_all:
        common = {min(v for v in common if v > start)}
    sx = lambda v: x0 + (x1 - x0) * v / vmax
    top = 64
    for v in sorted(common):
        f.rect(sx(v) - 13, top - 6, 26, rows * 46 + 6, GREEN_FILL, GREEN, 1.5, rx=6)
    for i, (st, lab) in enumerate(zip(steps, labels)):
        y = top + 16 + i * 46
        col, fill = colours[i]
        f.text(20, y + 5, lab, 14, col, weight="bold")
        f.line(x0, y, x1, y, LINE, 1)
        vals = list(range(start, vmax + 1, st))
        for v in vals:
            f.circle(sx(v), y, 7, fill, col, 2)
            if len(vals) <= 8 and v != start:
                f.text(sx(v), y - 12, v, 11, col, "middle")
    axis_y = top + rows * 46 + 14
    tick_vals = sorted(set().union(*sets))
    f.line(x0, axis_y, x1, axis_y, MUTED, 1.5)
    for v in tick_vals:
        f.line(sx(v), axis_y - 4, sx(v), axis_y + 4, MUTED, 1)
    label_vals = sorted(common | {start, vmax})
    for v in label_vals:
        f.text(sx(v), axis_y + 20, v, 12, GREEN if v in common else MUTED, "middle",
               "bold" if v in common else "normal")
    f.text(x1, axis_y + 36, unit, 12, MUTED, "end")
    f.text(20, height - 16, foot, 14)
    return f


# ------------------------------------------------------------ learning page
def learn_gcf_bags():
    f = groups_figure("learn-gcf-bags.svg", "Cutting up what you have: GCF", 18, 30,
                      "red tiles", "blue tiles", 6, 3,
                      "Each bag: 3 red + 5 blue = 8 tiles.  Check: 6 × 3 = 18 and 6 × 5 = 30.",
                      a_style=(RED, RED_FILL), b_style=(BLUE, BLUE_FILL))
    save(f, "learn-gcf-bags.svg")


def learn_lcm_line():
    f = multiples_rows("learn-lcm-line.svg", "Building up to a shared total: LCM",
                       "Multiples of 18 (18, 36, 54, 72, 90) and of 30 (30, 60, 90) first match at 90.",
                       [18, 30], ["packs of 18", "packs of 30"], 90, "tiles",
                       "First match: 90 = LCM(18, 30).  That is 5 packs of 18 and 3 packs of 30.",
                       highlight_all=False, start=0)
    save(f, "learn-lcm-line.svg")


def learn_decide():
    f = Fig(680, 250, "GCF or LCM?", "Decision chart: cutting up amounts you already have uses the GCF; "
            "building up to a total or time that several step sizes all reach uses the LCM.")
    f.rect(190, 18, 300, 44, GRAY_FILL, MUTED, 1.5, rx=10)
    f.text(340, 46, "Am I cutting up or building up?", 15, anchor="middle", weight="bold")
    f.line(290, 62, 175, 92, MUTED, 1.5, arrow=True)
    f.line(390, 62, 505, 92, MUTED, 1.5, arrow=True)
    for x, col, fill, head, big, lines in (
        (20, BLUE, BLUE_FILL, "Cutting up amounts I already have", "GCF",
         ["The answer is no bigger than", "the amounts you start with.", "18 red + 30 blue → 6 bags"]),
        (350, ORANGE, ORANGE_FILL, "Building up to a shared total or time", "LCM",
         ["The answer is at least as big", "as the largest step.", "packs of 18 and 30 → 90 each"])):
        f.rect(x, 96, 310, 140, fill, col, 2, rx=10)
        f.text(x + 155, 120, head, 14, col, "middle", "bold")
        f.text(x + 155, 156, big, 28, col, "middle", "bold")
        for i, s in enumerate(lines):
            f.text(x + 155, 182 + i * 18, s, 13, INK, "middle", "bold" if i == 2 else "normal")
    save(f, "learn-gcf-or-lcm.svg")


def crates(f, x, y, filled, size=8, cols=4, cell=16, label=None, full_col=BLUE, fill=BLUE_FILL):
    rows = math.ceil(size / cols)
    f.rect(x, y, cols * cell + 8, rows * cell + 8, GRAY_FILL, MUTED, 1.5, rx=4)
    for i in range(size):
        r, c = divmod(i, cols)
        cx, cy = x + 4 + c * cell + cell / 2, y + 4 + r * cell + cell / 2
        if i < filled:
            f.circle(cx, cy, cell / 2 - 2, fill, full_col, 1.5)
        else:
            f.circle(cx, cy, cell / 2 - 2, "#ffffff", RED, 1.5, dash="3 2")
    if label:
        f.text(x + (cols * cell + 8) / 2, y + rows * cell + 26, label, 12, MUTED, "middle")


def learn_remainder():
    f = Fig(680, 210, "Remainders: 46 bottles in crates of 8",
            "46 bottles fill 5 crates of 8 with 6 bottles left over; 2 more bottles would fill a sixth crate.")
    f.text(20, 30, "46 bottles in crates of 8", 17, weight="bold")
    for k in range(5):
        crates(f, 20 + k * 106, 50, 8, label=f"crate {k + 1}")
    crates(f, 20 + 5 * 106 + 20, 50, 6, label="6 left over", full_col=ORANGE, fill=ORANGE_FILL)
    f.text(20, 160, "46 = 5 × 8 + 6", 16, weight="bold")
    f.text(20, 186, "5 full crates  ·  6 left over  ·  8 − 6 = 2 more would fill another crate (dashed spaces)", 13, MUTED)
    save(f, "learn-remainder-crates.svg")


def learn_factor_tree():
    f = Fig(560, 360, "Factor tree for 180", "180 splits into 2 × 90, 90 into 2 × 45, 45 into 3 × 15, "
            "15 into 3 × 5, so 180 = 2² × 3² × 5.")
    f.text(20, 30, "Factor tree for 180", 17, weight="bold")
    nodes = [(150, 70, 180, False)]
    chain = [(180, 2, 90), (90, 2, 45), (45, 3, 15), (15, 3, 5)]
    x, y = 150, 70
    for (n, p, q) in chain:
        lx, rx_, ny = x - 50, x + 60, y + 58
        f.line(x - 10, y + 10, lx + 8, ny - 16, MUTED, 1.5)
        f.line(x + 10, y + 10, rx_ - 8, ny - 16, MUTED, 1.5)
        nodes.append((lx, ny, p, True))
        nodes.append((rx_, ny, q, q in (2, 3, 5, 7)))
        x, y = rx_, ny
    for (nx, ny, v, prime) in nodes:
        if prime:
            f.circle(nx, ny, 17, GREEN_FILL, GREEN, 2)
            f.text(nx, ny + 5, v, 15, GREEN, "middle", "bold")
        else:
            f.text(nx, ny + 5, v, 16, INK, "middle", "bold")
    f.circle(380, 72, 9, GREEN_FILL, GREEN, 2)
    f.text(395, 77, "= prime (stop here)", 13, MUTED)
    f.text(20, 340, "180 = 2 × 2 × 3 × 3 × 5 = 2² × 3² × 5", 16, weight="bold")
    save(f, "learn-factor-tree-180.svg")


def floor_tiling(name, title, desc, W, H, side, scale, foot, unit="cm"):
    gw, gh = W * scale, H * scale
    width, height = int(gw + 150), int(gh + 132)
    f = Fig(width, height, title, desc)
    f.text(20, 28, title, 17, weight="bold")
    x0, y0 = 70, 64
    nx, ny = W // side, H // side
    for i in range(nx):
        for j in range(ny):
            f.rect(x0 + i * side * scale, y0 + j * side * scale, side * scale, side * scale,
                   BLUE_FILL if (i + j) % 2 == 0 else "#c6dafc", BLUE, 1)
    f.rect(x0, y0, gw, gh, "none", INK, 2.5)
    f.text(x0 + gw / 2, y0 - 8, f"{W} {unit}", 14, INK, "middle", "bold")
    f.text(x0 - 10, y0 + gh / 2 + 5, f"{H} {unit}", 14, INK, "end", "bold")
    f.text(x0 + side * scale / 2, y0 + side * scale / 2 + 5, f"{side} cm", 12, BLUE, "middle", "bold")
    f.text(x0 + gw + 10, y0 + 14, f"{nx} across", 13, MUTED)
    f.text(x0 + gw + 10, y0 + 32, f"{ny} down", 13, MUTED)
    f.text(20, height - 22, foot, 14)
    return f


def learn_worked_floor():
    f = floor_tiling("learn-worked-floor.svg", "84 cm × 60 cm floor, 12 cm square tiles",
                     "An 84 by 60 rectangle divided into a 7 by 5 grid of 12 cm squares, 35 tiles.",
                     84, 60, 12, 5, "GCF(84, 60) = 12 cm tile side → 7 × 5 = 35 tiles")
    save(f, "learn-worked-floor.svg")


# ---------------------------------------------------------------- question stems
def time_axis(f, x0, x1, y, t0, t1, every, fmt):
    f.line(x0, y, x1, y, MUTED, 1.5)
    for t in range(t0, t1 + 1, every):
        x = x0 + (x1 - x0) * (t - t0) / (t1 - t0)
        f.line(x, y - 4, x, y + 4, MUTED, 1)
        f.text(x, y + 20, fmt(t), 11, MUTED, "middle")


def q13_stem():
    f = Fig(680, 200, "Two bus schedules", "Bus A first leaves at 6:00 and then every 8 minutes; "
            "bus B first leaves at 6:04 and then every 12 minutes.")
    f.text(20, 30, "M1-Q13: first departures", 17, weight="bold")
    x0, x1 = 120, 650
    sx = lambda m: x0 + (x1 - x0) * m / 40
    for y, lab, start, every, col, fill in ((70, "Bus A", 0, 8, BLUE, BLUE_FILL), (120, "Bus B", 4, 12, ORANGE, ORANGE_FILL)):
        f.text(20, y + 5, lab, 14, col, weight="bold")
        f.line(x0, y, x1, y, LINE, 1)
        f.circle(sx(start), y, 8, fill, col, 2)
        f.line(sx(start) + 12, y, sx(start) + 120, y, col, 2, dash="5 4", arrow=True)
        f.text(sx(start) + 126, y + 5, f"then every {every} min …", 13, col)
    time_axis(f, x0, x1, 152, 0, 40, 4, lambda m: f"6:{m:02d}")
    save(f, "q13-bus-schedules.svg")


def gear_path(cx, cy, teeth, r_pitch, depth, phase):
    pts = []
    n = teeth
    for i in range(n):
        a = phase + 2 * math.pi * i / n
        w = 2 * math.pi / n
        for frac, r in ((-0.5, r_pitch - depth), (-0.22, r_pitch - depth), (-0.14, r_pitch + depth),
                        (0.14, r_pitch + depth), (0.22, r_pitch - depth)):
            pts.append((cx + r * math.cos(a + frac * w), cy + r * math.sin(a + frac * w)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def q26_stem():
    f = Fig(600, 330, "Two meshed gears", "Gear A with 12 teeth meshes with gear B with 18 teeth. "
            "A chalk mark is drawn on each gear where they touch.")
    f.text(20, 30, "M1-Q26: meshed gears", 17, weight="bold")
    k, depth = 6.0, 6.5
    ra, rb = 12 * k, 18 * k
    cy = 175
    cxa = 170
    cxb = cxa + ra + rb
    # A has a tooth pointing right (angle 0); B has a gap facing left (angle pi)
    f.path(gear_path(cxa, cy, 12, ra, depth, 0.0), BLUE_FILL, BLUE, 2)
    f.path(gear_path(cxb, cy, 18, rb, depth, math.pi + math.pi / 18), ORANGE_FILL, ORANGE, 2)
    for cx, r, col in ((cxa, ra, BLUE), (cxb, rb, ORANGE)):
        f.circle(cx, cy, 8, "#ffffff", col, 2)
    contact = cxa + ra
    f.circle(contact - 9, cy, 5, "#ffffff", INK, 2)
    f.circle(contact + 9, cy, 5, "#ffffff", INK, 2)
    f.line(contact - 10, cy - 8, contact - 60, cy - 95, MUTED, 1.2)
    f.text(contact - 64, cy - 101, "chalk marks", 13, INK, "end", "bold")
    f.text(cxa, cy + ra + 34, "Gear A: 12 teeth", 14, BLUE, "middle", "bold")
    f.text(cxb, cy + rb + 30 if cy + rb + 30 < 320 else 318, "Gear B: 18 teeth", 14, ORANGE, "middle", "bold")
    save(f, "q26-gears.svg")


def q27_stem():
    s = 9
    f = Fig(420, 200, "One card, 6 cm by 10 cm", "A single rectangular card 10 cm wide and 6 cm tall.")
    f.text(20, 30, "M1-Q27: one card", 17, weight="bold")
    x0, y0 = 120, 70
    f.rect(x0, y0, 10 * s * 1.6, 6 * s * 1.6, BLUE_FILL, BLUE, 2, rx=3)
    w, h = 10 * s * 1.6, 6 * s * 1.6
    f.text(x0 + w / 2, y0 - 10, "10 cm", 14, INK, "middle", "bold")
    f.text(x0 - 10, y0 + h / 2 + 5, "6 cm", 14, INK, "end", "bold")
    f.text(20, 186, "Cards are placed side by side, all facing the same way.", 13, MUTED)
    save(f, "q27-card.svg")


def q28_stem():
    n = 12
    f = Fig(680, 210, "Lockers and students", "A row of lockers 1 to 12 (of 100). Student 3 changes "
            "lockers 3, 6, 9 and 12, shown highlighted.")
    f.text(20, 30, "M1-Q28: what one student does (student 3)", 17, weight="bold")
    w, gap, x0, y0 = 44, 6, 20, 56
    for i in range(1, n + 1):
        x = x0 + (i - 1) * (w + gap)
        hit = i % 3 == 0
        f.rect(x, y0, w, 80, ORANGE_FILL if hit else GRAY_FILL, ORANGE if hit else MUTED, 2 if hit else 1.5, rx=4)
        f.line(x + w - 10, y0 + 36, x + w - 10, y0 + 48, MUTED, 2)
        f.text(x + w / 2, y0 + 22, i, 14, INK, "middle", "bold")
        if hit:
            f.text(x + w / 2, y0 + 100, "change", 11, ORANGE, "middle", "bold")
    f.text(x0 + n * (w + gap) + 4, y0 + 46, "… 100", 14, MUTED)
    f.text(20, 192, "“Change” = open it if closed, close it if open. Student 1 changes every locker; student 100 only locker 100.", 12, MUTED)
    save(f, "q28-lockers.svg")


def q29_stem():
    f = Fig(680, 170, "Chime recording", "A 0 to 60 minute timeline. The chime was heard at minutes 0, 36 and 60. "
            "At minute 18 the recording is clear and there is no chime. Every other minute is unknown.")
    f.text(20, 30, "M1-Q29: what the recording shows", 17, weight="bold")
    x0, x1, y = 40, 640, 90
    sx = lambda m: x0 + (x1 - x0) * m / 60
    f.rect(x0, y - 14, x1 - x0, 28, GRAY_FILL, LINE, 1, rx=4)
    f.text(sx(48), y + 5, "unknown", 12, MUTED, "middle", italic=True)
    f.text(sx(8), y + 5, "unknown", 12, MUTED, "middle", italic=True)
    f.text(sx(27), y + 5, "unknown", 12, MUTED, "middle", italic=True)
    for m in (0, 36, 60):
        f.circle(sx(m), y, 10, GREEN_FILL, GREEN, 2.5)
        f.text(sx(m), y - 22, "heard", 12, GREEN, "middle", "bold")
    f.circle(sx(18), y, 10, "#ffffff", RED, 2.5)
    f.cross(sx(18), y, 5)
    f.text(sx(18), y - 22, "silent", 12, RED, "middle", "bold")
    for m in range(0, 61, 6):
        f.line(sx(m), y + 18, sx(m), y + 24, MUTED, 1)
        f.text(sx(m), y + 40, m, 11, MUTED, "middle")
    f.text(x1, y + 58, "minutes", 11, MUTED, "end")
    save(f, "q29-recording.svg")


# ---------------------------------------------------------------- solutions
def sol01():
    f = groups_figure("sol01-bouquets.svg", "M1-Q01: 14 identical bouquets", 28, 42, "roses", "tulips",
                      14, 7, "Each bouquet: 2 roses + 3 tulips.  7 also divides both, but 14 is the greatest.",
                      a_style=(RED, RED_FILL), b_style=(ORANGE, ORANGE_FILL))
    save(f, "sol01-bouquets.svg")


def sol03():
    f = multiples_rows("sol03-flashes.svg", "M1-Q03: when both lights flash",
                       "Light P every 6 seconds and light Q every 15 seconds from 0 to 120; they coincide at 0, 30, 60, 90 and 120.",
                       [6, 15], ["P (every 6 s)", "Q (every 15 s)"], 120, "seconds",
                       "Together every LCM(6, 15) = 30 s: at 0, 30, 60, 90, 120 → 5 times (count both ends).")
    save(f, "sol03-flashes.svg")


def sol08():
    f = Fig(520, 250, "March 2025 calendar", "March 2025: Maya swims every 4 days from March 3 (3, 7, 11, 15 ...) "
            "and Leo every 6 days (3, 9, 15 ...). Both swim again on Saturday March 15.")
    f.text(20, 28, "M1-Q08: March 2025", 17, weight="bold")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cell, x0, y0 = 66, 30, 66
    for i, d in enumerate(days):
        f.text(x0 + i * cell + cell / 2, y0 - 8, d, 12, MUTED, "middle", "bold")
    first_wd, ndays = calendar.monthrange(2025, 3)  # Monday = 0
    maya = set(range(3, 32, 4))
    leo = set(range(3, 32, 6))
    for day in range(1, 16 + 1):
        idx = first_wd + day - 1
        r, c = divmod(idx, 7)
        x, y = x0 + c * cell, y0 + r * 40
        both = day in maya and day in leo and day > 3
        fill = GREEN_FILL if both else ("#ffffff")
        f.rect(x + 2, y, cell - 4, 36, fill, GREEN if both else LINE, 2 if both else 1, rx=4)
        f.text(x + 8, y + 15, day, 12, INK, weight="bold" if both or day == 3 else "normal")
        if day in maya:
            f.rect(x + cell - 40, y + 20, 16, 11, BLUE_FILL, BLUE, 1, rx=2)
        if day in leo:
            f.circle(x + cell - 14, y + 26, 6, ORANGE_FILL, ORANGE, 1.2)
    ly = 210
    f.rect(30, ly - 10, 16, 11, BLUE_FILL, BLUE, 1, rx=2)
    f.text(52, ly, "Maya (every 4 days)", 12)
    f.circle(200, ly - 5, 6, ORANGE_FILL, ORANGE, 1.2)
    f.text(212, ly, "Leo (every 6 days)", 12)
    f.text(30, ly + 24, "LCM(4, 6) = 12 days after March 3 → March 15", 14, GREEN, weight="bold")
    save(f, "sol08-calendar.svg")


def sol10():
    f = Fig(680, 230, "250 eggs in cartons of 12", "20 full cartons hold 240 eggs; 10 eggs are left in a 21st carton, "
            "which has 2 empty spaces.")
    f.text(20, 28, "M1-Q10: 250 eggs, cartons of 12", 17, weight="bold")
    for k in range(20):
        r, c = divmod(k, 10)
        x, y = 20 + c * 56, 48 + r * 46
        f.rect(x, y, 50, 36, BLUE_FILL, BLUE, 1.5, rx=4)
        f.text(x + 25, y + 23, "12", 13, BLUE, "middle", "bold")
    crates(f, 20, 150, 10, size=12, cols=6, cell=14, full_col=ORANGE, fill=ORANGE_FILL)
    f.text(130, 166, "10 left over → 12 − 10 = 2 more eggs fill carton 21 (dashed)", 14, INK, weight="bold")
    f.text(130, 188, "250 = 20 × 12 + 10", 14, MUTED)
    save(f, "sol10-cartons.svg")


def sol13():
    f = Fig(680, 230, "Bus departures 6:00 to 6:40", "Bus A leaves at 6:00, 6:08, 6:16, 6:24, 6:32, 6:40. "
            "Bus B leaves at 6:04, 6:16, 6:28, 6:40. They first leave together at 6:16.")
    f.text(20, 30, "M1-Q13: list both schedules", 17, weight="bold")
    x0, x1 = 120, 650
    sx = lambda m: x0 + (x1 - x0) * m / 40
    a = set(range(0, 41, 8))
    b = set(range(4, 41, 12))
    first = min(a & b)
    f.rect(sx(first) - 16, 50, 32, 100, GREEN_FILL, GREEN, 1.5, rx=6)
    for y, lab, ts, col, fill in ((70, "Bus A", a, BLUE, BLUE_FILL), (125, "Bus B", b, ORANGE, ORANGE_FILL)):
        f.text(20, y + 5, lab, 14, col, weight="bold")
        f.line(x0, y, x1, y, LINE, 1)
        for t in sorted(ts):
            f.circle(sx(t), y, 8, fill, col, 2)
            f.text(sx(t), y - 13, f"6:{t:02d}", 10, col, "middle")
    time_axis(f, x0, x1, 162, 0, 40, 4, lambda m: f"6:{m:02d}")
    f.text(20, 214, f"First time on both lists: 6:{first:02d}.  6:24 is a bus A time only (B leaves at 6:28).", 14, GREEN, weight="bold")
    save(f, "sol13-buses.svg")


def sol17():
    f = Fig(680, 200, "135 students in rows of 8", "16 full rows of 8 seat 128 students; the other 7 need a 17th row.")
    f.text(20, 28, "M1-Q17: rows of 8 chairs", 17, weight="bold")
    s = 9
    for row in range(17):
        x = 20 + row * 38
        n = 8 if row < 16 else 7
        for i in range(8):
            y = 48 + i * (s + 3)
            if i < n:
                f.rect(x, y, 26, s, ORANGE_FILL if row == 16 else BLUE_FILL, ORANGE if row == 16 else BLUE, 1, rx=2)
            else:
                f.rect(x, y, 26, s, "#ffffff", MUTED, 1, rx=2, dash="3 2")
        f.text(x + 13, 158, row + 1, 10, ORANGE if row == 16 else MUTED, "middle", "bold" if row == 16 else "normal")
    f.text(20, 186, "135 = 16 × 8 + 7 → 16 full rows + 1 more row for the last 7 = 17 rows", 14, weight="bold")
    save(f, "sol17-rows.svg")


def rows_left(f, x, y, n, per, s=13, gap=3, col=BLUE, fill=BLUE_FILL):
    full, left = divmod(n, per)
    for r in range(full + (1 if left else 0)):
        for c in range(per):
            idx = r * per + c
            cx = x + c * (s + gap) + s / 2
            cy = y + r * (s + gap) + s / 2
            if idx < n:
                f.circle(cx, cy, s / 2, fill if r < full else ORANGE_FILL, col if r < full else ORANGE, 1.5)
            else:
                f.circle(cx, cy, s / 2, "#ffffff", RED, 1.5, dash="3 2")
    return full, left


def sol24():
    f = Fig(680, 230, "22 students in rows of 6 and rows of 8", "22 students make 3 rows of 6 with 4 left, and 2 rows of 8 with 6 left. "
            "Both times the last row is 2 short.")
    f.text(20, 28, "M1-Q24: both leftovers are “2 short”", 17, weight="bold")
    f.text(20, 56, "Rows of 6", 14, BLUE, weight="bold")
    rows_left(f, 20, 66, 22, 6)
    f.text(20, 154, "3 rows + 4 left (2 short)", 13, MUTED)
    f.text(340, 56, "Rows of 8", 14, BLUE, weight="bold")
    rows_left(f, 340, 66, 22, 8)
    f.text(340, 134, "2 rows + 6 left (2 short)", 13, MUTED)
    f.text(20, 186, "Add the 2 missing students: 22 + 2 = 24 = LCM(6, 8).", 14, GREEN, weight="bold")
    f.text(20, 208, "Next possibility is 48 − 2 = 46, which is not fewer than 40.", 13, MUTED)
    save(f, "sol24-rows.svg")


def sol26():
    f = multiples_rows("sol26-teeth.svg", "M1-Q26: teeth passing the contact point",
                       "Gear A completes a turn every 12 teeth and gear B every 18 teeth; both are back at the start after 36 teeth.",
                       [12, 18], ["A full turns", "B full turns"], 36, "teeth passed",
                       "Both marks are back after LCM(12, 18) = 36 teeth: A turns 36 ÷ 12 = 3 times, B turns 2 times.",
                       highlight_all=False)
    save(f, "sol26-teeth.svg")


def sol27():
    sc, cw, ch, side = 8, 10, 6, 30
    f = Fig(520, 372, "M1-Q27: smallest square from 10 × 6 cards",
            "A 30 by 30 square made of cards 10 wide and 6 tall: 3 across and 5 down, 15 cards.")
    f.text(20, 28, "M1-Q27: smallest square from 10 cm × 6 cm cards", 17, weight="bold")
    x0, y0 = 70, 64
    for i in range(side // cw):
        for j in range(side // ch):
            f.rect(x0 + i * cw * sc, y0 + j * ch * sc, cw * sc, ch * sc,
                   BLUE_FILL if (i + j) % 2 == 0 else "#c6dafc", BLUE, 1.2)
    f.rect(x0, y0, side * sc, side * sc, "none", INK, 2.5)
    f.text(x0 + side * sc / 2, y0 - 8, "30 cm", 14, INK, "middle", "bold")
    f.text(x0 - 10, y0 + side * sc / 2 + 5, "30 cm", 14, INK, "end", "bold")
    f.text(x0 + side * sc + 14, y0 + 20, "3 cards across", 13, MUTED)
    f.text(x0 + side * sc + 14, y0 + 40, "(30 ÷ 10)", 13, MUTED)
    f.text(x0 + side * sc + 14, y0 + 70, "5 cards down", 13, MUTED)
    f.text(x0 + side * sc + 14, y0 + 90, "(30 ÷ 6)", 13, MUTED)
    f.text(20, 354, "Side = LCM(6, 10) = 30 cm → 3 × 5 = 15 cards", 14, GREEN, weight="bold")
    save(f, "sol27-square.svg")


def sol28():
    f = Fig(500, 524, "Lockers 1 to 100 at the end", "A 10 by 10 grid of lockers. Only the perfect squares "
            "1, 4, 9, 16, 25, 36, 49, 64, 81 and 100 end open; 81 is highlighted.")
    f.text(20, 28, "M1-Q28: lockers left open", 17, weight="bold")
    cell, x0, y0 = 44, 30, 44
    squares = {k * k for k in range(1, 11)}
    for n in range(1, 101):
        r, c = divmod(n - 1, 10)
        x, y = x0 + c * cell, y0 + r * cell
        if n in squares:
            f.rect(x + 2, y + 2, cell - 4, cell - 4, GREEN_FILL, GREEN, 2.5 if n == 81 else 1.5, rx=4)
            f.text(x + cell / 2, y + cell / 2 + 5, n, 13, GREEN, "middle", "bold")
        else:
            f.rect(x + 2, y + 2, cell - 4, cell - 4, GRAY_FILL, LINE, 1, rx=4)
            f.text(x + cell / 2, y + cell / 2 + 5, n, 11, MUTED, "middle")
    f.text(20, 492, "Open = changed an odd number of times", 13)
    f.text(20, 510, "= an odd number of factors = a perfect square.", 13)
    save(f, "sol28-lockers.svg")


def sol29():
    cands = [2, 3, 4, 6, 12]
    f = Fig(680, 70 + len(cands) * 46 + 50, "Testing each possible interval",
            "Intervals 2, 3, 4, 6 and 12 all fit chimes at 0, 36 and 60. Intervals 2, 3 and 6 would also chime at "
            "minute 18, so they are ruled out; 4 and 12 remain.")
    f.text(20, 30, "M1-Q29: which intervals survive minute 18?", 17, weight="bold")
    x0, x1 = 120, 600
    sx = lambda m: x0 + (x1 - x0) * m / 60
    top = 56
    f.rect(sx(18) - 10, top - 6, 20, len(cands) * 46, "#fff1f1", RED, 1.2, rx=5)
    for i, k in enumerate(cands):
        y = top + 18 + i * 46
        bad = 18 % k == 0
        col = RED if bad else GREEN
        f.text(20, y + 5, f"every {k} min", 14, col, weight="bold")
        f.line(x0, y, x1, y, LINE, 1)
        for m in range(0, 61, k):
            f.circle(sx(m), y, 3.2 if m not in (0, 18, 36, 60) else 5.5,
                     GREEN_FILL if not bad else "#ffffff", col, 1.3)
        if bad:
            f.cross(x1 + 30, y, 7)
        else:
            f.tick(x1 + 30, y, 8)
    ay = top + len(cands) * 46 + 8
    for m in (0, 18, 36, 60):
        f.text(sx(m), ay, m, 12, RED if m == 18 else MUTED, "middle", "bold")
    f.text(20, ay + 26, "Common factors of 36 and 60 (at least 2): 2, 3, 4, 6, 12.  A chime at 18 rules out 2, 3, 6.", 13)
    save(f, "sol29-intervals.svg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    learn_gcf_bags(); learn_lcm_line(); learn_decide(); learn_remainder(); learn_factor_tree(); learn_worked_floor()
    q13_stem(); q26_stem(); q27_stem(); q28_stem(); q29_stem()
    sol01(); sol03(); sol08(); sol10(); sol13(); sol17(); sol24(); sol26(); sol27(); sol28(); sol29()
