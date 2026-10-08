"""Render the static profile cards in assets/ (hero, project cards) for both themes.

Usage: python3 .github/scripts/cards.py
The activity card is rendered separately by stats.py. Both share the look defined in tui.py.
"""
import os

from tui import CH, THEMES, kv, redact, window

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

# 5x7 pixel glyphs for the hero logo
GLYPHS = {
    "a": [".....", ".....", ".###.", "....#", ".####", "#...#", ".####"],
    "s": [".....", ".....", ".####", "#....", ".###.", "....#", "####."],
    "y": [".....", ".....", "#...#", "#...#", ".####", "....#", ".###."],
    "k": ["#....", "#....", "#..#.", "#.#..", "##...", "#.#..", "#..#."],
    "i": ["..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."],
    "x": [".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"],
    "d": ["....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"],
}


def prompt(t, x, y, cmd, delay=0.0, cursor=False):
    cur = (f'<rect x="{x + (len(cmd) + 2) * CH:.1f}" y="{y - 11}" width="{CH:.1f}" height="14" fill="{t["accent"]}" '
           f'class="blink"/>') if cursor else ""
    return (f'<g class="on" style="animation-delay:{delay:.2f}s"><text x="{x}" y="{y}" class="acc">$</text>'
            f'<text x="{x + 2 * CH:.1f}" y="{y}" class="fg">{cmd}</text>{cur}</g>')


# ---------------------------------------------------------------- hero

def hero(t):
    px, gap = 7, 1
    logo = []
    for li, ch in enumerate("asykixd"):
        for r, row in enumerate(GLYPHS[ch]):
            for c, on in enumerate(row):
                if on == "#":
                    x = 40 + li * 6 * (px + gap) + c * (px + gap)
                    y = 78 + r * (px + gap)
                    logo.append(f'<rect x="{x}" y="{y}" width="{px}" height="{px}" fill="{t["accent"]}"/>')
    swatches = "".join(f'<rect x="{40 + i * 22}" y="{168}" width="20" height="10" fill="{c}"/>'
                       for i, c in enumerate((t["fg"], t["muted"], t["dim"], t["accent"], t["warn"], "#79c0ff",
                                              "#d2a8ff", "#ff7b72")))
    a = t["accent"]
    rows = [
        ("role", "software engineer"),
        ("focus", "systems · dev tooling · desktop"),
        ("langs", "rust  python  typescript  c"),
        ("tools", "electron  react  docker  linux  adb"),
        ("projects", f'2 released <tspan fill="{t["dim"]}">·</tspan> 1 in beta'),
        ("latest", f'evelin <tspan fill="{a}">v1.1.9</tspan> <tspan fill="{t["dim"]}">2026-10-08</tspan>'),
    ]
    body = [
        "  " + prompt(t, 30, 50, "neofetch"),
        f'  <g class="on" style="animation-delay:.25s">{"".join(logo)}{swatches}</g>',
        f'  <line x1="420" y1="34" x2="420" y2="190" stroke="{t["border"]}" stroke-dasharray="2 3"/>',
        f'  <g class="on" style="animation-delay:.3s"><text x="444" y="56" class="acc">asykixd<tspan fill="{t["dim"]}">'
        f'@</tspan>github</text><text x="444" y="72" class="dim">{"─" * 18}</text></g>',
        "  " + kv(444, 96, rows, kw=80, delay=.35),
        "  " + prompt(t, 30, 218, "", delay=.9, cursor=True),
    ]
    return window(t, 840, 240, "asykixd — software engineer: systems programming, developer tooling, desktop "
                  "applications. Rust, Python, TypeScript, C. Latest release: Evelin v1.1.9",
                  "asykixd@github: ~", "zsh", "\n".join(body))


# ---------------------------------------------------------------- projects

def project(t, num, name, version, url, cmd, rows, right, aria, extra_css=""):
    body = [
        "  " + prompt(t, 30, 50, cmd),
        "  " + kv(30, 78, rows, kw=84, delay=.2),
        f'  <line x1="492" y1="17" x2="492" y2="{258 - 34.5}" stroke="{t["border"]}"/>',
        right,
    ]
    return window(t, 840, 258, aria, f"{num} · {name}", f"{version} · stable", "\n".join(body), extra_css,
                  status=(name, f"release {version}", url))


def evelin(t):
    css = """    .tap { opacity: 0; animation: tap 2.4s ease-out infinite; }
    @keyframes tap { 0%,40% { opacity: 0; } 44% { opacity: .35; } 80%,100% { opacity: 0; } }
"""
    a, off = t["accent"], {2, 5}
    out = [f'<text x="508" y="50" class="mu sm">devices</text>'
           f'<text x="812" y="50" class="sm" text-anchor="end"><tspan fill="{a}">●</tspan>'
           f'<tspan fill="{t["muted"]}"> broadcast 6/8</tspan></text>']
    for i in range(8):
        r, c = divmod(i, 4)
        x, y = 508 + c * 77, 64 + r * 68
        sel = i not in off
        col = a if sel else t["border"]
        bars = "".join(f'<rect x="{x + 8}" y="{y + 26 + k * 8}" width="{(28, 44, 20, 36)[(i + k) % 4]}" height="3" '
                       f'fill="{t["dim"]}" fill-opacity=".6"/>' for k in range(3))
        tap = f'<rect x="{x}" y="{y}" width="68" height="58" fill="{a}" class="tap"/>' if sel else ""
        out.append(f'<g class="on" style="animation-delay:{.3 + i * .06:.2f}s">'
                   f'<rect x="{x + .5}" y="{y + .5}" width="67" height="57" fill="{t["panel"]}" stroke="{col}"/>{tap}'
                   f'<text x="{x + 8}" y="{y + 16}" class="sm" fill="{t["fg"] if sel else t["dim"]}">dev0{i + 1}</text>'
                   f'<text x="{x + 60}" y="{y + 16}" class="sm" text-anchor="end" fill="{col}">'
                   f'{"●" if sel else "○"}</text>{bars}</g>')
    out.append(f'<g class="on" style="animation-delay:1s"><text x="508" y="210" class="sm"><tspan fill="{a}">&gt;</tspan>'
               f'<tspan fill="{t["fg"]}"> tap 540,1210</tspan><tspan fill="{t["dim"]}"> → 6 devices · 4 ms</tspan></text></g>')
    return project(
        t, "01", "evelin", "v1.1.9", "github.com/asykixd/Evelin", "evelin --help",
        [("name", "android device farm control panel"),
         ("about", "mirror and drive dozens of usb phones"),
         ("", "from one window. no root required."),
         ("features", "live screens · input broadcast · proxies"),
         ("", "text-aware scenarios · batch adb"),
         ("platform", "macos · windows"),
         ("stack", "electron react typescript scrcpy")],
        "  " + "".join(out),
        "Evelin v1.1.9 — desktop control panel for Android device farms. Electron, React, TypeScript, ADB, scrcpy.",
        css)


