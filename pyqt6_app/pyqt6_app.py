#12-02-2025
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt6.QtCore import Qt, QTimer
# from PyQt6.QtGui import QFont
# import requests  # To interact with the Django API endpoint

# class SecondaryScreenApp(QWidget):
#     def __init__(self, book, chapter, verse):
#         super().__init__()

#         self.book = book
#         self.chapter = chapter
#         self.verse = verse

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Create a label to display the formatted data
#         self.label = QLabel("Fetching verse...", self)
#         self.label.setFont(QFont('Arial', 16))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.setWordWrap(True)  # Ensure text wraps correctly

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

#         # Timer to refresh data every 5 seconds (5000 ms)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.fetch_data)  
#         self.timer.start(5000)  # Set timer interval (adjust as needed)

#         # Fetch initial data
#         self.fetch_data()

#     def fetch_data(self):
#         """ Fetch data from the Django API and update the UI """
#         url = f"http://127.0.0.1:8000/view-data/?book={self.book}&chapter={self.chapter}&verse={self.verse}"

#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 data = response.json()
#                 self.update_verse(data)
#             else:
#                 self.update_verse({"error": "Verse not found"})
#         except requests.exceptions.RequestException as e:
#             print(f"Request error: {e}")
#             self.update_verse({"error": "Failed to connect to server"})

#     def update_verse(self, data):
#         """ Update the displayed verse dynamically """
#         book = data.get("book", "Unknown Book")
#         tamilname = data.get("tamilname", "Unknown book")
#         chapter = data.get("chapter", "N/A")
#         verse = data.get("verse", "N/A")
#         english_verse = data.get("english", "No English verse available")
#         tamil_verse = data.get("tamil", "தமிழ் வசனம் இல்லை")

#         display_text = f"""
#         📖 {book} ({tamilname}) {chapter}:{verse}
        
#         🇬🇧 {english_verse}

#         🇹🇳 {tamil_verse}
#         """

#         self.label.setText(display_text)  # Update label text
#         self.label.repaint()  # Force UI update (important!)


# def fetch_data_and_update_ui(window, book, chapter, verse):
#     url = f"http://127.0.0.1:8000/view-data/?book={book}&chapter={chapter}&verse={verse}"
#     print(book,chapter,verse)
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             window.update_verse(data)  # Update UI with new data
#         else:
#             print(f"Error: {response.status_code}")
#             window.update_verse({"error": "Verse not found"})
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")
#         window.update_verse({"error": "Failed to connect to server"})

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Example: Replace with user-selected values
#     selected_book = "job"
#     selected_chapter = "1"
#     selected_verse = "1"

#     # Create window with dynamic book details
#     window = SecondaryScreenApp(selected_book, selected_chapter, selected_verse)
#     window.show()

#     sys.exit(app.exec())

