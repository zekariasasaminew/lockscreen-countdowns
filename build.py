"""Collect rendered frames from the three concept folders into the Pages site, plus covers.

python build.py      run after each concept's `render.py --all`
"""
import html
import json
import shutil
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HOME = Path.home()
ROOT = Path(__file__).parent
DOCS, COVERS = ROOT / "docs", ROOT / "covers"
SITE = "https://zekariasasaminew.github.io/lockscreen-countdowns"

CONCEPTS = [
    {
        "slug": "three-rounds",
        "title": "Three Rounds",
        "tagline": "A finals countdown served like an Ethiopian coffee ceremony. One cup fills per round.",
        "deadline": "Augustana fall finals, Fri Dec 11 2026 at 6 PM",
        "src": HOME / "three-rounds",
        "final": "2026-12-11-final",
        "cover_frames": ["2026-11-08", "2026-11-28", "2026-12-08", "2026-12-11-final"],
        "bg": "#f6e9cf", "fg": "#3a2317", "muted": "#9a7b62", "accent": "#b4532e",
        "font": ("three-rounds", "InstrumentSerif-Regular.ttf"), "body": ("three-rounds", "Inter-VariableFont_opsz,wght.ttf"),
        "web_display": "'Instrument Serif', Georgia, serif",
        "credit": "Illustration, layout, cup-fill compositing and daily rendering made with Gemini.",
    },
    {
        "slug": "chicago",
        "title": "City Lights",
        "tagline": "Counting down to day one in Chicago. Every day another window in the skyline comes on.",
        "deadline": "Moving to Chicago, Wed Jan 6 2027",
        "src": HOME / "chicago-skyline",
        "final": None,
        "cover_frames": ["2026-11-08", "2026-12-01", "2026-12-19", "2027-01-06"],
        "bg": "#071430", "fg": "#f4efe6", "muted": "#9fb0c8", "accent": "#f3c46b",
        "font": ("chicago-skyline", "InterTight.ttf"), "body": ("chicago-skyline", "Inter-VariableFont_opsz,wght.ttf"),
        "web_display": "'Inter Tight', system-ui, sans-serif",
        "credit": "Skyline illustration, window-by-window lighting, layout and daily rendering made with Gemini.",
    },
    {
        "slug": "merge-to-main",
        "title": "Merge to Main",
        "tagline": "Fall term as a GitHub pull request. Each day is a commit; finals are the merge.",
        "deadline": "Augustana fall finals, Fri Dec 11 2026 at 6 PM",
        "src": HOME / "merge-to-main",
        "final": "2026-12-11-merged",
        "cover_frames": ["2026-11-08", "2026-11-28", "2026-12-09", "2026-12-11-merged"],
        "bg": "#f6f8fa", "fg": "#1f2328", "muted": "#59636e", "accent": "#1f883d",
        "font": ("merge-to-main", "MonaSans-SemiBold.ttf"), "body": ("merge-to-main", "MonaSans-Regular.ttf"),
        "web_display": "'Mona Sans', system-ui, sans-serif",
        "credit": "Milestones, GitHub-style layout and daily rendering made with Gemini.",
    },
]


def frames_of(c):
    """(name, path) for every rendered day, in order; the after-6 PM frame last."""
    out = c["src"] / "out"
    days = sorted(p for p in out.glob("20??-??-??.png"))
    if not days:
        raise SystemExit(f"{c['slug']}: no daily frames in {out}; run render.py --all first")
    items = [(p.stem, p) for p in days]
    if c["final"]:
        items.append((c["final"], out / f"{c['final']}.png"))
    return items


def font(c, key, size):
    folder, name = c[key]
    return ImageFont.truetype(str(HOME / folder / "assets" / "fonts" / name), size)


def label_for(name):
    d = date.fromisoformat(name[:10])
    s = f"{d.strftime('%b')} {d.day}"
    return s + (", after 6 PM" if len(name) > 10 else "")


