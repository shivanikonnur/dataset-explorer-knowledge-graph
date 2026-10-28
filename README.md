# DataSet Explorer: Knowledge Graph

An interactive dataset discovery system built using Python, NetworkX, Pandas, Matplotlib, and Streamlit. The project represents dataset metadata as a knowledge graph connecting datasets with their domains, machine-learning tasks, file formats, and features.

## Features

- Browse and search dataset metadata.
- Filter datasets by domain, task, and file format.
- Build a directed knowledge graph using NetworkX.
- Visualize relationships between datasets and their metadata.
- Analyze graph structure and dataset distributions.
- Download the dataset catalogue as a CSV file.

## Technology Stack

- **Python** — Core programming language
- **NetworkX** — Knowledge graph creation and analysis
- **Pandas** — Dataset processing and filtering
- **Matplotlib** — Graph visualization and analytics charts
- **Streamlit** — Interactive web dashboard

## Project Structure

```text
dataset-explorer-knowledge-graph/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── datasets.csv
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/shivanikonnur/dataset-explorer-knowledge-graph.git
cd dataset-explorer-knowledge-graph
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## Knowledge Graph Design

The graph represents datasets as nodes connected to metadata nodes.

**Node types:** Dataset, Domain, Task, Format, Feature.

**Relationship types:**
- `BELONGS_TO_DOMAIN`
- `SUITABLE_FOR_TASK`
- `AVAILABLE_AS_FORMAT`
- `HAS_FEATURE`

## Current Scope and Limitations

The current implementation uses a small demonstration dataset catalogue. It is an educational prototype inspired by the Data Set Knowledge Graph (DSKG) concept and does not yet reproduce the complete original DSKG.

## Future Enhancements

- Integrate real DSKG RDF data.
- Add RDF parsing using RDFLib.
- Explore SPARQL queries for graph-based dataset discovery.
- Develop more advanced graph-based recommendation methods.
- Evaluate search quality and recommendation performance.

## References

- [Knowledge Graphs in Python using NetworkX](https://www.youtube.com/watch?v=n7BTWc2C1Eg)
- [NetworkX Knowledge Graph Notebook](https://github.com/bnsreenu/python_for_microscopists/blob/master/354_knowledge_graphs_using_NetworkX.ipynb)
- [Data Set Knowledge Graph (DSKG)](https://github.com/michaelfaerber/data-set-knowledge-graph)