def uroboros(t):
    a, d, f = t["accent"], t["dim"], t["fg"]
    log = [("&gt;", a, ".dlm notes"), ("scan", f, "notes.py: 0 issues"), ("perm", f, "none requested"),
           ("ok", a, "notes 1.0 · 4 commands"), ("&gt;", a, ".update"), ("git", f, "fetch master: done"),
           ("ok", a, "uroboros 1.0.0 latest")]
    n, period = len(log), 12.0
    css = "".join(
        f"    .l{i} {{ animation: l{i} {period}s infinite; }} @keyframes l{i} {{ 0%,{(i * .8 + .3) / period * 100:.1f}% "
        f"{{ opacity: 0; }} {(i * .8 + .31) / period * 100:.1f}%,94% {{ opacity: 1; }} 95%,100% {{ opacity: 0; }} }}\n"
        for i in range(n))
    out = [f'<text x="508" y="50" class="mu sm">saved messages</text>'
           f'<text x="812" y="50" class="sm" text-anchor="end"><tspan fill="{a}" class="pulse">●</tspan>'
           f'<tspan fill="{t["muted"]}"> online</tspan></text>']
    for i, (tag, col, msg) in enumerate(log):
        y = 76 + i * 19
        out.append(f'<g class="l{i}"><text x="508" y="{y}" class="sm" fill="{d}">03:12:0{1 + i}</text>'
                   f'<text x="574" y="{y}" class="sm" fill="{col}" font-weight="600">{tag}</text>'
                   f'<text x="614" y="{y}" class="sm" fill="{f if col != a or tag == "&gt;" else a}">{msg}</text></g>')
    return project(
        t, "02", "uroboros", "v1.0.0", "github.com/asykixd/uroboros", "uroboros --help",
        [("name", "modular telegram userbot"),
         ("about", "one-command modules, inline forms,"),
         ("", "code scan before install, rollback"),
         ("runtime", "python 3.10+ · telethon"),
         ("install", "pypi · docker · termux"),
         ("compat", "hikka and ftg modules"),
         ("license", "agpl-3.0")],
        "  " + "".join(out),
        "Uroboros v1.0.0 — modular Telegram userbot on Python and Telethon. PyPI, Docker. AGPL-3.0.", css)


def vpn(t):
    css = """    .prog { transform-box: fill-box; transform-origin: left; animation: prog 6s steps(24,end) infinite; }
    @keyframes prog { 0% { transform: scaleX(.05); } 85%,100% { transform: scaleX(1); } }
"""
    w = t["warn"]
    body = [
        "  " + prompt(t, 30, 50, "cargo build --release"),
        f'  <g class="on" style="animation-delay:.3s"><text x="44" y="74" class="acc">Compiling</text>'
        f'{redact(t, 125, 74, 72)}<text x="205" y="74" class="dim">v0.1.0</text></g>',
        f'  <g class="on" style="animation-delay:.5s"><text x="44" y="93" class="acc">Compiling</text>'
        f'{redact(t, 125, 93, 104)}<text x="237" y="93" class="dim">v0.1.0</text></g>',
        f'  <g class="on" style="animation-delay:.7s"><text x="44" y="112" class="acc">Building</text>'
        f'<text x="125" y="112" class="dim">[</text><rect x="135" y="103" width="190" height="10" fill="{w}" '
        f'class="prog"/><text x="330" y="112" class="dim">]</text></g>',
        "  " + kv(30, 150, [("status", f'<tspan fill="{w}">private beta</tspan>'), ("kind", "proxy &amp; vpn client"),
                              ("stack", "rust · slint · clash-rs"), ("platform", "macos · windows")], kw=76, delay=.9),
        f'  <g class="on" style="animation-delay:1.2s"><text x="30" y="238" class="dim"># codename classified</text>'
        f'<text x="30" y="256" class="dim"># until public release</text></g>',
        "  " + prompt(t, 30, 286, "", delay=1.4, cursor=True),
    ]
    return window(t, 412, 312, "Unannounced proxy and VPN client in Rust for macOS and Windows — private beta", "03 · classified",
                  "private", "\n".join(body), css, title_cls="warn")


CARDS = {"hero": hero, "evelin": evelin, "uroboros": uroboros, "secret-vpn": vpn}

if __name__ == "__main__":
    for name, fn in CARDS.items():
        for theme, t in THEMES.items():
            with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
                f.write(fn(t))
