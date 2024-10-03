import sys
from PySide6.QtWidgets import QApplication
from application import Application
from mainWindow import MainWindow
from imageProcessor import ImageProcessor

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Instantiate MainWindow and ImageProcessor
    image_processor = ImageProcessor()
    main_window = MainWindow()

    # Pass them to the Application class
    application = Application(main_window, image_processor)

    main_window.show()  # Display the main window
    sys.exit(app.exec_())

    