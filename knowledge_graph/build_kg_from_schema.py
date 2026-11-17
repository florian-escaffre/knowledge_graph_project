import asyncio, json, os
from collections import Counter

# Avoid importing s3fs (AWS variables injected by Onyxia)
for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
    os.environ.pop(k, None)

import cognee
from cognee import visualize_graph
from schema import EngipediaGraph

N_ARTICLES = 5

# Minimal test: send the first 5 Engipedia articles to Cognee, build the graph, save an HTML visualization.
data = json.load(open("data/engipedia_fr_store.json", encoding="utf-8"))
ents = list(data["entities"].values())[:N_ARTICLES]


async def main():
    # WARNING: wipes all existing cognee data
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    for e in ents:
        await cognee.add(f"{e['_term']}\n\n{e['_text']}")

    await cognee.cognify(
        graph_model=EngipediaGraph,  # type: ignore[arg-type]
        summary_method="from_extraction",
    )
    await visualize_graph("data/kg/graph_test_schema.html")

    # Check: node types present
    try:
        from cognee.infrastructure.databases.graph import get_graph_engine
        engine = await get_graph_engine()
        nodes, edges = await engine.get_graph_data()
        print("Node types:", Counter(n[1].get("type") for n in nodes))
        print("Nodes:", len(nodes), "| Edges:", len(edges))
    except Exception as exc:
        print("Could not count nodes:", exc)

asyncio.run(main())