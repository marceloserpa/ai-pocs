import numpy as np
import sys
from transformers.pipelines.pt_utils import KeyDataset
from transformers import pipeline

review_text = sys.argv[1]

model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
pipe = pipeline(
    model=model_path,
    tokenizer=model_path,
    return_all_scores=True,
    device="cpu:0"
)

def run_inference(review_text):
    output = pipe(review_text)
    negative_score = output[0][0]["score"]
    positive_score = output[0][2]["score"]

    return np.argmax([negative_score, positive_score])


print(run_inference(review_text))