"""Generate labelled circuit diagrams for the S4 lessons, drills and solutions."""

from dataclasses import dataclass
from pathlib import Path

from svgkit import BLUE, BLUE_FILL, GRAY_FILL, INK, MUTED, ORANGE_FILL, Fig


ASSETS = Path(__file__).resolve().parents[2] / "assets" / "S4"


def card(width, height, title, description):
    fig = Fig(width, height, title, description)
    fig.text(24, 27, title, 17, weight="bold")
    return fig


def save(fig, name):
    fig.save(ASSETS / f"{name}.svg")


def wire(fig, x1, y1, x2, y2, color=INK):
    fig.line(x1, y1, x2, y2, color, 2.6)


def junction(fig, x, y):
    fig.circle(x, y, 3.9, INK, "none")


def terminal(fig, x, y, positive):
    fig.circle(x, y, 12, GRAY_FILL, INK)
    fig.text(x, y + 5, "+" if positive else "−", 17, anchor="middle", weight="bold")


def contact(fig, x, y, color=INK):
    fig.circle(x, y, 3.5, "#fff", color, 1.6)


@dataclass(frozen=True)
class Part:
    x: int
    kind: str
    label: str
    state: str = ""

    @property
    def radius(self):
        return {"switch": 16, "lamp": 13, "sample": 16, "site": 0, "material": 19, "break": 9}[self.kind]

    def draw(self, fig, y, color):
        x, radius = self.x, self.radius
        if self.kind == "lamp":
            fill = ORANGE_FILL if self.state == "lit" else "#fff"
            fig.circle(x, y, radius, fill, color, 2)
            fig.line(x - 5, y - 5, x + 5, y + 5, color, 1.6)
            fig.line(x - 5, y + 5, x + 5, y - 5, color, 1.6)
        elif self.kind == "switch":
            if not self.state:
                fig.rect(x - radius, y - 10, 2 * radius, 20, BLUE_FILL, color, 1.5, 4)
                fig.text(x, y + 5, self.label, 13, anchor="middle", weight="bold")
                return
            angle = 11 if self.state == "open" else 0
            wire(fig, x - radius, y, x + radius, y - angle, color)
            contact(fig, x - radius, y, color)
            contact(fig, x + radius, y, color)
        elif self.kind == "break":
            fig.line(x - 5, y - 5, x + 5, y + 5, INK, 2)
            fig.line(x - 5, y + 5, x + 5, y - 5, INK, 2)
        elif self.kind == "site":
            fig.rect(x - 8, y - 7, 16, 14, "none", MUTED, 1, 3, dash="3 2")
        else:
            if self.kind == "material":
                fill = BLUE_FILL if color == BLUE else GRAY_FILL
                fig.rect(x - radius, y - 6, 2 * radius, 12, fill, color, 1.5, 2)
            contact(fig, x - radius, y)
            contact(fig, x + radius, y)

        below = self.kind == "switch" and self.state
        label = f"{self.label} {self.state}" if below else self.label
        fig.text(x, y + 23 if below else y - 19, label, 13, anchor="middle",
                 weight="bold" if self.kind == "site" else "normal")


def lamp(x, label, state=""):
    return Part(x, "lamp", label, state)


def switch(x, label, state=""):
    return Part(x, "switch", label, state)


def sample(x, label):
    return Part(x, "sample", label)


def site(x, label):
    return Part(x, "site", label)


def trace(fig, start, end, y, parts=(), color=INK):
    left = start
    for part in parts:
        wire(fig, left, y, part.x - part.radius, y, color)
        part.draw(fig, y, color)
        left = part.x + part.radius
    wire(fig, left, y, end, y, color)


