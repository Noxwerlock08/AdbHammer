import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFileDialog, QInputDialog, QHBoxLayout, QLineEdit, QLabel

class ADBGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ADB GUI')
        self.setGeometry(100, 100, 800, 600)
        
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout(self.centralWidget)
        
        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)
        
        self.packageLabel = QLabel("Package Name:", self)
        self.packageInput = QLineEdit(self)
        self.packageInput.setPlaceholderText("Enter package name here")
        
        packageLayout = QHBoxLayout()
        packageLayout.addWidget(self.packageLabel)
        packageLayout.addWidget(self.packageInput)
        
        self.layout.addLayout(packageLayout)
        
        self.buttonConnect = QPushButton('Connect Device', self)
        self.buttonConnect.clicked.connect(self.connect_device)
        self.layout.addWidget(self.buttonConnect)
        
        self.buttonListFiles = QPushButton('List Files', self)
        self.buttonListFiles.clicked.connect(self.list_files)
        self.layout.addWidget(self.buttonListFiles)
        
        self.buttonInstallAPK = QPushButton('Install APK', self)
        self.buttonInstallAPK.clicked.connect(self.install_apk)
        self.layout.addWidget(self.buttonInstallAPK)
        
        self.buttonScreenshot = QPushButton('Capture Screenshot', self)
        self.buttonScreenshot.clicked.connect(self.capture_screenshot)
        self.layout.addWidget(self.buttonScreenshot)
        
        self.buttonReboot = QPushButton('Reboot Device', self)
        self.buttonReboot.clicked.connect(self.reboot_device)
        self.layout.addWidget(self.buttonReboot)
        
        self.buttonPushFile = QPushButton('Push File', self)
        self.buttonPushFile.clicked.connect(self.push_file)
        self.layout.addWidget(self.buttonPushFile)
        
        self.buttonPullFile = QPushButton('Pull File', self)
        self.buttonPullFile.clicked.connect(self.pull_file)
        self.layout.addWidget(self.buttonPullFile)
        
        self.buttonDeviceInfo = QPushButton('Device Info', self)
        self.buttonDeviceInfo.clicked.connect(self.device_info)
        self.layout.addWidget(self.buttonDeviceInfo)

        # New ADB Features
        self.buttonUninstallApp = QPushButton('ADB Uninstall App', self)
        self.buttonUninstallApp.clicked.connect(self.uninstall_app)
        self.layout.addWidget(self.buttonUninstallApp)

        self.buttonKillApp = QPushButton('ADB Kill App', self)
        self.buttonKillApp.clicked.connect(self.kill_app)
        self.layout.addWidget(self.buttonKillApp)

        self.buttonStartApp = QPushButton('ADB Start App', self)
        self.buttonStartApp.clicked.connect(self.start_app)
        self.layout.addWidget(self.buttonStartApp)

        self.buttonRestartApp = QPushButton('ADB Restart App', self)
        self.buttonRestartApp.clicked.connect(self.restart_app)
        self.layout.addWidget(self.buttonRestartApp)

        self.buttonClearAppData = QPushButton('ADB Clear App Data', self)
        self.buttonClearAppData.clicked.connect(self.clear_app_data)
        self.layout.addWidget(self.buttonClearAppData)

        self.buttonClearAppDataRestart = QPushButton('ADB Clear App Data and Restart', self)
        self.buttonClearAppDataRestart.clicked.connect(self.clear_app_data_and_restart)
        self.layout.addWidget(self.buttonClearAppDataRestart)

        self.buttonStartAppWithDebugger = QPushButton('ADB Start App With Debugger', self)
        self.buttonStartAppWithDebugger.clicked.connect(self.start_app_with_debugger)
        self.layout.addWidget(self.buttonStartAppWithDebugger)

        self.buttonRestartAppWithDebugger = QPushButton('ADB Restart App With Debugger', self)
        self.buttonRestartAppWithDebugger.clicked.connect(self.restart_app_with_debugger)
        self.layout.addWidget(self.buttonRestartAppWithDebugger)

        self.buttonGrantPermissions = QPushButton('ADB Grant Permissions', self)
        self.buttonGrantPermissions.clicked.connect(self.grant_permissions)
        self.layout.addWidget(self.buttonGrantPermissions)

        self.buttonRevokePermissions = QPushButton('ADB Revoke Permissions', self)
        self.buttonRevokePermissions.clicked.connect(self.revoke_permissions)
        self.layout.addWidget(self.buttonRevokePermissions)

        self.buttonEnableWiFi = QPushButton('ADB Enable Wi-Fi', self)
        self.buttonEnableWiFi.clicked.connect(self.enable_wifi)
        self.layout.addWidget(self.buttonEnableWiFi)

        self.buttonDisableWiFi = QPushButton('ADB Disable Wi-Fi', self)
        self.buttonDisableWiFi.clicked.connect(self.disable_wifi)
        self.layout.addWidget(self.buttonDisableWiFi)

        self.buttonEnableMobileData = QPushButton('ADB Enable Mobile Data', self)
        self.buttonEnableMobileData.clicked.connect(self.enable_mobile_data)
        self.layout.addWidget(self.buttonEnableMobileData)

        self.buttonDisableMobileData = QPushButton('ADB Disable Mobile Data', self)
        self.buttonDisableMobileData.clicked.connect(self.disable_mobile_data)
        self.layout.addWidget(self.buttonDisableMobileData)

    def run_adb_command(self, command):
        try:
            # Ejecutar el comando ADB y capturar la salida y los errores
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout
            error = result.stderr
            
            # Mostrar la salida y los errores en el textEdit
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
        self.run_adb_command('adb pull /sdcard/screenshot.png .')
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

