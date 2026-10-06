"""Render assets/stats-{dark,light}.svg from the GitHub GraphQL API.

Usage: GITHUB_TOKEN=... python3 .github/scripts/stats.py [login]
A token with `repo` scope also counts private repositories in the language breakdown.
"""
import datetime as dt
import json
import os
import sys
import urllib.request

from tui import THEMES, window

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

    a = t["accent"]
    o = [f'<g class="on" style="animation-delay:.1s"><text x="30" y="50" class="acc">$</text>'
         f'<text x="44.4" y="50" class="fg">gh activity --since 12mo</text></g>']
    # metrics
    for i, (value, cap) in enumerate(((fmt(s["contributions"]), "contribs"), (fmt(s["commits"]), "commits"),
                                      (f'{s["streak"]}d', "streak"))):
        x = 30 + i * 124
        o.append(f'<g class="on" style="animation-delay:{.25 + i * .08:.2f}s"><text x="{x}" y="82" '
                 f'style="font-size:22px;font-weight:700;fill:{a}">{value}</text>'
                 f'<text x="{x}" y="98" class="dim sm">{cap}</text></g>')

    # heatmap
    cell, gap = 10, 2
    hx, hy = 30 + (352 - (WEEKS * (cell + gap) - gap)) / 2, 126
    prev_month = None
    for wi, week in enumerate(s["weeks"]):
        x = hx + wi * (cell + gap)
        first = dt.date.fromisoformat(week["contributionDays"][0]["date"])
        if first.month != prev_month and wi < WEEKS - 2:
            if prev_month is not None or first.day <= 7:
                o.append(f'<text x="{x:.1f}" y="{hy - 6}" class="dim" style="font-size:9.5px">'
                         f'{first.strftime("%b").lower()}</text>')
            prev_month = first.month
        o.append(f'<g class="on" style="animation-delay:{.4 + wi * .02:.2f}s">')
        for d in week["contributionDays"]:
            row = (dt.date.fromisoformat(d["date"]).weekday() + 1) % 7  # Sun first, like GitHub
            fill = level(d["contributionCount"]) or t["empty"]
            o.append(f'<rect x="{x:.1f}" y="{hy + row * (cell + gap)}" width="{cell}" height="{cell}" fill="{fill}"/>')
        o.append("</g>")

    # languages as htop meters
    width = 24
    for i, (name, share, _) in enumerate(s["langs"][:4]):
        n = round(share * width)
        y = 232 + i * 17
        o.append(f'<g class="on" style="animation-delay:{1 + i * .08:.2f}s"><text x="30" y="{y}" class="sm" '
                 f'xml:space="preserve"><tspan fill="{t["fg"]}">{name.lower()[:10]:<11}</tspan>'
                 f'<tspan fill="{t["dim"]}">[</tspan><tspan fill="{a}">{"|" * n}</tspan>{" " * (width - n)}'
                 f'<tspan fill="{t["dim"]}">]</tspan><tspan fill="{t["muted"]}"> {share * 100:>3.0f}%</tspan></text></g>')

    updated = dt.date.today().strftime("%b %-d").lower()
    return window(t, 412, 312, f"GitHub activity: {s['contributions']} contributions in the last year",
                  "activity", f"upd {updated}", "  " + "".join(o))


if __name__ == "__main__":
    stats = summarize(fetch())
    for mode, theme in THEMES.items():
        with open(os.path.join(OUT, f"stats-{mode}.svg"), "w") as f:
            f.write(render(stats, theme))
    print(f"{stats['contributions']} contributions, {stats['commits']} commits, langs: "
          + ", ".join(f"{n} {s * 100:.0f}%" for n, s, _ in stats["langs"]))
