"""Build index.html and README.md from jokes.json. Run: python build.py"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
jokes = json.loads((ROOT / "jokes.json").read_text(encoding="utf-8"))


def label(j):
    tags = []
    if j.get("keeper"):
        tags.append("keeper")
    if j.get("series"):
        tags.append(j["series"])
    score = f", {j['score']} of 10" if j.get("score") else ""
    return f"{j['n']}. {j['title']}{score}" + (f" ({', '.join(tags)})" if tags else "")


def joke_block(j):
    paras = "\n".join(f"<p>{html.escape(p)}</p>" for p in j["text"].split("\n\n"))
    note = f'<p class="note">{html.escape(j["note"])}</p>' if j.get("note") else ""
    cls = ' class="keeper"' if j.get("keeper") else ""
    return (f'<details id="j{j["n"]}"{cls}>\n<summary><h3>{html.escape(label(j))}</h3></summary>\n'
            f"{note}\n{paras}\n</details>")


def link_list(items):
    return "<ul>\n" + "\n".join(
        f'<li><a href="#j{j["n"]}">{html.escape(label(j))}</a></li>' for j in items) + "\n</ul>"


keepers = [j for j in jokes if j.get("keeper")]
ranked = sorted((j for j in jokes if j.get("score")), key=lambda j: (-j["score"], not j.get("keeper"), j["n"]))
brown = [j for j in jokes if j.get("series") == "Farmer Brown"]
stories = [j for j in jokes if j["kind"] == "story"]
oneliners = [j for j in jokes if j["kind"] == "one-liner"]

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chip's Joke Book</title>
<style>
:root {{ --bg:#fff; --text:#1a1a1a; --muted:#555; --accent:#b34700; --rule:#ddd; --card:#f7f5f2; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#121212; --text:#f2f2f2; --muted:#b8b8b8; --accent:#ff9a4d; --rule:#333; --card:#1c1c1c; }} }}
* {{ box-sizing:border-box; }}
html {{ font-size:112.5%; scroll-behavior:auto; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:Georgia,"Times New Roman",serif; line-height:1.65; }}
header, main {{ max-width:44rem; margin:0 auto; padding:0 1rem; }}
header {{ padding-top:2rem; border-bottom:1px solid var(--rule); }}
.kicker {{ font-family:Arial,Helvetica,sans-serif; font-size:.8rem; letter-spacing:.08em; text-transform:uppercase; color:var(--accent); margin:0; }}
h1 {{ font-size:2rem; margin:.4rem 0 .6rem; }}
h2 {{ font-size:1.35rem; margin:2.2rem 0 .6rem; }}
h3 {{ display:inline; font-size:1.1rem; }}
a {{ color:var(--accent); }}
details {{ border-bottom:1px solid var(--rule); padding:.6rem 0; }}
details.keeper summary h3 {{ color:var(--accent); }}
summary {{ cursor:pointer; }}
.note {{ background:var(--card); border-left:4px solid var(--accent); padding:.5rem .8rem; color:var(--muted); }}
</style>
</head>
<body>
<header>
<p class="kicker">Keeping the told joke alive</p>
<h1>Chip's Joke Book</h1>
<p>Joke telling was a pastime on Southern porches, in Irish pubs, and in English music halls. It is becoming a lost art. This book keeps the jokes worth telling, written the way they are told.</p>
<p>{len(jokes)} jokes. {len(keepers)} keepers. The standard is number 19: a slow build, real dialogue, and a punchline that gets a laugh.</p>
</header>
<main>
<h2>Ranked by laughs</h2>
<ol>
{chr(10).join(f'<li><a href="#j{j["n"]}">{html.escape(label(j))}</a></li>' for j in ranked)}
</ol>
<h2>Keepers</h2>
{link_list(keepers)}
<h2>The Farmer Brown series</h2>
{link_list(brown)}
<h2>All story jokes</h2>
{chr(10).join(joke_block(j) for j in stories)}
<h2>One-liners (retired)</h2>
{chr(10).join(joke_block(j) for j in oneliners)}
</main>
<script>
function openHash() {{
  var el = location.hash && document.querySelector(location.hash);
  if (el && el.tagName === "DETAILS") {{ el.open = true; el.scrollIntoView(); }}
}}
window.addEventListener("hashchange", openHash);
openHash();
</script>
</body>
</html>
"""
(ROOT / "index.html").write_text(page, encoding="utf-8")

readme = ["# Chip's Joke Book", "",
          "Live page: https://grandpi224.github.io/JOKES/", "",
          "Source of truth is `jokes.json`. Run `python build.py` to rebuild `index.html`.", "",
          "## Keepers", ""] + [f"- {label(j)}" for j in keepers] + \
         ["", "## All jokes", ""] + [f"- {label(j)}" for j in jokes] + [""]
(ROOT / "README.md").write_text("\n".join(readme), encoding="utf-8")
print(f"{len(jokes)} jokes, {len(keepers)} keepers, {len(brown)} Farmer Brown")
