# Simple Python Image Processing App

![image](https://github.com/user-attachments/assets/fc166a42-e036-4fbc-b877-c6a329aea469)

This is a simple image processing application, developed in Python using OpenCV and PySide6 (Qt for Python).

### Features

- Single Image Processing: Load an image, apply a processing-option to it trough the provided buttons, save the result.
- Batch Processing: Apply the most recently performed processing-option to all the images in a folder.

### Requirements

- Python 3.x
- PySide6
- OpenCV
- NumPy

### Install Dependencies

Create a virtual environment (example uses venv) and then install the aforementioned required libraries:
```bash
# create virtual environment
python -m venv myenv
myenv\Scripts\activate # windows
source myenv/bin/activate # linux/mac

# install dependencies
pip install PySide6 opencv-python numpy
```

### Licence

The code here provided falls under the very permissive MIT licence. However, if you plan to use this code in a commercial manner, remember that the PySide library (to be installed separately) falls under the Lesser GNU General Public Licence (LGPL, so still commerciable but with some limitations, inform yourself accordingly).
