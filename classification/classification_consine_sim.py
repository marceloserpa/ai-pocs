import numpy as np
from datasets import load_dataset
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

data = load_dataset("rotten_tomatoes")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

train_embeddings = model.encode(data["train"]["text"], show_progress_bar=True)
test_embeddings = model.encode(data["test"]["text"], show_progress_bar=True)
label_embeddings = model.encode(["A negative review", "A positive review"])

def evaluate_performance(y_true, y_pred):
    """Create and print the classification report"""
    performance = classification_report(
        y_true, y_pred,
        target_names=["Negative Review", "Positive Review"]
    )
    print(performance)


sim_matrix = cosine_similarity(test_embeddings, label_embeddings)
y_pred = np.argmax(sim_matrix, axis=1)

evaluate_performance(data["test"]["label"], y_pred)

"""
                 precision    recall  f1-score   support

Negative Review       0.78      0.77      0.78       533
Positive Review       0.77      0.79      0.78       533

       accuracy                           0.78      1066
      macro avg       0.78      0.78      0.78      1066
   weighted avg       0.78      0.78      0.78      1066
"""