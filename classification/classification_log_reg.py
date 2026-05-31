from datasets import load_dataset
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression

data = load_dataset("rotten_tomatoes")
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

train_embeddings = model.encode(data["train"]["text"], show_progress_bar=True)
test_embeddings = model.encode(data["test"]["text"], show_progress_bar=True)

# Train a logistic regression on our train embeddings
clf = LogisticRegression(random_state=42)
clf.fit(train_embeddings, data["train"]["label"])


def evaluate_performance(y_true, y_pred):
    """Create and print the classification report"""
    performance = classification_report(
        y_true, y_pred,
        target_names=["Negative Review", "Positive Review"]
    )
    print(performance)

# Predict previously unseen instances
y_pred = clf.predict(test_embeddings)
evaluate_performance(data["test"]["label"], y_pred)

"""
Batches: 100%|████████████████████████████████████████████████████████████████████| 267/267 [00:11<00:00, 23.86it/s]
Batches: 100%|██████████████████████████████████████████████████████████████████████| 34/34 [00:01<00:00, 25.25it/s]
                 precision    recall  f1-score   support

Negative Review       0.85      0.86      0.85       533
Positive Review       0.86      0.85      0.85       533

       accuracy                           0.85      1066
      macro avg       0.85      0.85      0.85      1066
   weighted avg       0.85      0.85      0.85      1066

"""