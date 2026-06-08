import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from transformers import pipeline
from bertopic import BERTopic
from bertopic.representation import MaximalMarginalRelevance
from bertopic.representation import TextGeneration
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

#original_topics = deepcopy(topic_model.topic_representations_)
original_topics = {
    topic_id: [
        (word, importance_score)
        for word, importance_score in topic_words_and_scores
    ]
    for topic_id, topic_words_and_scores in topic_model.get_topics().items()
}

print("\n\n ====== Using MMR ====== ")

representation_model = MaximalMarginalRelevance(diversity=0.2)
topic_model.update_topics(abstracts, representation_model=representation_model)
df = topic_differences(topic_model, original_topics)
print(df.to_string(index=False))

print("\n\n ====== Using Flan-T5-small ====== ")
prompt = """I have a topic that contains the following documents:
[DOCUMENTS]
The topic is described by the following keywords: '[KEYWORDS]'.
Based on the documents and keywords, what is this topic about?"""
# Update our topic representations using Flan-T5
generator = pipeline("text2text-generation", model="google/flan-t5-small")
representation_model = TextGeneration(generator, prompt=prompt, doc_length=50, tokenizer="whitespace")
topic_model.update_topics(abstracts, representation_model=representation_model)

df2 = topic_differences(topic_model, original_topics)
print(df2.to_string(index=False))

topics = [t for t in topic_model.get_topic_info()["Topic"].tolist() if t != -1][:20]

# Replace visualize_document_datamap with visualize_documents
fig = topic_model.visualize_documents(
    titles,
    topics=topics,
    reduced_embeddings=reduced_embeddings,
    width=1200,
    height=750
)
fig.show()