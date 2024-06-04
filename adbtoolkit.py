import sys
import subprocess
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget,
                             QFileDialog, QInputDialog, QHBoxLayout, QLineEdit, QLabel, QGridLayout, QScrollArea, QTabWidget, QMenuBar, QAction)
from PyQt5.QtGui import QIcon, QFont, QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class ADBThread(QThread):
    output = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in iter(process.stdout.readline, ''):
                self.output.emit(line)
            for line in iter(process.stderr.readline, ''):
                self.output.emit(line)
            process.stdout.close()
            process.stderr.close()
            process.wait()
        except Exception as e:
            self.output.emit(f"Exception: {str(e)}\n")

class ADBGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ADB Commander')
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowIcon(QIcon('src/androide.png'))

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.createMenuBar()

        self.tabWidget = QTabWidget()
        self.layout.addWidget(self.tabWidget)

        self.commandTab = QWidget()
        self.commandLayout = QVBoxLayout(self.commandTab)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)

        self.gridLayout = QGridLayout()
        self.scrollLayout.addLayout(self.gridLayout)

        self.scrollArea.setWidget(self.scrollWidget)
        self.commandLayout.addWidget(self.scrollArea)

        self.packageLabel = QLabel("Package Name:", self)
        self.packageInput = QLineEdit(self)
        self.packageInput.setPlaceholderText("Enter package name here")

        packageLayout = QHBoxLayout()
        packageLayout.addWidget(self.packageLabel)
        packageLayout.addWidget(self.packageInput)

        self.scrollLayout.addLayout(packageLayout)

        self.tabWidget.addTab(self.commandTab, "Commands")

        self.consoleTab = QWidget()
        self.consoleLayout = QVBoxLayout(self.consoleTab)

        self.consoleInput = QLineEdit(self)
        self.consoleInput.setFont(QFont("Courier", 10))
        self.consoleInput.returnPressed.connect(self.execute_console_command)
        self.consoleLayout.addWidget(self.consoleInput)

        self.tabWidget.addTab(self.consoleTab, "Console")

        self.outputTab = QWidget()
        self.outputLayout = QVBoxLayout(self.outputTab)

        self.consoleOutput = QTextEdit(self)
        self.consoleOutput.setFont(QFont("Courier", 10))
        self.consoleOutput.setReadOnly(True)
        self.outputLayout.addWidget(self.consoleOutput)

        self.tabWidget.addTab(self.outputTab, "Output")

        self.createButtons()

        self.applyDarkMode()

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        helpMenu = menubar.addMenu('Help')

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.showAboutDialog)
        helpMenu.addAction(aboutAction)

    def showAboutDialog(self):
        aboutText = """
        ADB Commander v1.5\n
        Developed by: Noxwerlock\n
        A tool for managing Android devices using ADB.\n
        """
        self.consoleOutput.append(aboutText)

    def createButtons(self):
        buttons = [
            ('Connect Device', self.connect_device),
            ('List Files', self.list_files),
            ('Install APK', self.install_apk),
            ('Capture Screenshot', self.capture_screenshot),
            ('Reboot Device', self.reboot_device),
            ('Push File', self.push_file),
            ('Pull File', self.pull_file),
            ('Device Info', self.device_info),
            ('ADB Uninstall App', self.uninstall_app),
            ('ADB Kill App', self.kill_app),
            ('ADB Start App', self.start_app),
            ('ADB Restart App', self.restart_app),
            ('ADB Clear App Data', self.clear_app_data),
            ('ADB Clear App Data and Restart', self.clear_app_data_and_restart),
            ('ADB Start App With Debugger', self.start_app_with_debugger),
            ('ADB Restart App With Debugger', self.restart_app_with_debugger),
            ('ADB Grant Permissions', self.grant_permissions),
            ('ADB Revoke Permissions', self.revoke_permissions),
            ('ADB Enable Wi-Fi', self.enable_wifi),
            ('ADB Disable Wi-Fi', self.disable_wifi),
            ('ADB Enable Mobile Data', self.enable_mobile_data),
            ('ADB Disable Mobile Data', self.disable_mobile_data),
        ]

        row, col = 0, 0
        for btn_text, btn_method in buttons:
            button = QPushButton(btn_text, self)
            button.setFont(QFont("Arial", 10))
            button.clicked.connect(btn_method)
            button.setStyleSheet("padding: 10px; margin: 5px;")
            self.gridLayout.addWidget(button, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def applyDarkMode(self):
        dark_stylesheet = """
        QMainWindow {
            background-color: #2b2b2b;
        }
        QTextEdit, QLineEdit {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #5a5a5a;
        }
        QLabel {
            color: #ffffff;
        }
        QPushButton {
            background-color: #4a4a4a;
            color: #ffffff;
            border: 1px solid #5a5a5a;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QTabWidget::pane {
            border: 1px solid #5a5a5a;
        }
        QTabBar::tab {
            background-color: #4a4a4a;
            color: #ffffff;
            border: 1px solid #5a5a5a;
            padding: 10px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background-color: #5a5a5a;
        }
        QScrollArea {
            background-color: #2b2b2b;
        }
        """
        self.setStyleSheet(dark_stylesheet)

    def run_adb_command(self, command):
        self.thread = ADBThread(command)
        self.thread.output.connect(self.update_console_output)
        self.thread.start()

    def update_console_output(self, output):
        self.consoleOutput.append(output)
        self.consoleOutput.moveCursor(QTextCursor.End)

    def execute_console_command(self):
        command = self.consoleInput.text()
        if command:
            self.consoleInput.clear()
            self.consoleOutput.append(f"Executing: {command}\n")
            self.run_adb_command(command)

    def connect_device(self):
        self.run_adb_command('adb devices')

    def list_files(self):
        self.run_adb_command('adb shell ls /sdcard')

    def install_apk(self):
        options = QFileDialog.Options()
        apk_file, _ = QFileDialog.getOpenFileName(self, "Select APK File", "", "APK Files (*.apk);;All Files (*)", options=options)
        if apk_file:
            self.run_adb_command(f'adb install {apk_file}')

    def capture_screenshot(self):
        screenshot_dir = 'src'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        base_filename = os.path.join(screenshot_dir, 'Screenshot')
        filename = base_filename + '.png'
        index = 1
        while os.path.exists(filename):
            filename = f"{base_filename}_{index}.png"
            index += 1

        self.run_adb_command(f'adb shell screencap /sdcard/screenshot.png')
        self.run_adb_command(f'adb pull /sdcard/screenshot.png {filename}')
        self.consoleOutput.append(f"Screenshot saved as {filename}")

    def reboot_device(self):
        self.run_adb_command('adb reboot')

    def push_file(self):
        options = QFileDialog.Options()
        file_to_push, _ = QFileDialog.getOpenFileName(self, "Select File to Push", "", "All Files (*)", options=options)
        if file_to_push:
            self.run_adb_command(f'adb push {file_to_push} /sdcard/')

    def pull_file(self):
        file_to_pull, ok = QInputDialog.getText(self, 'Pull File', 'Enter the file path on the device:')
        if ok:
            self.run_adb_command(f'adb pull {file_to_pull} .')

    def device_info(self):
        self.run_adb_command('adb shell getprop')

    # New ADB Features
    def uninstall_app(self):
        package_name = self.packageInput.text()
        if package_name:
            self.run_adb_command(f'adb uninstall {package_name}')

    def kill_app(self):
        package_name = self.packageInput.text()
        if package_name:
            self.run_adb_command(f'adb shell am force-stop {package_name}')

    def start_app(self):
        package_name = self.packageInput.text()
        if package_name:
            self.run_adb_command(f'adb shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1')

    def restart_app(self):
        package_name = self.packageInput.text()
        if package_name:
            self.kill_app()
            self.start_app()

    def clear_app_data(self):
        package_name = self.packageInput.text()
        if package_name:
            self.run_adb_command(f'adb shell pm clear {package_name}')

    def clear_app_data_and_restart(self):
        self.clear_app_data()
        self.restart_app()

    def start_app_with_debugger(self):
        package_name = self.packageInput.text()
        if package_name:
            self.run_adb_command(f'adb shell am set-debug-app -w {package_name}')
            self.start_app()

    def restart_app_with_debugger(self):
        self.kill_app()
        self.start_app_with_debugger()

    def grant_permissions(self):
        package_name = self.packageInput.text()
        permission, ok = QInputDialog.getText(self, 'Grant Permission', 'Enter the permission to grant:')
        if package_name and ok:
            self.run_adb_command(f'adb shell pm grant {package_name} {permission}')

    def revoke_permissions(self):
        package_name = self.packageInput.text()
        permission, ok = QInputDialog.getText(self, 'Revoke Permission', 'Enter the permission to revoke:')
        if package_name and ok:
            self.run_adb_command(f'adb shell pm revoke {package_name} {permission}')

    def enable_wifi(self):
        self.run_adb_command('adb shell svc wifi enable')

    def disable_wifi(self):
        self.run_adb_command('adb shell svc wifi disable')

    def enable_mobile_data(self):
        self.run_adb_command('adb shell svc data enable')

    def disable_mobile_data(self):
        self.run_adb_command('adb shell svc data disable')

def main():
    app = QApplication(sys.argv)
    ex = ADBGui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

