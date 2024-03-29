"""
This is the main file for the PixelArt project.
It is responsible for creating the PixelEditor and BoardGUI objects.
"""

import sys
import os
from pixel_editor import PixelEditor
from board_gui import BoardGUI
from custom_toolbar import CustomToolbar
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    # check for a picture in the command line arguments
    IMAGE_PATH = None
    if len(sys.argv) > 1:
        IMAGE_PATH = sys.argv[1]
    # check for .png files in the current directory
    if not IMAGE_PATH:
        for file in os.listdir("."):
            if file.endswith(".png"):
                IMAGE_PATH = file
                break

    if not IMAGE_PATH or not os.path.isfile(IMAGE_PATH):
        print("No image found - starting with a pop-up window.")
    app = QApplication(sys.argv)
    image_editor = PixelEditor(image_path=IMAGE_PATH)
    main_window = BoardGUI(image_editor)
    toolbar = CustomToolbar(main_window.canvas, main_window, main_window)
    main_window.layout.addWidget(toolbar)
    main_window.show()
    sys.exit(app.exec_())
