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
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider, TextBox
import matplotlib.colors as mcolors
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


class ImageEditor:
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
        index = int(label.split(" ")[-1]) - 1
        self.paint_color = self.color_palette[index]

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

    def save_image(self, file_name):
        """
        Save the image as a png file.
        """
        file_name = (
            file_name if file_name else datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        )
        self.image.save(file_name, "PNG")

    def save_transparent_png(self, event=None):
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
        file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
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


class BoardGUI:
    """
    Class to represent the GUI for the image editor.
    """

    def __init__(self, image_editor):
        self.is_slider_adjusting = False
        self.image_editor = image_editor
        self.fig, self.ax = plt.subplots()

        self.fig.patch.set_facecolor("lightyellow")
        plt.subplots_adjust(left=0.3)
        self.display_image()
        self.add_widgets()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        plt.show()

    def display_image(self):
        """
        Display the image on the GUI.
        """
        self.ax.imshow(self.image_editor.image)
        self.ax.set_title("Pixel Art Editor")
        self.ax.figure.canvas.draw()

    def add_widgets(self):
        """
        Add the widgets to the GUI.
        """
        button_width = 0.2
        button_height = 0.05
        start_x = 0.05
        save_button_y = 0.8
        undo_button_y = 0.7
        slider_y = 0.5

        color_num_button_y = 0
        color_palette_y = 0 + button_height

        # Save Button
        ax_save = plt.axes(
            [start_x, save_button_y, button_width / 2, button_height])
        self.btn_save = Button(ax_save, "Save")
        self.btn_save.on_clicked(self.image_editor.save_image)

        # Save Transparent Button
        ax_save_transparent = plt.axes(
            [
                start_x + (button_width / 2),
                save_button_y,
                button_width / 2,
                button_height,
            ]
        )
        self.btn_save_transparent = Button(ax_save_transparent, "Transparent")
        self.btn_save_transparent.on_clicked(
            self.image_editor.save_transparent_png)

        # Undo Button
        ax_undo = plt.axes(
            [start_x, undo_button_y, button_width, button_height])
        self.btn_undo = Button(ax_undo, "Undo")
        self.btn_undo.on_clicked(self.undo)

        # Slider for Pixel Size
        ax_pixel_size_slider = plt.axes(
            [start_x, slider_y, button_width, button_height]
        )
        self.pixel_size_slider = Slider(
            ax_pixel_size_slider,
            "Pixel Size",
            valmin=1,
            valmax=20,
            valinit=self.image_editor.pixel_size,
        )
        self.pixel_size_slider.on_changed(self.on_slider_change)
        self.fig.canvas.mpl_connect(
            "button_release_event", self.on_slider_released)

        # Increase/Decrease Pixel Size Buttons
        ax_decrease_pixel_size = plt.axes(
            [start_x, slider_y - button_height, button_width / 2, button_height]
        )
        self.btn_decrease_pixel_size = Button(ax_decrease_pixel_size, "-")
        self.btn_decrease_pixel_size.on_clicked(self.decrease_pixel_size)

        ax_increase_pixel_size = plt.axes(
            [
                start_x + button_width / 2,
                slider_y - button_height,
                button_width / 2,
                button_height,
            ]
        )
        self.btn_increase_pixel_size = Button(ax_increase_pixel_size, "+")
        self.btn_increase_pixel_size.on_clicked(self.increase_pixel_size)

        # Num Colors Button
        ax_num_colors = plt.axes(
            [start_x, color_num_button_y, button_width, button_height]
        )
        self.btn_num_colors = Button(
            ax_num_colors, f"Colors: {self.image_editor.num_colors}"
        )
        self.btn_num_colors.on_clicked(self.change_num_colors)

        # Color Palette
        normalized_color_palette = [
            (r / 255, g / 255, b / 255) for r, g, b in self.image_editor.color_palette
        ]
        ax_color = plt.axes(
            [
                start_x,
                color_palette_y,
                button_width,
                button_height * len(normalized_color_palette),
            ]
        )
        color_labels = [
            f"Color {i+1}" for i in range(len(normalized_color_palette))]
        self.radio_color = RadioButtons(ax_color, color_labels)
        for i, label in enumerate(self.radio_color.labels):
            color = normalized_color_palette[i]
            hex_color = mcolors.to_hex(color)
            label.set_color(hex_color)
        self.radio_color.on_clicked(self.image_editor.change_color)

        ax_exit = plt.axes([start_x, 0.9, button_width, button_height])
        self.btn_exit = Button(ax_exit, "Exit")
        self.btn_exit.on_clicked(self.exit)

    def exit(self, event):
        """
        Called when the exit button is clicked.
        """
        plt.close()

    def undo(self, event):
        """
        Called when the undo button is clicked.
        """
        self.image_editor.undo()
        self.pixel_size_slider.set_val(self.image_editor.pixel_size)
        self.display_image()

    def change_num_colors(self, event):
        """
        Called when the num colors button is clicked.
        """
        def submit(text):
            num_colors = int(text)
            self.image_editor.change_num_colors(num_colors)
            self.pixel_size_slider.set_val(self.image_editor.pixel_size)
            self.display_image()
            plt.close()

        small_fig = plt.figure()
        dialog_box = small_fig.add_subplot()
        text_box = TextBox(dialog_box, "Enter number of colors: ")
        text_box.on_submit(submit)
        plt.show()

    def on_slider_change(self, event):
        """
        Called whenever the slider value changes
        """
        self.is_slider_adjusting = True
        self.temp_pixel_size = int(event)

    def increase_pixel_size(self, event):
        """
        Called when the increase pixel size button is clicked
        """
        self.image_editor.change_pixel_size(self.image_editor.pixel_size + 1)
        self.pixel_size_slider.set_val(self.image_editor.pixel_size)
        self.display_image()

    def decrease_pixel_size(self, event):
        """
        Called when the decrease pixel size button is clicked
        """
        self.image_editor.change_pixel_size(self.image_editor.pixel_size - 1)
        self.pixel_size_slider.set_val(self.image_editor.pixel_size)
        self.display_image()

    def on_slider_released(self, event):
        """
        Called when mouse is released from the slider
        """
        if self.is_slider_adjusting:
            self.image_editor.change_pixel_size(self.temp_pixel_size)
            self.is_slider_adjusting = False
            self.display_image()

    def on_click(self, event):
        """
        Called when the mouse is clicked on the image
        """
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(event.ydata)
            x = min(
                x // self.image_editor.pixel_size * self.image_editor.pixel_size,
                self.image_editor.image.width - self.image_editor.pixel_size,
            )
            y = min(
                y // self.image_editor.pixel_size * self.image_editor.pixel_size,
                self.image_editor.image.height - self.image_editor.pixel_size,
            )
            self.image_editor.paint_pixel(x, y)
            self.display_image()


image_editor = ImageEditor()
board_gui = BoardGUI(image_editor)
