import sys
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

# Image Processor class for handling image operations
class ImageProcessor:
    def __init__(self):
        self.mImg = None  # cv::Mat equivalent in Python is a numpy array

    def load_image(self, file_path):
        self.mImg = cv2.imread(file_path)  # Load image with OpenCV

    def to_grayscale(self):
        if self.mImg is not None:
            self.mImg = cv2.cvtColor(self.mImg, cv2.COLOR_BGR2GRAY)

# MainWindow class inheriting from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, img_processor):
        super().__init__()
        self.img_processor = img_processor
        self.initUI()

    def initUI(self):
        # Set up the window
        self.setWindowTitle('Qt OpenCV Image Processing App')
        self.setGeometry(100, 100, 800, 600)
        
        # Add buttons
        self.load_button = QPushButton('Load Image', self)
        self.load_button.setGeometry(50, 500, 150, 40)
        self.load_button.clicked.connect(self.load_image)

        self.grayscale_button = QPushButton('Grayscale Image', self)
        self.grayscale_button.setGeometry(250, 500, 150, 40)
        self.grayscale_button.clicked.connect(self.convert_to_grayscale)

        # QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 700, 400)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

    def load_image(self):
        # Open file dialog to select an image
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.img_processor.load_image(file_path)
            self.display_image()

    def convert_to_grayscale(self):
        self.img_processor.to_grayscale()
        self.display_image()

    def display_image(self):
        # Convert the OpenCV image to QImage for display in QLabel
        if self.img_processor.mImg is not None:
            image = self.img_processor.mImg
            if len(image.shape) == 2:  # If grayscale
                q_img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
            else:  # If color image
                q_img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
                q_img = q_img.rgbSwapped()  # Convert BGR to RGB
            self.image_label.setPixmap(QPixmap.fromImage(q_img))

# Application class inheriting from QApplication
class Application(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.mImageProcessor = ImageProcessor()
        self.mMainWindow = MainWindow(self.mImageProcessor)
        self.mMainWindow.show()

if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec_())
