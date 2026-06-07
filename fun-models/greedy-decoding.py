import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cpu",
    torch_dtype="auto",
    trust_remote_code=True,
)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,
    max_new_tokens=50,
    do_sample=False,
)

prompt = "The capital of France is"

input_ids = tokenizer(prompt, return_tensors="pt").input_ids
input_ids = input_ids.to("cpu")
model_output = model.model(input_ids)
lm_head_output = model.lm_head(model_output[0])

token_id = lm_head_output[0, -1].argmax(-1)
print(tokenizer.decode(token_id))