def fork(fig, left, right, rows, entering=(), leaving=(), proved=None):
    """Draw rails, the shared route, and a separate row for each branch.

    Each distinct row is attached to both rails. A blue row is one proved
    conducting route and includes the shared wire back to the battery.
    """
    first_y, _ = rows[0]
    last_y, _ = rows[-1]
    terminal(fig, 31, first_y, True)
    terminal(fig, fig.w - 31, first_y, False)
    rail_end = proved if proved is not None else first_y
    rail_color = BLUE if proved is not None else INK
    for x in (left, right):
        wire(fig, x, first_y, x, last_y)
        wire(fig, x, first_y, x, rail_end, rail_color)
    trace(fig, 43, left, first_y, entering, rail_color)
    trace(fig, right, fig.w - 43, first_y, leaving, rail_color)
    for y, parts in rows:
        trace(fig, left, right, y, parts, BLUE if y == proved else INK)
        if y != last_y:
            junction(fig, left, y)
            junction(fig, right, y)


def series(fig, y, parts, color=INK):
    terminal(fig, 31, y, True)
    terminal(fig, fig.w - 31, y, False)
    trace(fig, 43, fig.w - 43, y, parts, color)


def teaching():
    fig = card(583, 229, "Trace the whole route between the terminals",
               "Two versions of a one-switch circuit. A closed switch gives a complete path through the lit "
               "lamp. An open switch leaves a break after the dark lamp.")
    series(fig, 77, (lamp(202, "Lamp lit", "lit"), switch(386, "S", "closed")), BLUE)
    series(fig, 164, (lamp(202, "Lamp dark"), switch(386, "S", "open")))
    fig.line(22, 120, fig.w - 22, 120, MUTED, 0.8, dash="3 4")
    fig.text(24, 213, "A break after the bulb interrupts the same loop.", 14, MUTED)
    save(fig, "learn-trace-loop")

    fig = card(583, 294, "Compare one route with two branches",
               "The upper diagram has two bulbs in a single route. The lower diagram splits at one junction "
               "and rejoins at another, with one bulb on each branch.")
    series(fig, 85, (lamp(225, "Bulb 1"), lamp(365, "Bulb 2")))
    fig.text(24, 116, "Series · both bulbs are on the same route.", 14, MUTED)
    fig.line(22, 136, fig.w - 22, 136, MUTED, 0.8, dash="3 4")
    fork(fig, 143, 442, [(182, (lamp(292, "Bulb 1"),)), (242, (lamp(292, "Bulb 2"),))])
    fig.text(143, 266, "Split", 13, MUTED, "middle")
    fig.text(442, 266, "Rejoin", 13, MUTED, "middle")
    fig.text(24, 281, "Parallel · each branch connects the same two junctions.", 14, MUTED)
    save(fig, "learn-series-parallel")

    fig = card(548, 225, "Use the lit bulb as evidence",
               "K is lit on the lower branch, so its switch B and the common switch C are closed. "
               "J is dark on the upper branch; its switch A is open in this illustrated circuit.")
    fork(fig, 170, 467,
         [(81, (switch(244, "A", "open"), lamp(368, "J dark"))),
          (152, (switch(244, "B", "closed"), lamp(368, "K lit", "lit")))],
         entering=(switch(108, "C", "closed"),), proved=152)
    fig.text(24, 205, "Blue shows the route that proves B and C conduct.", 14, BLUE)
    save(fig, "learn-trace-lit")

    fig = card(583, 210, "Test a sample with one gap",
               "First, bridge both contacts with known metal and check that the bulb lights. "
               "Next place the unknown sample across the same contacts and observe the bulb again.")
    series(fig, 74, (lamp(213, "Bulb lit", "lit"), Part(385, "material", "Known metal")), BLUE)
    fig.text(24, 106, "1. Check the tester with a known conductor.", 14, MUTED)
    series(fig, 151, (lamp(213, "Observe bulb"), Part(385, "material", "Unknown sample")))
    fig.text(24, 184, "2. Replace the metal with the sample. Keep the rest of the loop the same.", 14, MUTED)
    save(fig, "learn-test-material")


