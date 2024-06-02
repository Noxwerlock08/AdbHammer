import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget,
                             QFileDialog, QInputDialog, QHBoxLayout, QLineEdit, QLabel, QGridLayout, QScrollArea)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class ADBGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ADB Commander')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('/src/androide.png'))

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollWidget)

        self.gridLayout = QGridLayout()
        self.scrollLayout.addLayout(self.gridLayout)

        self.scrollArea.setWidget(self.scrollWidget)
        self.layout.addWidget(self.scrollArea)

        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(QFont("Courier", 10))
        self.layout.addWidget(self.textEdit)

        self.packageLabel = QLabel("Package Name:", self)
        self.packageInput = QLineEdit(self)
        self.packageInput.setPlaceholderText("Enter package name here")

        packageLayout = QHBoxLayout()
        packageLayout.addWidget(self.packageLabel)
        packageLayout.addWidget(self.packageInput)

        self.scrollLayout.addLayout(packageLayout)

        # Buttons
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
            button.setStyleSheet("padding: 10px;")
            self.gridLayout.addWidget(button, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

    def run_adb_command(self, command):
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            error = result.stderr

            if output:
                self.textEdit.append("Output:\n" + output)
            if error:
                self.textEdit.append("Error:\n" + error)
        except Exception as e:
            self.textEdit.append("Exception:\n" + str(e))

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
        self.run_adb_command('adb shell screencap /sdcard/screenshot.png')
        self.run_adb_command('adb pull /sdcard/screenshot.png /src/screenshot.png.')
        self.textEdit.append("Screenshot saved as screenshot.png in the current directory.")

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
