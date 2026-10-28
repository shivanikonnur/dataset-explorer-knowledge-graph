# DataSet Explorer: Knowledge Graph

A beginner-friendly educational project using Python, NetworkX, Pandas, Matplotlib, and Streamlit.

## Features
- Browse and filter dataset metadata
- Build a directed knowledge graph connecting datasets with domains, tasks, formats, and features
- Visualize graph relationships
- View catalogue charts and graph degree statistics
- Download the CSV catalogue

## Run on macOS (including Apple Silicon)
1. Install Python 3.10+ and VS Code.
2. Open this folder in VS Code.
3. Open Terminal in VS Code and create a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

6. Open the local URL printed in Terminal (usually http://localhost:8501).

## Data model
Each dataset has metadata fields: name, domain, task, format, features, description, and URL. Each dataset becomes a node, connected to domain, task, format, and feature nodes.

## Important
The included CSV is a small starter/demo catalogue. It is not the official DSKG dataset. For a research extension, download the DSKG RDF dump from the official Zenodo record and inspect its license, schema, and size before loading it.
