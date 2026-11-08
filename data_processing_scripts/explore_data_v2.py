import json, html
from collections import Counter, defaultdict
from pathlib import Path

MIN_EDGE = 1   # category links below this count are hidden
out = Path("data/exploration"); out.mkdir(parents=True, exist_ok=True)
ents = list(json.load(open("data/engipedia_fr_store.json", encoding="utf-8"))["entities"].values())
esc = html.escape

terms = {e["_term"] for e in ents}
cats_of = {e["_term"]: (e.get("_categories") or ["(none)"]) for e in ents}
links = [(e["_term"], t) for e in ents for t in (e.get("_linked_terms") or []) if t in terms]
out_deg = Counter(s for s, _ in links)
in_deg = Counter(t for _, t in links)
isolated = {t for t in terms if out_deg[t] == 0 and in_deg[t] == 0}

tree = defaultdict(list)
for t, cs in cats_of.items():
    for c in cs:
        tree[c].append(t)

# Category -> category link weights (links within the same category ignored)
w = Counter((a, b) for s, t in links for a in cats_of[s] for b in cats_of[t] if a != b)

# --- Tab 1: categories -> articles
def label(t, c):
    s = esc(t)
    others = [x for x in cats_of[t] if x != c]
    if others:
        s += f" <i style='color:#888'>+ {esc(', '.join(others))}</i>"
    if t in isolated:
        s += " <b style='color:#c00'>[isolated]</b>"
    return f"<li>{s}</li>"

tab1 = [f"<h3>{len(terms)} articles, {len(tree)} categories</h3>"]
for c, ts in sorted(tree.items(), key=lambda kv: -len(kv[1])):
    items = "".join(label(t, c) for t in sorted(ts, key=str.lower))
    tab1.append(f"<details><summary><b>{esc(c)}</b> ({len(ts)})</summary><ul>{items}</ul></details>")

# --- Tab 2: multi-category articles
multi = sorted(((t, cs) for t, cs in cats_of.items() if len(cs) > 1), key=lambda x: (-len(x[1]), x[0].lower()))
tab2 = [f"<h3>{len(multi)} articles in several categories</h3><table><tr><th>Article</th><th>#</th><th>Categories</th></tr>"]
tab2 += [f"<tr><td>{esc(t)}</td><td>{len(cs)}</td><td>{esc('; '.join(cs))}</td></tr>" for t, cs in multi]
tab2.append("</table>")

# --- Tab 3: isolated articles
iso = sorted(isolated, key=str.lower)
tab3 = [f"<h3>{len(iso)} isolated articles (no incoming or outgoing link)</h3><table><tr><th>Article</th><th>Categories</th></tr>"]
tab3 += [f"<tr><td>{esc(t)}</td><td>{esc('; '.join(cats_of[t]))}</td></tr>" for t in iso]
tab3.append("</table>")

# --- Tab 4: links between categories
pairs = [(a, b, n) for (a, b), n in w.most_common() if n >= MIN_EDGE]
tab4 = [f"<h3>{len(pairs)} category pairs (≥ {MIN_EDGE} links)</h3>",
        "<input placeholder='filter...' oninput='filt(this)' style='margin-bottom:8px;width:300px'>",
        "<table id='pairs'><tr><th>Source</th><th>→ Target</th><th>Links</th></tr>"]
tab4 += [f"<tr class='r'><td>{esc(a)}</td><td>{esc(b)}</td><td>{n}</td></tr>" for a, b, n in pairs]
tab4.append("</table>")

names = ["Categories → articles", "Multi-category", "Isolated", "Links between categories"]
tabs = [tab1, tab2, tab3, tab4]
page = ["<!DOCTYPE html><html lang='en'><meta charset='utf-8'><title>Exploration</title>",
        "<style>body{font-family:sans-serif;margin:20px}.tab{display:none}.tab.on{display:block}"
        "button{margin-right:6px;padding:6px 12px}table{border-collapse:collapse}"
        "td,th{border:1px solid #ccc;padding:3px 8px;text-align:left}</style>",
        "<script>function show(i){document.querySelectorAll('.tab').forEach((e,j)=>e.classList.toggle('on',i==j))}"
        "function filt(x){const q=x.value.toLowerCase();document.querySelectorAll('#pairs tr.r')"
        ".forEach(r=>r.style.display=r.textContent.toLowerCase().includes(q)?'':'none')}</script>",
        "<body>" + "".join(f"<button onclick='show({i})'>{n}</button>" for i, n in enumerate(names))]
for i, t in enumerate(tabs):
    page.append(f"<div class='tab{' on' if i == 0 else ''}'>" + "\n".join(t) + "</div>")

(out / "exploration.html").write_text("\n".join(page), encoding="utf-8")
print("Written:", out / "exploration.html")