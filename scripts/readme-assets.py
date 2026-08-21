#!/usr/bin/env python3
"""Generate the README's branded SVG assets: docs/splash.svg and docs/gates.svg.

MIDAS runs a dark-surface palette (ink + gold) so it reads as its own product
next to its sibling frameworks while keeping the same asset shape. The wordmark
is outlined from Literata at weight 600 so the splash renders identically on
every machine — SVG-as-<img> on GitHub loads no fonts.

Usage:
    python3 scripts/readme-assets.py --font /path/to/Literata[opsz,wght].ttf

Literata: https://github.com/google/fonts/tree/main/ofl/literata (OFL).
"""

import argparse
from pathlib import Path

# brand tokens — MIDAS: deep ink surface, one gold mark, cool slate text
INK = "#0D1926"       # surface
INK2 = "#122232"      # raised
LINE = "#1E3346"      # hairline
LINE2 = "#28425A"     # brighter hairline
PAPER = "#F2F1ED"     # wordmark / primary text
TEXT2 = "#A9BDCE"     # secondary text
TEXT3 = "#6C879F"     # tertiary / eyebrow
GOLD = "#D8A32B"      # the mark: once per surface, nowhere else
GOLD_DIM = "#8A6A22"
GREEN = "#3E9C6B"     # a gate that passed
RED = "#C4523F"       # a gate that bit

MONO = "'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


# ---------------------------------------------------------------- wordmark

def wordmark_paths(font_path: str, text: str, size: float, tracking_em: float = -0.02):
    """Outline `text` from the font at `size` px. Returns (paths, width) where
    paths is a list of (svg_path_d, advance_x_offset) per glyph."""
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    from fontTools.pens.svgPathPen import SVGPathPen

    font = TTFont(font_path)
    if "fvar" in font:
        instantiateVariableFont(font, {"wght": 600, "opsz": 24}, inplace=True)
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyph_set = font.getGlyphSet()
    hmtx = font["hmtx"]

    paths, x = [], 0.0
    for ch in text:
        gname = cmap[ord(ch)]
        pen = SVGPathPen(glyph_set)
        glyph_set[gname].draw(pen)
        paths.append((pen.getCommands(), x))
        x += hmtx[gname][0] * scale + tracking_em * size
    return paths, x - tracking_em * size


def build_splash(font_path: str, wordmark: str = "MIDAS") -> str:
    W, H = 1200, 300
    size = 76
    paths, width = wordmark_paths(font_path, wordmark + ".", size, tracking_em=0.02)
    ox = (W - width) / 2
    oy = 168  # baseline

    glyphs = []
    for i, (d, dx) in enumerate(paths):
        fill = GOLD if i == len(paths) - 1 else PAPER
        # font units are y-up; flip around the baseline
        glyphs.append(
            f'<path transform="translate({ox + dx:.1f},{oy}) scale({size / 1000:.6f},-{size / 1000:.6f})" '
            f'd="{d}" fill="{fill}"/>'
        )

    eyebrow = "THE OPS DISCIPLINE NOBODY TAUGHT YOU · ENFORCED, THEN EVIDENCED"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="MIDAS — the ops discipline nobody taught you, enforced then evidenced">
