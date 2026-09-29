"""Builds stats.svg and activity.svg from the GitHub API.
   Run by .github/workflows/stats.yml.  Local test:  MOCK=1 python3 stats.py"""
import os, json, datetime, urllib.request
from collections import Counter
from html import escape
from theme import save, LIME, ROBIN

USER = os.environ.get("GH_USER", "hafsakhan09090")

def api(path):
    h = {"Accept": "application/vnd.github+json", "User-Agent": "stats-card"}
    if os.environ.get("GITHUB_TOKEN"): h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=h), timeout=30) as r:
        return json.load(r)

def fetch():
    if os.environ.get("MOCK"):
        return dict(mock=True, repos=15, stars=17, followers=31, following=38,
                    langs=[("Python", 4), ("HTML", 3), ("Dockerfile", 1)])
    u = api(f"/users/{USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"]]
    c = Counter(r["language"] for r in own if r["language"])
    return dict(repos=u["public_repos"], stars=sum(r["stargazers_count"] for r in own),
                followers=u["followers"], following=u["following"], langs=c.most_common(5))

def fetch_activity():
    q = ("query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions "
         "weeks{firstDay contributionDays{contributionCount}}}}}}")
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"u": USER}}).encode(),
        headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"], "User-Agent": "stats-card", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [(w["firstDay"], sum(d["contributionCount"] for d in w["contributionDays"])) for w in cal["weeks"]]
    return dict(total=cal["totalContributions"], weeks=weeks)

def _head(W, H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'font-family="ui-monospace,SFMono-Regular,Consolas,Menlo,monospace">'
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0e14"/><stop offset="1" stop-color="#161b22"/></linearGradient>'
            f'<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#21262d"/></pattern></defs>'
            f'<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/>')

def build(d):
    W, H = 900, 270
    tiles = [("REPOSITORIES", d["repos"], LIME), ("STARS EARNED", d["stars"], ROBIN),
             ("FOLLOWERS", d["followers"], LIME), ("FOLLOWING", d["following"], ROBIN)]
    o = [_head(W, H), f'<text x="24" y="30" font-size="12" letter-spacing="3" fill="#8b949e">▸ LIVE GITHUB STATS  ·  @{escape(USER)}</text>']
    for i, (lab, val, col) in enumerate(tiles):
        x, y = 24 + (i % 2) * 212, 52 + (i // 2) * 100
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur=".6s" begin="{i*.2}s" fill="freeze"/><animateTransform attributeName="transform" type="translate" values="0 10;0 0" dur=".6s" begin="{i*.2}s" fill="freeze"/>'
                 f'<rect x="{x}" y="{y}" width="200" height="88" rx="12" fill="#0d1117" stroke="{col}" stroke-opacity=".55"/><rect x="{x}" y="{y+16}" width="4" height="56" rx="2" fill="{col}"/>'
                 f'<text x="{x+22}" y="{y+52}" font-size="38" font-weight="800" fill="{col}">{val}</text><text x="{x+22}" y="{y+74}" font-size="10" letter-spacing="2" fill="#8b949e">{lab}</text></g>')
    o.append('<text x="480" y="30" font-size="12" letter-spacing="3" fill="#8b949e">TOP LANGUAGES</text>')
    total = sum(n for _, n in d["langs"]) or 1
    for i, (name, n) in enumerate(d["langs"]):
        y = 62 + i * 34
        pct = n / total * 100
        w = 2.4 * pct
        col = LIME if i % 2 == 0 else ROBIN
        o.append(f'<text x="480" y="{y+12}" font-size="13" fill="#e6edf3">{escape(name)}</text><rect x="600" y="{y}" width="240" height="16" rx="8" fill="#21262d"/>'
                 f'<rect x="600" y="{y}" width="0" height="16" rx="8" fill="{col}"><animate attributeName="width" values="0;{w:.0f};{w:.0f};0" keyTimes="0;.15;.92;1" dur="9s" begin="{i*.15}s" repeatCount="indefinite"/></rect>'
                 f'<text x="880" y="{y+12}" text-anchor="end" font-size="12" fill="#8b949e">{pct:.0f}%</text>')
    footer = "sample data · run the 'Update stats card' Action to go live" if d.get("mock") else "auto-updated " + datetime.date.today().isoformat() + " by GitHub Actions"
    o.append(f'<text x="24" y="{H-14}" font-size="10" fill="#484f58">{footer}</text>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#30363d"/></svg>')
    return "\n".join(o)

def build_activity(a):
    W, H = 900, 230
    o = [_head(W, H), '<text x="24" y="30" font-size="12" letter-spacing="3" fill="#8b949e">▸ COMMIT ACTIVITY  ·  LAST 12 MONTHS</text>']
    base, top = 182, 112
    weeks = a["weeks"] if a else [("", 0)] * 52
    mx = max([n for _, n in weeks] + [1])
    step = (W - 48) / max(len(weeks), 1)
    peak = max(range(len(weeks)), key=lambda i: weeks[i][1]) if a else -1
    last_m = ""
    for i, (day, n) in enumerate(weeks):
        x = 24 + i * step
        h = max(3, n / mx * top)
        col = ROBIN if i == peak and n > 0 else LIME
        op = 0.22 if n == 0 else 0.45 + 0.55 * n / mx
        o.append(f'<rect x="{x:.1f}" width="{step-4:.1f}" rx="3" fill="{col}" fill-opacity="{op:.2f}" y="{base-h:.1f}" height="{h:.1f}">'
                 f'<animate attributeName="height" values="0;{h:.1f};{h:.1f};0" keyTimes="0;.12;.92;1" dur="10s" begin="{i*0.03:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{base};{base-h:.1f};{base-h:.1f};{base}" keyTimes="0;.12;.92;1" dur="10s" begin="{i*0.03:.2f}s" repeatCount="indefinite"/></rect>')
        m = day[:7]
        if a and m and m != last_m:
            mon = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(m[5:7]) - 1]
            if i == 0 or day[8:10] <= "07":
                o.append(f'<text x="{x:.1f}" y="202" font-size="10" fill="#8b949e">{mon}</text>')
            last_m = m
    if a:
        o.append(f'<text x="{W-24}" y="30" text-anchor="end" font-size="13" font-weight="700" fill="#e6edf3">{a["total"]} contributions</text>')
        o.append(f'<text x="24" y="{H-10}" font-size="10" fill="#484f58">auto-updated {datetime.date.today().isoformat()} by GitHub Actions</text>')
    else:
        o.append(f'<text x="{W/2}" y="120" text-anchor="middle" font-size="14" fill="#8b949e">Waiting for the first Action run. Your commit activity loads here automatically.</text>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#30363d"/></svg>')
    return "\n".join(o)

if __name__ == "__main__":
    d = fetch()
    save("stats", build(d))
    print("stats.svg + stats_light.svg written")
    if os.environ.get("MOCK"):
        save("activity", build_activity(None))
    else:
        try:
            save("activity", build_activity(fetch_activity()))
            print("activity.svg + activity_light.svg written")
        except Exception as e:
            print("activity skipped:", e)
