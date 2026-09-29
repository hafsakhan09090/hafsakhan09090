import random, textwrap
from html import escape
from theme import save, LIME, ROBIN

random.seed(7)
FONT = "ui-monospace,SFMono-Regular,Consolas,Menlo,monospace"

def vis(ranges):
    eps = 0.004
    def st(t):
        if t >= 1: t = 0
        return 1 if any(s <= t < e for s, e in ranges) else 0
    ts = {0, 1}
    for s, e in ranges:
        for t in (s, e):
            for d in (-eps, 0):
                x = round(t + d, 4)
                if 0 <= x <= 1: ts.add(x)
    ts = sorted(ts)
    return ";".join(str(t) for t in ts), ";".join(str(st(t)) for t in ts)

def head(W, H, extra=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0e14"/><stop offset="1" stop-color="#161b22"/></linearGradient>
<linearGradient id="tt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LIME}"/><stop offset="1" stop-color="{ROBIN}"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ROBIN}" stop-opacity="0"/><stop offset="1" stop-color="{ROBIN}" stop-opacity=".55"/></linearGradient>
<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#21262d" stroke-width="1"/></pattern>
<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".05"/></pattern>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-60%" y="-150%" width="220%" height="400%"><feGaussianBlur stdDeviation="22"/></filter>
<clipPath id="all"><rect width="{W}" height="{H}" rx="14"/></clipPath>
{extra}
</defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>'''

def stars(W, H, n):
    s = ""
    for _ in range(n):
        c = LIME if random.random() < .5 else ROBIN
        s += f'<circle cx="{random.randint(8,W-8)}" cy="{random.randint(8,H-8)}" r="1.2" fill="{c}"><animate attributeName="opacity" values=".08;.7;.08" dur="{random.uniform(2,5):.1f}s" begin="{random.uniform(0,3):.1f}s" repeatCount="indefinite"/></circle>'
    return s

def frame_border(W, H, col=ROBIN):
    return (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{col}" stroke-width="1.5">'
            f'<animate attributeName="stroke-opacity" values=".25;.85;.25" dur="4s" repeatCount="indefinite"/></rect>')

# =============================== BANNER ===============================
def banner():
    W, H = 900, 300
    o = [head(W, H)]
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/><g clip-path="url(#all)">')
    chars = list("0101010101{}[]()<>/=+*#;:$&|%?")
    for i in range(36):
        x = 10 + i * 25
        n = 15
        col = ROBIN if i % 2 == 0 else LIME
        t = ""
        for k in range(n):
            c = escape(random.choice(chars))
            op = 0.08 + 0.55 * (k / (n - 1))
            fill = LIME if k == n - 1 else col
            if k == n - 1: op = 0.95
            t += f'<tspan x="{x}" dy="16" fill="{fill}" fill-opacity="{op:.2f}">{c}</tspan>'
        d = random.uniform(5, 11)
        o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 -260;0 {H+30}" dur="{d:.1f}s" begin="-{random.uniform(0,d):.1f}s" repeatCount="indefinite"/><text font-size="14">{t}</text></g>')
    o.append(f'<ellipse cx="450" cy="140" rx="340" ry="78" fill="#0a0e14" opacity=".82" filter="url(#soft)"/>')
    def title(fill, x, y, extra="", op=1):
        return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="70" font-weight="800" letter-spacing="14" fill="{fill}" opacity="{op}" {extra}>HAFSA KHAN'
    kt = "0;.84;.86;.88;.9;.92;.94;1"
    o.append(title(ROBIN, 450, 150, 'style="mix-blend-mode:screen"', .8) +
             f'<animate attributeName="x" values="450;450;443;458;445;455;450;450" keyTimes="{kt}" dur="4s" repeatCount="indefinite"/></text>')
    o.append(title(LIME, 450, 150, 'style="mix-blend-mode:screen"', .8) +
             f'<animate attributeName="x" values="450;450;457;442;455;446;450;450" keyTimes="{kt}" dur="4s" repeatCount="indefinite"/></text>')
    o.append(title("url(#tt)", 450, 150, 'filter="url(#glow)"') + '</text>')
    roles = ["CS UNDERGRADUATE", "COMPUTER VISION + ASSISTIVE TECH", "FULL-STACK · PYTHON · FASTAPI", "AI / ML · OPEN TO WORK"]
    for i, r in enumerate(roles):
        kt2, v2 = vis([(i / 4, (i + 1) / 4)])
        o.append(f'<text x="450" y="196" text-anchor="middle" font-size="16" letter-spacing="3" fill="#c9d1d9" opacity="0"><tspan fill="{LIME}">&gt; </tspan>{escape(r)}<tspan fill="{LIME}">▍<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan><animate attributeName="opacity" values="{v2}" keyTimes="{kt2}" dur="10s" repeatCount="indefinite"/></text>')
    o.append(f'<rect x="0" y="240" width="{W}" height="36" fill="#0d1117" opacity=".9"/><line x1="0" x2="{W}" y1="240" y2="240" stroke="#30363d"/><line x1="0" x2="{W}" y1="276" y2="276" stroke="#30363d"/>')
    s = "OPEN TO INTERNSHIPS  ///  ENTRY-LEVEL SWE  ///  AI/ML COLLABS  ///  hafsakhan09090@gmail.com  ///  "
    L = len(s) * 9.6
    o.append(f'<g><animateTransform attributeName="transform" type="translate" values="0 0;-{L:.0f} 0" dur="28s" repeatCount="indefinite"/><text x="0" y="263" font-size="13" letter-spacing="2" fill="{ROBIN}">{escape(s*3)}</text></g>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#sl)"/><rect x="0" y="-70" width="{W}" height="70" fill="url(#band)"><animate attributeName="y" values="-70;{H}" dur="6s" repeatCount="indefinite"/></rect>')
    o.append('</g>')
    for d in ["M14,34 V14 H34", f"M{W-34},14 H{W-14} V34", f"M14,{H-34} V{H-14} H34", f"M{W-34},{H-14} H{W-14} V{H-34}"]:
        o.append(f'<path d="{d}" fill="none" stroke="{LIME}" stroke-width="2"/>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#30363d"/></svg>')
    save("banner", "\n".join(o))

# ================================ HAND =================================
OPEN = {"w":(125,220),"t1":(85,195),"t2":(60,170),"t3":(45,148),"t4":(35,128),
"i1":(95,140),"i2":(90,105),"i3":(88,80),"i4":(86,58),"m1":(125,130),"m2":(125,92),"m3":(125,64),"m4":(125,40),
"r1":(155,138),"r2":(160,102),"r3":(163,78),"r4":(165,56),"p1":(180,155),"p2":(192,125),"p3":(199,105),"p4":(204,88)}
FIST = dict(OPEN)
FIST.update({"t2":(80,172),"t3":(96,152),"t4":(110,150),
"i2":(92,112),"i3":(106,108),"i4":(110,128),"m2":(125,100),"m3":(138,100),"m4":(136,122),
"r2":(158,110),"r3":(170,110),"r4":(166,130),"p2":(190,132),"p3":(199,134),"p4":(190,150)})
EDGES = [("w","t1"),("t1","t2"),("t2","t3"),("t3","t4"),("w","i1"),("i1","i2"),("i2","i3"),("i3","i4"),
("i1","m1"),("m1","m2"),("m2","m3"),("m3","m4"),("m1","r1"),("r1","r2"),("r2","r3"),("r3","r4"),
("r1","p1"),("p1","p2"),("p2","p3"),("p3","p4"),("w","p1")]

def hand(P, tf, ranges, color, scale_tag=""):
    kt, v = vis(ranges)
    g = f'<g transform="{tf}" opacity="0"><animate attributeName="opacity" values="{v}" keyTimes="{kt}" dur="10s" repeatCount="indefinite"/>'
    for p, q in EDGES:
        g += f'<line x1="{P[p][0]}" y1="{P[p][1]}" x2="{P[q][0]}" y2="{P[q][1]}" stroke="{color}" stroke-width="2.5" stroke-opacity=".85"/>'
    for i, (k, (x, y)) in enumerate(P.items()):
        tip = k.endswith("4")
        g += f'<circle cx="{x}" cy="{y}" r="4" fill="{LIME if tip else "#fff"}"><animate attributeName="r" values="3.5;5.5;3.5" dur="2s" begin="{i*0.09:.2f}s" repeatCount="indefinite"/></circle>'
    return g + '</g>'

# ================================ SCENE ================================
def scene():
    W, H = 900, 270
    D = 10
    KT = "0;.05;.35;.5;.8;1"
    SP = "0 0 1 1;0.45 0 0.25 1;0 0 1 1;0.45 0 0.25 1;0 0 1 1"
    def mv(vals):
        return f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{KT}" calcMode="spline" keySplines="{SP}" dur="{D}s" repeatCount="indefinite"/>'
    def rot(vals):
        return f'<animateTransform attributeName="transform" type="rotate" values="{vals}" keyTimes="{KT}" calcMode="spline" keySplines="{SP}" dur="{D}s" repeatCount="indefinite"/>'
    o = [head(W, H, '<clipPath id="road"><rect x="548" y="30" width="332" height="220" rx="14"/></clipPath><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#1b2340"/></linearGradient>')]
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/>{stars(W,H,22)}')
    o.append(f'<text x="22" y="20" font-size="11" letter-spacing="2" fill="#8b949e">▸ LIVE PIPELINE  ·  GESTURE → COMMAND → MOTION</text><circle cx="878" cy="16" r="4" fill="{LIME}"><animate attributeName="opacity" values="1;0;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="866" y="20" font-size="10" text-anchor="end" fill="{LIME}">REC</text>')
    o.append(f'<rect x="20" y="30" width="210" height="220" rx="14" fill="#0d1117" fill-opacity=".75" stroke="#30363d"/>')
    open_tf = "translate(35,25) scale(.75)"
    o.append(hand(FIST, open_tf, [(0, .05), (.35, .5), (.8, 1)], ROBIN))
    o.append(hand(OPEN, open_tf, [(.05, .35)], LIME))
    o.append(hand(OPEN, "translate(35,25) scale(.75) rotate(180 120 130)", [(.5, .8)], LIME))
    o.append(f'<rect x="22" y="50" width="206" height="26" fill="url(#scan)"><animate attributeName="y" values="50;168;50" dur="3.5s" repeatCount="indefinite"/></rect>')
    for txt, col, rg in [("STOP", ROBIN, [(0, .05), (.35, .5), (.8, 1)]), ("FORWARD", LIME, [(.05, .35)]), ("REVERSE", LIME, [(.5, .8)])]:
        kt, v = vis(rg)
        o.append(f'<text x="125" y="222" text-anchor="middle" font-size="16" font-weight="700" fill="{col}" opacity="0">gesture: {txt}<animate attributeName="opacity" values="{v}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/></text>')
    o.append(f'<text x="125" y="240" text-anchor="middle" font-size="10" fill="#8b949e">MediaPipe · 21 landmarks</text>')
    def link(x1, x2, y=140):
        s = f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#30363d" stroke-width="2" stroke-dasharray="4 4"/>'
        for i in range(3):
            s += f'<circle r="3" fill="{LIME}"><animateMotion dur="1.2s" begin="{i*0.4}s" repeatCount="indefinite" path="M{x1},{y} L{x2},{y}"/></circle>'
        return s
    o.append(link(230, 296) + link(372, 436) + link(500, 548))
    o.append(f'<rect x="296" y="100" width="76" height="80" rx="6" fill="#0d1117" stroke="{ROBIN}" stroke-width="2"/>')
    for k in range(5):
        o.append(f'<rect x="290" y="{108+k*14}" width="6" height="4" fill="{ROBIN}"/><rect x="372" y="{108+k*14}" width="6" height="4" fill="{ROBIN}"/>')
    o.append(f'<text x="334" y="146" text-anchor="middle" font-size="14" font-weight="700" fill="#e6edf3">UNO</text><circle cx="310" cy="113" r="3.5" fill="{LIME}"><animate attributeName="opacity" values="1;.15;1" dur=".6s" repeatCount="indefinite"/></circle><text x="334" y="200" text-anchor="middle" font-size="10" fill="#8b949e">Arduino</text>')
    o.append(f'<rect x="436" y="110" width="64" height="60" rx="6" fill="#0d1117" stroke="{ROBIN}" stroke-width="2"/><text x="468" y="145" text-anchor="middle" font-size="12" font-weight="700" fill="#e6edf3">L298N</text><text x="468" y="190" text-anchor="middle" font-size="10" fill="#8b949e">motor driver</text>')
    o.append(f'<g clip-path="url(#road)"><rect x="548" y="30" width="332" height="220" fill="url(#sky)"/>')
    o.append(f'<circle cx="620" cy="80" r="22" fill="{LIME}" opacity=".14"/><circle cx="620" cy="80" r="11" fill="{LIME}" opacity=".45"/>')
    for layer, (col, fac, hmin, hmax) in enumerate([("#141b2b", -36, 50, 110), ("#1b2436", -72, 30, 80)]):
        b = f'<g>{mv(f"0 0;0 0;{fac} 0;{fac} 0;0 0;0 0")}'
        x = 470
        while x < 1040:
            w = random.randint(22, 52); h = random.randint(hmin, hmax)
            b += f'<rect x="{x}" y="{210-h}" width="{w}" height="{h}" fill="{col}"/>'
            if layer:
                for wy in range(210-h+8, 205, 14):
                    if random.random() < .45: b += f'<rect x="{x+6}" y="{wy}" width="4" height="5" fill="{ROBIN}" opacity=".3"/>'
            x += w + random.randint(2, 8)
        o.append(b + '</g>')
    o.append('<rect x="548" y="210" width="332" height="40" fill="#12161e"/><line x1="548" x2="880" y1="210" y2="210" stroke="#30363d" stroke-width="2"/>')
    o.append(f'<line x1="540" x2="890" y1="232" y2="232" stroke="#8b949e" stroke-width="3" stroke-dasharray="28 28"><animate attributeName="stroke-dashoffset" values="0;0;240;240;0;0" keyTimes="{KT}" calcMode="spline" keySplines="{SP}" dur="{D}s" repeatCount="indefinite"/></line>')
    def wheel(cx, cy, r, spokes, rotvals):
        s = f'<g transform="translate({cx},{cy})"><circle r="{r}" fill="#0d1117" stroke="#c9d1d9" stroke-width="3"/><g>{rot(rotvals)}'
        for a in range(spokes):
            s += f'<line x1="0" y1="{-r+2}" x2="0" y2="{r-2}" stroke="#8b949e" stroke-width="1.5" transform="rotate({a*180/spokes})"/>'
        return s + f'<circle r="3" fill="{ROBIN}"/></g></g>'
    rear = "0 0 0;0 0 0;626 0 0;626 0 0;0 0 0;0 0 0"
    front = "0 0 0;0 0 0;1529 0 0;1529 0 0;0 0 0;0 0 0"
    o.append(f'<g transform="translate(730,210)" filter="url(#glow)">')
    o.append(f'<path d="M-8,-40 L52,-40 M-8,-40 L-15,-92 M-15,-92 L-30,-92 M-6,-64 L36,-64 L36,-40 M52,-40 L66,-14 L80,-14" fill="none" stroke="{ROBIN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<rect x="-6" y="-44" width="56" height="7" rx="3" fill="{LIME}"/><rect x="8" y="-33" width="30" height="13" rx="3" fill="#0d1117" stroke="{LIME}" stroke-width="1.5"/><circle cx="14" cy="-26" r="2.5" fill="{LIME}"><animate attributeName="opacity" values="1;.1;1" dur=".7s" repeatCount="indefinite"/></circle>')
    o.append(wheel(0, -22, 22, 3, rear) + wheel(62, -9, 9, 2, front) + '</g>')
    for txt, rg in [("M_L=0    M_R=0", [(0, .05), (.35, .5), (.8, 1)]), ("M_L=+180 M_R=+180", [(.05, .35)]), ("M_L=-140 M_R=-140", [(.5, .8)])]:
        kt, v = vis(rg)
        o.append(f'<text x="566" y="56" font-size="11" fill="{LIME}" opacity="0">{txt}<animate attributeName="opacity" values="{v}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/></text>')
    o.append('</g>')
    o.append(f'<rect x="548" y="30" width="332" height="220" rx="14" fill="none" stroke="#30363d"/>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#30363d"/></svg>')
    save("scene", "\n".join(o))

# ================================ ORBIT ================================
def orbit():
    W, H, cx, cy = 900, 500, 450, 250
    o = [head(W, H, f'<radialGradient id="core"><stop offset="0" stop-color="{ROBIN}" stop-opacity=".5"/><stop offset="1" stop-color="{ROBIN}" stop-opacity="0"/></radialGradient>')]
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/>{stars(W,H,36)}')
    o.append(f'<text x="24" y="30" font-size="12" letter-spacing="3" fill="#8b949e">▸ TOOLKIT · IN ORBIT</text>')
    rings = [
     (165, 82, 26, 1, LIME, [("Python","core"),("OpenCV","core"),("MediaPipe","core"),("Whisper","core"),("FastAPI","core")]),
     (270, 135, 40, 0, ROBIN, [("Flask","tool"),("FFmpeg","tool"),("Arduino","tool"),("C++","tool"),("Docker","tool"),("JWT","tool"),("SQLite","tool")]),
     (368, 195, 60, 1, LIME, [("JavaScript","core"),("SQL","core"),("React","tool"),("Next.js","tool"),("YOLO","core"),("scikit-learn","core"),("Pandas","core"),("NumPy","core"),("Git","tool"),("Vercel","tool"),("Hugging Face","tool")]),
    ]
    for rx, ry, dur, sw, col, items in rings:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#30363d" stroke-width="1.5" stroke-dasharray="3 7"><animate attributeName="stroke-dashoffset" values="0;{-100 if sw else 100}" dur="8s" repeatCount="indefinite"/></ellipse>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="95" fill="url(#core)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="none" stroke="{LIME}" stroke-width="2"><animate attributeName="r" values="44;90" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values=".8;0" dur="2.6s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="54" fill="none" stroke="{ROBIN}" stroke-width="2" stroke-dasharray="6 8"><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" dur="14s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="#0d1117" stroke="url(#tt)" stroke-width="3" filter="url(#glow)"/><text x="{cx}" y="{cy+11}" text-anchor="middle" font-size="30" font-weight="800" fill="url(#tt)">HK</text>')
    for rx, ry, dur, sw, defcol, items in rings:
        n = len(items)
        path = f"M{cx+rx},{cy} A{rx},{ry} 0 1 {sw} {cx-rx},{cy} A{rx},{ry} 0 1 {sw} {cx+rx},{cy}"
        for i, (name, cat) in enumerate(items):
            col = LIME if cat == "core" else ROBIN
            w = len(name) * 7.6 + 24
            o.append(f'<g><animateMotion dur="{dur}s" begin="-{dur*i/n:.2f}s" repeatCount="indefinite" path="{path}"/><rect x="{-w/2:.1f}" y="-12" width="{w:.1f}" height="24" rx="12" fill="#0d1117" stroke="{col}" stroke-width="1.5"/><rect x="{-w/2:.1f}" y="-12" width="{w:.1f}" height="24" rx="12" fill="{col}" opacity=".15"/><text y="4.5" text-anchor="middle" font-size="12" fill="#e6edf3">{escape(name)}</text></g>')
    o.append(f'<circle cx="30" cy="{H-22}" r="5" fill="{LIME}"/><text x="41" y="{H-18}" font-size="11" fill="#8b949e">Core: languages &amp; AI/CV</text>')
    o.append(f'<circle cx="230" cy="{H-22}" r="5" fill="{ROBIN}"/><text x="241" y="{H-18}" font-size="11" fill="#8b949e">Tools: backend, frontend &amp; workflow</text>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#30363d"/></svg>')
    save("orbit", "\n".join(o))

# ================================ CARDS =================================
def chips(names):
    x, s = 20, ""
    for i, n in enumerate(names):
        col = LIME if i % 2 == 0 else ROBIN
        w = len(n) * 6.3 + 14
        s += f'<rect x="{x:.0f}" y="272" width="{w:.0f}" height="20" rx="10" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".7"/><text x="{x+w/2:.0f}" y="286" text-anchor="middle" font-size="10.5" fill="#e6edf3">{escape(n)}</text>'
        x += w + 6
    return s

def card_frame(title, tag, col, visual, desc, tech, repo):
    W, H = 290, 340
    o = [head(W, H)]
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/>{stars(W,H,8)}')
    o.append(frame_border(W, H, col))
    o.append(f'<text x="20" y="38" font-size="18" font-weight="800" fill="#e6edf3">{escape(title)}</text><text x="20" y="58" font-size="11" letter-spacing="2" fill="{col}">{escape(tag)}</text>')
    o.append('<rect x="20" y="72" width="250" height="110" rx="10" fill="#0d1117" stroke="#30363d"/>')
    o.append(visual)
    for i, ln in enumerate(textwrap.wrap(desc, 32)):
        o.append(f'<text x="20" y="{206+i*18}" font-size="12" fill="#c9d1d9">{escape(ln)}</text>')
    o.append(chips(tech))
    o.append(f'<text x="20" y="322" font-size="10" fill="#8b949e">↗ {escape(repo)}</text></svg>')
    return "\n".join(o)

def card_scrideo():
    v = '<clipPath id="cv"><rect x="0" y="0" width="0" height="20"><animate attributeName="width" values="0;216;216;0" keyTimes="0;.5;.92;1" dur="6s" repeatCount="indefinite"/></rect></clipPath>'
    v += '<rect x="32" y="80" width="226" height="74" rx="6" fill="#161b22"/>'
    for i in range(22):
        h = 8 + (i * 7) % 26
        v += f'<rect x="{40+i*10}" width="6" rx="3" fill="{ROBIN}" y="{112-h/2:.1f}" height="{h}"><animate attributeName="height" values="{h};{34-(h%20)};{h}" dur="{0.9+(i%5)*.25:.2f}s" repeatCount="indefinite"/><animate attributeName="y" values="{112-h/2:.1f};{112-(34-(h%20))/2:.1f};{112-h/2:.1f}" dur="{0.9+(i%5)*.25:.2f}s" repeatCount="indefinite"/></rect>'
    v += f'<g transform="translate(43,128)"><g clip-path="url(#cv)"><text x="0" y="14" font-size="12" font-weight="700" fill="{LIME}" stroke="#000" stroke-width="3" paint-order="stroke">Hello, world. Captions ready.</text></g></g>'
    v += f'<rect x="32" y="164" width="226" height="4" rx="2" fill="#30363d"/><rect x="32" y="164" width="0" height="4" rx="2" fill="{LIME}"><animate attributeName="width" values="0;226" dur="6s" repeatCount="indefinite"/></rect>'
    return card_frame("Scrideo", "AI SUBTITLES", ROBIN, v, "Video in, styled subtitles out. Whisper transcribes, FFmpeg renders. Upload a file or paste a YouTube link.", ["Python", "Flask", "Whisper", "FFmpeg"], "hafsakhan09090/Scrideo")

def card_gesture():
    def h(P, rg, col):
        kt, vv = vis(rg)
        g = f'<g transform="translate(85,61) scale(.5)" opacity="0"><animate attributeName="opacity" values="{vv}" keyTimes="{kt}" dur="6s" repeatCount="indefinite"/>'
        for p, q in EDGES:
            g += f'<line x1="{P[p][0]}" y1="{P[p][1]}" x2="{P[q][0]}" y2="{P[q][1]}" stroke="{col}" stroke-width="3" stroke-opacity=".85"/>'
        for i, (k, (x, y)) in enumerate(P.items()):
            g += f'<circle cx="{x}" cy="{y}" r="5" fill="{LIME if k.endswith("4") else "#fff"}"><animate attributeName="r" values="4;7;4" dur="1.6s" begin="{i*.08:.2f}s" repeatCount="indefinite"/></circle>'
        return g + '</g>'
    v = h(OPEN, [(0, .5)], LIME) + h(FIST, [(.5, 1)], ROBIN)
    v += f'<rect x="22" y="74" width="246" height="20" fill="url(#scan)"><animate attributeName="y" values="74;160;74" dur="3s" repeatCount="indefinite"/></rect>'
    for t, c, rg in [("FORWARD", LIME, [(0, .5)]), ("STOP", ROBIN, [(.5, 1)])]:
        kt, vv = vis(rg)
        v += f'<text x="32" y="94" font-size="11" font-weight="700" fill="{c}" opacity="0">▸ {t}<animate attributeName="opacity" values="{vv}" keyTimes="{kt}" dur="6s" repeatCount="indefinite"/></text>'
    v += f'<text x="258" y="94" text-anchor="end" font-size="10" fill="#8b949e">21 pts</text>'
    return card_frame("Gesture Wheelchair", "ASSISTIVE TECH", LIME, v, "Webcam hand gestures become drive commands for an Arduino Uno and L298N motor driver.", ["OpenCV", "MediaPipe", "Arduino", "C++"], "…/Gesture-Controlled-Wheelchair")

def card_stockwise():
    ys = [160, 150, 154, 140, 144, 130, 134, 118, 124, 108, 112, 96]
    xs = [34 + i * 11 for i in range(12)]
    line = " ".join(f"{x},{y}" for x, y in zip(xs, ys))
    v = f'<polygon points="{line} {xs[-1]},170 {xs[0]},170" fill="{LIME}" opacity="0"><animate attributeName="opacity" values="0;.16;.16;0" keyTimes="0;.6;.9;1" dur="5s" repeatCount="indefinite"/></polygon>'
    v += f'<polyline points="{line}" fill="none" stroke="{LIME}" stroke-width="2.5" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.6;.9;1" dur="5s" repeatCount="indefinite"/></polyline>'
    for i, (ny, nm) in enumerate([(94, "M"), (126, "T"), (158, "N")]):
        v += f'<circle cx="196" cy="{ny}" r="9" fill="#0d1117" stroke="{ROBIN}" stroke-width="1.5"/><text x="196" y="{ny+4}" text-anchor="middle" font-size="10" fill="{ROBIN}">{nm}</text>'
        v += f'<line x1="205" y1="{ny}" x2="240" y2="126" stroke="#30363d"/><circle r="2.5" fill="{LIME}"><animateMotion dur="1.8s" begin="{i*.5}s" repeatCount="indefinite" path="M205,{ny} L240,126"/></circle>'
    v += f'<circle cx="248" cy="126" r="9" fill="{LIME}"><animate attributeName="r" values="8;12;8" dur="1.8s" repeatCount="indefinite"/></circle>'
    return card_frame("Stockwise AI", "MULTI-AGENT · MCP", ROBIN, v, "Agents combine market data, technical indicators and news sentiment into explainable, educational signals.", ["FastAPI", "yfinance", "Docker", "MCP"], "hafsakhan09090/stockwise-ai")

if __name__ == "__main__":
    banner(); scene(); orbit()
    save("card_scrideo", card_scrideo())
    save("card_gesture", card_gesture())
    save("card_stockwise", card_stockwise())
    print("build ok")