def q03_and_q05():
    fig = card(584, 171, "Two branches and two shared switches",
               "The upper branch passes through T and bulb A. The lower passes through U and bulb B. "
               "Both routes pass through R and S after rejoining.")
    fork(fig, 110, 369, [(82, (switch(174, "T"), lamp(268, "Bulb A"))),
                        (135, (switch(174, "U"), lamp(268, "B lit", "lit")))],
         leaving=(switch(425, "R"), switch(490, "S")))
    save(fig, "q03-shared-return")

    fig = card(584, 171, "Red and White branches",
               "The battery feeds shared switch M, then splits. One branch contains Red, the other X, Y and White. "
               "Red is lit and White is dark.")
    fork(fig, 174, 491, [(82, (lamp(383, "Red lit", "lit"),)),
                        (135, (switch(239, "X"), switch(311, "Y"), lamp(417, "White dark")))],
         entering=(switch(107, "M"),))
    save(fig, "q05-red-white")


def q07_q09_q12():
    fig = card(562, 123, "Two sample gaps in one route",
               "From the positive terminal, the path passes through gap 1, the bulb and gap 2 to the negative terminal.")
    series(fig, 80, (sample(163, "Gap 1"), lamp(281, "Bulb"), sample(399, "Gap 2")))
    save(fig, "q07-sample-gaps")

    fig = card(584, 170, "Intact wire positions W, U and V",
               "W lies before the split. U is on the East lamp branch and V is on the West lamp branch. "
               "All three marked positions are intact wire.")
    fork(fig, 163, 484, [(79, (site(254, "U"), lamp(391, "East"))),
                        (136, (site(254, "V"), lamp(391, "West")))], entering=(site(106, "W"),))
    save(fig, "q09-switch-positions")

    fig = card(610, 173, "Four labelled positions on intact wires",
               "Position 3 is before the split and 4 is after the rejoin. On the upper route, position 1 is "
               "before bulbs P and Q and position 2 follows them. The lower route contains bulb R.")
    fork(fig, 131, 483, [(82, (site(186, "1"), lamp(248, "P"), lamp(327, "Q"), site(418, "2"))),
                        (138, (lamp(327, "R"),))], entering=(site(84, "3"),), leaving=(site(526, "4"),))
    save(fig, "q12-break-positions")


def q11_selector():
    fig = card(596, 181, "Selector S has two separate outputs",
               "The battery positive lead enters selector S. Output U leads to K and output D leads to L then M. "
               "Both branches meet the negative return. S connects to just one output at a time.")
    y_top, y_bottom = 78, 132
    terminal(fig, 31, 105, True)
    trace(fig, 43, 121, 105)
    fig.rect(121, 59, 93, 92, GRAY_FILL, MUTED, 1.4, 6)
    fig.text(167, 101, "Selector S", 13, anchor="middle", weight="bold")
    fig.text(203, y_top + 5, "U", 13, anchor="end")
    fig.text(203, y_bottom + 5, "D", 13, anchor="end")
    for y, parts in [(y_top, (lamp(354, "K"),)), (y_bottom, (lamp(305, "L"), lamp(401, "M")))]:
        contact(fig, 214, y)
        trace(fig, 218, 495, y, parts)
    wire(fig, 495, y_top, 495, y_bottom)
    trace(fig, 495, 553, y_top)
    junction(fig, 495, y_top)
    terminal(fig, 565, y_top, False)
    save(fig, "q11-selector-outputs")


def q15_samples(fig, known=False):
    upper = "Blue lit"
    lower = "Amber dark"
    labels = ("X conducts", "Y insulates", "Z conducts") if known else ("Sample X", "Sample Y", "Sample Z")
    upper_sample, lower_sample, shared_sample = (
        Part(x, "material", label) for x, label in zip((242, 242, 101), labels, strict=True)
    )
    fork(fig, 166, 482, [(79, (upper_sample, lamp(389, upper, "lit"))),
                        (137, (lower_sample, lamp(389, lower)))],
         entering=(shared_sample,), proved=79 if known else None)


