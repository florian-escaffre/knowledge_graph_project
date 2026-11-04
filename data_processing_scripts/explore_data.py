import json, csv, collections, statistics as st
from pathlib import Path

# Quick exploration of engipedia_fr_store.json: counts, categories, first article, links, text lengths.
out = Path("data/exploration"); out.mkdir(exist_ok=True)
data = json.load(open("data/engipedia_fr_store.json", encoding="utf-8"))
ents = list(data["entities"].values())

lines = []
def log(s=""):
    print(s); lines.append(str(s))

# Counts
print("Articles:", len(ents))
cats = collections.Counter(c for e in ents for c in (e.get("_categories") or []))
print("Distinct categories:", len(cats))
print("Top categories:", cats.most_common(10))

# First article
print("\n--- First article ---")
print(json.dumps(ents[0], indent=2, ensure_ascii=False)[:1500])

# Links
links = [len(e.get("_linked_terms") or []) for e in ents]
terms = {e["_term"] for e in ents}

# (source, target) pairs, one per link
link_pairs = [(e["_term"], t) for e in ents for t in (e.get("_linked_terms") or [])]
print("\n--- Links ---")
print("Total links:", len(link_pairs))
print("Articles with >=1 link:", sum(l > 0 for l in links))
print("Links pointing to an existing article:", sum(t in terms for _, t in link_pairs), "/", len(link_pairs))

# Text lengths (decides which articles are worth cognify)
lens = [len(e.get("_text") or "") for e in ents]
print("\n--- Text length ---")
print("Median:", st.median(lens), "| > 300 chars:", sum(l > 300 for l in lens))


# All categories with counts
with open(out / "categories.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["category", "n_articles"])
    w.writerows(cats.most_common())

# All articles: name, categories, number of links, text length, url
with open(out / "articles.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["term", "categories", "n_links", "text_length", "url"])
    for e in ents:
        w.writerow([e["_term"], "; ".join(e.get("_categories") or []),
                    len(e.get("_linked_terms") or []), len(e.get("_text") or ""), e.get("_url")])

# All links: source -> target, with flag if target has its own article
with open(out / "links.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["source", "target", "target_exists"])
    for s, t in link_pairs:
        w.writerow([s, t, t in terms])

print(f"\nFiles written to {out.resolve()}")