import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QLabel
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal

class MainWindow(QMainWindow):
    load_image_signal = Signal(str)
    grayscale_signal = Signal()
    save_image_signal = Signal(str)
    revert_image_signal = Signal()
    process_all_images_signal = Signal()
    equalize_histogram_signal = Signal()
    color_balance_signal = Signal()
    adjust_exposure_signal = Signal()
    contrast_enhancement_signal = Signal()
    shadow_removal_signal = Signal()
    details_enhancement_signal = Signal()

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

        # New buttons for the additional functionality
        self.histogram_button = QPushButton('Equalize Histogram', self)
        self.histogram_button.setGeometry(50, 450, 150, 40)
        self.histogram_button.clicked.connect(self.equalize_histogram)

        self.color_balance_button = QPushButton('Color Balance', self)
        self.color_balance_button.setGeometry(250, 450, 150, 40)
        self.color_balance_button.clicked.connect(self.color_balance)

        self.exposure_button = QPushButton('Adjust Exposure', self)
        self.exposure_button.setGeometry(450, 450, 150, 40)
        self.exposure_button.clicked.connect(self.adjust_exposure)

        self.contrast_button = QPushButton('Enhance Contrast', self)
        self.contrast_button.setGeometry(650, 450, 150, 40)
        self.contrast_button.clicked.connect(self.enhance_contrast)

        self.shadow_button = QPushButton('Remove Shadows', self)
        self.shadow_button.setGeometry(50, 400, 150, 40)
        self.shadow_button.clicked.connect(self.remove_shadows)

        self.details_button = QPushButton('Enhance Details', self)
        self.details_button.setGeometry(250, 400, 150, 40)
        self.details_button.clicked.connect(self.enhance_details)

        # QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 700, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

    def load_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.current_image_path = file_path
            self.load_image_signal.emit(file_path)  # Emit the signal with file_path

    def convert_to_grayscale(self):
        self.grayscale_signal.emit()

    def save_image(self):
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg);;Bitmap Files (*.bmp)")
        if save_path:
            self.save_image_signal.emit(save_path)

    def revert_image(self):
        self.revert_image_signal.emit()

    def process_all_images(self):
        self.process_all_images_signal.emit()

    def equalize_histogram(self):
        self.equalize_histogram_signal.emit()

    def color_balance(self):
        self.color_balance_signal.emit()

    def adjust_exposure(self):
        self.adjust_exposure_signal.emit()

    def enhance_contrast(self):
        self.contrast_enhancement_signal.emit()

    def remove_shadows(self):
        self.shadow_removal_signal.emit()

    def enhance_details(self):
        self.details_enhancement_signal.emit()

    def display_image(self, q_img):
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def convert_cv_to_qt(self, image, is_grayscale=False):
        if is_grayscale:
            return QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
        else:
            q_img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
            return q_img.rgbSwapped()  # Convert BGR to RGB
        
        