def cover(c):
    W, H = 1800, 1200
    img = Image.new("RGB", (W, H), c["bg"])
    dr = ImageDraw.Draw(img)
    dr.text((90, 70), c["title"], font=font(c, "font", 84), fill=c["fg"])
    sub = font(c, "body", 30)
    dr.text((92, 178), c["tagline"], font=sub, fill=c["muted"])

    ph, gap = 840, 54
    pw = round(ph * 1179 / 2556)
    x = (W - 4 * pw - 3 * gap) // 2
    y = 260
    src = c["src"] / "out"
    lf = font(c, "body", 28)
    for name in c["cover_frames"]:
        fr = Image.open(src / f"{name}.png").convert("RGB").resize((pw, ph), Image.LANCZOS)
        r = 34
        mask = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=r, fill=255)
        shadow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(shadow).rounded_rectangle((x, y + 14, x + pw, y + ph + 14), radius=r, fill=90)
        shadow = shadow.filter(ImageFilter.GaussianBlur(22))
        img.paste(Image.new("RGB", (W, H), "#000000"), (0, 0), shadow)
        img.paste(fr, (x, y), mask)
        ImageDraw.Draw(img).rounded_rectangle((x, y, x + pw - 1, y + ph - 1), radius=r, outline=c["muted"], width=2)
        dr = ImageDraw.Draw(img)
        dr.text((x + pw / 2, y + ph + 50), label_for(name), font=lf, fill=c["fg"], anchor="mm")
        x += pw + gap
    COVERS.mkdir(exist_ok=True)
    img.save(COVERS / f"{c['slug']}.png", optimize=True)
    img.save(DOCS / c["slug"] / "cover.jpg", quality=90)


STEPS = """
<ol class="steps">
  <li>In <b>Shortcuts</b>, tap <b>+</b> to start a new shortcut.</li>
  <li>Add <b>Format Date</b> on <i>Current Date</i>, Custom format <code>yyyy-MM-dd</code>.</li>
  <li>Add <b>Text</b>: <code>{site}/{slug}/frames/</code>, then the <i>Formatted Date</i>, then <code>.jpg</code>.</li>
  <li>Add <b>Get Contents of URL</b> with that Text, then <b>Set Wallpaper</b>: Lock Screen, Show Preview off.</li>
  <li>Set your Lock Screen to a <b>Photos</b> wallpaper once, so there is one to replace.</li>
  <li>In <b>Automation</b>: <b>Time of Day</b>, 12:01 AM, Daily, Run Immediately, run this shortcut.</li>
  {evening}
</ol>
<p class="fine">There is a frame for every day from {first} to {last}. Untested on every iOS version; action names can vary slightly.</p>
"""

EVENING = """<li>Finale: duplicate it with <code>-evening.jpg</code> in place of <code>.jpg</code>, on a 6:01 PM daily automation.</li>"""


