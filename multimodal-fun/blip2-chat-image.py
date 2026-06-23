from transformers import AutoProcessor, Blip2ForConditionalGeneration
from PIL import Image
from urllib.request import urlopen
import torch

blip_processor = AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
model = Blip2ForConditionalGeneration.from_pretrained(
    "Salesforce/blip2-opt-2.7b",
    torch_dtype=torch.float16
)

device = "cpu"
model.to(device)

car_path = "https://raw.githubusercontent.com/HandsOnLLM/Hands-On-Large-Language-Models/main/chapter09/images/car.png"
image = Image.open(urlopen(car_path)).convert("RGB")

# Chat-like prompting
prompt = """Question: Write down what you see in this picture. 
Answer: A sports car driving on the road at sunset. 
Question: What would it cost me to drive that car? Answer:"""

inputs = blip_processor(image, text=prompt, return_tensors="pt").to(device, torch.float16)
print(inputs["pixel_values"].shape)

# the original image has 520x492, after process 224x224

print(blip_processor.tokenizer)

image = Image.open(urlopen(car_path)).convert("RGB")
inputs = blip_processor(image, return_tensors="pt").to(device, torch.float16)

# Generate image ids to be passed to the decoder (LLM)
generated_ids = model.generate(**inputs, max_new_tokens=30)
    # Generate text from the image ids
generated_text = blip_processor.batch_decode(
    generated_ids, skip_special_tokens=True
)
generated_text = generated_text[0].strip()
print(generated_text)