"""
This module contains the BoardGUI class which is used to create the GUI
for the image editor.
"""

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, \
    QFileDialog, QComboBox, QApplication, QMainWindow, QVBoxLayout, QMessageBox, QStyle
from PyQt5.QtGui import QPixmap, QColor, QIcon
from matplotlib.widgets import TextBox
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent=None, board_gui=None):
        super().__init__(canvas, parent)
        self.clear()
        self.color_plate_combobox = None
        self.reset_button = None
        self.exit_button = None
        self.save_button = None
        self.board_gui = board_gui
        self.init_color_palette()
        self.init_pixel_size_slider()
        self.init_buttons()

    def init_color_palette(self):
        self.color_plate_combobox = QComboBox(self)
        self.color_plate_combobox.setToolTip("Select Color")
        self.color_plate_combobox.setStyleSheet("""
            QComboBox {
                background-color: #333;
                color: #fff;
                border: 1px solid #000;
                padding: 10px;
                font-size: 18px;
            }
            QComboBox::drop-down {
                border: 0;
            }
            QComboBox::down-arrow {
                image: url("down-arrow.png");
            }
        """)
        self.colors = []
        self.updat_color_palette(self.board_gui.image_editor)
        self.color_plate_combobox.currentIndexChanged.connect(
            self._on_color_plate_selected)
        self.addWidget(self.color_plate_combobox)

    def init_reset_button(self):
        # Set text to an empty string
        self.reset_button = QPushButton("", self)
        self.reset_button.setIcon(
            self.style().standardIcon(QStyle.SP_BrowserReload))
        self.reset_button.setToolTip("Reset Image")  # Add tooltip
        self.reset_button.clicked.connect(self.reset_image)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: #fff;
                border: 1px solid #000;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #999;
            }
        """)  # Add modern design effects
        self.addWidget(self.reset_button)

    def init_exit_button(self):
        self.exit_button = QPushButton("", self)
        self.exit_button.setIcon(
            self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.exit_button.setToolTip("Exit")  # Add tooltip
        self.exit_button.clicked.connect(self.board_gui.exit)
        self.exit_button.autoFillBackground()
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: #222;
                border: 1px solid #000;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #666;
                color: red;
            }
            QPushButton:pressed {
                background-color: red;
                color: red;
            }
        """)  # Add modern design effects
        self.addWidget(self.exit_button)

    def init_pixel_size_slider(self):
        self.image_editor = self.board_gui.image_editor
        self.pixel_size_slider = QSlider(self)
        self.pixel_size_slider.setOrientation(1)
        self.pixel_size_slider.setRange(1, 20)
        self.pixel_size_slider.setValue(self.image_editor.pixel_size)
        self.pixel_size_slider.setTickPosition(QSlider.TicksBelow)
        self.pixel_size_slider.setStyleSheet("""
            QSlider::groove:vertical {
                border: 1px solid #000;
                background: #333;
                width: 10px;
                margin: 0px;
            }
            QSlider::handle:vertical {
                background: #fff;
                border: 1px solid #000;
                width: 10px;
                height: 10px;
                margin: 0px;
            }
        """)
        self.pixel_size_slider.setTickInterval(1)

        self.pixel_size_slider.valueChanged.connect(
            self._on_pixel_size_slider_changed)
        self.addWidget(self.pixel_size_slider)

    def init_buttons(self):
        self.init_reset_button()
        self.init_exit_button()
        self.init_save_button()

    def init_save_button(self):
        self.save_button = QPushButton("", self)
        self.save_button.setIcon(
            self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_button.setToolTip("Save Image")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: #fff;
                border: 1px solid #000;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #999;
            }
        """)
        self.save_button.clicked.connect(self.save_image)
        self.addWidget(self.save_button)

    def save_image(self):
        """
        Open a dialog box to save the image in different formats.
        """
        # choose saving format: transparent or not
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Save Image")
        msg_box.setText("Choose saving format:")
        normal_button = msg_box.addButton("Normal", QMessageBox.ActionRole)
        transparent_button = msg_box.addButton(
            "Transparent", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton("Cancel", QMessageBox.RejectRole)
        gif_button = msg_box.addButton("GIF", QMessageBox.ActionRole)
        msg_box.exec_()
        saving_format = None
        if msg_box.clickedButton() == normal_button:
            saving_format = "Normal"
        elif msg_box.clickedButton() == transparent_button:
            saving_format = "Transparent"
        if saving_format:
            file_dialog = QFileDialog()
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setDefaultSuffix("png")
            file_dialog.setDirectory(".")
            file_path = file_dialog.getSaveFileName(
                self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")[0]
            file_name = ""
            if file_path:
                file_name = file_path.split("/")[-1]
            if file_name:  # Check if a file name was provided
                if saving_format == "Normal":
                    self.image_editor.save_image(file_name)
                else:
                    self.image_editor.save_transparent_png(
                        file_path, file_name)

    def reset_image(self):
        self.image_editor.reset_image()
        self.board_gui.display_image()

    def _on_pixel_size_slider_changed(self):
        self.image_editor.change_pixel_size(self.pixel_size_slider.value())
        print(self.pixel_size_slider.value())
        print(self.image_editor.pixel_size)
        self.board_gui.display_image()

    def updat_color_palette(self, image_editor):
        self.colors = image_editor.color_palette
        self.color_plate_combobox.clear()
        print(self.colors)
        for color in self.colors:
            # convert to RGBA
            color = (color[0]/255, color[1]/255, color[2]/255, 1)
            hex_color = mcolors.to_hex(color)
            # Create a QPixmap, fill it with the color, and create an QIcon from it
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(hex_color))
            icon = QIcon(pixmap)
            # paint the color on the combobox
            self.color_plate_combobox.addItem(icon, f'{hex_color}')
            self.color_plate_combobox.setIconSize(pixmap.rect().size())

    def _on_color_plate_selected(self):
        # update the default color
        color = self.colors[self.color_plate_combobox.currentIndex()]
        color_index = self.color_plate_combobox.currentIndex()
        self.image_editor.change_color(color_index)


class BoardGUI:
    def __init__(self, image_editor):
        self.image_editor = image_editor
        self.fig, self.ax = plt.subplots()
        self.fig.set_facecolor('#2B2B2B')  # Set a dark theme for the figure
        self.fig.set_alpha(0.5)
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.is_slider_adjusting = False
        self.main_window.setWindowTitle("Pixel Art Editor")
        self.main_window.setGeometry(100, 100, 800, 800)

        self.main_window.setWindowIcon(
            self.main_window.style().standardIcon(QStyle.SP_FileDialogInfoView))
        self.main_window.setStyleSheet("background-color: #333; color: #fff;")

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setStyleSheet("background-color: #333; color: #fff;")
        self.canvas.setParent(self.main_window)
        self.canvas.setFocusPolicy(0)

        self.toolbar = CustomToolbar(self.canvas, self.main_window, self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.main_window.setCentralWidget(widget)
        self.main_window.show()
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.buttons = []
        self.display_image()
        self.app.exec_()
        # self.app.quit()

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
            self.ax.imshow(self.image_editor.image)
            # update main window
            self.canvas.draw()
            self.main_window.update()
            self.main_window.show()

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
