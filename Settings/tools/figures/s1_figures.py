"""Regenerate the S1 ecology learning, question and solution figures."""

from pathlib import Path

from svgkit import (
    BLUE, BLUE_FILL, GRAY_FILL, GREEN, GREEN_FILL, INK, LINE, MUTED,
    ORANGE, ORANGE_FILL, Fig,
)

ASSETS = Path(__file__).resolve().parents[2] / "assets" / "S1"


def card(title, description, height, width=600):
    fig = Fig(width, height, title, description)
    fig.text(22, 29, title, 18, weight="bold")
    return fig


def node(fig, cx, cy, label, fill=GRAY_FILL, width=106, height=34):
    fig.rect(cx - width / 2, cy - height / 2, width, height, fill, LINE, rx=7)
    fig.text(cx, cy + 5, label, 14, anchor="middle", weight="bold")


def arrow(fig, *points):
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        fig.line(x1, y1, x2, y2, MUTED, 1.6, arrow=(x2, y2) == points[-1])


def legend(fig, label):
    fig.text(22, fig.h - 14, label, 13, MUTED)


def roles():
    fig = card("One animal can fill both roles",
               "A grasshopper is eaten by a frog, and the frog is eaten by a heron. "
               "The frog is a predator of the grasshopper and prey of the heron.", 158)
    arrow(fig, (158, 90), (234, 90))
    arrow(fig, (366, 90), (442, 90))
    node(fig, 95, 90, "Grasshopper", ORANGE_FILL, width=114)
    node(fig, 300, 90, "Frog", BLUE_FILL, width=120)
    node(fig, 505, 90, "Heron", ORANGE_FILL, width=114)
    fig.text(198, 69, "Frog is predator", 14, anchor="middle")
    fig.text(402, 69, "Frog is prey", 14, anchor="middle")
    legend(fig, "Read each arrow as “is eaten by.”")
    return fig


def chain():
    fig = card("Follow energy from the producer",
               "Grass makes its own food. A rabbit eats the grass, "
               "and a fox eats the rabbit. Energy flows from grass to rabbit to fox.", 154)
    arrow(fig, (158, 82), (234, 82))
    arrow(fig, (366, 82), (442, 82))
    for x, label, role, fill in [
        (95, "Grass", "Producer", GREEN_FILL),
        (300, "Rabbit", "Consumer", BLUE_FILL),
        (505, "Fox", "Consumer", ORANGE_FILL),
    ]:
        node(fig, x, 82, label, fill, width=112)
        fig.text(x, 122, role, 14, MUTED, "middle")
    return fig


def resources():
    fig = card("Change one resource to test its effect",
               "In the first comparison both light and water change. "
               "In the second comparison light changes and water stays the same, "
               "so the result can be used to test light.", 228)
    columns = (383, 519)
    for y, title, changed in [(54, "Two resources change", True), (139, "Only light changes", False)]:
        fig.rect(22, y, 556, 67, GRAY_FILL, LINE, rx=8)
        fig.text(36, y + 26, title, 14, weight="bold")
        fig.text(36, y + 48, "A and B are identical otherwise.", 12, MUTED)
        for x, text in zip(columns, ("Group A", "Group B"), strict=True):
            fig.text(x, y + 19, text, 14, anchor="middle", weight="bold")
        for x, light, water, light_fill in [
            (columns[0], "Bright light", "20 mL water", BLUE_FILL),
            (columns[1], "Shade", "10 mL water" if changed else "20 mL water", ORANGE_FILL),
        ]:
            fig.rect(x - 54, y + 26, 108, 19, light_fill, "none", rx=4)
            fig.text(x, y + 40, light, 13, anchor="middle")
            fig.text(x, y + 59, water, 13, anchor="middle")
    return fig


