# Project Tracking: Knowledge Graph & GraphRAG – Engipedia (Renault Group)

## 1. Goal

Build a **knowledge graph** (KG) from Renault's internal technical articles, then exploit it with a **GraphRAG** approach (Retrieval-Augmented Generation built on top of the graph) to query this knowledge.

Concretely: create a KG for a RAG agent from a dataset of about 3,400 Engipedia articles.

## 2. Steps

1. **Define a graph schema.**
2. **Extract entities and relations** with NLP and LLM techniques (a priori using Cognee).
3. **Integrate agentic AI** for RAG purposes.
4. **Compare traditional RAG and GraphRAG** (performance, latency, etc.; criteria to be defined).

## 3. Data

- The dataset is a collection of **Engipedia** articles (Renault's internal wiki), provided as a JSON file (`engipedia.json`).

### Exploration

Exploration of the dataset with a Python script (`data_processing_scripts/explore_data.py`): categories, links, text length, etc.

#### Engipedia dataset: key figures

- **3,533 articles**, 80 categories, 4,072 links
- **Categories:** 525 articles have none, 631 have several. Sizes vary widely (median 21 articles, 9 categories above 100, 8 with 5 or fewer).
- **Text:** median 235 characters.
- **Links:** 98 % point to an existing article (73 links to 15 targets without an article). 1,182 articles are isolated, with no incoming or outgoing link.

**Observations so far:**
- The dataset already contains many categories, entities and links between entities.
- This is not enough to make a knowledge graph : need to reorganize the categories, name the links (relationships), complete the relationships... So as to build a proper Knowledge Graph Schema

## 4. Cognee

Cognee is an open framework for building KGs and GraphRAG.

- Used for both KG creation and RAG queries (the AI agent part).
- Can run with a local LLM using Ollama: LLM and embeddings are both served by Ollama, no external API is used (so it's free and local).
- **Main functions:** `.add()`, `.cognify()`, `.visualize_graph()`, `.remember()`, `.improve()`, `.recall()`, `.forget()`, `.search()`.
- **Limitation:** entities and relations are detected automatically by the LLM, but the result is not precise or relevant enough. (Using an LLM to extract the entities and relationships means that the choice of the model and the computing power will directly impact the quality of the result)
- **Improvement:** use a graph model and/or an ontology.

- Cognee build at the same time the vectors, graph and relational databases.

An alternative of Cognee for building the Knowledge graph can be Neo4j : so Why cognee ?
--> seems to be the most used for GraphRAG applications, automatisation of the KG building (implies spending more time on the graphmodel and ontology and refining of the KG), LLM integrations for RAG and Graph queries

### Graph Model vs Ontology

|        | Graph Model                  | Ontology                                                                         |
| ------ | ---------------------------- | -------------------------------------------------------------------------------- |
| Format | Pydantic class               | RDF/OWL file                                                                     |
| When   | During extraction            | After extraction                                                                 |
| Role   | Limits what the LLM produces | Normalises and enriches the KG (hierarchy between entities, normalisation, etc.) |

**Graph model:** defines the structure of the graph, i.e. which types of entities and relationships are allowed. It constrains what the LLM can extract.

**Ontology:** a reference vocabulary of the domain: official entity names and the hierarchy between concepts (e.g. a Clio is a Vehicle). It is used to normalise and enrich the extracted entities.