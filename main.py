import sys
import os
import cv2
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QMessageBox
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, Signal, QObject

# Image Processor class for handling image operations
class ImageProcessor(QObject):
    image_processed = Signal()  # Signal to notify when the image is processed

    def __init__(self):
        super().__init__()
        self.mImg = None  # cv::Mat equivalent in Python is a numpy array
        self.originalImg = None  # Keep a copy of the original image

    def load_image(self, file_path):
        self.mImg = cv2.imread(file_path)  # Load image with OpenCV
        self.originalImg = self.mImg.copy()  # Save the original image
        self.image_processed.emit()

    def to_grayscale(self):
        if self.mImg is not None:
            self.mImg = cv2.cvtColor(self.mImg, cv2.COLOR_BGR2GRAY)
            self.image_processed.emit()

    def revert_image(self):
        if self.originalImg is not None:
            self.mImg = self.originalImg.copy()  # Revert to the original image
            self.image_processed.emit()

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
        self.image_processed.emit()


# MainWindow class inheriting from QMainWindow
class MainWindow(QMainWindow):
    load_image_signal = Signal(str)         # Signal to notify the Application to load an image
    grayscale_signal = Signal()             # Signal to notify the Application to apply grayscale
    save_image_signal = Signal(str)         # Signal to notify the Application to save an image
    revert_image_signal = Signal()          # Signal to revert the image
    process_all_images_signal = Signal()    # Signal to process all images in a folder

    def __init__(self):
        super().__init__()
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
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.current_image_path = file_path
            self.load_image_signal.emit(file_path)  # Emit the signal with file_path

    def convert_to_grayscale(self):
        self.grayscale_signal.emit()  # Emit the signal to apply grayscale

    def save_image(self):
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;Bitmap Files (*.bmp)")
        if save_path:
            self.save_image_signal.emit(save_path)  # Emit the signal to save the image

    def revert_image(self):
        self.revert_image_signal.emit()  # Emit the signal to revert the image

    def process_all_images(self):
        self.process_all_images_signal.emit()  # Emit the signal to process all images in folder

    def display_image(self, q_img):
        self.image_label.setPixmap(QPixmap.fromImage(q_img))


# Application class inheriting from QApplication
class Application(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.mImageProcessor = ImageProcessor()
        self.mMainWindow = MainWindow()

        # Connect signals from MainWindow to slots in Application
        self.mMainWindow.load_image_signal.connect(self.load_image)
        self.mMainWindow.grayscale_signal.connect(self.convert_to_grayscale)
        self.mMainWindow.save_image_signal.connect(self.save_image)
        self.mMainWindow.revert_image_signal.connect(self.revert_image)
        self.mMainWindow.process_all_images_signal.connect(self.process_all_images)

        # Connect ImageProcessor's signal to update UI
        self.mImageProcessor.image_processed.connect(self.update_image_display)

        self.mMainWindow.show()

    def load_image(self, file_path):
        self.mImageProcessor.load_image(file_path)

    def convert_to_grayscale(self):
        self.mImageProcessor.to_grayscale()

    def save_image(self, save_path):
        self.mImageProcessor.save_image(save_path)

    def revert_image(self):
        self.mImageProcessor.revert_image()

    def process_all_images(self):
        if self.mMainWindow.current_image_path:
            folder_path = os.path.dirname(self.mMainWindow.current_image_path)
            self.mImageProcessor.process_all_images_in_folder(folder_path)
            QMessageBox.information(self.mMainWindow, "Processing Done", "Grayscale processing has been applied to all images in the folder.")

    def update_image_display(self):
        if self.mImageProcessor.mImg is not None:
            image = self.mImageProcessor.mImg
            if len(image.shape) == 2:  # If grayscale
                q_img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
            else:  # If color image
                q_img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
                q_img = q_img.rgbSwapped()  # Convert BGR to RGB
            self.mMainWindow.display_image(q_img)


if __name__ == "__main__":
    app = Application(sys.argv)
    sys.exit(app.exec_())