#######################################################################################
import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class SecondaryScreenApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Secondary Screen Viewer")
        # self.setGeometry(0, 0, 600, 400)  # Set window size
        self.setGeometry(100,100,800,200)

        # Create label
        self.label = QLabel("Waiting for selection...", self)
        self.label.setFont(QFont('Arial', 16))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        # self.showFullScreen()
        
        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Check if a secondary screen is available and move the window to it
        screens = QApplication.screens()
        if len(screens) > 1:
            # self.move(screens[1].geometry().topLeft())
            # self.move(screens[1].geometry().showFullScreen())
            secondary_screen_geometry = screens[1].geometry()
        self.move(secondary_screen_geometry.x(), secondary_screen_geometry.y())
        self.showFullScreen()

        # Auto-fetch latest selection every 2 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_latest_selection)
        self.timer.start(2000)  # Check every 2 seconds

        self.fetch_latest_selection()  # Initial fetch

    def fetch_latest_selection(self):
        """ Fetch the latest user selection from Django """
        url = "http://127.0.0.1:8000/latest-selection/"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "error" not in data:
                    self.fetch_data(data["book"], data["chapter"], data["verse"])
                else:
                    self.label.setText("No selection found.")
            else:
                self.label.setText("Failed to fetch latest selection.")
        except requests.exceptions.RequestException as e:
            self.label.setText("Server error.")
            print(f"Request error: {e}")

    def fetch_data(self, book, chapter, verse):
        """ Fetch verse from the Django API and update UI """
        url = f"http://127.0.0.1:8000/view-data/?book={book}&chapter={chapter}&verse={verse}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.update_verse(data)
            else:
                self.update_verse({"error": "Verse not found"})
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            self.update_verse({"error": "Failed to connect to server"})

    def update_verse(self, data):
        """ Update the displayed verse dynamically """
        book = data.get("book", "Unknown Book")
        tamilname = data.get("tamilname", "Unknown book")
        chapter = data.get("chapter", "N/A")
        verse = data.get("verse", "N/A")
        english_verse = data.get("english", "No English verse available")
        tamil_verse = data.get("tamil", "தமிழ் வசனம் இல்லை")

        display_text = f"""
        📖 {book} ({tamilname}) {chapter}:{verse}
        
        🇬🇧 {english_verse}

        🇹🇳 {tamil_verse}
        """

        self.label.setText(display_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecondaryScreenApp()
    window.show()
    sys.exit(app.exec())


###################################################################################### pyqt6_app.py
# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
# import requests  # To interact with the Django API endpoint

# class SecondaryScreenApp(QWidget):
#     def __init__(self, data):
#         super().__init__()

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Create a label to display data
#         self.label = QLabel(data, self)
#         self.label.setFont(QFont('Arial', 24))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

# def fetch_data_from_django():
#     # Replace with your Django server URL
#     url = "http://127.0.0.1:8000/view-data/"
#     response = requests.get(url)
#     return response.json().get('data')

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Fetch data from Django API
#     data = fetch_data_from_django()

#     # Create a secondary screen application
#     window = SecondaryScreenApp(data)
#     window.show()

#     sys.exit(app.exec())

########################################################################


# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
# import requests  # To interact with the Django API endpoint

# class SecondaryScreenApp(QWidget):
#     def __init__(self, data):
#         super().__init__()

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Format the data into a string to display it in the label
#         data_str = '\n'.join([f"{key}: {value}" for key, value in data.items()])

#         # Create a label to display the formatted data
#         self.label = QLabel(data_str, self)
#         self.label.setFont(QFont('Arial', 18))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

# def fetch_data_from_django():
#     # Replace with your Django server URL
#     url = "http://127.0.0.1:8000/view-data/"
#     response = requests.get(url)
    
#     # Check if the response is valid
#     if response.status_code == 200:
#         # The response JSON is expected to contain the dictionary data
#         return response.json()  # This will return the entire dictionary
#     else:
#         print(f"Error: {response.status_code}")
#         return {}  # Return an empty dictionary if the request failed

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Fetch data from Django API
#     data = fetch_data_from_django()

#     if not data:
#         print("No data received from Django API.")
#         data = {"error": "No data available"}

#     # Create a secondary screen application
#     window = SecondaryScreenApp(data)
#     window.show()

#     sys.exit(app.exec())

######################################################

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import requests  # To interact with the Django API endpoint

# class SecondaryScreenApp(QWidget):
#     def __init__(self, data):
#         super().__init__()

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Extract data
#         book = data.get("book", "Unknown Book")
#         tamilname=data.get("tamilname","Unknown book")
#         chapter = data.get("chapter", "N/A")
#         verse = data.get("verse", "N/A")
#         english_verse = data.get("english", "No English verse available")
#         tamil_verse = data.get("tamil", "தமிழ் வசனம் இல்லை")

#         # Format the displayed text
#         display_text = f"""
#         📖 {book} {(tamilname)} {chapter}:{verse}
        
#         🇬🇧 {english_verse}

#         🇹🇳 {tamil_verse}
#         """

#         # Create a label to display the formatted data
#         self.label = QLabel(display_text, self)
#         self.label.setFont(QFont('Arial', 16))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.setWordWrap(True)  # Ensure text wraps correctly

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

# class SecondaryScreenApp(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Create a label to display the formatted data
#         self.label = QLabel("", self)
#         self.label.setFont(QFont('Arial', 16))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.label.setWordWrap(True)  # Ensure text wraps correctly

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

#     def update_verse(self, data):
#         """ Update the displayed verse dynamically. """
#         book = data.get("book", "Unknown Book")
#         tamilname = data.get("tamilname", "Unknown book")
#         chapter = data.get("chapter", "N/A")
#         verse = data.get("verse", "N/A")
#         english_verse = data.get("english", "No English verse available")
#         tamil_verse = data.get("tamil", "தமிழ் வசனம் இல்லை")

#         display_text = f"""
#         📖 {book} ({tamilname}) {chapter}:{verse}
        
#         🇬🇧 {english_verse}

#         🇹🇳 {tamil_verse}
#         """

#         self.label.setText(display_text)  # Update label text

###############################################################################



# def fetch_data_from_django(book, chapter, verse):
#     url = f"http://127.0.0.1:8000/view-data/?book={book}&chapter={chapter}&verse={verse}"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()  # Return fetched verse data
#         else:
#             print(f"Error: {response.status_code}")
#             return {"error": "Verse not found"}
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")
#         return {"error": "Failed to connect to server"}

# def fetch_data_and_update_ui(window, book, chapter, verse):
#     url = f"http://127.0.0.1:8000/view-data/?book={book}&chapter={chapter}&verse={verse}"
#     print(book,chapter,verse)
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             window.update_verse(data)  # Update UI with new data
#         else:
#             print(f"Error: {response.status_code}")
#             window.update_verse({"error": "Verse not found"})
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")
#         window.update_verse({"error": "Failed to connect to server"})


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Example: User selects "Genesis", chapter 1, verse 1 (You can replace this with user input)
#     selected_book = "Genesis"
#     selected_chapter = "1"
#     selected_verse = "1"

#     # Fetch data dynamically
#     data = fetch_data_from_django(selected_book, selected_chapter, selected_verse)

#     # Create and display the window
#     window = SecondaryScreenApp(data)
#     window.show()

#     sys.exit(app.exec())

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     window = SecondaryScreenApp()
#     window.show()

#     # Example: Change these values dynamically to test
#     selected_book = "Genesis"
#     selected_chapter = "1"
#     selected_verse = "1"

#     # Fetch and update UI
#     fetch_data_and_update_ui(window, selected_book, selected_chapter, selected_verse)

#     sys.exit(app.exec())

#####################
# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Example: Replace with user-selected values
#     selected_book = "job"
#     selected_chapter = "1"
#     selected_verse = "1"

#     # Create window with dynamic book details
#     window = SecondaryScreenApp(selected_book, selected_chapter, selected_verse)
#     window.show()

#     sys.exit(app.exec())

#####################



# def fetch_data_from_django():
#     # Replace with your Django server URL
#     url = "http://127.0.0.1:8000/view-data/"
#     response = requests.get(url)
    
#     # Check if the response is valid
#     if response.status_code == 200:
#         # The response JSON is expected to contain the dictionary data
#         return response.json()  # This will return the entire dictionary
#     else:
#         print(f"Error: {response.status_code}")
#         return {}  # Return an empty dictionary if the request failed

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Fetch data from Django API
#     data = fetch_data_from_django()

#     if not data:
#         print("No data received from Django API.")
#         data = {
#             "book": "N/A",
#             "chapter": "N/A",
#             "verse": "N/A",
#             "english": "No verse available",
#             "tamil": "வசனம் இல்லை"
#         }

#     # Create a secondary screen application
#     window = SecondaryScreenApp(data)
#     window.show()

#     sys.exit(app.exec())




######################################################

# from flask import Flask, request, jsonify
# import sys
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
# from PyQt6.QtCore import QThread, pyqtSignal

# app = Flask(__name__)

# # Create a thread to run PyQt6 safely
# class PyQtWorker(QThread):
#     update_signal = pyqtSignal(str, str)

#     def __init__(self):
#         super().__init__()
#         self.app = QApplication(sys.argv)
#         self.window = None
#         self.update_signal.connect(self.show_window)

#     def show_window(self, tamil_text, kjv_text):
#         if self.window is None:
#             self.window = QWidget()
#             self.window.setWindowTitle("Bible Verse Display")
#             layout = QVBoxLayout()
#             self.label_tamil = QLabel(f"<b>Tamil:</b> {tamil_text}")
#             self.label_kjv = QLabel(f"<b>KJV:</b> {kjv_text}")
#             layout.addWidget(self.label_tamil)
#             layout.addWidget(self.label_kjv)
#             self.window.setLayout(layout)
#             self.window.show()
#         else:
#             self.label_tamil.setText(f"<b>Tamil:</b> {tamil_text}")
#             self.label_kjv.setText(f"<b>KJV:</b> {kjv_text}")

#     def run(self):
#         self.app.exec()

# # Start the PyQt6 worker
# pyqt_worker = PyQtWorker()
# pyqt_worker.start()

# @app.route('/', methods=['GET'])
# def home():
#     return "Flask PyQt6 Server is Running!"

# # Correct the route for display-data
# @app.route('/display-data/', methods=['POST'])
# def display_data():
#     try:
#         data = request.json
#         tamil_text = data.get("tamil_version", "No Tamil verse provided")
#         kjv_text = data.get("kjv_version", "No KJV verse provided")

#         # Send data to the PyQt6 thread
#         pyqt_worker.update_signal.emit(tamil_text, kjv_text)

#         return jsonify({"status": "success", "message": "Data sent to PyQt6"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000, debug=True, use_reloader=False)


#############################################################################


# from flask import Flask, request, jsonify
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
# import sys

# app = Flask(__name__)

# class SecondaryScreenApp(QWidget):
#     def __init__(self, data):
#         super().__init__()

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Format the data into a string to display it in the label
#         data_str = '\n'.join([f"{key}: {value}" for key, value in data.items()])

#         # Create a label to display the formatted data
#         self.label = QLabel(data_str, self)
#         self.label.setFont(QFont('Arial', 18))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

# @app.route('/display-data', methods=['POST'])
# def display_data():
#     data = request.json
#     app = QApplication(sys.argv)
#     window = SecondaryScreenApp(data)
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

###################################################################

# from flask import Flask, request, jsonify
# from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QFont
# import sys

# # Initialize Flask app
# app = Flask(__name__)

# class SecondaryScreenApp(QWidget):
#     def __init__(self, data):
#         super().__init__()

#         self.setWindowTitle("Secondary Screen Viewer")
#         self.setGeometry(0, 0, 600, 400)  # Set window size

#         # Format the data into a string to display it in the label
#         data_str = '\n'.join([f"{key}: {value}" for key, value in data.items()])

#         # Create a label to display the formatted data
#         self.label = QLabel(data_str, self)
#         self.label.setFont(QFont('Arial', 18))
#         self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         # Set layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.label)
#         self.setLayout(layout)

#         # Check if a secondary screen is available and move the window to it
#         screens = QApplication.screens()
#         if len(screens) > 1:
#             self.move(screens[1].geometry().topLeft())

# @app.route('/display-data', methods=['POST'])
# def display_data():
#     data = request.json  # Get the data sent from the Django backend
    
#     # Create and display PyQt6 app with the received data
#     app = QApplication(sys.argv)
#     window = SecondaryScreenApp(data)
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)  # Start Flask server on port 5000


