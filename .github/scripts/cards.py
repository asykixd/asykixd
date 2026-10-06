"""Render the static profile cards in assets/ (hero, stack, project cards) for both themes.

Usage: python3 .github/scripts/cards.py
The stats card is rendered separately by stats.py.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", stroke="#30363d", line="#21262d", title="#e6edf3",
                 desc="#8b949e", label="#6e7681", accent="#2dd4bf", warn="#d29922", dot="#21262d",
                 bubble="#0f3d38", glow=".10"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", stroke="#d0d7de", line="#eaeef2", title="#1f2328",
                  desc="#656d76", label="#8c959f", accent="#0f766e", warn="#9a6700", dot="#d8dee4",
                  bubble="#d5f5ef", glow=".08"),
}

RELEASES = [  # name, version, date, state
    ("uroboros", "v1.0.0", "2026-10-04", "latest"),
    ("Evelin", "v1.1.1", "2026-10-02", "stable"),
    (None, "v0.x", "in development", "private"),
]


def style(t, extra=""):
    return f"""<style>
    .label {{ font: 600 10.5px {MONO}; fill: {t['label']}; letter-spacing: 1.6px; }}
    .tiny  {{ font: 500 9.5px {MONO}; fill: {t['label']}; letter-spacing: 1.2px; }}
    .title {{ font: 600 24px {SANS}; fill: {t['title']}; }}
    .desc  {{ font: 400 13.5px {SANS}; fill: {t['desc']}; }}
    .val   {{ font: 500 12.5px {SANS}; fill: {t['title']}; }}
    .pill  {{ font: 500 11.5px {MONO}; fill: {t['desc']}; }}
    .link  {{ font: 400 12px {MONO}; fill: {t['label']}; }}
    .mono  {{ font: 400 12px {MONO}; fill: {t['title']}; }}
    .acc   {{ font: 500 12px {MONO}; fill: {t['accent']}; }}
    .rise  {{ opacity: 0; animation: rise .7s cubic-bezier(.2,.8,.2,1) forwards; }}
    .live  {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes rise  {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .25; }} }}
{extra}  </style>"""


def frame(t, w, h, label, body, extra_css="", glow=True):
    defs = (f'<defs><radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{t["accent"]}" '
            f'stop-opacity="{t["glow"]}"/><stop offset=".7" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>'
            f'<pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" '
            f'fill="{t["panel"]}"/><circle cx="6" cy="6" r=".9" fill="{t["dot"]}"/></pattern></defs>')
    g = f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="url(#glow)"/>' if glow else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{label}">\n  {style(t, extra_css)}\n  {defs}\n'
            f'  <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="12" fill="{t["bg"]}" stroke="{t["stroke"]}"/>\n'
            f'  {g}\n{body}\n</svg>\n')


def pills(t, x, y, items):
    out = []
    for it in items:
        w = len(it) * 6.95 + 22
        out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="none" stroke="{t["stroke"]}"/>'
                   f'<text x="{x + w / 2:.1f}" y="{y + 16}" class="pill" text-anchor="middle">{it}</text>')
        x += w + 8
    return "".join(out)


def specs(t, x, y, items):
    out, cx = [], x
    for i, (k, v) in enumerate(items):
        if i:
            out.append(f'<line x1="{cx - 14}" y1="{y - 10}" x2="{cx - 14}" y2="{y + 22}" stroke="{t["line"]}"/>')
        out.append(f'<text x="{cx}" y="{y}" class="tiny">{k}</text><text x="{cx}" y="{y + 19}" class="val">{v}</text>')
        cx += max(len(k) * 7.5, len(v) * 7.4) + 30
    return "".join(out)


def redacted(t, x, y, w, h=14):
    return f'<rect x="{x}" y="{y - h + 3}" width="{w}" height="{h}" rx="2" fill="{t["label"]}" fill-opacity=".55"/>'


# ---------------------------------------------------------------- hero

def hero(t):
    body = [
        f'  <g class="rise" style="animation-delay:.1s"><circle cx="35" cy="36" r="3.5" fill="{t["accent"]}" class="live"/>'
        f'<text x="46" y="40" class="label">SOFTWARE ENGINEER</text></g>',
        f'  <g class="rise" style="animation-delay:.2s"><text x="30" y="94" style="font:700 44px {SANS};fill:{t["title"]};'
        f'letter-spacing:-.5px">asykixd</text><rect x="32" y="108" width="56" height="3" rx="1.5" fill="{t["accent"]}"/></g>',
        f'  <g class="rise" style="animation-delay:.3s"><text x="32" y="140" class="desc">Systems programming, developer tooling'
        f'</text><text x="32" y="161" class="desc">and desktop applications. Open source, shipped end to end.</text></g>',
        f'  <g class="rise" style="animation-delay:.4s">{pills(t, 32, 184, ["Rust", "Python", "TypeScript", "C"])}</g>',
    ]
    px, py, pw = 476, 24, 332
    rows = [f'<rect x="{px}" y="{py}" width="{pw}" height="184" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>',
            f'<text x="{px + 18}" y="{py + 26}" class="tiny">RECENT RELEASES</text>',
            f'<text x="{px + pw - 18}" y="{py + 26}" class="tiny" text-anchor="end">GITHUB.COM/ASYKIXD</text>']
    for i, (name, ver, date, state) in enumerate(RELEASES):
        y = py + 66 + i * 44
        color = t["warn"] if state == "private" else t["accent"]
        live = ' class="live"' if i == 0 else ""
        nm = f'<text x="{px + 34}" y="{y}" class="mono">{name}</text>' if name else redacted(t, px + 34, y, 64)
        rows.append(
            f'<g class="rise" style="animation-delay:{.5 + i * .15:.2f}s">'
            f'<line x1="{px + 18}" y1="{y - 26}" x2="{px + pw - 18}" y2="{y - 26}" stroke="{t["line"]}"/>'
            f'<circle cx="{px + 22}" cy="{y - 4}" r="3.5" fill="{color}"{live}/>{nm}'
            f'<text x="{px + 120}" y="{y}" class="acc" style="fill:{color}">{ver}</text>'
            f'<text x="{px + 120}" y="{y + 15}" class="tiny">{state.upper()}</text>'
            f'<text x="{px + pw - 18}" y="{y}" class="link" text-anchor="end">{date}</text></g>')
    body.append(f'  <g class="rise" style="animation-delay:.25s">{"".join(rows)}</g>')
    return frame(t, 840, 232, "asykixd — software engineer: systems programming, developer tooling, desktop applications. "
                 "Latest releases: uroboros v1.0.0, Evelin v1.1.1", "\n".join(body))


# ---------------------------------------------------------------- stack

def stack(t):
    langs = [("Rust", "#dea584", "Systems and networking", "vpn client"),
             ("Python", "#3572a5", "Automation, bots, async I/O", "uroboros"),
             ("TypeScript", "#3178c6", "Desktop and web apps", "Evelin"),
             ("C", "#a8b9cc", "Low-level and performance", "systems work")]
    tools = [("DESKTOP", "Electron · React · Node.js"), ("INFRA", "Linux · Docker · Actions"),
             ("ANDROID", "ADB · scrcpy · WebCodecs"), ("TELEGRAM", "Telethon · aiogram")]
    body = [f'  <text x="32" y="36" class="label">STACK</text>']
    for i, ((name, color, cap, used), (grp, items)) in enumerate(zip(langs, tools)):
        x = 32 + i * 199
        body.append(
            f'  <g class="rise" style="animation-delay:{.2 + i * .12:.2f}s">'
            f'<circle cx="{x + 5}" cy="63" r="5" fill="{color}"/><text x="{x + 18}" y="68" '
            f'style="font:600 16px {SANS};fill:{t["title"]}">{name}</text>'
            f'<text x="{x}" y="92" class="desc" style="font-size:12.5px">{cap}</text>'
            f'<text x="{x}" y="114" class="link"><tspan style="fill:{t["accent"]}">→</tspan> {used}</text>'
            f'<text x="{x}" y="164" class="tiny">{grp}</text><text x="{x}" y="184" class="link" '
            f'style="fill:{t["desc"]}">{items}</text></g>')
    body.append(f'  <line x1="32" y1="138" x2="808" y2="138" stroke="{t["line"]}"/>')
    return frame(t, 840, 208, "Stack: Rust, Python, TypeScript, C; Electron, React, Node.js, Linux, Docker, ADB, scrcpy, "
                 "Telethon, aiogram", "\n".join(body), glow=False)


# ---------------------------------------------------------------- project cards

def project(t, num, kind, name, repo, version, lines, spec, stack_items, panel_head, panel, label, extra_css=""):
    tw = len(name) * 13.6
    body = [
        f'  <circle cx="35" cy="34" r="3.5" fill="{t["accent"]}" class="live"/>'
        f'<text x="46" y="38" class="label">{num} · {kind}</text>',
        f'  <text x="32" y="78" class="title">{name}</text>'
        f'<rect x="{32 + tw + 12:.1f}" y="60" width="{len(version) * 7.2 + 18:.1f}" height="22" rx="11" '
        f'fill="{t["bubble"]}"/><text x="{32 + tw + 21:.1f}" y="75" class="acc">{version}</text>',
        f'  <text x="32" y="100" class="link">{repo}</text>',
        "  " + "".join(f'<text x="32" y="{132 + i * 20}" class="desc">{ln}</text>' for i, ln in enumerate(lines)),
        "  " + specs(t, 32, 210, spec),
        "  " + pills(t, 32, 244, stack_items),
        f'  <rect x="500" y="24" width="308" height="244" rx="10" fill="url(#dots)" stroke="{t["line"]}"/>',
        f'  <text x="516" y="46" class="tiny">{panel_head[0]}</text>'
        f'<text x="792" y="46" class="tiny" text-anchor="end">{panel_head[1]}</text>',
        panel,
    ]
    return frame(t, 840, 292, label, "\n".join(body), extra_css)


def evelin(t):
    css = f"""    .rip {{ transform-box: fill-box; transform-origin: center; animation: rip 2.4s ease-out infinite; }}
    .cur {{ animation: cur 2.4s ease-in-out infinite; }}
    .ln  {{ animation: pulse 3.2s ease-in-out infinite; }}
    @keyframes rip {{ 0%,30% {{ transform: scale(.2); opacity: 0; }} 34% {{ opacity: .9; }} 80%,100% {{ transform: scale(1.6); opacity: 0; }} }}
    @keyframes cur {{ 0% {{ transform: translate(14px,16px); }} 30%,100% {{ transform: none; }} }}
