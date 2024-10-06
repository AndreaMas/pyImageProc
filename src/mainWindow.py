import os
from PySide6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QLabel
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
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
        self.setWindowTitle('OpenCV/Qt/Python Image Processing App')
        self.setGeometry(100, 100, 800, 600)

        # QLabel to display image
        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 700, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")

        # Add buttons
        self.load_button = QPushButton('Load Image', self)
        self.save_button = QPushButton('Save Image', self)
        self.revert_button = QPushButton('Revert Image', self)
        self.process_all_button = QPushButton('Process All Images in Folder', self)
        self.grayscale_button = QPushButton('Grayscale Image', self)
        self.equalize_histogram_button = QPushButton('Equalize Hist. (gray img only)', self)
        self.color_balance_button = QPushButton('Color Balance', self)
        self.adjust_exposure_button = QPushButton('Adjust Exposure', self)
        self.enhance_contrast_button = QPushButton('Enhance Contrast', self)
        self.shadow_removal_button = QPushButton('Remove Shadows', self)
        self.details_enhancement_button = QPushButton('Enhance Details', self)

        # Arrange buttons in layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.revert_button)
        button_layout.addWidget(self.process_all_button)
        button_layout.addSpacing(self.load_button.size().height())
        button_layout.addWidget(self.grayscale_button)
        button_layout.addWidget(self.equalize_histogram_button)
        button_layout.addWidget(self.color_balance_button)
        button_layout.addWidget(self.adjust_exposure_button)
        button_layout.addWidget(self.enhance_contrast_button)
        button_layout.addWidget(self.shadow_removal_button)
        button_layout.addWidget(self.details_enhancement_button)
        button_layout.addStretch(1) # stretch to push buttons to the top

        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Arrange image & buttons in central widget
        main_layout = QHBoxLayout(central_widget) # main layout for the window: image on the left, buttons on the right
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)

        # Connect button signals to methods
        self.load_button.clicked.connect(self.load_image)
        self.grayscale_button.clicked.connect(self.convert_to_grayscale)
        self.save_button.clicked.connect(self.save_image)
        self.revert_button.clicked.connect(self.revert_image)
        self.process_all_button.clicked.connect(self.process_all_images)
        self.equalize_histogram_button.clicked.connect(self.equalize_histogram)
        self.color_balance_button.clicked.connect(self.color_balance)
        self.adjust_exposure_button.clicked.connect(self.adjust_exposure)
        self.enhance_contrast_button.clicked.connect(self.enhance_contrast)
        self.shadow_removal_button.clicked.connect(self.remove_shadows)
        self.details_enhancement_button.clicked.connect(self.enhance_details)

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
        
        