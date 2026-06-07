import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from bertopic import BERTopic
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN


# Loading data from Hugging Face
dataset = load_dataset("maartengr/arxiv_nlp")["train"]

abstracts = dataset["Abstracts"]
titles = dataset["Titles"]

embedding_model = SentenceTransformer("thenlper/gte-small")
embeddings = embedding_model.encode(abstracts, show_progress_bar=True)

# We reduce the input embeddings from 384 dimensions to 5 dimensions
umap_model = UMAP(
    n_components=5, # define the shape of the lower dimensional space. Work well 5-10
    min_dist=0.0, # minimal distance between embeddings
    metric='cosine', # 
    random_state=42
)

reduced_embeddings = umap_model.fit_transform(embeddings)

# We fit the model and extract the clusters
hdbscan_model = HDBSCAN(min_cluster_size=50, 
    metric="euclidean", 
    cluster_selection_method="eom"
).fit(reduced_embeddings)

# Train our model with our previously defined models
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    verbose=True
).fit(abstracts, embeddings)


# to adapt the vizualition
#topic_model.visualize_barchart()
#topic_model.visualize_heatmap(n_clusters=30)
#topic_model.visualize_hierarchy()

print(topic_model.get_topic_info())

# notes:
#  the topic with prefix -1 contains all outliers

print(topic_model.find_topics("topic modeling"))

# Visualize topics and documents
fig = topic_model.visualize_documents(
    titles,
    reduced_embeddings=reduced_embeddings,
    width=1200,
    hide_annotations=True
)
# Update fonts of legend for easier visualization
fig.update_layout(font=dict(size=16))



fig.show()