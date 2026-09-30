"""Minimal SVG builder for portfolio figures.

Figures are self-contained: explicit colors, light "paper figure" ground so they
read the same in light and dark site themes (same convention academic sites use
for embedded paper figures).
"""

BG      = "#fbfcfd"
BORDER  = "#e3e8ef"
INK     = "#0f172a"
MUTED   = "#5b6b7f"
FAINT   = "#93a2b6"
GRID    = "#eef2f7"

SANS = "'Inter','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class SVG:
    def __init__(self, w, h, pad=0):
        self.w, self.h = w, h
        self.parts = []
        self.defs = []
        self._markers = set()

    # ---------- primitives ----------
    def text(self, x, y, s, size=13, color=None, weight=400, anchor="start",
             font=SANS, opacity=1.0, spacing=None):
        color = color or INK
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}" '
            f'opacity="{opacity}"{ls}>{esc(s)}</text>')

    def rect(self, x, y, w, h, fill="none", stroke=None, rx=8, sw=1.25, dash=None, opacity=1.0):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}"{st}{da} opacity="{opacity}"/>')

    def line(self, x1, y1, x2, y2, stroke=None, sw=1.25, dash=None):
        stroke = stroke or FAINT
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}"{da} stroke-linecap="round"/>')

    def path(self, d, stroke=None, sw=1.25, fill="none", dash=None, marker=True):
        stroke = stroke or FAINT
        da = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#a-{self._mk(stroke)})"' if marker else ""
        self.parts.append(
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
            f'{da}{mk} stroke-linecap="round" stroke-linejoin="round"/>')

    def _mk(self, color):
        key = color.lstrip("#")
        if key not in self._markers:
            self._markers.add(key)
            self.defs.append(
                f'<marker id="a-{key}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{color}"/></marker>')
        return key

    # ---------- composites ----------
    def node(self, x, y, w, h, title, sub=None, accent="#6366f1", mono=False, tsize=13):
        """A labeled box with a tinted fill and a left accent rule."""
        self.rect(x, y, w, h, fill=accent, stroke="none", rx=9, opacity=0.09)
        self.rect(x, y, w, h, fill="none", stroke=accent, rx=9, sw=1.1, opacity=0.55)
        cy = y + h / 2
        if sub:
            self.text(x + w / 2, cy - 3, title, size=tsize, weight=600,
                      anchor="middle", font=MONO if mono else SANS, color=INK)
            self.text(x + w / 2, cy + 13, sub, size=10.5, weight=400,
                      anchor="middle", font=MONO, color=MUTED)
        else:
            self.text(x + w / 2, cy + 4.5, title, size=tsize, weight=600,
                      anchor="middle", font=MONO if mono else SANS, color=INK)

    def arrow(self, x1, y1, x2, y2, label=None, color=None, dash=None, lsize=10):
        color = color or FAINT
        self.path(f"M {x1} {y1} L {x2} {y2}", stroke=color, dash=dash)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.text(mx, my - 6, label, size=lsize, color=MUTED,
                      anchor="middle", font=MONO)

    def elbow(self, x1, y1, x2, y2, via_y=None, label=None, color=None, dash=None):
        """Orthogonal connector: horizontal, vertical, horizontal."""
        color = color or FAINT
        vy = via_y if via_y is not None else (y1 + y2) / 2
        d = f"M {x1} {y1} L {x1} {vy} L {x2} {vy} L {x2} {y2}"
        self.path(d, stroke=color, dash=dash)
        if label:
            self.text((x1 + x2) / 2, vy - 6, label, size=10, color=MUTED,
                      anchor="middle", font=MONO)

    def caption(self, x, y, s, size=10.5):
        self.text(x, y, s, size=size, color=FAINT, font=MONO)

    def band(self, x, y, w, h, label, color=FAINT):
        """Dashed grouping container with a small caps label."""
        self.rect(x, y, w, h, fill="none", stroke=color, rx=11, sw=1, dash="4 4", opacity=0.5)
        self.text(x + 12, y + 15, label.upper(), size=9, color=color,
                  weight=600, font=MONO, spacing="0.09em")

    def save(self, path, title=""):
        defs = f"<defs>{''.join(self.defs)}</defs>" if self.defs else ""
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-label="{esc(title)}">'
            f'{defs}'
            f'<rect x="0.5" y="0.5" width="{self.w-1}" height="{self.h-1}" rx="14" '
            f'fill="{BG}" stroke="{BORDER}"/>'
            + "".join(self.parts) + "</svg>")
        with open(path, "w") as f:
            f.write(svg)
        return path
