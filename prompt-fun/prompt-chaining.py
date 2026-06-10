from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cpu",
    torch_dtype="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")


from transformers import pipeline

# Create a pipeline
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,
    max_new_tokens=500,
    do_sample=False
)

product_prompt = [{"role": "user", "content": "Create a name and slogan for a chatbot that leverages LLMs."}]
outputs = generator(product_prompt)
product_description = outputs[0]["generated_text"]
print(product_description)

sales_prompt = [{"role": "user", "content": f"Generate a very short sales pitch for the following product: '{product_description}'"}]
outputs = generator(sales_prompt)
sales_pitch = outputs[0]["generated_text"]
print(sales_pitch)