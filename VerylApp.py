import sys
import os
import shutil
import zipfile
import urllib.request
import json
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QInputDialog,
    QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

APP_NAME = "VerylApp"
GITHUB_API_URL = "https://api.github.com/repos/ondrablaha2000-cell/VerylApp.code/commits/master"
GITHUB_ZIP_URL = "https://github.com/ondrablaha2000-cell/VerylApp.code/archive/refs/heads/master.zip"

VERSIONS = ["v1.0.0 (Stable)", "v1.1.0-dev (Development)", "v2.0.0-alpha (Experimental)"]

def get_install_dir():
    if sys.platform == "win32":
        base_dir = Path(os.getenv("APPDATA", Path.home()))
    else:
        base_dir = Path.home() / ".local" / "share"
    
    install_path = base_dir / APP_NAME
    install_path.mkdir(parents=True, exist_ok=True)
    return install_path

STYLE_SHEET = """
    QWidget {
        background-color: #18181b;
        color: #f4f4f5;
        font-family: "Segoe UI", Arial;
    }
    QLabel#logo { font-size: 26px; font-weight: 700; }
    QLabel#subtitle { color: #a1a1aa; font-size: 13px; }
    QProgressBar {
        background-color: #27272a;
        border: none;
        border-radius: 6px;
        height: 10px;
    }
    QProgressBar::chunk {
        background-color: #8b5cf6;
        border-radius: 6px;
    }
"""

class UpdateWorker(QThread):
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def run(self):
        try:
            install_dir = get_install_dir()
            commit_file = install_dir / "commit.txt"
            
            self.status_signal.emit("Checking GitHub repository...")
            
            req = urllib.request.Request(
                GITHUB_API_URL, 
                headers={"User-Agent": "VerylApp-Updater"}
            )
            
            remote_sha = None
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    remote_sha = data.get("sha")
            except Exception:
                pass

            self.status_signal.emit("Downloading latest code from GitHub...")
            
            for item in install_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()

            zip_path = install_dir / "repo.zip"
            urllib.request.urlretrieve(GITHUB_ZIP_URL, zip_path)

            self.status_signal.emit("Extracting files...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(install_dir)

            if zip_path.exists():
                zip_path.unlink()

            if remote_sha:
                commit_file.write_text(remote_sha)

            # 🚀 Run the .bat script if present
            self.status_signal.emit("Executing setup script (.bat)...")
            bat_files = list(install_dir.rglob("*.bat"))
            if bat_files:
                bat_path = bat_files[0]
                if sys.platform == "win32":
                    subprocess.run([str(bat_path)], cwd=str(bat_path.parent), check=True, shell=True)
                else:
                    print(f"Script {bat_path.name} skipped on non-Windows environment.")

            self.finished_signal.emit(True, "Installation complete! 🎉")

        except Exception as e:
            self.finished_signal.emit(False, f"Error: {str(e)}")


class LauncherWindow(QWidget):
    def __init__(self, is_dev_mode=False):
        super().__init__()
        self.is_dev_mode = is_dev_mode
        self.setWindowTitle(APP_NAME)
        self.setFixedSize(450, 250)
        self.setStyleSheet(STYLE_SHEET)

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        logo = QLabel(APP_NAME)
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignCenter)

        self.status = QLabel("Initializing...")
        self.status.setObjectName("subtitle")
        self.status.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 0)

        layout.addStretch()
        layout.addWidget(logo)
        layout.addWidget(self.status)
        layout.addWidget(self.progress)
        layout.addStretch()

        self.setLayout(layout)
        
        if self.is_dev_mode:
            self.status.setText("Developer Mode: Select a version to install...")
            self.progress.setRange(0, 100)
            self.progress.setValue(0)
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(500, self.select_dev_version)
        else:
            self.check_updates()

    def select_dev_version(self):
        version, ok = QInputDialog.getItem(
            self, 
            "Developer Version Select", 
            "Choose version to deploy:", 
            VERSIONS, 
            0, 
            False
        )
        if ok and version:
            self.status.setText(f"Installing {version}...")
            self.progress.setRange(0, 0)
            self.check_updates()
        else:
            self.check_updates()

    def check_updates(self):
        self.worker = UpdateWorker()
        self.worker.status_signal.connect(self.status.setText)
        self.worker.finished_signal.connect(self.on_update_finished)
        self.worker.start()

    def on_update_finished(self, updated, message):
        self.status.setText(message)
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        
        install_dir = get_install_dir()
        
        main_script = None
        for path in install_dir.rglob("*.py"):
            if path.name.lower() in ["main.py", "verylappmain.py"] and path.resolve() != Path(__file__).resolve():
                main_script = path
                break

        if main_script and main_script.exists():
            subprocess.Popen([sys.executable, str(main_script)], cwd=str(main_script.parent))
        else:
            print(f"Critical Error: No main.py or chat script found in {install_dir}")

        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    is_dev = "--dev" in sys.argv
    launcher = LauncherWindow(is_dev_mode=is_dev)
    launcher.show()
    sys.exit(app.exec_())
