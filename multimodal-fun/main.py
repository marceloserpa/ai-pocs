from urllib.request import urlopen
from PIL import Image

from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel

puppy_path = "https://raw.githubusercontent.com/HandsOnLLM/Hands-On-Large-Language-Models/main/chapter09/images/puppy.png"
image = Image.open(urlopen(puppy_path)).convert("RGB")
caption = "a puppy playing in the snow"

model_id = "openai/clip-vit-base-patch32"
clip_tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
clip_processor = CLIPProcessor.from_pretrained(model_id)

model = CLIPModel.from_pretrained(model_id)

inputs = clip_tokenizer(caption, return_tensors="pt")
print(inputs)

print(clip_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0]))