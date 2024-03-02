import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider, TextBox
import matplotlib.colors as mcolors
from PIL import Image
import numpy as np


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
        self.btn_save_transparent = Button(ax_save_transparent, "Cooler")
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

        ax_crop_background = plt.axes(
            [start_x, 0.6, button_width, button_height])
        self.btn_crop_background = Button(
            ax_crop_background, "Crop Background")
        self.btn_crop_background.on_clicked(self.image_editor.crop_background)

        # Adjust the 'bottom' value to ensure the button does not overlap with other widgets
        ax_create_gif = plt.axes([start_x, 0.4, button_width, button_height])
        self.btn_create_gif = Button(ax_create_gif, "Create GIF")
        self.btn_create_gif.on_clicked(self.create_GIF)

        # add button to display the grid
        ax_display_grid = plt.axes([start_x, 0.35, button_width, button_height])
        self.btn_display_grid = Button(ax_display_grid, "Display Grid")
        self.btn_display_grid.on_clicked(self.turn_on_grid)

    def turn_on_grid(self, event):
        """
        Display the grid on the image.
        """
        # check if the grid is already displayed - if so turn it off
        if self.ax.xaxis.get_visible():
            self.ax.xaxis.set_visible(False)
            self.ax.yaxis.set_visible(False)
        else:
            self.ax.xaxis.set_visible(True)
            self.ax.yaxis.set_visible(True)
            self.change_pixel_size(self.image_editor.pixel_size)

        self.fig.canvas.draw()

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


    def change_pixel_size(self, new_pixel_size):
        """
        Change the number of ticks on the axes when the pixel size changes.
        """
        # Calculate the new ticks
        all_ticks = np.arange(0, max(self.ax.get_xlim()[1], self.ax.get_ylim()[1]), new_pixel_size)
        label_ticks = all_ticks[::len(all_ticks)//5]  # Label every 1/5 of the board

        # Set the new ticks
        self.ax.set_xticks(all_ticks, minor=True)
        self.ax.set_yticks(all_ticks, minor=True)

        # Set the new labels
        self.ax.set_xticks(label_ticks)
        self.ax.set_yticks(label_ticks)

        # Set the labels to be the 1D count of pixels until the current tick
        self.ax.set_xticklabels([str(int(tick / new_pixel_size)) for tick in label_ticks])
        self.ax.set_yticklabels([len(all_ticks) - 1 - int(tick / new_pixel_size) for tick in label_ticks])

        # Enable the grid
        self.ax.grid(True, which='both')

        # Redraw the canvas
        self.fig.canvas.draw()

    def increase_pixel_size(self, event):
        """
        Called when the increase pixel size button is clicked
        """
        self.image_editor.change_pixel_size(self.image_editor.pixel_size + 1)
        self.pixel_size_slider.set_val(self.image_editor.pixel_size)
        # update the axes accordingly - aka the number of pixels
        self.change_pixel_size(self.image_editor.pixel_size)

        self.display_image()

    def decrease_pixel_size(self, event):
        """
        Called when the decrease pixel size button is clicked
        """
        if self.image_editor.pixel_size > 1:
            self.image_editor.change_pixel_size(self.image_editor.pixel_size - 1)
            self.pixel_size_slider.set_val(self.image_editor.pixel_size)
            # update the axes accordingly - aka the number of pixels
            self.change_pixel_size(self.image_editor.pixel_size)
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


    def create_GIF(self, event):
        """
        Save the state of the GUI as an image at each step and create a GIF.
        """
        images = []
        for i in range(12):
            # Save the current state of the GUI as an image
            self.fig.canvas.draw()
            image = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype='uint8')
            image  = image.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
            images.append(Image.fromarray(image))

            self.increase_pixel_size(None)

        for _ in range(3):
            # create a pause in the GIF
            images.append(Image.fromarray(image))

        for i in range(17):
            # Save the current state of the GUI as an image
            self.fig.canvas.draw()
            image = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype='uint8')
            image  = image.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
            images.append(Image.fromarray(image))

            self.decrease_pixel_size(None)

        for _ in range(3):
            images.append(Image.fromarray(image))

        # Convert the list of images into a GIF
        images[0].save("record.gif", save_all=True, append_images=images[1:], loop=0, duration=250)
        plt.close()
        print("GIF created")