############################# 11-02-2025

# from flask import Flask, request, jsonify
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
# import sys
# import threading

# app = Flask(__name__)

# class DisplayWindow(QWidget):
#     def __init__(self, data):
#         super().__init__()
#         self.setWindowTitle("Bible Verse Display")
#         self.setGeometry(100, 100, 400, 200)

#         layout = QVBoxLayout()
#         layout.addWidget(QLabel(f"Tamil: {data.get('tamil_version', 'N/A')}"))
#         layout.addWidget(QLabel(f"KJV: {data.get('kjv_version', 'N/A')}"))

#         self.setLayout(layout)

# @app.route('/display-data/', methods=['POST'])
# def display_data():
#     data = request.json
#     if data:
#         threading.Thread(target=launch_pyqt6, args=(data,)).start()
#         return jsonify({"status": "Displayed in PyQt6 window"})
#     return jsonify({"error": "No data received"}), 400

# def launch_pyqt6(data):
#     app = QApplication(sys.argv)
#     window = DisplayWindow(data)
#     window.show()
#     app.exec()

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)


############################################### update 2

# from flask import Flask, request, jsonify
# import sys
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
# from PyQt6.QtCore import QThread, pyqtSignal

# app = Flask(__name__)

# # Create a thread to run PyQt6 safely
# class PyQtWorker(QThread):
#     update_signal = pyqtSignal(str, str)

