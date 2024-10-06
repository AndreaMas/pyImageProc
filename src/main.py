import sys
from application import Application

if __name__ == "__main__":

    # Application inherits from QApplication
    # App contains MainWindow (which inherits from QMainWindow), the UI side of the app.
    # App also contains ImageProcessor, the Core side of the app.
    # App works as a listener to MainWindow and ImageProcessor, hearing their signals, enabling communication betw UI and Core.

    app = Application(sys.argv)
    sys.exit(app.exec()) # exec() executes QApplication's main loop, which lets signals work

    