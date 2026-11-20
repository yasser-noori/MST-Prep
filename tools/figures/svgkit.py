"""Tiny SVG helper for the MST prep question bank.

Figures are drawn on an opaque white card so they stay readable in both
GitHub's light and dark themes. Every figure gets a <title> and <desc> for
screen readers. Use only the palette below so pictures look consistent across
categories.
"""

from html import escape

FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

INK = "#1f2328"        # main text and outlines
MUTED = "#57606a"      # secondary text, axes
LINE = "#d0d7de"       # card border, light grid
BLUE = "#1f6feb"       # series 1
BLUE_FILL = "#ddeaff"
ORANGE = "#d4600f"     # series 2
ORANGE_FILL = "#ffe6d2"
GREEN = "#1a7f37"      # "this is the answer / match" highlight
GREEN_FILL = "#dcf5e3"
RED = "#cf222e"        # "ruled out"
GRAY_FILL = "#f2f4f7"


class Fig:
    def __init__(self, width, height, title, desc=""):
        self.w, self.h = width, height
        self.title, self.desc = title, desc
        self.parts = []

    # primitives -----------------------------------------------------------
    def add(self, raw):
        self.parts.append(raw)

    def rect(self, x, y, w, h, fill="none", stroke=INK, sw=1.5, rx=0, dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{o}/>')

    def circle(self, cx, cy, r, fill="none", stroke=INK, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.5, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = ' marker-end="url(#arrow)"' if arrow else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}{a}/>')

    def path(self, d, fill="none", stroke=INK, sw=1.5):
        self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')

    def text(self, x, y, s, size=15, fill=INK, anchor="start", weight="normal", italic=False):
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
                 f'text-anchor="{anchor}" font-weight="{weight}"{st}>{escape(str(s))}</text>')

    def cross(self, cx, cy, r=7, stroke=RED, sw=2.5):
        self.line(cx - r, cy - r, cx + r, cy + r, stroke, sw)
        self.line(cx - r, cy + r, cx + r, cy - r, stroke, sw)

    def tick(self, cx, cy, r=7, stroke=GREEN, sw=2.5):
        self.path(f"M{cx - r},{cy} L{cx - r/3},{cy + r*0.7} L{cx + r},{cy - r*0.7}", stroke=stroke, sw=sw)

    # output ---------------------------------------------------------------
    def svg(self):
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" font-family="{FONT}">'
                f'<title>{escape(self.title)}</title><desc>{escape(self.desc or self.title)}</desc>'
                '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>'
                f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}" rx="12" fill="#ffffff" stroke="{LINE}"/>')
        return head + "".join(self.parts) + "</svg>\n"

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())
