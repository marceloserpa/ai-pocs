from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sentence_transformers import losses
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.training_args import SentenceTransformerTrainingArguments
from sentence_transformers.trainer import SentenceTransformerTrainer

from mteb import MTEB


# Step 1: Load dataset

# Load MNLI dataset from GLUE
# 0 = entailment, 1 = neutral, 2 = contradiction
train_dataset = load_dataset("nyu-mll/glue", "mnli", split="train").select(range(50_000))
train_dataset = train_dataset.remove_columns("idx")

print(train_dataset[2])

# Step 2: Define the base model
embedding_model = SentenceTransformer('bert-base-uncased')

# Cap sequence length to keep activation memory in check on small GPUs.
# 128 tokens is plenty for MNLI/STSB sentence pairs.
embedding_model.max_seq_length = 128

# Step 3: Define loss function

# Define the loss function. In softmax loss, we will also need to explicitly set the number of labels.
train_loss = losses.SoftmaxLoss(
    model=embedding_model,
    sentence_embedding_dimension=embedding_model.get_sentence_embedding_dimension(),
    num_labels=3
)

# Step 4: Create an embedding similarity evaluator for STSB
val_sts = load_dataset("nyu-mll/glue", "stsb", split="validation")
evaluator = EmbeddingSimilarityEvaluator(
    sentences1=val_sts["sentence1"],
    sentences2=val_sts["sentence2"],
    scores=[score/5 for score in val_sts["label"]],
    main_similarity="cosine",
)

# Step 5: Setup and run the train model
args = SentenceTransformerTrainingArguments(
    output_dir="base_embedding_model",
    num_train_epochs=1,

    # limit to 16 since it is running on RXT 3060
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=100,
    fp16=True,
    eval_steps=100,
    logging_steps=100,
)

trainer = SentenceTransformerTrainer(
    model=embedding_model,
    args=args,
    train_dataset=train_dataset,
    loss=train_loss,
    evaluator=evaluator
)
trainer.train()

print(evaluator(embedding_model))

print("#### MTEB Evaluation")

tasks = MTEB.get_tasks(tasks=["Banking77Classification"])
results = MTEB.evaluate(
    embedding_model,
    tasks=tasks,
)

print(results)