"""
This module uses the OpenCV library to crop the background of an image.
"""

import os
import sys
import cv2
import numpy as np


class CropBackground:
    """
    This class contains the methods to crop the background of an image.
    """

    def __init__(self, image_path="cover.png", output_path="output.png"):
        """
        The constructor method for the CropBackground class.

        :param image_path: The path to the image file.
        :param output_path: The path to the output file.
        """
        # Ensure image_path is a string
        if not isinstance(image_path, str):
            Warning("The image path must be a string - converting to string")
            image_path = str(image_path)
        self.image_path = image_path
        self.output_path = output_path

    def crop_background(self):
        """
        This method crops the background of an image.
        """

        # Read the image
        image = cv2.imread(self.image_path)
        if image is None:
            raise ValueError(
                f"Could not read image at path: {self.image_path}")

        # crop background using the GrabCut algorithm use advanced OpenCV functions to detect foreground and background
        mask = np.zeros(image.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        # avoid cutting head or dark hair
        # Adjust the rectangle to more accurately encompass the face
        # Adjust the rectangle to more accurately encompass the face
        # Increase start_x and start_y to move the rectangle to the right and up
        # Decrease width and height to make the rectangle smaller
        start_x = 300
        start_y = 300
        width = image.shape[1] - 400
        height = image.shape[0] - 200
        rect = (start_x, start_y, width, height)

        # Initialize the mask as probable background
        mask = np.full(image.shape[:2], cv2.GC_PR_BGD, dtype=np.uint8)

        # Specify a region in the center of the image as probable foreground
        # try to detect figure in the center of the image
        mask[rect[1]:rect[3], rect[0]:rect[2]] = cv2.GC_PR_FGD

        # Apply the GrabCut algorithm
        cv2.grabCut(image, mask, rect, bgd_model,
                    fgd_model, 10, cv2.GC_INIT_WITH_MASK)

        # Create a mask to remove the background
        mask2 = np.where((mask == cv2.GC_FGD) | (
            mask == cv2.GC_PR_FGD), 1, 0).astype('uint8')

        # Apply the mask to the image
        image = image * mask2[:, :, np.newaxis]

        # Save the image
        cv2.imwrite(self.output_path, image)


def main():
    """
    The main function for the CropBackground class.
    """

    # ask for input and output paths
    input_path = input("Enter the path to the image: ")
    # Get the input and output paths from the command line arguments if they exist
    output_path = "output.png"

    # Check if the input path is a file
    if not os.path.isfile(input_path):
        print("Error: The input path is not a file.")
        sys.exit(1)

    print("Cropping the background of the image...")

    # Create an instance of the CropBackground class
    crop_background = CropBackground(input_path, output_path)

    # Crop the background of the image
    crop_background.crop_background()


if __name__ == "__main__":
    main()
