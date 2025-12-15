import torch
import numpy as np
from PIL import Image
import torchvision.transforms as transforms

# Use the SAME image you tested with
IMG_PATH = "test.png" 

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.Grayscale(num_output_channels=1),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

img = Image.open(IMG_PATH)
if img.mode != 'RGB': img = img.convert('RGB')
tensor = transform(img)

# Export to C array
data = tensor.numpy().flatten()

with open("image_data.h", "w") as f:
    f.write(f"// Image: {IMG_PATH}\n")
    f.write("const float test_image[1][32][32] = {\n")
    f.write("\t{\n\t\t")
    for i, val in enumerate(data):
        f.write(f"{val:.6f}, ")
        if (i+1) % 32 == 0: f.write("\n\t\t")
    f.write("\n\t}\n};\n")

print("Generated image_data.h")