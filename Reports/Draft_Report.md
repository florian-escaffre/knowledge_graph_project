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


The script explore_data_v2.py generates a HTML report with four tabs: categories → articles (multi-category and isolated articles flagged), multi-category articles, isolated articles, and link counts between categories.

**Categories**
- 81 entries: the 80 categories + "(none)".
- Names mix French and English, and some overlap or duplicate each other

**Multi-category articles (631)**
- 586 articles have 2 categories, 45 have 3.
  
These suggest categories to merge or to arrange hierarchically.

**Isolated articles**
- No incoming or outgoing link to another article of the corpus.

**Links between categories**
- 916 category pairs have at least 1 link; 221 have ≥ 5 and 30 have ≥ 20.

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

### Use of Cognee to build knowledge graphs

**Structured-output failures and timeouts**. Without an explicit BAML configuration, the local LLM (Llama 3.1 8B via Ollama) often returned output that did not match the expected schema. Cognee logged warnings and retried the call, and the accumulated retries eventually ended in a timeout. Explicitly configuring BAML to use the local Ollama endpoint (BAML_LLM_PROVIDER, BAML_LLM_MODEL, BAML_LLM_ENDPOINT, BAML_LLM_API_KEY in .env) resolved this.

**Missing node descriptions**. Once extraction completed, some graph nodes still had null descriptions. Cognee’s default summary mode appears to run a separate summarization step (a second LLM call), which likely dropped them : the graph ended up with 0 entities. Setting summary_method="from_extraction" reuses the description generated during graph extraction, in a single LLM call per document, and fixed the issue.
