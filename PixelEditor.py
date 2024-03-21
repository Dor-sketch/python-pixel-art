"""
This program allows the user to create pixel art from an image.
The user can select an image, and then use the slider to change the pixel size.
The user can also select the number of colors to use in the image.
The user can then click on the image to paint the pixels.
The user can also save the image as a png file.
"""

import copy
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from PIL import Image


def save_history_before_action(method):
    """
    Decorator to save the current state of the image before an action is performed.
    """

    def wrapper(self, *args, **kwargs):
        if len(self.history) > 10:
            self.history.pop(0)
        self.save_to_history()  # Save current state before action
        return method(self, *args, **kwargs)

    return wrapper


class PixelEditor:
    """
    Class to represent the image editor.
    """

    def __init__(self, image_path=None, pixel_size=6, num_colors=4):
        self.pixel_size = pixel_size
        self.num_colors = num_colors
        self.image_path = image_path if image_path else self.load_image()
        self.original_image = Image.open(self.image_path)
        self.quantized_image = self.original_image.quantize(colors=num_colors)
        self.color_palette = [
            tuple(self.quantized_image.getpalette()[i: i + 3])
            for i in range(0, num_colors * 3, 3)
        ]
        self.image = self.pixelate_image(self.image_path, pixel_size)
        self.history = []
        self.paint_color = self.color_palette[0]

    def reset_image(self):
        """
        Reset the image to the original image.
        """
        temp = self.image
        self.image = self.original_image
        self.original_image = temp
        self.history = []


    @save_history_before_action
    def change_num_colors(self, num_colors):
        """
        Change the number of colors in the image.
        """
        self.num_colors = num_colors
        self.image = self.pixelate_image(self.image_path, self.pixel_size)
        # reset the color palette buttons
        self.color_palette = self.calculate_new_palette(self.num_colors)

    def change_color(self, label):
        """
        Change the color of the paint brush.
        """
        # index = int(label.split(" ")[-1]) - 1
        self.paint_color = self.color_palette[label]

    def load_image(self):
        """
        Load an image from the user's computer.
        """
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename(title="Select Image")

    def save_to_history(self):
        """
        Save the current state of the image to the history.
        """
        self.history.append(
            [copy.deepcopy(self.image), self.pixel_size, self.num_colors]
        )

    def pixelate_image(self, image_path, pixel_size):
        """
        Pixelate the image.
        """
        image = Image.open(image_path)
        image = image.resize(
            (image.size[0] // pixel_size,
             image.size[1] // pixel_size), Image.NEAREST
        )
        if self.num_colors:
            image = image.convert(
                "P", palette=Image.ADAPTIVE, colors=self.num_colors)
        return image.resize(
            (image.size[0] * pixel_size, image.size[1]
             * pixel_size), Image.NEAREST
        )


    def save_image(self, file_name=None):
        """
        Save the image as a png file.
        """
        file_name = (
            file_name if file_name else datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        )
        self.image.save(file_name, "PNG")

    def save_transparent_png(self, event=None, file_name=None):
        """
        Save the image as a transparent png file.
        """
        image = self.image.convert("RGBA")
        new_data = []
        brightest_color = self.color_palette[0]
        for item in image.getdata():
            if all(abs(item[i] - brightest_color[i]) < 20 for i in range(3)):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        image.putdata(new_data)
        if file_name is None:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        else:
            # check if has .png extension
            if file_name[-4:] != ".png":
                file_name += ".png"
        image.save(file_name, "PNG")





    @save_history_before_action
    def paint_pixel(self, x, y):
        """
        Paint the pixel at the given coordinates.
        """
        for i in range(x, min(x + self.pixel_size, self.image.width)):
            for j in range(y, min(y + self.pixel_size, self.image.height)):
                self.image.putpixel((i, j), self.paint_color)

    def calculate_new_palette(self, new_num_colors):
        """
        Calculate the new color palette when the number of colors is changed.
        """
        # Calculate the new palette
        new_palette = self.quantized_image.getpalette()[: new_num_colors * 3]
        # Convert the palette list into a list of tuples for easier use
        new_palette = [
            tuple(new_palette[i: i + 3]) for i in range(0, len(new_palette), 3)
        ]
        return new_palette

    @save_history_before_action
    def change_pixel_size(self, pixel_size):
        """
        Change the pixel size.
        """
        self.pixel_size = int(pixel_size)
        self.image = self.pixelate_image(self.image_path, self.pixel_size)
        self.color_palette = self.calculate_new_palette(self.num_colors)

    def undo(self):
        """
        Undo the last action.
        """
        if len(self.history) > 0:
            self.image, self.pixel_size, self.num_colors = self.history.pop()
