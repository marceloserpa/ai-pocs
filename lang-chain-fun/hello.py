from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

llm = LlamaCpp(
    model_path="./models/Phi-3-mini-4k-instruct-fp16.gguf",
    n_gpu_layers=-1,
    max_tokens=500,
    n_ctx=2048,
    seed=42,
    verbose=False
)

template = """<s><|user|>
{input_prompt}<|end|>
<|assistant|>"""

prompt = PromptTemplate(
    template=template,
    input_variables=["input_prompt"]
)

basic_chain = prompt | llm

response = basic_chain.invoke({ "input_prompt": "Hi! My name is Marcelo. What is 1 + 1?"})

print(response)