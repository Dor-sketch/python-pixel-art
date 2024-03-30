import numpy as np
from PIL import Image


def create_mask_with_angle(shape, angle):
    """
    Create a boolean mask with a diagonal at a certain angle.

    :param shape: The shape of the mask (height, width).
    :param angle: The angle of the diagonal in degrees. An angle of 0 degrees will create a diagonal from the top-left to the bottom-right.
    :return: A boolean mask with the specified shape and diagonal angle.
    """
    # Create an array with the indices of each element
    indices = np.indices(shape)

    # Calculate the tangent of the angle
    tan_angle = np.tan(np.radians(angle))

    # Create the mask
    mask = indices[0] >= tan_angle * indices[1]

    return mask


# Open the images
image2 = Image.open('result.png').convert('RGBA')
image1 = Image.open('Bruce_crop.png').convert('RGBA')

# Ensure second image is the same size as the first
image2 = image2.resize(image1.size)

# Convert images to numpy arrays
image1_np = np.array(image1)
image2_np = np.array(image2)

# Create a mask for the diagonal split
# Use the function to create a mask with a diagonal at a 45 degree angle
mask = create_mask_with_angle(image1_np.shape[:2], 35)

# Flip the mask to change the direction of the diagonal
mask = np.fliplr(mask)

# Extend the mask to have the same number of channels as the images
mask = np.stack([mask]*image1_np.shape[2], axis=-1)

# Apply the mask to create the final image
final_image_np = np.where(mask, image1_np, image2_np)

# Convert the final image back to a PIL Image and save it
final_image = Image.fromarray(final_image_np.astype(np.uint8))
final_image.save('final_image.png')
