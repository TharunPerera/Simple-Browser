import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import *
import base64

# Main Browser Class
class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Simple Browser")
        # Set the window geometry
        self.setGeometry(100, 100, 1200, 800)

        # Create the browser widget
        self.browser = QWebEngineView()
        # Set the default URL to Google
        self.browser.setUrl(QUrl("http://www.google.com"))
        # Set the browser as the central widget
        self.setCentralWidget(self.browser)

        # Create the toolbar
        self.create_toolbar()
        # Create the status bar
        self.create_status_bar()

        # Connect the loadFinished signal to the inject_custom_css method
        self.browser.page().loadFinished.connect(self.inject_custom_css)
        
        # Show the main window
        self.show()

    def create_toolbar(self):
        # Create the toolbar
        toolbar = QToolBar("Navigation")
        # Add the toolbar to the main window
        self.addToolBar(toolbar)

        # Set the icon size for the toolbar actions
        toolbar.setIconSize(QSize(32, 32))  # Increase the size as needed

        # Set the minimum height of the toolbar
        toolbar.setStyleSheet("QToolBar { min-height: 50px; }")  # Increase the height as needed

        # Create the back button
        back_button = QAction(QIcon("icons/back2_green.png"), "Back", self)
        # Connect the back button to the browser's back method
        back_button.triggered.connect(self.browser.back)
        # Add the back button to the toolbar
        toolbar.addAction(back_button)

        # Create the forward button
        forward_button = QAction(QIcon("icons/right2_green.png"), "Forward", self)
        # Connect the forward button to the browser's forward method
        forward_button.triggered.connect(self.browser.forward)
        # Add the forward button to the toolbar
        toolbar.addAction(forward_button)

        # Create the reload button
        reload_button = QAction(QIcon("icons/reload_green.png"), "Reload", self)
        # Connect the reload button to the browser's reload method
        reload_button.triggered.connect(self.browser.reload)
        # Add the reload button to the toolbar
        toolbar.addAction(reload_button)

        # Create the home button
        home_button = QAction(QIcon("icons/home_green.png"), "Home", self)
        # Connect the home button to the navigate_home method
        home_button.triggered.connect(self.navigate_home)
        # Add the home button to the toolbar
        toolbar.addAction(home_button)

        # Create the URL bar
        self.url_bar = QLineEdit()
        # Connect the returnPressed signal to the navigate_to_url method
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        # Add the URL bar to the toolbar
        toolbar.addWidget(self.url_bar)

        # Create the bookmark button
        bookmark_button = QAction(QIcon("icons/bookmark_green.png"), "Bookmark", self)
        # Connect the bookmark button to the add_bookmark method
        bookmark_button.triggered.connect(self.add_bookmark)
        # Add the bookmark button to the toolbar
        toolbar.addAction(bookmark_button)

        # Create the history button
        history_button = QAction(QIcon("icons/history_green.png"), "History", self)
        # Connect the history button to the show_history method
        history_button.triggered.connect(self.show_history)
        # Add the history button to the toolbar
        toolbar.addAction(history_button)

        # Connect the browser's urlChanged signal to the update_url method
        self.browser.urlChanged.connect(self.update_url)

    def create_status_bar(self):
        # Create the status bar
        self.status = QStatusBar()
        # Set the status bar for the main window
        self.setStatusBar(self.status)
        # Connect the browser's loadStarted signal to the load_started method
        self.browser.loadStarted.connect(self.load_started)
        # Connect the browser's loadProgress signal to the load_progress method
        self.browser.loadProgress.connect(self.load_progress)
        # Connect the browser's loadFinished signal to the load_finished method
        self.browser.loadFinished.connect(self.load_finished)

    def load_started(self):
        # Show "Loading..." message in the status bar
        self.status.showMessage("Loading...")

    def load_progress(self, progress):
        # Show loading progress in the status bar
        self.status.showMessage(f"Loading... {progress}%")

    def load_finished(self):
        # Show "Finished" message in the status bar
        self.status.showMessage("Finished")

    def navigate_home(self):
        # Navigate to the home URL
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        # Get the URL from the URL bar
        url = self.url_bar.text()
        # Add "http://" prefix if missing
        if not url.startswith("http"):
            url = "http://" + url
        # Navigate to the specified URL
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        # Update the URL bar with the current URL
        self.url_bar.setText(q.toString())

    def add_bookmark(self):
        # Get the current URL
        url = self.browser.url().toString()
        # Prompt the user for a bookmark name
        name, ok = QInputDialog.getText(self, 'Bookmark', 'Enter a name for this bookmark:')
        if ok:
            # Append the bookmark to the bookmarks file
            with open('bookmarks.txt', 'a') as file:
                file.write(f"{name}\t{url}\n")
            # Show a confirmation message
            QMessageBox.information(self, "Bookmark Added", f"Bookmark '{name}' added successfully!")

    def show_history(self):
        # Create a history window
        history_window = QDialog(self)
        history_window.setWindowTitle("History")
        layout = QVBoxLayout()

        # Create a list widget for the history
        history_list = QListWidget()
        try:
            # Read the history from the history file
            with open('history.txt', 'r') as file:
                for line in file:
                    history_list.addItem(line.strip())
        except FileNotFoundError:
            # Show a message if no history is available
            history_list.addItem("No history available.")

        # Add the history list to the layout
        layout.addWidget(history_list)
        # Set the layout for the history window
        history_window.setLayout(layout)
        # Show the history window
        history_window.exec()

    def closeEvent(self, event):
        # Append the current URL to the history file when the window is closed
        with open('history.txt', 'a') as file:
            file.write(f"{self.browser.url().toString()}\n")
        # Accept the close event
        event.accept()

    def inject_custom_css(self):
        # Read the background image file
        with open('C:/Users/User/Downloads/backgorud_img.png', 'rb') as f:
            img_data = f.read()
            # Encode the image in base64
            img_base64 = base64.b64encode(img_data).decode('utf-8')

        # Define the custom CSS to set the background image
        css = f"""
        body {{
            background-image: url(data:image/png;base64,{img_base64}) !important;
            background-size: cover;
        }}
        """
        # Inject the custom CSS into the web page
        self.browser.page().runJavaScript(f"""
            var style = document.createElement('style');
            style.type = 'text/css';
            style.innerHTML = `{css}`;
            document.head.appendChild(style);
        """)

# Create the application
app = QApplication(sys.argv)
QApplication.setApplicationName("Simple Browser")
# Create and show the main window
window = Browser()
# Execute the application
app.exec()
