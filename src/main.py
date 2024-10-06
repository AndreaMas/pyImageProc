import sys
from application import Application

if __name__ == "__main__":
    # Create Application (inherits from QApplication)
    # Application contains MainWindow (inherits from QMainWindow)
    app = Application(sys.argv)
    sys.exit(app.exec()) # execute's QApplication's main loop, which lets signals work

    