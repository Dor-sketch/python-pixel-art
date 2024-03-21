"""
This module contains the BoardGUI class which is used to create the GUI
for the image editor.
"""

import sys
from PyQt5.QtWidgets import QWidget,QApplication, QVBoxLayout, QStyle
from matplotlib.widgets import TextBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PIL import Image
from PixelEditor import PixelEditor
from PyQt5.QtCore import Qt

class BoardGUI(QWidget):
    def __init__(self, image_editor):
        super().__init__()
        self.image_editor = image_editor
        self.fig, self.ax = plt.subplots()
        self.init_figure()
        self.canvas = None
        self.init_canvas()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.display_image()
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self.setWindowTitle("Pixel Art Editor")
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def init_figure(self):
        self.fig.patch.set_visible(False)  # Make figure background invisible
        self.fig.set_size_inches(
            (self.image_editor.image.width / 140, self.image_editor.image.height / 135))
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.ax.axis("off")

    def init_canvas(self):
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background-color:transparent;")  # Make canvas background transparent
        self.canvas.updateGeometry()

    def display_image(self, update_only=False):
        """
        Display the image on the GUI. If update_only is True, only update the modified region.
        """
        if update_only:
            # Logic to update only the modified region
            pass
        else:
            print("Displaying image")
            self.ax.clear()  # Clear before displaying to avoid overlaying images
            self.ax.axis("off")
            self.ax.imshow(self.image_editor.image)
            # update main window
            self.canvas.draw()
            self.update()
            self.show()

    def reset_image(self, event):
        """
        Reset the image to the original state.
        """
        self.image_editor.reset_image()

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

    def exit(self, event):
        """
        Called when the exit button is clicked.
        """
        plt.close()
        self.app.quit()

    def undo(self, event):
        """
        Called when the undo button is clicked.
        """
        self.image_editor.undo()
        self.pixel_size_slider.set_val(self.image_editor.pixel_size)

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

    def on_click(self, event):
        """
        Called when the mouse is clicked on the image
        """
        print("Mouse clicked")
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
            self.canvas.draw()
            self.display_image()

    def create_GIF(self, event):
        """
        Save the state of the GUI as an image at each step and create a GIF.
        """
        images = []
        for i in range(12):
            # Save the current state of the GUI as an image
            self.fig.canvas.draw()
            image = np.frombuffer(
                self.fig.canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(
                self.fig.canvas.get_width_height()[::-1] + (3,))
            images.append(Image.fromarray(image))

            self.increase_pixel_size(None)

        for _ in range(3):
            # create a pause in the GIF
            images.append(Image.fromarray(image))

        for i in range(17):
            # Save the current state of the GUI as an image
            self.fig.canvas.draw()
            image = np.frombuffer(
                self.fig.canvas.tostring_rgb(), dtype="uint8")
            image = image.reshape(
                self.fig.canvas.get_width_height()[::-1] + (3,))
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_editor = PixelEditor()
    main_window = BoardGUI(image_editor)
    toolbar = CustomToolbar(main_window.canvas, main_window, main_window)
    main_window.layout.addWidget(toolbar)
    main_window.show()
    sys.exit(app.exec_())