def distance():
    fig = card("Count links to the changed population",
               "Grass is eaten by rabbits, and rabbits are eaten by foxes. "
               "If foxes change, rabbits are one link away and grass is two links away.", 172)
    arrow(fig, (147, 90), (235, 90))
    arrow(fig, (365, 90), (453, 90))
    for x, label, note, fill in [
        (90, "Grass", "Two links · indirect", GREEN_FILL),
        (300, "Rabbit", "One link · direct", BLUE_FILL),
        (510, "Fox", "Changed population", ORANGE_FILL),
    ]:
        node(fig, x, 90, label, fill)
        fig.text(x, 133, note, 14, anchor="middle")
    legend(fig, "Feeding arrows still point from food to eater.")
    return fig


def pond():
    fig = card("Garden pond feeding relationships",
               "Flower nectar is eaten by flies. Flies are eaten by spiders and dragonflies. "
               "Frogs eat spiders and dragonflies, bats eat dragonflies, and herons eat frogs.", 266, width=622)
    for points in [
        ((133, 125), (151, 125)),
        ((241, 118), (262, 118), (262, 83), (281, 83)),
        ((241, 132), (262, 132), (262, 168), (281, 168)),
        ((385, 83), (404, 83), (404, 114), (424, 114)),
        ((385, 164), (410, 164), (410, 129), (424, 129)),
        ((385, 175), (405, 175), (405, 197), (424, 197)),
        ((509, 121), (533, 121)),
    ]:
        arrow(fig, *points)
    for x, y, width, label in [
        (76, 125, 110, "Flower nectar"), (198, 125, 82, "Fly"), (332, 83, 96, "Spider"),
        (332, 171, 96, "Dragonfly"), (466, 121, 78, "Frog"), (466, 197, 78, "Bat"),
        (567, 121, 62, "Heron"),
    ]:
        node(fig, x, y, label, width=width)
    legend(fig, "Feeding arrows point from food to eater.")
    return fig


def farmland():
    fig = card("Farmland food web",
               "Seeds are eaten by mice and sparrows. Mice are eaten by owls and snakes. "
               "Owls also eat snakes and sparrows. Weasels eat sparrows.", 242)
    for points in [
        ((122, 123), (174, 73)), ((122, 131), (174, 176)),
        ((270, 65), (348, 65)), ((270, 72), (310, 108), (472, 108), (492, 118)),
        ((452, 65), (493, 104)), ((270, 173), (340, 143), (475, 143), (492, 135)),
        ((270, 182), (348, 182)),
    ]:
        arrow(fig, *points)
    for x, y, label in [
        (72, 127, "Seeds"), (222, 68, "Mouse"), (222, 178, "Sparrow"),
        (400, 65, "Snake"), (400, 182, "Weasel"), (540, 125, "Owl"),
    ]:
        node(fig, x, y, label, width=92)
    legend(fig, "Feeding arrows point from food to eater.")
    return fig


def ocean():
    fig = card("Ocean food web",
               "Phytoplankton are eaten by zooplankton, which are eaten by sardines. "
               "Sardines are eaten by tuna and seabirds. Sharks eat tuna.", 206, width=662)
    for points in [
        ((138, 117), (154, 117)), ((270, 117), (286, 117)),
        ((376, 109), (395, 109), (395, 74), (413, 74)),
        ((376, 126), (395, 126), (395, 158), (413, 158)),
        ((513, 74), (553, 74)),
    ]:
        arrow(fig, *points)
    for x, y, label, width in [
        (80, 117, "Phytoplankton", 110), (212, 117, "Zooplankton", 110),
        (330, 117, "Sardine", 88), (463, 74, "Tuna", 94),
        (463, 158, "Seabird", 94), (601, 74, "Shark", 90),
    ]:
        node(fig, x, y, label, width=width)
    legend(fig, "Feeding arrows point from food to eater.")
    return fig


