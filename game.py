from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import sys
from PixelEditor import PixelEditor
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from BoardGUI import BoardGUI


GAME_BOY_PURPLE = QColor(100, 100, 160)
GAME_BOY_BUTTON = QColor(200, 200, 200)

class GameboyAdvanceWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.pixel_size = 6
        self.num_of_colors = 4

        # Set color palette
        palette = QPalette()
        palette.setColor(QPalette.Window, GAME_BOY_PURPLE)
        palette.setColor(QPalette.WindowText, GAME_BOY_BUTTON)
        self.setPalette(palette)

        # Set layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addStretch()

        # Set fixed window size
        self.setFixedSize(300, 500)
        image_editor = PixelEditor()
        self.main_window = BoardGUI(image_editor)
        layout.addWidget(self.main_window)

        # Add arrow buttons
        arrowLayout = QGridLayout()
        buttonUp = QPushButton('^')
        buttonDown = QPushButton('v')
        buttonLeft = QPushButton('<')
        buttonRight = QPushButton('>')
        arrowLayout.addWidget(buttonUp, 0, 1)
        arrowLayout.addWidget(buttonDown, 2, 1)
        arrowLayout.addWidget(buttonLeft, 1, 0)
        arrowLayout.addWidget(buttonRight, 1, 2)

        # bind arrow buttons to the image editor
        buttonUp.clicked.connect(self.increase_num_colors)
        buttonLeft.clicked.connect(self.decrease_num_colors)
        buttonRight.clicked.connect(self.increase_pixel_size)
        buttonDown.clicked.connect(self.decrease_pixel_size)
        # Add A and B buttons
        buttonLayout = QHBoxLayout()
        buttonA = QPushButton('A')
        buttonB = QPushButton('B')
        buttonA.setStyleSheet(
            "background-color: rgba(211, 212, 207, 128); border-radius: 15px; min-width: 30px; min-height: 30px;")
        buttonB.setStyleSheet(
            "background-color: rgba(211, 212, 207, 128); border-radius: 15px; min-width: 30px; min-height: 30px;")
        buttonLayout.addWidget(buttonA)
        buttonLayout.addWidget(buttonB)

        # Add arrow and button layouts to main layout
        controlLayout = QHBoxLayout()
        layout.addLayout(controlLayout)
        controlLayout.addLayout(arrowLayout)
        controlLayout.addLayout(buttonLayout)

        # Add LED light
        ledLight = QLabel()
        ledLight.setStyleSheet(
            "background-color: red; border-radius: 50%; min-width: 10px; min-height: 10px;")
        layout.addWidget(ledLight, 0, Qt.AlignCenter)

        # Add Start and Select buttons
        startSelectLayout = QHBoxLayout()
        buttonStart = QPushButton('Start')
        buttonSelect = QPushButton('Select')
        buttonStart.setStyleSheet(
            "background-color: rgba(211, 212, 207, 128); border-radius: 15px; min-width: 30px; min-height: 30px;")
        buttonSelect.setStyleSheet(
            "background-color: rgba(211, 212, 207, 128); border-radius: 15px; min-width: 30px; min-height: 30px;")
        startSelectLayout.addWidget(buttonStart)
        startSelectLayout.addWidget(buttonSelect)
        layout.addLayout(startSelectLayout)


    def increase_pixel_size(self):
        self.pixel_size += 1
        self.main_window.image_editor.change_pixel_size(self.pixel_size)
        self.main_window.display_image()

    def decrease_pixel_size(self):
        if self.pixel_size > 1:
            self.pixel_size -= 1
            self.main_window.image_editor.change_pixel_size(self.pixel_size)
            self.main_window.display_image()

    def increase_num_colors(self):
        self.num_of_colors += 1
        self.main_window.image_editor.change_num_colors(self.num_of_colors)
        self.main_window.display_image()

    def decrease_num_colors(self):
        if self.num_of_colors > 1:
            self.num_of_colors -= 1
            self.main_window.image_editor.change_num_colors(self.num_of_colors)
            self.main_window.display_image()

app = QApplication(sys.argv)

window = GameboyAdvanceWindow()
window.show()
app.exec_()
