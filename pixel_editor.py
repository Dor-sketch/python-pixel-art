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
from PIL import Image, UnidentifiedImageError
import os
from PyQt5.QtWidgets import QFileDialog


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
        self.image_path = image_path if image_path else self.load_image(
            init=True)
        self.original_image = None
        try:
            self.image = Image.open(self.image_path)
        except FileNotFoundError:
            raise FileNotFoundError("File not found")
        except UnidentifiedImageError:
            print("Invalid image format")
            raise UnidentifiedImageError("Invalid image format")
        self.color_palette = self.calculate_new_palette(
            self.num_colors, self.original_image)
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
        try:
            color_index = self.color_palette.index(label)
        except ValueError:
            color_index = -1
        if color_index != -1:
            self.paint_color = self.color_palette[color_index]
        else:
            print("Color not found in palette")

    def load_image(self, init=False):
        """
        Load an image from the user's computer.
        """
        print("Select an image file")
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName()
        if not file_path:
            raise FileNotFoundError("No file selected")
        if init:
            return file_path
        self.image_path = file_path
        self.original_image = Image.open(self.image_path)
        self.image = self.pixelate_image(self.image_path, self.pixel_size)
        self.color_palette = self.calculate_new_palette(self.num_colors)
        self.history = []

    def save_to_history(self):
        """
        Save the current state of the image to the history.
        """
        self.history.append(
            [copy.deepcopy(self.image), self.pixel_size, self.num_colors]
        )

    def pixelate_image(self, image_path=None, pixel_size=None):
        """
        Pixelate the image.
        """
        pixel_size = pixel_size if pixel_size else self.pixel_size + 1
        if not image_path:
            image_path = self.image_path
        image = Image.open(image_path)
        image = image.resize(
            (image.size[0] // pixel_size,
             image.size[1] // pixel_size), Image.NEAREST
        )
        if self.num_colors:
            image = image.convert(
                "P", palette=Image.ADAPTIVE, colors=self.num_colors, dither=Image.FLOYDSTEINBERG
            )
        self.pixel_size = pixel_size
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
        # # set pic size based on pixel size
        # self.image = self.image.resize(
        #     (self.image.width // self.pixel_size, self.image.height // self.pixel_size)
        # )
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

    def calculate_new_palette(self, new_num_colors, image=None):
        """
        Calculate the new color palette when the number of colors is changed.
        """
        if not image:
            image = self.image
        # Calculate the new palette
        quantized_image = image.quantize(new_num_colors)
        new_palette = quantized_image.getpalette()[: new_num_colors * 3]
        # Convert the palette list into a list of tuples for easier use
        print(new_palette)
        new_palette = [
            tuple(new_palette[i: i + 3]) for i in range(0, len(new_palette), 3)
        ]
        # if dont have enough colors remove duplicates
        # check for duplicates
        unique_colors = set()
        for color in new_palette:
            unique_colors.add(color)
        new_palette = list(unique_colors)
        print(new_palette)
        print(new_num_colors)
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

    def make_gif(self, file_name, frames=19):
        """
        Create a gif of the image by changing the pixel size,
        and saving the image at each step, then combining the images into a gif.
        """

        for i in range(frames):
            # Save the current state of the GUI as an image
            self.image.save("temp" + str(i) + ".png")
            self.change_pixel_size(self.pixel_size + 1)

        # create a gif from the saved images than delete them
        images_forward = []
        images_reverse = []
        for i in range(frames):
            image = Image.open("temp" + str(i) + ".png")
            images_forward.append(image)
            # Add to the start of the list for reverse sequence
            images_reverse.insert(0, image.copy())

        # Create a longer pause in the GIF at the most pixelated image
        # Increase this number for a longer pause
        pause_images = [images_forward[-1]] * 5

        # Combine forward sequence, pause, and reverse sequence
        images = images_forward + pause_images
        # check for gif directory
        if not os.path.exists("gifs"):
            os.makedirs("gifs")
        file_name = "gifs/" + file_name
        images[0].save(file_name, save_all=True,
                       append_images=images[1:], duration=100, loop=0)
        for i in range(frames):
            os.remove("temp" + str(i) + ".png")

        print("GIF created")