"""
    out, off = [], {1, 6}
    for i in range(8):
        r, c = divmod(i, 4)
        x, y = 524 + c * 68, 62 + r * 100
        sel = i not in off
        stroke = t["accent"] if sel else t["stroke"]
        op = "" if sel else ' opacity=".45"'
        widths = [30, 20, 26, 16]
        screen = "".join(f'<rect x="{x + 8}" y="{y + 18 + k * 12}" width="{widths[(k + i) % 4]}" height="4" rx="2" '
                         f'fill="{t["stroke"]}" class="ln" style="animation-delay:{(i + k) * .3:.1f}s"/>' for k in range(4))
        tap = (f'<circle cx="{x + 23}" cy="{y + 62}" r="9" fill="none" stroke="{t["accent"]}" stroke-width="1.5" class="rip"/>'
               if sel else "")
        out.append(f'<g class="rise" style="animation-delay:{.2 + i * .07:.2f}s"{op}>'
                   f'<rect x="{x}" y="{y}" width="46" height="84" rx="8" fill="{t["bg"]}" stroke="{stroke}"/>'
                   f'<rect x="{x + 16}" y="{y + 6}" width="14" height="3" rx="1.5" fill="{t["stroke"]}"/>{screen}{tap}</g>')
    cx, cy = 524 + 23, 62 + 62
    out.append(f'<path d="M{cx} {cy} l0 14 l3.5 -3.5 l3 6 l2.2 -1 l-3 -6 l5 0 z" fill="{t["title"]}" '
               f'stroke="{t["bg"]}" stroke-width="1" class="cur"/>')
    return project(
        t, "01", "DESKTOP APP", "Evelin", "github.com/asykixd/Evelin", "v1.1.1",
        ["Control panel for Android device farms. Mirror and drive",
         "dozens of USB phones from one window: live screens, input",
         "broadcast, recorded scenarios, batch ADB and proxies."],
        [("PLATFORM", "macOS · Windows"), ("LICENSE", "MIT"), ("VIDEO", "scrcpy · H.264"), ("ROOT", "not required")],
        ["Electron", "React", "TypeScript", "ADB", "scrcpy"],
        ("INPUT BROADCAST", "6 / 8 DEVICES"), "  " + "".join(out),
        "Evelin v1.1.1 — desktop control panel for Android device farms. Electron, React, TypeScript, ADB, scrcpy. MIT.",
        css)


def uroboros(t):
    css = """    .m1 { animation: m1 10s infinite; } .m2 { animation: m2 10s infinite; }
    .m3 { animation: m3 10s infinite; } .m4 { animation: m4 10s infinite; }
    @keyframes m1 { 0%,2% { opacity: 0; transform: translateY(6px); } 5%,92% { opacity: 1; transform: none; } 96%,100% { opacity: 0; } }
    @keyframes m2 { 0%,12% { opacity: 0; transform: translateY(6px); } 16%,92% { opacity: 1; transform: none; } 96%,100% { opacity: 0; } }
    @keyframes m3 { 0%,42% { opacity: 0; transform: translateY(6px); } 45%,92% { opacity: 1; transform: none; } 96%,100% { opacity: 0; } }
    @keyframes m4 { 0%,52% { opacity: 0; transform: translateY(6px); } 56%,92% { opacity: 1; transform: none; } 96%,100% { opacity: 0; } }
