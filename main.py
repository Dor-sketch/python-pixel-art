"""
This is the main file for the PixelArt project.
It is responsible for creating the PixelEditor and BoardGUI objects.
"""

import sys
import os
from PixelEditor import PixelEditor
from BoardGUI import BoardGUI


if __name__ == "__main__":
    # check for a picture in the command line arguments
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    # check for .png files in the current directory
    for file in os.listdir():
        if file.endswith(".png"):
            image_path = file
            break
    if not image_path or not os.path.isfile(image_path):
        print("No image found - starting with a pop-up window.")
    editor = PixelEditor(image_path)
    board_gui = BoardGUI(editor)
