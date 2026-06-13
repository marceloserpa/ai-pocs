from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from langchain_classic.memory import ConversationSummaryMemory

llm = LlamaCpp(
    model_path="./models/Phi-3-mini-4k-instruct-fp16.gguf",
    n_gpu_layers=-1,
    max_tokens=500,
    n_ctx=2048,
    seed=42,
    verbose=False
)

template = """<s><|user|>Current conversation:{chat_history}
{input_prompt}<|end|>
<|assistant|>"""

prompt = PromptTemplate(
    template=template,
    input_variables=["input_prompt", "chat_history"]
)

# setup memory
summary_prompt_template = """<s><|user|>Summarize the conversations and update
    with the new lines.
    Current summary:
    {summary}
    new lines of conversation:
    {new_lines}
    New summary:<|end|>
    <|assistant|>"""
summary_prompt = PromptTemplate(
    input_variables=["new_lines", "summary"],
    template=summary_prompt_template
)
memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    prompt=summary_prompt
)
# Chain the LLM, prompt, and memory together
llm_chain = LLMChain(
    prompt=prompt,
    llm=llm,
    memory=memory
)

print(llm_chain.invoke({"input_prompt": "Hi! My name is Marcelo. What is 1 + 1?"}))
print("\n\n\n")

print(llm_chain.invoke({"input_prompt": "What is 1 - 1?"}))
print("\n\n\n")

print(llm_chain.invoke({"input_prompt": "What is PHI in math?"}))
print("\n\n\n")

print(llm_chain.invoke({"input_prompt": "What is mean in math?"}))
print("\n\n\n")

print(llm_chain.invoke({"input_prompt": "What is my name?"}))
print("\n\n\n")

print(memory.load_memory_variables({}))
