import numpy as np
from PIL import Image

# Open the images
image2 = Image.open('bruce2.png').convert('RGBA')
image1 = Image.open('bruce1.png').convert('RGBA')

# Ensure second image is the same size as the first
image2 = image2.resize(image1.size)

# Crop the images
crop_width = 0  # The amount to crop from each side
image1 = image1.crop((crop_width, 0, image1.width - crop_width, image1.height))
image2 = image2.crop((crop_width, 0, image2.width - crop_width, image2.height))

# Convert images to numpy arrays
image1_np = np.array(image1)
image2_np = np.array(image2)

# Concatenate the images along the second axis (side by side)
final_image_np = np.concatenate((image1_np, image2_np), axis=1)

# Convert the final image back to a PIL Image and save it
final_image = Image.fromarray(final_image_np.astype(np.uint8))
final_image.save('bruce3.png')