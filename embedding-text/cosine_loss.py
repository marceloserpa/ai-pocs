from datasets import Dataset, load_dataset
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator

from sentence_transformers import losses, SentenceTransformer
from sentence_transformers.trainer import SentenceTransformerTrainer
from sentence_transformers.training_args import SentenceTransformerTrainingArguments

# Step 1: prepare the dataset 

# Load MNLI dataset from GLUE
# 0 = entailment, 1 = neutral, 2 = contradiction
train_dataset = load_dataset(
    "nyu-mll/glue", "mnli", split="train"
).select(range(50_000))
train_dataset = train_dataset.remove_columns("idx")

# (neutral/contradiction)=0 and (entailment)=1
mapping = {2: 0, 1: 0, 0:1}
train_dataset = Dataset.from_dict({
    "sentence1": train_dataset["premise"],
    "sentence2": train_dataset["hypothesis"],
    "label": [float(mapping[label]) for label in train_dataset["label"]]
})

# Step 2: setup evaluator

# Create an embedding similarity evaluator for stsb
val_sts = load_dataset("nyu-mll/glue", "stsb", split="validation")
evaluator = EmbeddingSimilarityEvaluator(
    sentences1=val_sts["sentence1"],
    sentences2=val_sts["sentence2"],
    scores=[score/5 for score in val_sts["label"]],
    main_similarity="cosine"
)

# Step 3: Define model
embedding_model = SentenceTransformer("bert-base-uncased")

# Step 4: Loss function
train_loss = losses.CosineSimilarityLoss(model=embedding_model)

# Step 5: Define the training arguments
args = SentenceTransformerTrainingArguments(
    output_dir="cosineloss_embedding_model",
    num_train_epochs=1,

    # reduced from 32 to 16 (RTX 3060)
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    
    warmup_steps=100,
    fp16=True,
    eval_steps=100,
    logging_steps=100,
)

# Step 6: Train
trainer = SentenceTransformerTrainer(
    model=embedding_model,
    args=args,
    train_dataset=train_dataset,
    loss=train_loss,
    evaluator=evaluator
)
trainer.train()

print("#### Evaluator #### ")
print(evaluator(embedding_model))