def planet():
    fig = card("Feeding relationships on the planet",
               "Glims eat floots, zarks eat glims, and vexes eat zarks and glims.", 198)
    for x in (131, 278, 425):
        arrow(fig, (x, 91), (x + 39, 91))
    arrow(fig, (223, 111), (223, 138), (517, 138), (517, 111))
    for x, label in [(76, "Floots"), (223, "Glims"), (370, "Zarks"), (517, "Vexes")]:
        node(fig, x, 91, label)
    legend(fig, "Feeding arrows point from food to eater.")
    return fig


def lake():
    fig = card("Lake food chain",
               "Phytoplankton are eaten by zooplankton, which are eaten by small fish. "
               "Large fish eat small fish.", 134)
    for x in (144, 286, 426):
        arrow(fig, (x, 76), (x + 27, 76))
    for x, width, label in [
        (85, 112, "Phytoplankton"), (229, 110, "Zooplankton"),
        (369, 110, "Small fish"), (509, 110, "Large fish"),
    ]:
        node(fig, x, 76, label, width=width)
    legend(fig, "Feeding arrows point from food to eater.")
    return fig


def plot_series(fig, label, points, ceiling, top, height, color):
    """Draw one zero-based count axis and label every observed point."""
    left, right = 113, 558
    baseline = top + height
    step = (right - left) / (len(points) - 1)
    result = [(left + index * step, baseline - height * count / ceiling)
              for index, count in enumerate(points)]
    fig.text(22, top + 22, label, 14, weight="bold")
    fig.text(98, top + 4, f"{ceiling:,}", 12, MUTED, "end")
    fig.text(98, baseline + 4, "0", 12, MUTED, "end")
    fig.line(left, baseline, right, baseline, LINE)
    fig.line(left, top, right, top, LINE, dash="4 4")
    fig.line(left, top, left, baseline, LINE)
    for (x1, y1), (x2, y2) in zip(result, result[1:]):
        fig.line(x1, y1, x2, y2, color, 2.5)
    for (x, y), number in zip(result, points, strict=True):
        fig.circle(x, y, 4.2, "#ffffff", color, 2)
        fig.text(x, y - 8, number, 13, INK, "middle", "bold")
    return [x for x, _ in result]


def hares_and_lynx():
    fig = card("The lynx peak follows the hare peak",
               "Hare counts across years 1 to 6 are 40, 60, 80, 50, 30, 45. "
               "Lynx counts are 4, 6, 10, 14, 9, 5. "
               "Hares are highest in year 3 and lynx are highest in year 4.", 288)
    xs = plot_series(fig, "Hares", [40, 60, 80, 50, 30, 45], 100, 61, 65, GREEN)
    plot_series(fig, "Lynx", [4, 6, 10, 14, 9, 5], 20, 152, 65, BLUE)
    for year, x in enumerate(xs, 1):
        fig.text(x, 241, f"Year {year}", 13, anchor="middle")
    legend(fig, "Compare when each line changes direction. The count axes have different scales.")
    return fig


def aphids():
    fig = card("Compare each week with the previous week",
               "The aphid counts from week 1 to week 5 are 200, 260, 300, 180 and 90. "
               "The four changes are plus 60, plus 40, minus 120 and minus 90.", 220)
    xs = plot_series(fig, "Aphids", [200, 260, 300, 180, 90], 350, 54, 79, BLUE)
    for index, x in enumerate(xs, 1):
        fig.text(x, 156, f"Week {index}", 13, anchor="middle")
    for start, end, change in zip(xs, xs[1:], ["+60", "+40", "−120", "−90"]):
        cx = (start + end) / 2
        node(fig, cx, 186, change, GREEN_FILL if change == "−120" else GRAY_FILL,
             width=73, height=27)
    return fig


