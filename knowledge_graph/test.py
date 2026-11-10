import asyncio, json, os, re
from collections import Counter
from pathlib import Path

# Avoid importing s3fs (AWS variables injected by Onyxia)
for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
    os.environ.pop(k, None)

import cognee
from cognee import visualize_graph

N_ARTICLES = 150

# --- Extraction prompt: forces a non-null description on every node ---
prompt_file = Path(cognee.__file__).parent / "infrastructure/llm/prompts/generate_graph_prompt.txt"
base = prompt_file.read_text()
base = re.sub(r"\{% if temporal_hints %\}.*?\{% endif %\}", "", base, flags=re.S)  # Jinja block not interpreted by custom_prompt


# Minimal test: send the first 150 Engipedia articles to Cognee, build the graph, save an HTML visualization.
data = json.load(open("data/engipedia_fr_store.json", encoding="utf-8"))
ents = list(data["entities"].values())[:N_ARTICLES]


async def main():
    # WARNING: wipes all existing cognee data
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    for e in ents:
        await cognee.add(f"{e['_term']}\n\n{e['_text']}")

    await cognee.cognify(summary_method="from_extraction") # Reuse extraction output for summaries instead of a separate LLM call
    await visualize_graph("data/kg/graph_test.html")

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