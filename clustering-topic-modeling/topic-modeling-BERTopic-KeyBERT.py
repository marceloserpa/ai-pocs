import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.representation import MaximalMarginalRelevance
from copy import deepcopy
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN

def topic_differences(model, original_topics, nr_topics=5):
    """Show the differences in topic representations between two models """
    df = pd.DataFrame(columns=["Topic", "Original", "Updated"])
    for topic in range(nr_topics):
        # Extract top 5 words per topic per model
        og_words = " | ".join(list(zip(*original_topics[topic]))[0][:5])
        new_words = " | ".join(list(zip(*model.get_topic(topic)))[0][:5])
        df.loc[len(df)] = [topic, og_words, new_words]
    return df


# Loading data from Hugging Face
dataset = load_dataset("maartengr/arxiv_nlp")["train"]

abstracts = dataset["Abstracts"]
titles = dataset["Titles"]

embedding_model = SentenceTransformer("thenlper/gte-small")
embeddings = embedding_model.encode(abstracts, show_progress_bar=True)
umap_model = UMAP(
    n_components=5,
    min_dist=0.0,
    metric='cosine', 
    random_state=42
)
reduced_embeddings = umap_model.fit_transform(embeddings)

hdbscan_model = HDBSCAN(min_cluster_size=50, 
    metric="euclidean", 
    cluster_selection_method="eom"
).fit(reduced_embeddings)

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    verbose=True
).fit(abstracts, embeddings)

original_topics = deepcopy(topic_model.topic_representations_)

representation_model = KeyBERTInspired()
topic_model.update_topics(abstracts, representation_model=representation_model)
df = topic_differences(topic_model, original_topics)
print(df.to_string(index=False))

print("\n\n")
representation_model = MaximalMarginalRelevance(diversity=0.2)
topic_model.update_topics(abstracts, representation_model=representation_model)

# interesting observation is the MMR avoid to return redundant words. 
# In KeyBERTInspired many variation of summary appers avoing other words to be ranked
df2 = topic_differences(topic_model, original_topics)
print(df2.to_string(index=False))