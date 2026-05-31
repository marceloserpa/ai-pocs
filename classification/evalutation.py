import numpy as np

from datasets import load_dataset
from transformers import pipeline
from tqdm import tqdm
from transformers.pipelines.pt_utils import KeyDataset
from sklearn.metrics import classification_report


data = load_dataset("rotten_tomatoes")
model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
pipe = pipeline(
    model=model_path,
    tokenizer=model_path,
    return_all_scores=True,
    device="cpu:0"
)

def run_inference(data):
    y_pred = []
    for output in tqdm(pipe(KeyDataset(data["test"], "text")), total=len(data["test"])):
        negative_score = output[0]["score"]
        positive_score = output[2]["score"]
        assignment = np.argmax([negative_score, positive_score])
        y_pred.append(assignment)
    return y_pred

def evaluate_performance(y_true, y_pred):
    """Create and print the classification report"""
    performance = classification_report(
        y_true, y_pred,
        target_names=["Negative Review", "Positive Review"]
    )
    print(performance)

y_pred = run_inference(data)
evaluate_performance(data["test"]["label"], y_pred)

"""
  warnings.warn(
100%|███████████████████████████████████████████████████████████████████████████| 1066/1066 [00:28<00:00, 37.33it/s]
                 precision    recall  f1-score   support

Negative Review       0.76      0.88      0.81       533
Positive Review       0.86      0.72      0.78       533

       accuracy                           0.80      1066
      macro avg       0.81      0.80      0.80      1066
   weighted avg       0.81      0.80      0.80      1066


"""