#     def __init__(self):
#         super().__init__()
#         self.app = QApplication(sys.argv)
#         self.window = None
#         self.update_signal.connect(self.show_window)

#     def show_window(self, tamil_text, kjv_text):
#         if self.window is None:
#             self.window = QWidget()
#             self.window.setWindowTitle("Bible Verse Display")
#             layout = QVBoxLayout()
#             self.label_tamil = QLabel(tamil_text)
#             self.label_kjv = QLabel(kjv_text)
#             layout.addWidget(self.label_tamil)
#             layout.addWidget(self.label_kjv)
#             self.window.setLayout(layout)
#             self.window.show()
#         else:
#             self.label_tamil.setText(tamil_text)
#             self.label_kjv.setText(kjv_text)

#     def run(self):
#         self.app.exec()

# # Start the PyQt6 worker
# pyqt_worker = PyQtWorker()
# pyqt_worker.start()

# @app.route('/display-data/', methods=['POST'])
# def display_data():
#     try:
#         data = request.json
#         tamil_text = data.get("tamil_version", "No Tamil verse provided")
#         kjv_text = data.get("kjv_version", "No KJV verse provided")

#         # Send data to the PyQt6 thread
#         pyqt_worker.update_signal.emit(tamil_text, kjv_text)

#         return jsonify({"status": "success", "message": "Data sent to PyQt6"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=5000, debug=True, use_reloader=False)
