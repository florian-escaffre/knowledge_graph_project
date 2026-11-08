"""Cognee test on the key Quality articles (GMF, DRG, PIMOF...).

Builds a knowledge graph from 10 related Quality articles, saves a
visualization, then asks 3 questions to the graph.

Run:  python knowledge_graph/quality_test.py
"""
import asyncio
import json

import cognee
from cognee import SearchType, visualize_graph

# The 10 Quality articles linked to Ayhan's example (GMF <-> DRG)
TERMS = ["GMF", "DRG", "PIMOF", "IRIS", "NITG", "Cas pour mille"]

QUESTIONS = [
    "Qu'est-ce que le GMF ?",
    "Quel est le lien entre la DRG et le GMF ?",
    "Quelle est la différence entre le PIMOF et le GMF ?",
]

data = json.load(open("data/engipedia_fr_store.json", encoding="utf-8"))
articles = {a["_term"]: a for a in data["entities"].values()}


def to_text(a):
    """Article -> text with its title, acronym meaning and linked terms."""
    lines = [f"Terme : {a['_term']}"]
    if a["_acro_definition"]:
        lines.append(f"Signification : {a['_acro_definition']}")
    if a["_linked_terms"]:
        lines.append("Termes liés : " + ", ".join(a["_linked_terms"]))
    lines.append("")
    lines.append(a["_text"])
    return "\n".join(lines)


async def main():
    # 1. Start from an empty memory
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    # 2. Add the articles
    for t in TERMS:
        if t not in articles:
            print("NOT FOUND:", t)
            continue
        await cognee.add(to_text(articles[t]), dataset_name="quality")
        print("Added:", t)

    # 3. Build the knowledge graph (the AI reads the texts)
    await cognee.cognify(datasets=["quality"])

    # 4. Save the picture of the graph
    await visualize_graph("data/kg/graph_quality.html")

    # 5. Ask questions to the graph
    for q in QUESTIONS:
        result = await cognee.search(query_text=q,
                                     query_type=SearchType.GRAPH_COMPLETION)
        print("\n" + "=" * 70)
        print("QUESTION:", q)
        print("ANSWER:", result)


asyncio.run(main())