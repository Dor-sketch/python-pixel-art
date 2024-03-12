"""
This module contains the BoardGUI class which is used to create the GUI
for the image editor.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider, TextBox
import matplotlib.font_manager
import matplotlib.colors as mcolors
from PIL import Image
import numpy as np

fonts = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext="ttf")


class BoardGUI:
    """
    Class to represent the GUI for the image editor.
    """

    def __init__(self, image_editor):
        self.is_slider_adjusting = False
        self.image_editor = image_editor
        self.fig, self.ax = plt.subplots()
        # define the background color and transparency
        self.fig.patch.set_facecolor("grey")
        self.fig.patch.set_alpha(0.6)
        self.fig.subplots_adjust(right=0.70)
        self.display_image()
        self.buttons = []
        self.add_widgets()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        plt.show()

    def display_image(self):
        """
        Display the image on the GUI.
        """
        self.ax.imshow(self.image_editor.image)
        self.ax.set_title("Pixel Art Editor")
        self.ax.title.set_fontsize(20)
        self.ax.title.set_fontname("Comic Sans MS")
        self.ax.title.set_color(plt.cm.cool(3))
        self.ax.title.set_fontweight("bold")
        self.ax.title.set_fontfamily("Comic Sans MS")
        self.ax.title.set_fontstyle("italic")
        self.ax.title.set_alpha(0.5)
        self.ax.figure.canvas.draw()

    def add_widgets(self):
        """
        Add the widgets to the GUI.
        """
        self.button_width = 0.19
        self.button_height = 0.05
        button_width = self.button_width
        button_height = self.button_height
        self.start_x = self.fig.subplotpars.right + button_width / 3
        self.save_button_y = self.fig.subplotpars.top - 0.2
        self.undo_button_y = self.save_button_y - button_height
        self.slider_y = self.undo_button_y - button_height
        self.color_num_button_y = 0
        self.color_palette_y = 0 + button_height

        self.add_save_buttons()
        self.add_undo_button()
        self.add_color_palette_buttons()
        self.add_pixel_size_slider()
        self.add_exit_button()
        self.add_display_grid_button()
        self.add_crop_background_button()
        self.add_reset_image_button()
        self.add_create_gif_button()
        # start with grid off
        self.ax.xaxis.set_visible(False)
        self.set_buttons_font(self.buttons)

    def add_save_buttons(self):
        """
        Add the save buttons to the GUI.
        """
        start_x = self.start_x
        save_button_y = self.save_button_y
        button_width = self.button_width
        button_height = self.button_height

        # Save Button
        ax_save = plt.axes(
            [start_x, save_button_y, button_width / 2, button_height],
            facecolor="lightgreen",
        )
        self.btn_save = Button(
            ax_save, "Save", color="lightblue", hovercolor="lightgreen"
        )
        self.btn_save.on_clicked(self.image_editor.save_image)
        self.buttons.append(self.btn_save)

        # Save Transparent Button
        ax_save_transparent = plt.axes(
            [
                start_x + (button_width / 2),
                save_button_y,
                button_width / 2,
                button_height,
            ]
        )
        self.btn_save_transparent = Button(
            ax_save_transparent, "Cooler", color=plt.cm.cool(1), hovercolor="lightcoral"
        )
        self.btn_save_transparent.on_clicked(self.image_editor.save_transparent_png)
        self.buttons.append(self.btn_save_transparent)

    def add_undo_button(self):
        """
        Add the undo button to the GUI.
        """
        start_x = self.start_x
        undo_button_y = self.undo_button_y
        button_width = self.button_width
        button_height = self.button_height

        # Undo Button
        ax_undo = plt.axes(
            [start_x, undo_button_y, button_width, button_height],
            facecolor="lightcoral",
        )
        self.btn_undo = Button(
            ax_undo, "Undo", color="lightblue", hovercolor="lightcoral"
        )
        self.btn_undo.on_clicked(self.undo)
        self.buttons.append(self.btn_undo)

    def add_pixel_size_slider(self):
        """
        Add the pixel size slider to the GUI.
        """
        start_x = self.start_x
        slider_y = self.slider_y
        button_width = self.button_width
        button_height = self.button_height

        # Slider for Pixel Size
        ax_pixel_size_slider = plt.axes(
            [start_x, slider_y, button_width, button_height],
            facecolor="lightblue",
            frameon=True,
            visible=True,
        )

        self.pixel_size_slider = Slider(
            ax_pixel_size_slider,
            valmin=1,
            valmax=20,
            valinit=self.image_editor.pixel_size,
            valstep=1,
            alpha=0.5,
            # Change this number to get a different color from the gradient
            facecolor=plt.cm.cool(self.image_editor.pixel_size / 10),
            # Change this number to get a different color from the gradient
            track_color=plt.cm.cool(self.image_editor.pixel_size / 30),
            label="Size",
        )

        self.pixel_size_slider.label.set_color(plt.cm.cool(3))
        self.pixel_size_slider.valtext.set_color(plt.cm.cool(3))
        self.pixel_size_slider.label.set_size(10)
        self.pixel_size_slider.on_changed(self.on_slider_change)
        self.fig.canvas.mpl_connect("button_release_event", self.on_slider_released)
        self.buttons.append(self.pixel_size_slider)
        # Increase/Decrease Pixel Size Buttons
        ax_decrease_pixel_size = plt.axes(
            [start_x, slider_y - button_height, button_width / 2, button_height],
            facecolor="lightblue",
            frameon=True,
            visible=True,
        )
        self.btn_decrease_pixel_size = Button(
            ax_decrease_pixel_size, "-", color="lightgrey", hovercolor="thistle"
        )
        self.btn_decrease_pixel_size.on_clicked(self.decrease_pixel_size)
        self.buttons.append(self.btn_decrease_pixel_size)
        ax_increase_pixel_size = plt.axes(
            [
                start_x + button_width / 2,
                slider_y - button_height,
                button_width / 2,
                button_height,
            ]
        )
        self.btn_increase_pixel_size = Button(
            ax_increase_pixel_size, "+", color="pink", hovercolor="green"
        )
        self.btn_increase_pixel_size.on_clicked(self.increase_pixel_size)
        self.buttons.append(self.btn_increase_pixel_size)

    def add_color_palette_buttons(self):
        """
        Add the color palette buttons to the GUI.
        """
        start_x = self.start_x
        color_num_button_y = self.color_num_button_y
        color_palette_y = self.color_palette_y
        button_width = self.button_width
        button_height = self.button_height

        # Num Colors Button
        ax_num_colors = plt.axes(
            [start_x, color_num_button_y, button_width, button_height]
        )
        self.btn_num_colors = Button(
            ax_num_colors, f"Colors: {self.image_editor.num_colors}"
        )
        self.btn_num_colors.on_clicked(self.change_num_colors)
        self.buttons.append(self.btn_num_colors)
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
        color_labels = [f"Color {i+1}" for i in range(len(normalized_color_palette))]
        self.radio_color = RadioButtons(ax_color, color_labels)
        for i, label in enumerate(self.radio_color.labels):
            color = normalized_color_palette[i]
            hex_color = mcolors.to_hex(color)
            label.set_color(hex_color)
        self.radio_color.on_clicked(self.image_editor.change_color)
        self.buttons.append(self.radio_color)

    def add_exit_button(self):
        """
        Add the exit button to the GUI.
        """
        start_x = self.start_x
        save_button_y = self.save_button_y
        button_width = self.button_width
        button_height = self.button_height

        ax_exit = plt.axes(
            [start_x, save_button_y - button_height * 8, button_width, button_height],
            facecolor="lightcoral",
        )
        self.btn_exit = Button(
            ax_exit, "Exit", color=plt.cm.cool(0.5), hovercolor="lightcoral"
        )
        self.btn_exit.on_clicked(self.exit)
        self.buttons.append(self.btn_exit)

    def add_display_grid_button(self):
        """
        Add the display grid button to the GUI.
        """
        start_x = self.start_x
        save_button_y = self.save_button_y
        button_width = self.button_width
        button_height = self.button_height

        # add button to display the grid
        ax_display_grid = plt.axes(
            [start_x, save_button_y - button_height * 4, button_width, button_height],
            facecolor="lightblue",
        )
        self.btn_display_grid = Button(
            ax_display_grid, "Display Grid", color="lightblue", hovercolor="lightgreen"
        )
        self.btn_display_grid.on_clicked(self.turn_on_grid)
        self.buttons.append(self.btn_display_grid)

    def add_crop_background_button(self):
        """
        Add the crop background button to the GUI.
        """
        start_x = self.start_x
        save_button_y = self.save_button_y
        button_width = self.button_width
        button_height = self.button_height

        ax_crop_background = plt.axes(
            [start_x, save_button_y - button_height * 5, button_width, button_height]
        )
        self.btn_crop_background = Button(ax_crop_background, "Crop Background")
        self.btn_crop_background.on_clicked(self.image_editor.crop_background)
        self.buttons.append(self.btn_crop_background)

    def add_reset_image_button(self):
        """
        Add the reset image button to the GUI.
        """
        start_x = self.start_x
        save_button_y = self.save_button_y
        button_width = self.button_width
        button_height = self.button_height

        ax_reset_image = plt.axes(
            [start_x, save_button_y - button_height * 7, button_width, button_height],
            facecolor=plt.cm.cool(0.6),
        )
        self.btn_reset_image = Button(
            ax_reset_image, "Reset Image", color="lightblue", hovercolor="lightgreen"
        )
        self.btn_reset_image.on_clicked(self.reset_image)
        self.buttons.append(self.btn_reset_image)

    def add_create_gif_button(self):
        """
        Add the create GIF button to the GUI.
        """
        start_x = self.start_x
        save_button_y = self.save_button_y
        button_width = self.button_width
        button_height = self.button_height

        # Adjust the 'bottom' value to ensure the button does not overlap with other widgets
        ax_create_gif = plt.axes(
            [start_x, save_button_y - button_height * 6, button_width, button_height]
        )
        self.btn_create_gif = Button(
            ax_create_gif, "Create GIF", color="lightblue", hovercolor="yellow"
        )
        self.btn_create_gif.on_clicked(self.create_GIF)
        self.buttons.append(self.btn_create_gif)

    def set_buttons_font(self, button):
        plt.rcParams["font.family"] = "Comic Sans MS"
        plt.rcParams["font.size"] = 12
        # Change the font of all buttons
        for btn in self.buttons:
            if isinstance(btn, Button):
                btn.label.set_fontfamily("Comic Sans MS")
                btn.label.set_fontsize(12)
                btn.label.set_fontname("Comic Sans MS")

            elif isinstance(btn, Slider):
                btn.valtext.set_fontsize(12)
                btn.valtext.set_fontname("Comic Sans MS")
                btn.fontfamily = "Comic Sans MS"
                btn.label.set_fontsize(12)
                btn.label.set_fontname("Comic Sans MS")
            elif isinstance(btn, RadioButtons):
                for label in btn.labels:
                    label.set_fontname("Comic Sans MS")

        # same for text box in the dialog box ax
        for ax in self.fig.axes:
            if isinstance(ax, TextBox):
                ax.label.set_fontsize(12)
                ax.label.set_fontname("Comic Sans MS")

    def reset_image(self, event):
        """
        Reset the image to the original state.
        """
        self.image_editor.reset_image()
        self.display_image()

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
        all_ticks = np.arange(
            0, max(self.ax.get_xlim()[1], self.ax.get_ylim()[1]), new_pixel_size
        )
        # Label every 1/5 of the board
        label_ticks = all_ticks[:: len(all_ticks) // 5]

        # Set the new ticks
        self.ax.set_xticks(all_ticks, minor=True)
        self.ax.set_yticks(all_ticks, minor=True)

        # Set the new labels
        self.ax.set_xticks(label_ticks)
        self.ax.set_yticks(label_ticks)

        # Set the labels to be the 1D count of pixels until the current tick
        self.ax.set_xticklabels(
            [str(int(tick / new_pixel_size)) for tick in label_ticks]
        )
        self.ax.set_yticklabels(
            [len(all_ticks) - 1 - int(tick / new_pixel_size) for tick in label_ticks]
        )

        # Enable the grid if user has clicked the button
        if self.ax.xaxis.get_visible():
            self.ax.grid(which="both")
            self.ax.grid(which="minor", linestyle="-", linewidth=0.2, color="black")
            self.ax.grid(which="major", linestyle="-", linewidth=0.5, color="black")
            # set ticks color
            self.ax.tick_params(axis="both", which="both", colors=plt.cm.cool(3))


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
            image = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
            images.append(Image.fromarray(image))

            self.increase_pixel_size(None)

        for _ in range(3):
            # create a pause in the GIF
            images.append(Image.fromarray(image))

        for i in range(17):
            # Save the current state of the GUI as an image
            self.fig.canvas.draw()
            image = np.frombuffer(self.fig.canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
            images.append(Image.fromarray(image))

            self.decrease_pixel_size(None)

        for _ in range(3):
            images.append(Image.fromarray(image))

        # Convert the list of images into a GIF
        images[0].save(
            "record.gif", save_all=True, append_images=images[1:], loop=0, duration=250
        )
        plt.close()
        print("GIF created")
