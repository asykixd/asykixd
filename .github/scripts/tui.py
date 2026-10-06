"""Shared terminal-style (TUI) look for the profile cards: palette, CSS and window frame."""

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
CH = 7.22  # approximate advance of a 12px monospace glyph

THEMES = {
    "dark": dict(bg="#0a0d12", panel="#11161d", border="#2a313c", fg="#d6dde6", muted="#9aa5b1", dim="#5d6773",
                 accent="#7ee787", warn="#e3b341", sel="#7ee787", heat=("#0f2e1a", "#1a5c2e", "#2ea043", "#7ee787"),
                 empty="#151b23"),
    "light": dict(bg="#fbfbf8", panel="#f0f1ea", border="#c9cdc4", fg="#1f2328", muted="#57606a", dim="#8a9099",
                  accent="#1a7f37", warn="#9a6700", sel="#1a7f37", heat=("#c6f0d0", "#7ad18e", "#2da44e", "#1a7f37"),
                  empty="#e9ebe4"),
}


def css(t, extra=""):
    return f"""<style>
    text  {{ font-family: {MONO}; }}
    .fg   {{ font-size: 12px; fill: {t['fg']}; }}
    .mu   {{ font-size: 12px; fill: {t['muted']}; }}
    .dim  {{ font-size: 12px; fill: {t['dim']}; }}
    .acc  {{ font-size: 12px; fill: {t['accent']}; font-weight: 600; }}
    .warn {{ font-size: 12px; fill: {t['warn']}; font-weight: 600; }}
    .sm   {{ font-size: 11px; }}
    .hd   {{ font-size: 11px; font-weight: 600; letter-spacing: .6px; }}
    .on   {{ opacity: 0; animation: on .01s steps(1,end) forwards; }}
    .blink {{ animation: blink 1.1s steps(1,end) infinite; }}
    .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
    @keyframes on    {{ to {{ opacity: 1; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .3; }} }}
{extra}  </style>"""


def label(t, x, y, text, cls="acc", anchor="start"):
    """Text cut into a border line, like `┌─ title ─┐`."""
    w = len(text) * 6.65 + 14
    rx = x if anchor == "start" else x - w
    return (f'<rect x="{rx:.1f}" y="{y - 8}" width="{w:.1f}" height="16" fill="{t["bg"]}"/>'
            f'<text x="{rx + 7:.1f}" y="{y + 4}" class="{cls} hd">{text}</text>')


def window(t, w, h, aria, title, right, body, extra_css="", title_cls="acc", status=None):
    """Card with an inset box whose top border carries the titles; optional tmux-like status bar."""
    x0, y0, x1, y1 = 12.5, 16.5, w - 12.5, h - 12.5
    sb = ""
    if status:
        tag, mid, tail = status
        sy = y1 - 22
        tw = len(tag) * CH + 16
        sb = (f'<rect x="{x0 + .5}" y="{sy}" width="{x1 - x0 - 1}" height="21.5" fill="{t["panel"]}"/>'
              f'<rect x="{x0 + .5}" y="{sy}" width="{tw:.1f}" height="21.5" fill="{t["accent"]}"/>'
              f'<text x="{x0 + 8.5}" y="{sy + 15}" class="fg" style="fill:{t["bg"]};font-weight:700">{tag}</text>'
              f'<text x="{x0 + tw + 10:.1f}" y="{sy + 15}" class="mu">{mid}</text>'
              f'<text x="{x1 - 10}" y="{sy + 15}" class="dim" text-anchor="end">{tail}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" '
            f'aria-label="{aria}">\n  {css(t, extra_css)}\n'
            f'  <rect width="{w}" height="{h}" rx="8" fill="{t["bg"]}"/>\n'
            f'  <rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{t["border"]}"/>\n'
            f'  {label(t, x0 + 12, y0, title, title_cls)}{label(t, x1 - 12, y0, right, "dim", "end")}\n'
            f'  {sb}\n{body}\n</svg>\n')


def kv(x, y, rows, kw=88, step=19, delay=0.0, dstep=0.06):
    """Aligned `key  value` lines; values may contain raw SVG tspans."""
    out = []
    for i, (k, v) in enumerate(rows):
        out.append(f'<g class="on" style="animation-delay:{delay + i * dstep:.2f}s"><text x="{x}" y="{y + i * step}" '
                   f'class="acc">{k}</text><text x="{x + kw}" y="{y + i * step}" class="fg">{v}</text></g>')
    return "".join(out)


def redact(t, x, y, w, h=13):
    return f'<rect x="{x}" y="{y - h + 3}" width="{w}" height="{h}" fill="{t["dim"]}" fill-opacity=".7"/>'