def beetles():
    fig = card("Compare each species with its own tank",
               "Red beetles finish at 200 alone and 120 together, 80 fewer. "
               "Grey beetles finish at 180 alone and 40 together, 140 fewer.", 239)
    for index, (label, alone, together) in enumerate([
        ("Red beetles", 200, 120), ("Grey beetles", 180, 40),
    ]):
        y = 52 + 85 * index
        fig.text(22, y + 11, label, 14, weight="bold")
        for offset, state, count, fill, line in [
            (0, "Alone", alone, BLUE_FILL, BLUE), (28, "Together", together, ORANGE_FILL, ORANGE),
        ]:
            fig.text(126, y + offset + 14, state, 13, MUTED)
            width = count * 1.34
            fig.rect(195, y + offset, width, 19, fill, line, rx=4)
            fig.text(204 + width, y + offset + 14, count, 13, weight="bold")
        fig.text(510, y + 31, f"{alone - together} fewer", 14, INK, weight="bold")
    legend(fig, "Bar lengths use the same scale. Both species started with 50 per occupied tank.")
    return fig


def marker_test():
    fig = card("One population separates the two possibilities",
               "Phytoplankton, zooplankton, small fish and large fish are shown in that order. "
               "If the dye starts in zooplankton, the results are absent, detected, detected, detected. "
               "If it starts in small fish, the results are absent, absent, detected, detected.",
               216, width=650)
    columns = [242, 349, 456, 563]
    for x, label in zip(columns, ["Phytoplankton", "Zooplankton", "Small fish", "Large fish"], strict=True):
        fig.text(x, 68, label, 14, anchor="middle", weight="bold")
    for y, label, results in [
        (86, "Starts in zooplankton", [False, True, True, True]),
        (130, "Starts in small fish", [False, False, True, True]),
    ]:
        fig.text(22, y + 24, label, 14, weight="bold")
        for x, detected in zip(columns, results, strict=True):
            node(fig, x, y + 19, "Detected" if detected else "Absent",
                 BLUE_FILL if detected else GRAY_FILL, width=96)
    fig.rect(296, 49, 106, 123, "none", GREEN, 2, 8, dash="4 3")
    legend(fig, "Only the zooplankton result differs between the two starting populations.")
    return fig


def toads():
    fig = card("Compare the counts before and after toads arrive",
               "Lizard counts are 50, 52, 51, 40 and 28. Beetle counts are 900, 880, 890, 600 and 400. "
               "Toad counts are 0, 0, 20, 80 and 150. Toads arrived at the start of year 3.", 363)
    xs = plot_series(fig, "Lizards", [50, 52, 51, 40, 28], 65, 72, 57, BLUE)
    plot_series(fig, "Beetles", [900, 880, 890, 600, 400], 1100, 155, 57, GREEN)
    plot_series(fig, "Toads", [0, 0, 20, 80, 150], 200, 238, 57, ORANGE)
    threshold = (xs[1] + xs[2]) / 2
    fig.line(threshold, 61, threshold, 304, MUTED, 1, "4 4")
    fig.text(threshold + 8, 57, "Toads arrive in Year 3", 13, MUTED)
    for year, x in enumerate(xs, 1):
        fig.text(x, 321, f"Year {year}", 13, anchor="middle")
    legend(fig, "The counts fit competition for food. They do not establish a cause.")
    return fig


def main():
    figures = {
        "learn-relative-roles": roles,
        "learn-energy-flow": chain,
        "learn-change-one-resource": resources,
        "learn-direct-indirect": distance,
        "q02-pond-web": pond,
        "q13-farmland-web": farmland,
        "q19-ocean-web": ocean,
        "q24-planet-web": planet,
        "q27-lake-chain": lake,
        "sol09-hare-lynx-trends": hares_and_lynx,
        "sol15-aphid-change": aphids,
        "sol21-beetle-competition": beetles,
        "sol27-dye-test": marker_test,
        "sol29-lizard-beetle-toad-counts": toads,
    }
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, draw in figures.items():
        draw().save(ASSETS / f"{name}.svg")


if __name__ == "__main__":
    main()
