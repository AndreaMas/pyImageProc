import os
from PySide6.QtWidgets import QApplication
from mainWindow import MainWindow  # Assuming you have signals in MainWindow
from imageProcessor import ImageProcessor  # Assuming imageProcessor.py contains the ImageProcessor class

class Application(QApplication):
    def __init__(self, sys_argv):
        # call QApplication's constructor
        super().__init__(sys_argv)
        
        # Instantiate MainWindow and ImageProcessor
        self.main_window = MainWindow()
        self.image_processor = ImageProcessor()

        # Connect signals from MainWindow to ImageProcessor
        self.main_window.load_image_signal.connect(self.load_image)
        self.main_window.save_image_signal.connect(self.save_image)
        self.main_window.revert_image_signal.connect(self.revert_image)
        self.main_window.process_all_images_signal.connect(self.process_all_images)
        self.main_window.grayscale_signal.connect(self.convert_to_grayscale)
        self.main_window.equalize_histogram_signal.connect(self.equalize_histogram)
        self.main_window.color_balance_signal.connect(self.color_balance)
        self.main_window.adjust_exposure_signal.connect(self.adjust_exposure)
        self.main_window.contrast_enhancement_signal.connect(self.enhance_contrast)
        self.main_window.shadow_removal_signal.connect(self.remove_shadows)
        self.main_window.details_enhancement_signal.connect(self.enhance_details)

        # Connect ImageProcessor's signal to update the UI in MainWindow
        self.image_processor.image_processed.connect(self.update_image_display)

        # Display the MainWindow
        self.main_window.show()

    def load_image(self, file_path):
        self.image_processor.load_image(file_path)

    def convert_to_grayscale(self):
        self.image_processor.to_grayscale()

    def save_image(self, save_path):
        self.image_processor.save_image(save_path)

    def revert_image(self):
        self.image_processor.revert_image()

    def process_all_images(self):
        if self.main_window.current_image_path:
            folder_path = os.path.dirname(self.main_window.current_image_path)
            self.image_processor.process_all_images_in_folder(folder_path)

    # Slots for new functionality
    def equalize_histogram(self):
        self.image_processor.equalize_histogram()

    def color_balance(self):
        self.image_processor.color_balance()

    def adjust_exposure(self):
        self.image_processor.adjust_exposure()

    def enhance_contrast(self):
        self.image_processor.enhance_contrast()

    def remove_shadows(self):
        self.image_processor.shadow_removal()

    def enhance_details(self):
        self.image_processor.enhance_details()

    def update_image_display(self):
        if self.image_processor.mImg is not None:
            image = self.image_processor.mImg
            if len(image.shape) == 2:  # Grayscale image
                q_img = self.main_window.convert_cv_to_qt(image, is_grayscale=True)
            else:  # Color image
                q_img = self.main_window.convert_cv_to_qt(image)
            self.main_window.display_image(q_img)

            