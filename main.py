# main.py

import sys
from PyQt5.QtWidgets import QApplication
from loading_screen import LoadingScreen
from Level_Down_Launcher import LauncherMainWindow

class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loading_screen = LoadingScreen()
        self.check_for_updates()

    def check_for_updates(self):
        self.loading_screen.show()
        self.loading_screen.start_update_check(self.launch_main_window)

    def launch_main_window(self):
        self.loading_screen.close()
        self.main_window = LauncherMainWindow()
        self.main_window.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app_manager = ApplicationManager()

