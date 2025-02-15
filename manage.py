#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# 12-02-2025 pyqt6_app


# import threading
# import sys
# from PyQt6.QtWidgets import QApplication
# from pyqt6_app import SecondaryScreenApp  # Import the PyQt6 app class

# def start_pyqt_app():
#     app = QApplication(sys.argv)
#     window = SecondaryScreenApp()
#     window.show()
#     app.exec()

# if __name__ == "__main__":
#     thread = threading.Thread(target=start_pyqt_app, daemon=True)
#     thread.start()

#!/usr/bin/env python
# import os
# import sys
# import threading

# def start_pyqt_app():
#     print("Starting PyQt6 app...")  # Debugging output
#     """ Function to start PyQt6 application in a separate thread """
#     from PyQt6.QtWidgets import QApplication
#     from pyqt6_app import SecondaryScreenApp  # Import your PyQt6 app class

#     app = QApplication(sys.argv)
#     window = SecondaryScreenApp()
#     window.show()
#     print("PyQt6 app launched!")  # Debugging output
#     app.exec()  # Run PyQt event loop

# if __name__ == "__main__":
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

#     # Start PyQt6 application in a separate thread
#     thread = threading.Thread(target=start_pyqt_app, daemon=True)
#     thread.start()

#     # Run Django server
#     from django.core.management import execute_from_command_line
#     execute_from_command_line(sys.argv)