def q15_and_q23():
    fig = card(584, 175, "Three samples and two bulbs",
               "Sample Z is on the shared wire. The upper branch contains X and Blue, which is lit. "
               "The lower branch contains Y and Amber, which is dark.")
    q15_samples(fig)
    save(fig, "q15-three-samples")

    fig = card(584, 176, "Starting positions for A, B and C",
               "C is closed on the shared wire. The upper branch contains closed A followed by L and M. "
               "The lower branch contains open B followed by N.")
    fork(fig, 162, 500,
         [(78, (switch(231, "A", "closed"), lamp(326, "L"), lamp(413, "M"))),
          (134, (switch(231, "B", "open"), lamp(326, "N")))],
         entering=(switch(102, "C", "closed"),))
    save(fig, "q23-three-switches")


def q27_cable():
    fig = card(612, 202, "Two-wire cable and clip lead",
               "The near contacts U and V are separate. The upper wire leads from U to Map and the lower wire "
               "from V to Desk as labelled. The lamps share a return to negative. The positive clip is unattached.")
    fig.rect(153, 43, 222, 111, BLUE_FILL, MUTED, 1.1, 6)
    fig.text(264, 63, "Two separate wires", 13, MUTED, "middle")
    for y, near, far in [(88, "U", "Map"), (131, "V", "Desk")]:
        contact(fig, 116, y)
        fig.text(98, y + 5, near, 14, anchor="end", weight="bold")
        trace(fig, 120, 529, y, (lamp(436, far),))
        contact(fig, 375, y)
    wire(fig, 529, 88, 529, 131)
    junction(fig, 529, 88)
    trace(fig, 529, 569, 88)
    terminal(fig, 581, 88, False)
    terminal(fig, 31, 171, True)
    fig.path("M43,171 H83 Q96,171 96,155", stroke=INK, sw=2.6)
    fig.path("M90,151 L96,155 L102,151", stroke=INK, sw=1.7)
    fig.text(110, 176, "Movable positive clip", 13, MUTED)
    save(fig, "q27-two-wire-cable")


def tracks(fig, upper, lower, left, right, highlight=True):
    """Draw separate rails with one independently selectable contact at each end."""
    mid = (upper + lower) / 2
    track_x1, track_x2 = 157, 452
    left_pivot, right_pivot = 111, 499
    complete = left == right
    route_color = BLUE if complete and highlight else INK
    terminal(fig, 31, mid, True)
    trace(fig, 43, left_pivot, mid, color=route_color)
    trace(fig, right_pivot, fig.w - 43, mid,
          (lamp(fig.w - 89, "Lamp", "lit" if complete else ""),), route_color)
    terminal(fig, fig.w - 31, mid, False)
    for y, label in [(upper, "Upper track"), (lower, "Lower track")]:
        color = route_color if y == left else INK
        wire(fig, track_x1, y, track_x2, y, color)
        contact(fig, track_x1, y, color)
        contact(fig, track_x2, y, color)
        fig.text((track_x1 + track_x2) / 2, y - 9, label, 13, MUTED, "middle")
    for pivot, other, selected, label in [(left_pivot, track_x1, left, "Left"), (right_pivot, track_x2, right, "Right")]:
        wire(fig, pivot, mid, other, selected, route_color)
        contact(fig, pivot, mid, route_color)
        fig.text(pivot, lower + 21, label, 13, MUTED, "middle")


def q29_tracks():
    fig = card(657, 178, "Both selectors start on the upper track",
               "The positive lead feeds the left selector. Both selectors touch the upper track. The right "
               "selector returns through the lit lamp to negative. The lower track stays separate.")
    tracks(fig, 81, 137, 81, 81, highlight=False)
    save(fig, "q29-track-selectors")


