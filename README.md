# Simple Python Image Processing App

![image](https://github.com/user-attachments/assets/fc166a42-e036-4fbc-b877-c6a329aea469)

This is a simple Python application for loading, processing, and saving images using PySide6 (Qt for Python) and OpenCV. The app provides a graphical user interface (GUI) to perform basic image processing operations such as converting an image to grayscale and processing images in a folder.

### Features

- Load an Image: Load any image in formats like PNG, JPEG, BMP.
- Grayscale Conversion: Convert the loaded image to grayscale.
- Save Image: Save the processed image to disk in the desired format.
- Revert to Original: Revert the processed image back to the original loaded image.
- Batch Processing: Automatically apply grayscale conversion to all images in the same folder as the currently loaded image.

### Requirements

- Python 3.x
- PySide6
- OpenCV
- NumPy

### Install Dependencies

Create a virtual environment (example uses venv) and then install the aforementioned required libraries:
```
# create virtual environment
python -m venv myenv
myenv\Scripts\activate

#install dependencies
pip install PySide6 opencv-python numpy
```

# LICENCE

The code here provided falls under the very permissive MIT licence. However, if you plan to use this code in a commercial manner, remember that the PySide library (to be installed separately) falls under the Lesser GNU General Public Licence (LGPL, so still commerciable but with some limitations, inform yourself accordingly).
