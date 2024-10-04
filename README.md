# Simple Python Image Processing App

![image](https://github.com/user-attachments/assets/fc166a42-e036-4fbc-b877-c6a329aea469)

This is a simple image processing application, developed in Python using OpenCV and PySide6 (Qt for Python).

### Features

- Single Image Processing: Load an image, process it trough the provided buttons, save the result.
- Batch Processing: Apply the most recently performed processing to all the images in the folder.

### Install Dependencies

To run the code, the following dependencies are required:
- Python 3.x
- PySide6
- OpenCV
- NumPy

To install them, suggestion is to first create a virtual environment in this project folder (or where you prefer), then install the dependencies. This can be done trough the following commands (example uses venv):
```bash
# create virtual environment named myenv
cd C:\pathToThisProjectFolder
python -m venv myenv

# activate virtual environment
myenv\Scripts\activate # windows
source myenv/bin/activate # linux/mac

# install dependencies
pip install PySide6 opencv-python numpy
```

### Licence

The code here provided falls under the very permissive MIT licence. However, if you plan to use this code in a commercial manner, remember that the PySide library (to be installed separately) falls under the Lesser GNU General Public Licence (LGPL, so still commerciable but with some limitations, inform yourself accordingly).