"""
    a = t["accent"]

    def cmd(cls, y, text):
        w = len(text) * 7.2 + 24
        return (f'<g class="{cls}"><rect x="{792 - w:.1f}" y="{y}" width="{w:.1f}" height="26" rx="8" fill="{t["bubble"]}"/>'
                f'<text x="{780}" y="{y + 17}" class="acc" text-anchor="end">{text}</text></g>')

    def card(cls, y, head, rows):
        h = 30 + len(rows) * 18
        body = "".join(f'<circle cx="531" cy="{y + 40 + k * 18}" r="2.5" fill="{a}"/>'
                       f'<text x="540" y="{y + 44 + k * 18}" class="link" style="fill:{t["desc"]}">{k_}</text>'
                       f'<text x="700" y="{y + 44 + k * 18}" class="link" text-anchor="end" style="fill:{t["title"]}">{v}</text>'
                       for k, (k_, v) in enumerate(rows))
        return (f'<g class="{cls}"><rect x="516" y="{y}" width="200" height="{h}" rx="8" fill="{t["bg"]}" '
                f'stroke="{t["line"]}"/><text x="528" y="{y + 20}" class="mono" style="font-weight:600">{head}</text>{body}</g>')

    panel = "  " + "".join([
        cmd("m1", 60, ".dlm notes"),
        card("m2", 94, "notes 1.0 installed", [("code scan", "passed"), ("permissions", "none"), ("commands", "4")]),
        cmd("m3", 182, ".update"),
        card("m4", 216, "uroboros 1.0.0", [("channel", "stable")]),
    ])
    return project(
        t, "02", "TELEGRAM USERBOT", "Uroboros", "github.com/asykixd/uroboros", "v1.0.0",
        ["Modular Telegram userbot. One-command modules, inline",
         "forms, code scanning before install, access levels, update",
         "channels with rollback, scheduled backups."],
        [("RUNTIME", "Python 3.10+"), ("LICENSE", "AGPL-3.0"), ("INSTALL", "PyPI · Docker"), ("COMPAT", "Hikka · FTG")],
        ["Python", "Telethon", "aiogram"],
        ("SAVED MESSAGES", "TELEGRAM"), panel,
        "Uroboros v1.0.0 — modular Telegram userbot on Python and Telethon. PyPI, Docker. AGPL-3.0.", css)


def vpn(t):
    css = """    .flow { animation: flow .9s linear infinite; }
    @keyframes flow { to { stroke-dashoffset: -20; } }
