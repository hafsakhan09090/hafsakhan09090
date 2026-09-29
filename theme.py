"""Two-colour palette (lime + robin's-egg blue) with light/dark output.
   Writes NAME.svg (GitHub dark) and NAME_light.svg (GitHub light)."""
import re

LIME, ROBIN = "#e2ff5c", "#3fd6e8"          # dark-theme accents
LIME_L, ROBIN_L = "#8a9a00", "#0e8fa3"      # same hues, darkened for a white page
FG, MUTE, BORDER, BG2 = "#e6edf3", "#8b949e", "#30363d", "#161b22"
FG_L, MUTE_L, BORDER_L, BG2_L = "#1f2328", "#57606a", "#d0d7de", "#f6f8fa"

LIGHT = {
    "#0a0e14": "#ffffff", "#0d1117": "#ffffff", BG2: BG2_L, "#21262d": "#eaeef2",
    BORDER: BORDER_L, "#484f58": "#8c959f", MUTE: MUTE_L, "#c9d1d9": FG_L,
    FG: FG_L, '"#fff"': f'"{FG_L}"', '"#ffffff"': f'"{FG_L}"',
    LIME: LIME_L, ROBIN: ROBIN_L,
}

def transparent(svg):
    return re.sub(r'<rect[^>]*fill="url\(#bg\)"[^>]*/>', "", svg)

def light(svg):
    svg = transparent(svg)
    pat = re.compile("|".join(re.escape(k) for k in sorted(LIGHT, key=len, reverse=True)))
    return pat.sub(lambda m: LIGHT[m.group(0)], svg)

def save(name, svg):
    open(f"{name}.svg", "w", encoding="utf-8").write(transparent(svg))
    open(f"{name}_light.svg", "w", encoding="utf-8").write(light(svg))
