import numpy as np

from datasets import load_dataset
from transformers import pipeline
from tqdm import tqdm
from transformers.pipelines.pt_utils import KeyDataset
from sklearn.metrics import classification_report


data = load_dataset("rotten_tomatoes")

pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device="cpu"
)

# Preparing data
prompt = "Is the following sentence positive or negative? "
data = data.map(lambda example: {"t5": prompt + example['text']})

def run_inference(data):
    y_pred = []
    for output in tqdm(pipe(KeyDataset(data["test"], "t5")), total=len(data["test"])):
        text = output[0]["generated_text"]
        y_pred.append(0 if text == "negative" else 1)
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
                 precision    recall  f1-score   support

Negative Review       0.83      0.85      0.84       533
Positive Review       0.85      0.83      0.84       533

       accuracy                           0.84      1066
      macro avg       0.84      0.84      0.84      1066
   weighted avg       0.84      0.84      0.84      1066
"""