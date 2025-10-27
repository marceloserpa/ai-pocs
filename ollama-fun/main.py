from ollama import Client

client = Client(host='http://localhost:11434')

response = client.chat(
    model="qwen3:8b",
    messages=[
        {"role": "user", "content": "Summarize the theory of evolution. /think"}
    ]
)

print(response["message"]["content"])