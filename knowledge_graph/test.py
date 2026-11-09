import asyncio, json, cognee
from cognee import visualize_graph

# Minimal test: send the first 5 Engipedia articles to Cognee, build the graph, save an HTML visualization.
data = json.load(open("data/engipedia_fr_store.json", encoding="utf-8"))
ents = list(data["entities"].values())[:150]

async def main():
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)
    for e in ents:
        await cognee.add(f"{e['_term']}\n\n{e['_text']}")
    await cognee.cognify()
    await visualize_graph("data/kg/graph_test.html")

asyncio.run(main())