def solutions():
    fig = card(584, 193, "Bulb B proves the shared return works",
               "The blue path runs through closed U and lit B, then through closed R and S. "
               "T is the open switch on dark bulb A's branch.")
    fork(fig, 110, 365, [(77, (switch(178, "T", "open"), lamp(269, "A dark"))),
                        (145, (switch(178, "U", "closed"), lamp(269, "B lit", "lit")))],
         leaving=(switch(420, "R", "closed"), switch(490, "S", "closed")), proved=145)
    save(fig, "sol03-trace-b")

    fig = card(584, 190, "Trace the blue branch to identify the samples",
               "Lit Blue proves both X and the shared Z conduct. Z serves Amber too, so the dark Amber branch "
               "identifies Y as the insulator.")
    q15_samples(fig, known=True)
    fig.text(24, 172, "The conducting route through Blue passes through X and Z.", 14, BLUE)
    save(fig, "sol15-trace-blue")

    fig = card(584, 327, "Before and after closing A",
               "Before, A and B are both open, so there is no route to the lamp even though C is closed. "
               "After A closes, the route through A and C lights L while B stays open.")
    for y, is_closed in [(77, False), (218, True)]:
        fig.text(24, y - 20, "After" if is_closed else "Before", 13, MUTED, weight="bold")
        fork(fig, 131, 336, [(y, (switch(231, "A", "closed" if is_closed else "open"),)),
                            (y + 58, (switch(231, "B", "open"),))],
             leaving=(switch(395, "C", "closed"), lamp(488, "L lit" if is_closed else "L dark", "lit" if is_closed else "")),
             proved=y if is_closed else None)
    fig.line(22, 177, fig.w - 22, 177, MUTED, 0.8, dash="3 4")
    save(fig, "sol19-before-after")

    fig = card(657, 335, "Matching track selections complete the route",
               "First snapshot: the left selector chooses lower and the right chooses upper, leaving the lamp dark. "
               "Second snapshot: both select lower, giving a complete route and lighting the lamp.")
    fig.text(24, 54, "First · lower / upper", 14, weight="bold")
    tracks(fig, 86, 134, 134, 86)
    fig.line(22, 170, fig.w - 22, 170, MUTED, 0.8, dash="3 4")
    fig.text(24, 198, "Second · lower / lower", 14, weight="bold")
    tracks(fig, 238, 286, 286, 286)
    save(fig, "sol29-track-snapshots")


def series_question(name, title, description, *parts):
    fig = card(584, 124, title, description)
    series(fig, 79, parts)
    save(fig, name)


def branch_question(name, title, description, left, right, branches, entering=(), leaving=()):
    fig = card(584, 123 + 58 * (len(branches) - 1), title, description)
    rows = [(78 + 58 * index, parts) for index, parts in enumerate(branches)]
    fork(fig, left, right, rows, entering, leaving)
    save(fig, name)


