import sys

from PyQt5.QtWidgets import (QApplication)

from ui.app_window import AppWindow

if __name__ == '__main__':
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create an instance of the AppWindow
    myApp = AppWindow(app)

    # Show the AppWindow
    myApp.show()

    try:
        # Start the application event loop
        sys.exit(app.exec_())
    except SystemExit:
        # Print a message when the window is closed
        print('Closing Window...')
