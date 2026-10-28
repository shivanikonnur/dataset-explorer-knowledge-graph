import os
from collections import Counter

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

st.set_page_config(page_title="DataSet Explorer KG", page_icon="🕸️", layout="wide")
st.title("🕸️ DataSet Explorer: Knowledge Graph")
st.write("Explore dataset metadata, relationships, and task-based recommendations.")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "datasets.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH).fillna("")
    return df

df = load_data()

def build_graph(data):
    graph = nx.DiGraph()
    for _, row in data.iterrows():
        dataset_node = f"Dataset: {row['name']}"
        graph.add_node(dataset_node, node_type="Dataset", label=row["name"])
        for node_type, value, relation in [
            ("Domain", row["domain"], "BELONGS_TO_DOMAIN"),
            ("Task", row["task"], "SUITABLE_FOR_TASK"),
            ("Format", row["file_format"], "AVAILABLE_AS_FORMAT"),
        ]:
            if value:
                related_node = f"{node_type}: {value}"
                graph.add_node(related_node, node_type=node_type, label=value)
                graph.add_edge(dataset_node, related_node, relation=relation)
        for feature in str(row["features"]).split(";"):
            feature = feature.strip()
            if feature:
                feature_node = f"Feature: {feature}"
                graph.add_node(feature_node, node_type="Feature", label=feature)
                graph.add_edge(dataset_node, feature_node, relation="HAS_FEATURE")
    return graph

G = build_graph(df)

with st.sidebar:
    st.header("Find datasets")
    task_options = ["All"] + sorted(df["task"].unique().tolist())
    domain_options = ["All"] + sorted(df["domain"].unique().tolist())
    format_options = ["All"] + sorted(df["file_format"].unique().tolist())
    selected_task = st.selectbox("Machine-learning task", task_options)
    selected_domain = st.selectbox("Domain", domain_options)
    selected_format = st.selectbox("File format", format_options)
    query = st.text_input("Search by name, feature, or description")

filtered = df.copy()
if selected_task != "All":
    filtered = filtered[filtered["task"] == selected_task]
if selected_domain != "All":
    filtered = filtered[filtered["domain"] == selected_domain]
if selected_format != "All":
    filtered = filtered[filtered["file_format"] == selected_format]
if query.strip():
    q = query.strip().lower()
    searchable = filtered[["name", "domain", "task", "file_format", "features", "description"]].astype(str).agg(" ".join, axis=1)
    filtered = filtered[searchable.str.lower().str.contains(q, regex=False)]

tab1, tab2, tab3, tab4 = st.tabs(["Dataset catalogue", "Knowledge graph", "Analytics", "About"])

with tab1:
    st.subheader("Matching datasets")
    st.caption(f"{len(filtered)} dataset(s) match your filters.")
    show = filtered[["name", "domain", "task", "file_format", "features", "description", "url"]].copy()
    st.dataframe(show, use_container_width=True, hide_index=True)
    if not filtered.empty:
        chosen = st.selectbox("View a dataset", filtered["name"].tolist())
        row = filtered[filtered["name"] == chosen].iloc[0]
        st.markdown(f"### {row['name']}")
        st.write(row["description"])
        st.write(f"**Domain:** {row['domain']}  |  **Task:** {row['task']}  |  **Format:** {row['file_format']}")
        st.write(f"**Features:** {row['features'].replace(';', ', ')}")
        st.markdown(f"[Open dataset resource]({row['url']})")

with tab2:
    st.subheader("Knowledge graph visualization")
    st.write("Dataset nodes connect to domain, task, format, and feature nodes.")
    max_nodes = st.slider("Maximum nodes to display", min_value=10, max_value=max(10, min(100, G.number_of_nodes())), value=min(40, max(10, G.number_of_nodes())))
    # Prioritize dataset nodes and their one-hop neighbors for a readable view.
    dataset_nodes = [n for n, d in G.nodes(data=True) if d.get("node_type") == "Dataset"]
    selected_nodes = set(dataset_nodes[:max(10, min(len(dataset_nodes), 10))])
    for node in list(selected_nodes):
        selected_nodes.update(G.successors(node))
    selected_nodes = list(selected_nodes)[:max_nodes]
    H = G.subgraph(selected_nodes).copy()
    fig, ax = plt.subplots(figsize=(14, 8))
    pos = nx.spring_layout(H, seed=17, k=0.8)
    node_colors = []
    for node in H.nodes:
        kind = H.nodes[node].get("node_type")
        node_colors.append({"Dataset": "#8ecae6", "Domain": "#b7e4c7", "Task": "#ffd6a5", "Format": "#cdb4db", "Feature": "#f1fa8c"}.get(kind, "#dddddd"))
    nx.draw_networkx(H, pos, ax=ax, with_labels=True, labels={n: H.nodes[n].get("label", n) for n in H.nodes}, node_color=node_colors, node_size=1250, font_size=7, arrows=True, arrowsize=12, edge_color="#777777")
    ax.set_axis_off()
    st.pyplot(fig, use_container_width=True)
    st.caption("This is a sample catalogue graph. Increase the catalogue size or use the full DSKG RDF data for a larger research-scale graph.")

with tab3:
    st.subheader("Catalogue analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Datasets", len(df))
    c2.metric("Graph nodes", G.number_of_nodes())
    c3.metric("Graph relationships", G.number_of_edges())
    left, right = st.columns(2)
    with left:
        st.write("Datasets by task")
        task_counts = df["task"].value_counts()
        fig1, ax1 = plt.subplots()
        task_counts.plot(kind="bar", ax=ax1)
        ax1.set_xlabel("Task")
        ax1.set_ylabel("Number of datasets")
        ax1.tick_params(axis="x", rotation=35)
        st.pyplot(fig1, use_container_width=True)
    with right:
        st.write("Datasets by domain")
        domain_counts = df["domain"].value_counts()
        fig2, ax2 = plt.subplots()
        domain_counts.plot(kind="bar", ax=ax2)
        ax2.set_xlabel("Domain")
        ax2.set_ylabel("Number of datasets")
        ax2.tick_params(axis="x", rotation=45)
        st.pyplot(fig2, use_container_width=True)
    st.write("Most connected nodes")
    degree_data = sorted(G.degree(), key=lambda item: item[1], reverse=True)[:10]
    st.dataframe(pd.DataFrame(degree_data, columns=["Node", "Degree"]), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Project scope")
    st.markdown("""
**Goal:** make dataset discovery easier by representing dataset metadata as a graph.

**Node types:** Dataset, Domain, Task, Format, Feature.

**Relationship types:** `BELONGS_TO_DOMAIN`, `SUITABLE_FOR_TASK`, `AVAILABLE_AS_FORMAT`, `HAS_FEATURE`.

**Current limitation:** the bundled CSV is a small demonstration catalogue. It is not the original DSKG dump, and its records are intended as starter metadata. Verify resource URLs and metadata before formal submission.

**Possible extensions:** import RDF from the DSKG Zenodo dump, parse RDF using `rdflib`, query SPARQL, add publication and author nodes, and compare graph-based recommendations with keyword search.
""")

st.download_button("Download catalogue CSV", data=df.to_csv(index=False), file_name="datasets.csv", mime="text/csv")