"""
    w = t["warn"]
    node = lambda x, lbl: (f'<rect x="{x}" y="96" width="56" height="44" rx="8" fill="{t["bg"]}" stroke="{t["stroke"]}"/>'
                           f'<text x="{x + 28}" y="122" class="tiny" text-anchor="middle">{lbl}</text>')
    body = [
        f'  <circle cx="35" cy="32" r="3.5" fill="{w}" class="live"/><text x="46" y="36" class="label">03 · IN DEVELOPMENT</text>',
        f'  <rect x="302" y="27" width="9" height="7" rx="1.5" fill="none" stroke="{t["label"]}" stroke-width="1.3"/>'
        f'<path d="M304 27 v-2.2 a2.5 2.5 0 0 1 5 0 V27" fill="none" stroke="{t["label"]}" stroke-width="1.3"/>'
        f'<text x="380" y="36" class="label" text-anchor="end">PRIVATE</text>',
        f'  <rect x="24" y="52" width="364" height="132" rx="10" fill="url(#dots)" stroke="{t["line"]}"/>',
        f'  {node(48, "CLIENT")}{node(308, "EXIT")}',
        f'  <rect x="104" y="108" width="204" height="20" rx="10" fill="none" stroke="{t["stroke"]}"/>'
        f'<line x1="112" y1="118" x2="300" y2="118" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="6 14" '
        f'stroke-linecap="round" class="flow"/>',
        f'  <text x="206" y="160" class="tiny" text-anchor="middle">ENCRYPTED TUNNEL</text>',
        f'  {redacted(t, 32, 224, 150, 22)}<text x="194" y="224" class="link">codename redacted</text>',
        f'  <text x="32" y="254" class="desc">Native VPN client. Details stay classified</text>'
        f'<text x="32" y="274" class="desc">until the first public release.</text>',
        "  " + specs(t, 32, 306, [("LANG", "Rust"), ("STATUS", "building"), ("RELEASE", "TBA")]),
    ]
    return frame(t, 412, 344, "Unannounced VPN client in Rust — private, in development", "\n".join(body), css)


CARDS = {"hero": hero, "stack": stack, "evelin": evelin, "uroboros": uroboros, "secret-vpn": vpn}

if __name__ == "__main__":
    for name, fn in CARDS.items():
        for theme, t in THEMES.items():
            with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
                f.write(fn(t))
