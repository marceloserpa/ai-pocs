import torch
import numpy as np
import matplotlib.pyplot as plt

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

text_embedding = model.get_text_features(**inputs)
processed_image = clip_processor(
    text=None, images=image, return_tensors="pt"
)["pixel_values"]

# Prepare image for visualization
img = processed_image.squeeze(0)
img = img.permute(*torch.arange(img.ndim - 1, -1, -1))
img = np.einsum("ijk->jik", img)

# Visualize preprocessed image
plt.imshow(img)
plt.axis("off")

image_embedding = model.get_image_features(processed_image)

# Normalize the embeddings
text_embedding /= text_embedding.norm(dim=-1, keepdim=True)
image_embedding /= image_embedding.norm(dim=-1, keepdim=True)


# Calculate their similarity
text_embedding = text_embedding.detach().cpu().numpy()
image_embedding = image_embedding.detach().cpu().numpy()
score = np.dot(text_embedding, image_embedding.T)
print(score)