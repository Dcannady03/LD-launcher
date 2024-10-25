# loading_screen.py

import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from Level_Down_Launcher import load_version

class LoadingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Load loading screen image
        loading_image_path = "assets/images/level_down_loading.png"
        self.loading_screen_label = QLabel()
        self.loading_screen_pixmap = QPixmap(loading_image_path)
        self.loading_screen_label.setPixmap(self.loading_screen_pixmap)
        self.loading_screen_label.setAlignment(Qt.AlignCenter)
        
        # Create layout and add label
        layout = QVBoxLayout(self)
        layout.addWidget(self.loading_screen_label)

        # Load progress images
        self.progress_images = {
            0: QPixmap('assets/images/loading0.png'),
            10: QPixmap('assets/images/loading10.png'),
            25: QPixmap('assets/images/loading25.png'),
            50: QPixmap('assets/images/loading50.png'),
            75: QPixmap('assets/images/loading75.png'),
            100: QPixmap('assets/images/loading100.png')
        }

        # Set up a progress timer
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_loading_progress)
        self.progress = 0

    def start_update_check(self, on_complete_callback):
        """Starts the update check process."""
        self.on_complete_callback = on_complete_callback
        self.progress_timer.start(500)  # Update every 500ms
        self.check_for_update()

    def check_for_update(self):
        """Check GitHub for the latest release version."""
        url = "https://api.github.com/repos/Dcannady03/LD-launcher/releases/latest"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                latest_release = response.json()
                latest_version = latest_release["tag_name"].lstrip('v')  # Remove 'v' prefix if present
                current_version = load_version()  # Load local version
                print(f"Latest version: {latest_version}, Current version: {current_version}")
            
                if latest_version > current_version:
                    self.progress = 50  # Indicate an update is needed
                else:
                    print("Already at the latest version.")
                    self.progress = 100  # Skip update if already up-to-date
            else:
                print("Failed to fetch release information.")
                self.progress = 100  # Complete if fetching fails
        except Exception as e:
            print(f"Error checking for updates: {e}")
            self.progress = 100  # End on error

        # If the check is complete, proceed to load the main application
        self.update_loading_progress()


    def update_loading_progress(self):
        """Updates the progress display based on the progress percentage."""
        if self.progress >= 100:
            self.progress_timer.stop()
            self.close()
            if self.on_complete_callback:
                self.on_complete_callback()  # Launch main application
        else:
            self.progress += 10  # Simulate progress
            # Update the image based on the progress
            closest_progress = max([p for p in self.progress_images.keys() if p <= self.progress])
            self.loading_screen_label.setPixmap(self.progress_images[closest_progress])
