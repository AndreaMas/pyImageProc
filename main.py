import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt

# Image Processor class for handling image operations
class ImageProcessor:
    def __init__(self):
        self.mImg = None  # cv::Mat equivalent in Python is a numpy array
        self.originalImg = None  # Keep a copy of the original image

    def load_image(self, file_path):
        self.mImg = cv2.imread(file_path)  # Load image with OpenCV
        self.originalImg = self.mImg.copy()  # Save the original image

    def to_grayscale(self):
        if self.mImg is not None:
            self.mImg = cv2.cvtColor(self.mImg, cv2.COLOR_BGR2GRAY)

    def revert_image(self):
        if self.originalImg is not None:
            self.mImg = self.originalImg.copy()  # Revert to the original image

    def save_image(self, save_path):
        if self.mImg is not None:
            cv2.imwrite(save_path, self.mImg)

    def process_all_images_in_folder(self, folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(('.png', '.jpg', '.bmp')):
                file_path = os.path.join(folder_path, file_name)
                img = cv2.imread(file_path)
                if img is not None:
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    save_path = os.path.join(folder_path, f"grayscale_{file_name}")
                    cv2.imwrite(save_path, gray_img)

# MainWindow class inheriting from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, img_processor):
        super().__init__()
        self.img_processor = img_processor
        self.current_image_path = None
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

        self.save_button = QPushButton('Save Image', self)
        self.save_button.setGeometry(450, 500, 150, 40)
        self.save_button.clicked.connect(self.save_image)

        self.revert_button = QPushButton('Revert Image', self)
        self.revert_button.setGeometry(650, 500, 150, 40)
        self.revert_button.clicked.connect(self.revert_image)

        self.process_all_button = QPushButton('Process All Images in Folder', self)
        self.process_all_button.setGeometry(50, 550, 300, 40)
        self.process_all_button.clicked.connect(self.process_all_images)

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
            self.current_image_path = file_path
            self.img_processor.load_image(file_path)
            self.display_image()

    def convert_to_grayscale(self):
        self.img_processor.to_grayscale()
        self.display_image()

    def save_image(self):
        if self.img_processor.mImg is not None:
            file_dialog = QFileDialog()
            save_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;Bitmap Files (*.bmp)")
            if save_path:
                self.img_processor.save_image(save_path)

    def revert_image(self):
        self.img_processor.revert_image()
        self.display_image()

    def process_all_images(self):
        if self.current_image_path:
            folder_path = os.path.dirname(self.current_image_path)
            self.img_processor.process_all_images_in_folder(folder_path)
            QMessageBox.information(self, "Processing Done", "Grayscale processing has been applied to all images in the folder.")

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