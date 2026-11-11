# Knowledge Graph & GraphRAG – Engipedia (Renault Group)

Final-year project of the Master Smart Data Science at ENSAI, carried out in partnership with Renault Group (academic year 2026-2027).

**Authors:** Florian Escaffre, Yasira Zafar

## Goal

Build a **knowledge graph** from Renault's internal technical articles, then exploit it with a **GraphRAG** approach (Retrieval-Augmented Generation built on top of the graph) to query this knowledge.

## Data

The dataset is a collection of **Engipedia** articles (Renault's internal wiki), provided as a JSON file.

> **The data is not included in this repo for confidentiality reasons.** The `data/` folder is ignored by git.

## Repository structure

```
.
├── data/                       # Dataset (not versioned), to be added locally
    ├── engipedia.json              # Original dataset
    ├── exploration/                # Results of the EDA
    └── knowledge_graph/            # Graphs made from the dataset
├── data_processing_scripts/    # Exploratory analysis and data preparation (for now only exploratory data analysis to understand better the dataset)
├── knowledge_graph/            # Scripts used to build a graph with cognee (for now, only contains a test of cognee usage)
├── Reports/                    
    └── Draft Report                # Draft of the report, with steps of work and reflexions
├── .env.example                # Configuration template
├── requirements.txt            # Python dependencies
└── README.md
```

## Installation and usage

### Prerequisites

- Python 3.12.5
- [Ollama](https://ollama.com), running locally (LLM and embeddings are served by Ollama, no external API is used)

### 1. Python environment

```bash
git clone <repo-url>
cd knowledge_graph_project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Ollama

Install Ollama (Linux):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

On macOS and Windows, use the installer from [ollama.com](https://ollama.com).

Check that it is running:

```bash
ollama --version
systemctl status ollama          # should be "active (running)"
curl http://localhost:11434      # should answer "Ollama is running"
```

If the service is not running:

```bash
sudo systemctl enable --now ollama
```

Pull the two models used by the project:

```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text:latest
```

### 3. Configuration

```bash
cp .env.example .env
```

The default `.env` points cognee to the local Ollama server:

```dotenv
# Use BAML for structured outputs  
STRUCTURED_OUTPUT_FRAMEWORK="BAML"  

# LLM — Ollama
LLM_PROVIDER="ollama"
LLM_MODEL="llama3.1:8b"
LLM_ENDPOINT="http://localhost:11434"
LLM_API_KEY="ollama"

# Embeddings — Ollama
EMBEDDING_PROVIDER="ollama"
EMBEDDING_MODEL="nomic-embed-text:latest"
EMBEDDING_ENDPOINT="http://localhost:11434/api/embed"
EMBEDDING_DIMENSIONS="768"
HUGGINGFACE_TOKENIZER="nomic-ai/nomic-embed-text-v1.5"

# BAML Configuration
BAML_LLM_PROVIDER="ollama"  
BAML_LLM_MODEL="llama3.1:8b"  
BAML_LLM_ENDPOINT="http://localhost:11434/v1"  
BAML_LLM_API_KEY="ollama"

COGNEE_SKIP_CONNECTION_TEST=true
```

`LLM_API_KEY="ollama"` is a dummy value required by cognee: Ollama does not need a real key.

### 4. Data

Place the JSON dataset file in `data/`.

### 5. Run the scripts

To understand better the data, and make a first use of cognee

```bash
python data_processing_scripts/explore_data.py
python knowledge_graph/test.py
```