def additional_drills():
    branch_question("q02-two-bulbs", "Bulbs L and M", "Each bulb starts out lit on a separate branch.",
                    137, 447, [(lamp(289, "L", "lit"),), (lamp(289, "M", "lit"),)])
    series_question("q04-test-gap", "Bulb tester", "The wire joins the battery terminals through a bulb and a test gap.",
                    lamp(193, "Bulb"), sample(383, "Test gap"))
    branch_question("q06-return-switch", "Two branches with a shared return",
                    "A and L are on one branch, B and R are on the other, and C is shared.",
                    128, 417, [(switch(202, "A"), lamp(329, "L")), (switch(202, "B"), lamp(329, "R"))],
                    leaving=(switch(485, "C"),))
    branch_question("q08-three-bulbs", "Three bulbs on two branches",
                    "Switch A is open with P. Closed B shares a branch with Q and R.",
                    117, 488, [(lamp(192, "P"), switch(393, "A", "open")),
                               (lamp(192, "Q"), lamp(290, "R"), switch(393, "B", "closed"))])
    branch_question("q10-two-switch-paths", "Two switch paths feed lamp L",
                    "The routes through P and Q rejoin before the lamp.",
                    135, 371, [(switch(252, "P"),), (switch(252, "Q"),)], leaving=(lamp(466, "L"),))
    series_question("q13-bypass-contacts", "Two switches and a bulb",
                    "Switch P is open. Switch Q is closed. Both are on the path to the bulb.",
                    switch(153, "P", "open"), switch(281, "Q", "closed"), lamp(421, "Bulb"))
    series_question("q14-model-house", "Attic and hall bulbs",
                    "The path runs through switch A and the attic bulb, then switch H and the hall bulb.",
                    switch(122, "A", "closed"), lamp(232, "Attic"), switch(342, "H", "closed"), lamp(452, "Hall"))
    branch_question("q16-branch-pairs", "Four bulbs on three branches",
                    "The top branch contains J and K. L and M each have their own branch.",
                    139, 445, [(lamp(242, "J"), lamp(342, "K")), (lamp(292, "L"),), (lamp(292, "M"),)])
    series_question("q17-door-and-floor", "Door and floor switches",
                    "Switches D and F are one after the other on the route to the lamp.",
                    switch(155, "D"), switch(282, "F"), lamp(418, "Lamp"))
    branch_question("q18-three-branches", "One switch per branch",
                    "Closed A is with bulb 1, closed B is with bulb 2, and open C is with bulb 3.",
                    124, 460, [(switch(222, "A", "closed"), lamp(370, "Bulb 1")),
                               (switch(222, "B", "closed"), lamp(370, "Bulb 2")),
                               (switch(222, "C", "open"), lamp(370, "Bulb 3"))])
    branch_question("q19-lamp-switches", "Three switches control one lamp",
                    "Switches A and B are on separate routes. Both routes use C and L after they rejoin.",
                    112, 333, [(switch(224, "A"),), (switch(224, "B"),)],
                    leaving=(switch(397, "C"), lamp(486, "L")))
    series_question("q20-strip-tester", "Tester with a strip across the gap",
                    "The strip's ends are in contact on either side of the tester gap.",
                    Part(201, "material", "Strip"), lamp(387, "Lamp"))
    branch_question("q21-lit-left-bulb", "The left bulb is lit",
                    "The lit bulb comes before a split through A or B. Both routes use C after they rejoin.",
                    211, 430, [(switch(322, "A"),), (switch(322, "B"),)],
                    entering=(lamp(129, "Left lit", "lit"),), leaving=(switch(486, "C"),))
    branch_question("q22-master-switch", "A master switch after the split",
                    "Closed P is with Map, closed Q is with Clock, and the shared master switch is open.",
                    124, 415, [(switch(204, "P", "closed"), lamp(322, "Map")),
                               (switch(204, "Q", "closed"), lamp(322, "Clock"))],
                    leaving=(switch(482, "Master", "open"),))
    series_question("q24-clip-tester", "Tester with two metal clips",
                    "The bulb lights if a conductor makes a path across both clips.",
                    lamp(187, "Bulb"), sample(385, "Clips"))
    series_question("q25-dark-bulbs", "Two dark bulbs on one path",
                    "Both bulbs are dark. The route goes through closed M, P, unknown B, Q, and closed A.",
                    switch(106, "M", "closed"), lamp(201, "P dark"), switch(292, "B"),
                    lamp(383, "Q dark"), switch(478, "A", "closed"))
    series_question("q26-beacon", "Beacon with two switches",
                    "Switch S and switch T share the only route to the beacon.",
                    switch(163, "S"), lamp(291, "Beacon"), switch(418, "T"))
    branch_question("q28-fold-breaks", "Breaks marked by an X",
                    "The fold cuts the wire before P and the wire after Q. R's wire stays intact.",
                    116, 473, [(Part(179, "break", "Break"), lamp(286, "P")),
                               (lamp(286, "Q"), Part(403, "break", "Break")),
                               (lamp(286, "R"),)])
    fig = card(584, 197, "Two clips test a pair of pins",
               "The battery and test bulb are connected to two loose clips. The plug has three separate pins, "
               "labelled 1, 2 and 3. Clip to just two pins for each test.")
    series(fig, 78, (lamp(165, "Test bulb"), sample(370, "Loose clips")))
    fig.rect(150, 119, 320, 61, BLUE_FILL, MUTED, 1.4, 6)
    fig.text(173, 156, "Plug pins", 14, weight="bold")
    for pin, x in enumerate((303, 365, 427), 1):
        contact(fig, x, 141)
        fig.text(x, 166, pin, 13, anchor="middle")
    save(fig, "q30-plug-pins")


if __name__ == "__main__":
    teaching()
    q03_and_q05()
    q07_q09_q12()
    q11_selector()
    q15_and_q23()
    q27_cable()
    q29_tracks()
    additional_drills()
    solutions()
