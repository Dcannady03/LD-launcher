# launcher.py

import os
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QPushButton, QLabel, QStatusBar, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize, Qt
from utils import load_config, save_config, load_version
from custom_web_engine import CustomWebEngineView
from login_dialog import LoginDialog
import subprocess  # Required for launching external executables
from PyQt5.QtCore import QUrl
import os
import json
from PyQt5.QtWidgets import QMenuBar, QAction, QMessageBox, QFileDialog

CONFIG_PATH = "assets/config/config.json"
VERSION_PATH = "assets/config/version.json"

# Default structure for config and version files
default_config = {
    "ashita_exe": "",
    "windower_exe": "",
    "xi_loader_exe": "assets/config/xiLoader.exe"
}

default_version = {
    "launcher_version": "1.0.0"
}

# Function to create a file with default content if it doesn't exist
def create_file_if_not_exists(path, default_content):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            json.dump(default_content, file, indent=4)
            print(f"Created {path} with default content.")

# Create config.json and version.json if they don't exist
create_file_if_not_exists(CONFIG_PATH, default_config)
create_file_if_not_exists(VERSION_PATH, default_version)
class LauncherMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.launcher_version = load_version()
        self.config = load_config()
        self.setWindowTitle(f"Level Down Launcher - Version {self.launcher_version}")
        self.setFixedSize(1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.set_background_image()
        
        # Initialize UI elements
        self.setup_menu_bar()  # Initialize the dark-themed menu bar
        self.setup_ui()
    def setup_menu_bar(self):
        # Create menu bar
        menu_bar = self.menuBar()
    
        # Apply dark theme style
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QMenuBar::item {
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #4b4b4b;
            }
            QMenu {
                background-color: #2e2e2e;
                color: #ffffff;
                border: 1px solid #5e5e5e;
            }
            QMenu::item:selected {
                background-color: #4b4b4b;
            }
        """)

        # File menu
        file_menu = menu_bar.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
        # Settings menu
        settings_menu = menu_bar.addMenu('Settings')
    
        # Add Ashita and Windower path settings
        ashita_action = QAction('Set Ashita Executable', self)
        ashita_action.triggered.connect(self.set_ashita_exe)
        settings_menu.addAction(ashita_action)
    
        windower_action = QAction('Set Windower Executable', self)
        windower_action.triggered.connect(self.set_windower_exe)
        settings_menu.addAction(windower_action)

    def set_ashita_exe(self):
        exe_path, _ = QFileDialog.getOpenFileName(self, "Select Ashita Executable", "", "Executable Files (*.exe)")
        if exe_path:
            self.config["ashita_exe"] = exe_path
            save_config(self.config)
            QMessageBox.information(self, "Executable Set", "Ashita executable set successfully!")

    def set_windower_exe(self):
        exe_path, _ = QFileDialog.getOpenFileName(self, "Select Windower Executable", "", "Executable Files (*.exe)")
        if exe_path:
            self.config["windower_exe"] = exe_path
            save_config(self.config)
            QMessageBox.information(self, "Executable Set", "Windower executable set successfully!")
    def set_background_image(self):
        background_path = os.path.join(os.getcwd(), "assets", "images", "wallpaper.png")
        background_label = QLabel(self.central_widget)
        background_pixmap = QPixmap(background_path)

        if not background_pixmap.isNull():
            scaled_background = background_pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            background_label.setPixmap(scaled_background)
            background_label.resize(self.size())
            background_label.lower()
        else:
            QMessageBox.warning(self, "Error", f"Failed to load background image from {background_path}")

    def setup_ui(self):
        layout = QVBoxLayout(self.central_widget)

        top_layout = QHBoxLayout()
        self.add_sidebar_with_buttons(top_layout)
        layout.addLayout(top_layout)
        self.add_web_browser(layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Launcher Version: {self.launcher_version}")

    def create_button_with_image(self, image_path, callback, image_below_path, button_size=(50, 50), icon_size=(50, 50), image_below_size=(100, 40)):
        button_with_image_layout = QVBoxLayout()
        button = QPushButton()
        button.setIcon(QIcon(QPixmap(image_path)))
        button.setIconSize(QSize(*icon_size))
        button.setFixedSize(QSize(*button_size))
        button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        button.clicked.connect(callback)

        image_label = QLabel()
        image_label.setPixmap(QPixmap(image_below_path).scaled(QSize(*image_below_size), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        button_with_image_layout.addWidget(button)
        button_with_image_layout.addWidget(image_label)

        return button_with_image_layout

    def add_sidebar_with_buttons(self, layout):
        sidebar_widget = QWidget()
        grid_layout = QGridLayout()  # Make sure grid_layout is defined here
        sidebar_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        buttons = [
            ('assets/images/ashita.png', self.launch_ashita, 'assets/images/ashitatxt.png'),
            ('assets/images/windower.png', self.launch_windower, 'assets/images/windowertxt.png'),
            ('assets/images/launcher.png', self.open_login_dialog, 'assets/images/stand copy.png'),
            ('assets/images/wiki.png', self.open_wiki, 'assets/images/wikitxt.png')
        ]

        # Set button positions in the grid
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i, (image_path, callback, image_below_path) in enumerate(buttons):
            button_layout = self.create_button_with_image(
                image_path, callback, image_below_path,
                button_size=(75, 75), icon_size=(75, 75), image_below_size=(90, 60)
            )
            grid_layout.addLayout(button_layout, *positions[i])

        # Set custom margins: (left, top, right, bottom)
        grid_layout.setContentsMargins(35, 50, 0, 250)  # Adjust these values as needed

        sidebar_widget.setLayout(grid_layout)
        layout.addWidget(sidebar_widget, alignment=Qt.AlignLeft)



    def add_web_browser(self, layout):
        news_view = CustomWebEngineView()
        news_view.setUrl(QUrl("http://www.playonline.com/ff11us/info/info_top.shtml"))
        news_view.setFixedHeight(200)
        layout.addWidget(news_view)
        #grid_layout.setContentsMargins(20, 30, 0, 200)


    def launch_ashita(self):
        if self.config["ashita_exe"]:
            subprocess.Popen([self.config["ashita_exe"]])
        else:
            QMessageBox.warning(self, "Executable Not Set", "Please set the Ashita executable in Settings.")

    def launch_windower(self):
        if self.config["windower_exe"]:
            subprocess.Popen([self.config["windower_exe"]])
        else:
            QMessageBox.warning(self, "Executable Not Set", "Please set the Windower executable in Settings.")

    def open_login_dialog(self):
        login_dialog = LoginDialog(self.config, self)
        login_dialog.exec_()

    def open_wiki(self):
        webbrowser.open("https://ffxileveldown.fandom.com/wiki/FFXILevelDown_Wiki")

