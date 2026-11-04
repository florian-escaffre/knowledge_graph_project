import pandas as pd, html
from collections import defaultdict
from collections import Counter
from pyvis.network import Network

# Minimal category graph: nodes = categories, edges = number of links between them.
arts = pd.read_csv("data/exploration/articles.csv")
links = pd.read_csv("data/exploration/links.csv")
links = links[links["target_exists"].astype(str) == "True"]

cats = {r.term: (r.categories.split("; ") if isinstance(r.categories, str) else ["(none)"])
        for r in arts.itertuples()}

w = Counter((a, b) for s, t in zip(links["source"], links["target"])
            for a in cats.get(s, ["(none)"]) for b in cats.get(t, ["(none)"]) if a != b)

net = Network(height="900px", width="100%", directed=True, cdn_resources="in_line")
for (a, b), n in w.items():
    if n >= 5:                                   # hide weak edges
        net.add_node(a, label=a); net.add_node(b, label=b)
        net.add_edge(a, b, value=n, title=str(n))
net.write_html("data/exploration/schema_graph.html")


# Collapsible HTML tree: category -> articles it contains (articles in several categories appear in each).
tree = defaultdict(list)
for r in arts.itertuples():
    cats = r.categories.split("; ") if isinstance(r.categories, str) else ["(none)"]
    for c in cats:
        tree[c].append(r.term)

parts = ["<meta charset='utf-8'><body style='font-family:sans-serif'>",
         f"<h2>{len(arts)} articles, {len(tree)} categories</h2>"]
for c, terms in sorted(tree.items(), key=lambda kv: -len(kv[1])):
    items = "".join(f"<li>{html.escape(t)}</li>" for t in sorted(terms, key=str.lower))
    parts.append(f"<details><summary><b>{html.escape(c)}</b> ({len(terms)})</summary><ul>{items}</ul></details>")

open("data/exploration/hierarchy.html", "w", encoding="utf-8").write("\n".join(parts))
print("Saved exploration/hierarchy.html")