import os
import cv2
import numpy as np
from PySide6.QtCore import QObject, Signal

class ImageProcessor(QObject):
    image_processed = Signal()
    last_operations = []  # To keep track of the operation performed

    def __init__(self):
        super().__init__()
        self.mImg = None
        self.originalImg = None

    def load_image(self, file_path):
        self.mImg = cv2.imread(file_path)
        self.originalImg = self.mImg.copy()
        self.image_processed.emit()

    def revert_image(self):
        if self.originalImg is not None:
            self.mImg = self.originalImg.copy()
            self.last_operations = []
            self.image_processed.emit()

    def save_image(self, save_path):
        if self.mImg is not None:
            cv2.imwrite(save_path, self.mImg)
                    
    def process_all_images_in_folder(self, folder_path):
        performed_last_operations = self.last_operations.copy()
        for file_name in os.listdir(folder_path):
            if file_name.endswith(('.png', '.jpg', '.bmp')):
                file_path = os.path.join(folder_path, file_name)
                img = cv2.imread(file_path)
                if img is not None:
                    self.mImg = img  # Set the current image
                    # Performed operations applied sequentially on the image
                    for operation in performed_last_operations:
                        if operation == 'grayscale':
                            self.to_grayscale()
                        elif operation == 'equalize_histogram':
                            self.equalize_histogram()
                        elif operation == 'color_balance':
                            self.color_balance()
                        elif operation == 'adjust_exposure':
                            self.adjust_exposure()
                        elif operation == 'enhance_contrast':
                            self.enhance_contrast()
                        elif operation == 'remove_shadows':
                            self.shadow_removal()
                        elif operation == 'enhance_details':
                            self.enhance_details()

                    save_path = os.path.join(folder_path, f"processed_{file_name}")
                    cv2.imwrite(save_path, self.mImg)  # Save the processed image
        performed_last_operations = []
        self.last_operations = []

    def to_grayscale(self):
        if self.mImg is not None:
            self.mImg = cv2.cvtColor(self.mImg, cv2.COLOR_BGR2GRAY)
            
            self.last_operations.append('grayscale')
            self.image_processed.emit()

    def equalize_histogram(self):
        if self.mImg is not None and len(self.mImg.shape) == 2:  # Grayscale image
            self.mImg = cv2.equalizeHist(self.mImg)
            
            self.last_operations.append('equalize_histogram')
            self.image_processed.emit()

    def color_balance(self):
        if self.mImg is not None:
            lab = cv2.cvtColor(self.mImg, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab = cv2.merge((l, a, b))
            self.mImg = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            self.last_operations.append('color_balance')
            self.image_processed.emit()

    def adjust_exposure(self):
        if self.mImg is not None:
            # Multiply pixel values by 1.2, then add 20 (brightness increase)
            # TODO: get alpha and beta values from UI (will also need to be stored in last_operations ... make it a tuple?)
            self.mImg = cv2.convertScaleAbs(self.mImg, alpha=1.2, beta=20) 
            
            self.last_operations.append('adjust_exposure')
            self.image_processed.emit()

    def enhance_contrast(self):
        if self.mImg is not None:
            # Divide image into brightness (l) and color bands (a, b), equalize just brightness, merge everything back together
            lab = cv2.cvtColor(self.mImg, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            l = cv2.equalizeHist(l)
            lab = cv2.merge((l, a, b))
            self.mImg = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            self.last_operations.append('enhance_contrast')
            self.image_processed.emit()

    def shadow_removal(self):
        if self.mImg is not None:
            rgb_planes = cv2.split(self.mImg)
            result_planes = []
            for plane in rgb_planes:
                dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
                bg_img = cv2.medianBlur(dilated_img, 21)
                diff_img = 255 - cv2.absdiff(plane, bg_img)
                result_planes.append(diff_img)
            self.mImg = cv2.merge(result_planes)
            
            self.last_operations.append('shadow_removal')
            self.image_processed.emit()

    def enhance_details(self):
        if self.mImg is not None:
            self.mImg = cv2.detailEnhance(self.mImg, sigma_s=10, sigma_r=0.15)
            
            self.last_operations.append('enhance_details')
            self.image_processed.emit()

            