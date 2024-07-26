"""
This file contains the CustomToolbar class, which is a subclass of the
NavigationToolbar class from matplotlib. It is used to create a custom toolbar
for the image editor.
"""

from PyQt5.QtWidgets import QPushButton, QSlider, \
    QFileDialog, QComboBox, QMessageBox, QStyle
from PyQt5.QtGui import QPixmap, QColor, QIcon
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QSlider, QStyle
import matplotlib.colors as mcolors
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class CustomToolbar(NavigationToolbar):
    """
    Class to represent the custom toolbar for the image editor.
    """
    def __init__(self, canvas, parent=None, board_gui=None):
        super().__init__(canvas, parent)
        self.clear()
        self.color_plate_combobox = None
        self.reset_button = None
        self.exit_button = None
        self.save_button = None
        self.pixel_size_slider = None
        self.num_colors_button = None
        self.load_button = None
        self.image_editor = None
        self.undo_button = None
        self.colors = []
        self.board_gui = board_gui
        self.init_buttons()

    def init_buttons(self):
        self.init_color_palette()
        self.init_reset_button()
        self.init_pixel_size_slider()
        self.init_save_button()
        self.init_num_colors_button()
        self.init_load_button()
        self.init_undo_button()
        self.init_exit_button()

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

    def init_pixel_size_slider(self):
        self.image_editor = self.board_gui.image_editor
        self.pixel_size_slider = QSlider(self)
        self.pixel_size_slider.setOrientation(1)
        self.pixel_size_slider.setRange(1, 50)
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

    def init_exit_button(self):
        """
        Initialize the exit button.
        """
        self.exit_button = QPushButton("", self)
        self.exit_button.setIcon(
            self.style().standardIcon(QStyle.SP_DialogCloseButton))
        self.exit_button.setToolTip("Exit")  # Add tooltip
        self.exit_button.clicked.connect(self.board_gui.exit)
        self.exit_button.autoFillBackground()
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: red;
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

    def init_num_colors_button(self):
        """
        Initialize the button to change the number of colors.
        """
        self.num_colors_button = QPushButton("Colors", self)
        self.num_colors_button.setToolTip("Change number of colors")
        self.num_colors_button.clicked.connect(self.change_num_colors)
        self.num_colors_button.setStyleSheet("""
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
        self.addWidget(self.num_colors_button)

    def change_num_colors(self):
        """
        Open a dialog box to change the number of colors.
        """
        current_num_colors = self.image_editor.num_colors  # Get current number of colors
        msg_box = QInputDialog(self)
        msg_box.setWindowTitle("Change Number of Colors")
        msg_box.setLabelText("Enter the number of colors:")
        msg_box.setOkButtonText("Ok")
        msg_box.setCancelButtonText("Cancel")
        # Set the initial value of the slider
        msg_box.setIntValue(current_num_colors)
        num_colors, ok = msg_box.getInt(
            self, "Change Number of Colors", "Enter the number of colors:", current_num_colors-1)
        if ok:
            self._on_num_colors_submit(num_colors+1)

    def _on_num_colors_submit(self, num_colors):
        self.image_editor.change_num_colors(num_colors)
        self.board_gui.display_image()
        self.updat_color_palette(self.board_gui.image_editor)

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
        elif msg_box.clickedButton() == gif_button:
            saving_format = "GIF"
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
                elif saving_format == "GIF":
                    # change the file name to a gif file
                    file_name = file_name.split(".")[0] + ".gif"
                    self.image_editor.make_gif(file_name)
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
        # make sure color plate matches
        if len(self.colors) > len(self.image_editor.color_palette):
            self.updat_color_palette(self.image_editor)
        # update the default color
        color = self.colors[self.color_plate_combobox.currentIndex()]
        print(color)
        self.image_editor.change_color(color)

    def init_load_button(self):
        self.load_button = QPushButton("Load", self)
        self.load_button.setToolTip("Load Image")
        self.load_button.clicked.connect(self.load_image)
        self.load_button.setStyleSheet("""
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
        self.addWidget(self.load_button)

    def load_image(self):
        """
        Open a dialog box to load an image from the user's computer.
        """
        self.board_gui.image_editor.load_image()
        self.board_gui.display_image()

    def init_undo_button(self):
        self.undo_button = QPushButton("", self)
        self.undo_button.setToolTip("Undo the last action")
        self.undo_button.clicked.connect(self.undo)
        self.undo_button.setIcon(
            self.style().standardIcon(QStyle.SP_ArrowBack))
        self.undo_button.setStyleSheet("""
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
        self.addWidget(self.undo_button)

    def undo(self):
        """
        Undo the last action.
        """
        self.image_editor.undo()
        self.board_gui.display_image()