<defs>
<radialGradient id="bloom" cx="0.5" cy="0.36" r="0.78">
<stop offset="0" stop-color="{GOLD}" stop-opacity="0.10"/>
<stop offset="0.5" stop-color="{INK2}" stop-opacity="0.55"/>
<stop offset="1" stop-color="{INK}" stop-opacity="0"/>
</radialGradient>
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.86" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="matrix" values="0 0 0 0 0.85 0 0 0 0 0.78 0 0 0 0 0.62 0 0 0 0.045 0"/></filter>
</defs>
<rect width="{W}" height="{H}" fill="{INK}"/>
<rect width="{W}" height="{H}" fill="url(#bloom)"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{LINE}"/>
<line x1="{W / 2 - 180}" y1="198" x2="{W / 2 + 180}" y2="198" stroke="{GOLD_DIM}" stroke-opacity="0.5"/>
{"".join(glyphs)}
<text x="{W / 2}" y="232" text-anchor="middle" font-family={MONO!r} font-size="12.5" font-weight="500" letter-spacing="1.75" fill="{TEXT3}">{eyebrow}</text>
</svg>'''


# ---------------------------------------------------------------- gates

def _wrap(text: str, width: int) -> list[str]:
    """Greedy wrap to `width` characters — mono type, so chars are the unit."""
    lines, line = [], ""
    for w in text.split():
        if line and len(line) + len(w) + 1 > width:
            lines.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        lines.append(line)
    return lines


def build_gates() -> str:
    """The four gates between a commit and production, and what each one catches."""
    W, H = 1160, 430

    gates = [
        ("01", "UNIT + FEATURE TESTS", "in CI, against a prod-parity database",
         ["logic errors", "contract breaks"],
         "cannot see the browser or the proxy layer"),
        ("02", "BROWSER SMOKE", "a headless browser against a served production build",
         ["console errors", "mixed content", "419 / 500 XHR", "empty app mount"],
         "cannot see live infrastructure"),
        ("03", "WAIT FOR CI", "the platform holds the deploy until CI is green",
         ["a deploy racing red checks"],
         "gates the release, not the build"),
        ("04", "LIVE SMOKE", "the same detectors, against the real environment URL",
         ["TLS / proxy drift", "env config rot"],
         "the last thing between you and a user"),
    ]

    col_w = 262
    gap = 20
    x0 = 30
    top = 118

    parts = [
        f'<rect width="{W}" height="{H}" fill="{INK}"/>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" fill="none" stroke="{LINE}"/>',
        f'<text x="{x0}" y="40" font-family={MONO!r} font-size="11" letter-spacing="1.6" fill="{TEXT3}">FOUR GATES BETWEEN A COMMIT AND PRODUCTION</text>',
        f'<text x="{W - 30}" y="40" text-anchor="end" font-family={MONO!r} font-size="11" letter-spacing="1.6" fill="{GOLD}">EACH CATCHES WHAT THE LAST ONE STRUCTURALLY CANNOT</text>',
        f'<line x1="{x0}" y1="56" x2="{W - 30}" y2="56" stroke="{LINE}"/>',
        # the rail
        f'<text x="{x0}" y="88" font-family={MONO!r} font-size="12" fill="{TEXT2}">git push</text>',
        f'<text x="{W - 30}" y="88" text-anchor="end" font-family={MONO!r} font-size="12" fill="{GOLD}">production</text>',
        f'<line x1="{x0 + 66}" y1="84" x2="{W - 96}" y2="84" stroke="{LINE2}" stroke-dasharray="3 4"/>',
    ]

    for i, (num, name, sub, catches, blind) in enumerate(gates):
        x = x0 + i * (col_w + gap)
        h = 258
        parts.append(
            f'<rect x="{x}" y="{top}" width="{col_w}" height="{h}" rx="10" fill="{INK2}" stroke="{LINE2}"/>'
        )
        # the rail tick down into the card
        parts.append(f'<line x1="{x + col_w / 2}" y1="84" x2="{x + col_w / 2}" y2="{top}" stroke="{LINE2}"/>')
        parts.append(f'<circle cx="{x + col_w / 2}" cy="84" r="3.5" fill="{GOLD}"/>')

        parts.append(f'<text x="{x + 18}" y="{top + 30}" font-family={MONO!r} font-size="20" font-weight="600" fill="{GOLD}">{num}</text>')
        parts.append(f'<text x="{x + 52}" y="{top + 30}" font-family={MONO!r} font-size="12.5" font-weight="600" letter-spacing="0.8" fill="{PAPER}">{name}</text>')
        sub_lines = _wrap(sub, 33)
        for j, ln in enumerate(sub_lines):
            parts.append(f'<text x="{x + 18}" y="{top + 52 + j * 15}" font-family={MONO!r} font-size="10.5" fill="{TEXT3}">{ln}</text>')
        rule_y = top + 52 + len(sub_lines) * 15
        parts.append(f'<line x1="{x + 18}" y1="{rule_y}" x2="{x + col_w - 18}" y2="{rule_y}" stroke="{LINE}"/>')
        parts.append(f'<text x="{x + 18}" y="{rule_y + 22}" font-family={MONO!r} font-size="9.5" letter-spacing="1.3" fill="{GREEN}">CATCHES</text>')

        y = rule_y + 42
        for c in catches:
            parts.append(f'<text x="{x + 18}" y="{y}" font-family={MONO!r} font-size="11" fill="{TEXT2}">✓ {c}</text>')
            y += 19

        # fixed baseline so the BLIND TO band aligns across all four cards
        y = top + 200
        parts.append(f'<text x="{x + 18}" y="{y}" font-family={MONO!r} font-size="9.5" letter-spacing="1.3" fill="{RED}">BLIND TO</text>')
        for j, ln in enumerate(_wrap(blind, 31)):
            parts.append(f'<text x="{x + 18}" y="{y + 19 + j * 15}" font-family={MONO!r} font-size="10.5" fill="{TEXT3}">{ln}</text>')

    parts.append(
        f'<text x="{x0}" y="{H - 26}" font-family={MONO!r} font-size="11.5" fill="{TEXT3}">'
        f'A green unit suite once shipped a blank page to production. '
        f'<tspan fill="{PAPER}">107 tests passed. Every browser rendered white.</tspan>'
        f'</text>'
    )
    parts.append(
        f'<text x="{W - 30}" y="{H - 26}" text-anchor="end" font-family={MONO!r} font-size="11.5" fill="{GOLD}">gate 02 exists because of that morning</text>'
    )

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'role="img" aria-label="The four gates MIDAS stands between a commit and production">'
            + "".join(parts) + "</svg>")


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True, help="path to Literata variable TTF")
    ap.add_argument("--out", default="docs", help="output directory")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    (out / "splash.svg").write_text(build_splash(args.font), encoding="utf-8")
    (out / "gates.svg").write_text(build_gates(), encoding="utf-8")
    print(f"wrote {out / 'splash.svg'}")
    print(f"wrote {out / 'gates.svg'}")


if __name__ == "__main__":
    main()