def page(c, names):
    nav = " ".join(
        f'<a href="../{o["slug"]}/"{" aria-current=page" if o is c else ""}>{html.escape(o["title"])}</a>' for o in CONCEPTS
    )
    data = json.dumps({"frames": names, "final": c["final"]})
    days = [n for n in names if len(n) == 10]
    steps = STEPS.format(
        title=html.escape(c["title"]), site=SITE, slug=c["slug"], evening=EVENING if c["final"] else "",
        first=label_for(days[0]), last=label_for(days[-1]),
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(c['title'])}</title>
<meta name="description" content="{html.escape(c['tagline'])}">
<meta property="og:image" content="{SITE}/{c['slug']}/cover.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter:wght@400;500;600&family=Inter+Tight:wght@600&family=Mona+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{ --bg: {c['bg']}; --fg: {c['fg']}; --muted: {c['muted']}; --accent: {c['accent']}; --ph: calc(100dvh - 150px); }}
* {{ box-sizing: border-box; }}
html, body {{ height: 100%; }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 15px/1.5 Inter, system-ui, sans-serif; }}
main {{ max-width: 1180px; height: 100%; margin: 0 auto; padding: 20px 24px; display: flex; flex-direction: column; }}
nav {{ display: flex; gap: 18px; flex-wrap: wrap; font-size: 14px; margin-bottom: 20px; }}
nav a {{ color: var(--muted); text-decoration: none; }}
nav a[aria-current] {{ color: var(--fg); font-weight: 600; }}
.grid {{ flex: 1; min-height: 0; display: grid; grid-template-columns: auto minmax(0, 1fr); gap: clamp(32px, 5vw, 64px); align-items: center; }}
.phone {{ height: var(--ph); width: calc(var(--ph) * 1179 / 2556); max-height: 2556px; border-radius: calc(var(--ph) / 17); overflow: hidden; box-shadow: 0 24px 50px rgba(0,0,0,.28), 0 0 0 2px color-mix(in srgb, var(--muted) 50%, transparent); background: #000; }}
.phone img {{ width: 100%; height: 100%; display: block; }}
.scrub {{ margin-top: 14px; width: calc(var(--ph) * 1179 / 2556); min-width: 280px; }}
.scrub input {{ width: 100%; margin: 0; accent-color: var(--accent); }}
.row {{ display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: var(--muted); margin-top: 6px; gap: 8px; }}
.row span:last-child {{ display: flex; gap: 6px; }}
button, .btn {{ font: inherit; font-size: 13px; color: var(--fg); background: transparent; border: 1px solid color-mix(in srgb, var(--muted) 60%, transparent); border-radius: 999px; padding: 5px 12px; cursor: pointer; text-decoration: none; white-space: nowrap; }}
h1 {{ font-family: {c['web_display']}; font-weight: 600; font-size: clamp(34px, 6vh, 56px); line-height: 1; margin: 0 0 10px; letter-spacing: -0.01em; }}
.tag {{ font-size: clamp(15px, 2.2vh, 18px); color: var(--muted); margin: 0 0 4px; }}
.dl {{ font-size: 13px; color: var(--muted); margin: 0; }}
h2 {{ font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: clamp(14px, 3vh, 28px) 0 8px; font-weight: 600; }}
.steps {{ padding-left: 20px; margin: 0; font-size: clamp(13px, 1.9vh, 15px); }}
.steps li {{ margin: 0 0 clamp(2px, .8vh, 8px); }}
code {{ font-size: .88em; background: color-mix(in srgb, var(--muted) 18%, transparent); padding: 1px 5px; border-radius: 5px; overflow-wrap: anywhere; }}
.fine, .credit {{ font-size: 12.5px; color: var(--muted); margin: 8px 0 0; }}
#setup-open, .close {{ display: none; }}
@media (max-width: 760px) {{
  :root {{ --ph: calc(100dvh - 250px); }}
  main {{ padding: 14px 16px; }}
  nav {{ margin-bottom: 12px; font-size: 13px; }}
  .grid {{ display: flex; flex-direction: column; align-items: center; gap: 12px; }}
  .info {{ order: -1; width: 100%; }}
  h1 {{ font-size: 30px; margin-bottom: 4px; }}
  .tag {{ font-size: 14px; line-height: 1.35; }}
  .dl {{ display: none; }}
  .scrub {{ width: 100%; max-width: 360px; }}
  #setup-open {{ display: inline-block; }}
  .more {{ display: none; position: fixed; inset: 0; z-index: 2; background: var(--bg); padding: 20px 20px 24px; overflow-y: auto; }}
  body.setup .more {{ display: block; }}
  .more h2:first-of-type {{ margin-top: 0; }}
  .close {{ display: block; margin-left: auto; margin-bottom: 8px; }}
}}
</style>
</head>
<body>
<main>
<nav>{nav}</nav>
<div class="grid">
  <div class="viewer">
    <div class="phone"><img id="frame" alt="Lock screen for the selected day" width="1179" height="2556"></div>
    <div class="scrub">
      <input id="day" type="range" min="0" max="{len(names) - 1}" step="1" aria-label="Day">
      <div class="row"><span id="label"></span><span><button id="play" type="button">Play</button><a class="btn" id="save" download>Save</a><button id="setup-open" type="button">Set up</button></span></div>
    </div>
  </div>
  <div class="info">
    <h1>{html.escape(c['title'])}</h1>
    <p class="tag">{html.escape(c['tagline'])}</p>
    <p class="dl">Deadline: {html.escape(c['deadline'])}. One image per day, swapped every morning by a Shortcut.</p>
    <section class="more" aria-label="Setup">
      <button class="close" id="setup-close" type="button">Close</button>
      <h2>Put it on your phone</h2>
      {steps}
      <h2>How it was made</h2>
      <p class="credit">{html.escape(c['credit'])} Designed and directed by Zekarias Asaminew.</p>
    </section>
  </div>
</div>
</main>
<script>
const D = {data};
const img = document.getElementById("frame"), range = document.getElementById("day"),
  label = document.getElementById("label"), save = document.getElementById("save"), play = document.getElementById("play");
const fmt = n => {{
  const d = new Date(n.slice(0, 10) + "T12:00:00");
  return d.toLocaleDateString("en-US", {{ weekday: "short", month: "short", day: "numeric" }}) + (n.length > 10 ? ", after 6 PM" : "");
}};
function show(i) {{
  const n = D.frames[i];
  img.src = "frames/" + n + ".jpg";
  save.href = img.src;
  label.textContent = fmt(n);
  range.value = i;
}}
function today() {{
  const now = new Date();
  const parts = new Intl.DateTimeFormat("en-CA", {{ timeZone: "America/Chicago", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", hourCycle: "h23" }}).formatToParts(now);
  const get = t => parts.find(p => p.type === t).value;
  const key = get("year") + "-" + get("month") + "-" + get("day");
  const days = D.frames.filter(n => n.length === 10);
  if (key < days[0]) return 0;
  if (key > days[days.length - 1]) return D.frames.length - 1;
  if (D.final && key === D.final.slice(0, 10) && +get("hour") >= 18) return D.frames.length - 1;
  return D.frames.indexOf(key);
}}
range.addEventListener("input", () => show(+range.value));
document.getElementById("setup-open").onclick = () => document.body.classList.add("setup");
document.getElementById("setup-close").onclick = () => document.body.classList.remove("setup");
let timer = null;
play.addEventListener("click", () => {{
  if (timer) {{ clearInterval(timer); timer = null; play.textContent = "Play"; return; }}
  let i = 0; show(i); play.textContent = "Pause";
  timer = setInterval(() => {{ i++; if (i >= D.frames.length) {{ clearInterval(timer); timer = null; play.textContent = "Play"; return; }} show(i); }}, 260);
}});
D.frames.forEach(n => {{ const p = new Image(); p.src = "frames/" + n + ".jpg"; }});
show(today());
</script>
</body>
</html>
"""


def index():
    cards = "\n".join(
        f'<a class="card" href="{c["slug"]}/"><img src="{c["slug"]}/cover.jpg" alt="{html.escape(c["title"])} cover" width="1800" height="1200"><b>{html.escape(c["title"])}</b><span>{html.escape(c["tagline"])}</span></a>'
        for c in CONCEPTS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Countdown Lock Screens</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {{ --bg: #f4f2ee; --fg: #1d1b18; --muted: #6b665e; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg: #141311; --fg: #f1eee8; --muted: #a39d93; }} }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.5 Inter, system-ui, sans-serif; }}
main {{ max-width: 1100px; margin: 0 auto; padding: 48px 16px 64px; }}
h1 {{ font-size: clamp(32px, 6vw, 52px); margin: 0 0 8px; letter-spacing: -0.02em; }}
p {{ color: var(--muted); max-width: 640px; margin: 0 0 36px; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 28px; }}
.card {{ color: inherit; text-decoration: none; display: grid; gap: 6px; }}
.card img {{ width: 100%; height: auto; border-radius: 14px; }}
.card span {{ color: var(--muted); font-size: 14px; }}
</style>
</head>
<body>
<main>
<h1>Countdown lock screens</h1>
<p>Three iPhone lock screens that change every day until a real deadline: finals, and a move to Chicago. Pick one to see the full run and set it up.</p>
<div class="cards">{cards}</div>
</main>
</body>
</html>
"""


def main():
    shutil.rmtree(DOCS, ignore_errors=True)
    shutil.rmtree(COVERS, ignore_errors=True)
    for c in CONCEPTS:
        fdir = DOCS / c["slug"] / "frames"
        fdir.mkdir(parents=True)
        items = frames_of(c)
        names = []
        for name, path in items:
            Image.open(path).convert("RGB").save(fdir / f"{name}.jpg", quality=90, subsampling=0)
            if c["final"] and name != c["final"]:
                shutil.copyfile(fdir / f"{name}.jpg", fdir / f"{name}-evening.jpg")
            names.append(name)
        # the 6:01 PM shortcut asks for <date>-evening.jpg; on deadline day that is the finale
        if c["final"]:
            shutil.copyfile(fdir / f"{c['final']}.jpg", fdir / f"{c['final'][:10]}-evening.jpg")
        (DOCS / c["slug"] / "index.html").write_text(page(c, names), encoding="utf-8")
        cover(c)
        print(c["slug"], len(names), "frames")
    (DOCS / "index.html").write_text(index(), encoding="utf-8")
    (DOCS / ".nojekyll").write_text("")


if __name__ == "__main__":
    main()
