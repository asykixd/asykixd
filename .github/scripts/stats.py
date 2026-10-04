"""Render assets/stats-{dark,light}.svg from the GitHub GraphQL API.

Usage: GITHUB_TOKEN=... python3 .github/scripts/stats.py [login]
A token with `repo` scope also counts private repositories in the language breakdown.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

LOGIN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REPOSITORY_OWNER", "asykixd")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
WEEKS = 26

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        name
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}"""

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
THEMES = {
    "dark": dict(bg="#0d1117", stroke="#30363d", line="#21262d", empty="#161b22", title="#e6edf3",
                 desc="#8b949e", label="#6e7681", heat=("#0f3d38", "#13695f", "#1fa594", "#2dd4bf")),
    "light": dict(bg="#ffffff", stroke="#d0d7de", line="#eaeef2", empty="#eff2f5", title="#1f2328",
                  desc="#656d76", label="#8c959f", heat=("#b2ece2", "#5fd2c0", "#14a493", "#0f766e")),
}


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(json.dumps(data["errors"], indent=2))
    return data["data"]["user"]


def summarize(user):
    cc = user["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    best = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        best = max(best, run)

    langs = {}
    for repo in user["repositories"]["nodes"]:
        if repo["name"].lower() == LOGIN.lower():
            continue
        for e in repo["languages"]["edges"]:
            n = e["node"]
            langs.setdefault(n["name"], [0, n["color"] or "#8b949e"])[0] += e["size"]
    total = sum(v[0] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])
    shares = [(name, size / total, color) for name, (size, color) in top[:5]]
    rest = 1 - sum(s for _, s, _ in shares)
    if rest > 0.005:
        shares.append(("Other", rest, None))

    return dict(
        contributions=cc["contributionCalendar"]["totalContributions"],
        commits=cc["totalCommitContributions"],
        streak=best,
        weeks=cc["contributionCalendar"]["weeks"][-WEEKS:],
        langs=shares,
    )


def fmt(n):
    return f"{n / 1000:.1f}k" if n >= 10000 else f"{n:,}".replace(",", " ")


def render(s, t):
    counts = sorted(d["contributionCount"] for w in s["weeks"] for d in w["contributionDays"] if d["contributionCount"])

    def level(c):
        if not c:
            return None
        q = [counts[int(len(counts) * p)] for p in (0.25, 0.5, 0.75)]
        return t["heat"][sum(c > x for x in q)]

    o = []
    # metrics
    for i, (value, cap) in enumerate(((fmt(s["contributions"]), "CONTRIBUTIONS"),
                                      (fmt(s["commits"]), "COMMITS"),
                                      (f'{s["streak"]}d', "BEST STREAK"))):
        x = 32 + i * 120
        o.append(f'<g class="rise" style="animation-delay:{0.15 + i * 0.1:.2f}s">'
                 f'<text x="{x}" y="84" class="num">{value}</text><text x="{x}" y="104" class="tiny">{cap}</text></g>')

    # heatmap
    cell, gap = 10, 3
    hx = 32 + (348 - (WEEKS * (cell + gap) - gap)) / 2
    hy = 146
    prev_month = None
    for wi, week in enumerate(s["weeks"]):
        x = hx + wi * (cell + gap)
        first = dt.date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != prev_month and wi < WEEKS - 2:
            if prev_month is not None or first.day <= 7:
                o.append(f'<text x="{x:.1f}" y="{hy - 8}" class="month">{first.strftime("%b")}</text>')
            prev_month = first.month
        o.append(f'<g class="col" style="animation-delay:{0.3 + wi * 0.025:.3f}s">')
        for d in week["contributionDays"]:
            row = (dt.date.fromisoformat(d["date"]).weekday() + 1) % 7  # Sun first, like GitHub
            fill = level(d["contributionCount"]) or t["empty"]
            o.append(f'<rect x="{x:.1f}" y="{hy + row * (cell + gap)}" width="{cell}" height="{cell}" rx="2" fill="{fill}"/>')
        o.append("</g>")

    # languages
    by = 264
    o.append(f'<text x="32" y="{by - 12}" class="tiny">LANGUAGES</text>')
    o.append(f'<clipPath id="bar"><rect x="32" y="{by}" width="348" height="8" rx="4"/></clipPath><g clip-path="url(#bar)" class="grow">')
    x = 32.0
    for name, share, color in s["langs"]:
        w = 348 * share
        o.append(f'<rect x="{x:.1f}" y="{by}" width="{max(w - 1.5, 0):.1f}" height="8" fill="{color or t["stroke"]}"/>')
        x += w
    o.append("</g>")
    for i, (name, share, color) in enumerate(s["langs"]):
        lx, ly = 32 + (i % 3) * 120, by + 34 + (i // 3) * 22
        o.append(f'<g class="rise" style="animation-delay:{1.0 + i * 0.08:.2f}s"><circle cx="{lx + 4}" cy="{ly - 4}" r="4" fill="{color or t["stroke"]}"/>'
                 f'<text x="{lx + 14}" y="{ly}" class="lang">{name}</text>'
                 f'<text x="{lx + 108}" y="{ly}" class="pct" text-anchor="end">{share * 100:.0f}%</text></g>')

    updated = dt.date.today().strftime("%b %-d").upper()
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="412" height="344" viewBox="0 0 412 344" role="img" aria-label="GitHub activity: {s['contributions']} contributions in the last year">
  <style>
    .label {{ font: 600 10.5px {MONO}; fill: {t['label']}; letter-spacing: 1.6px; }}
    .tiny  {{ font: 500 10px {MONO}; fill: {t['label']}; letter-spacing: 1.2px; }}
    .month {{ font: 400 9.5px {MONO}; fill: {t['label']}; }}
    .num   {{ font: 600 26px {SANS}; fill: {t['title']}; }}
    .lang  {{ font: 400 12px {SANS}; fill: {t['desc']}; }}
    .pct   {{ font: 400 11px {MONO}; fill: {t['label']}; }}
    .rise  {{ opacity: 0; animation: rise .6s cubic-bezier(.2,.8,.2,1) forwards; }}
    .col   {{ opacity: 0; animation: fade .5s ease forwards; }}
    .grow  {{ transform-box: fill-box; transform-origin: left; transform: scaleX(0); animation: grow 1.1s cubic-bezier(.65,0,.35,1) forwards .9s; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    @keyframes grow {{ to {{ transform: scaleX(1); }} }}
  </style>
  <rect x=".5" y=".5" width="411" height="343" rx="12" fill="{t['bg']}" stroke="{t['stroke']}"/>
  <text x="32" y="36" class="label">LAST 12 MONTHS</text>
  <text x="380" y="36" class="tiny" text-anchor="end">UPD {updated}</text>
  {"".join(o)}
</svg>
"""


if __name__ == "__main__":
    stats = summarize(fetch())
    for mode, theme in THEMES.items():
        with open(os.path.join(OUT, f"stats-{mode}.svg"), "w") as f:
            f.write(render(stats, theme))
    print(f"{stats['contributions']} contributions, {stats['commits']} commits, langs: "
          + ", ".join(f"{n} {s * 100:.0f}%" for n, s, _ in stats["langs"]))
