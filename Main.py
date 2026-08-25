import sys
import os
import shutil
import subprocess
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QListWidget, QFrame, 
    QLabel, QListWidgetItem, QDialog, QCheckBox, QTabWidget,
    QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

DEV_PASSWORD = "582011"

DISCORD_THEME = """
    QWidget {
        background-color: #313338;
        color: #dbdee1;
        font-family: "gg sans", "Segoe UI", Arial, sans-serif;
    }
    
    QFrame#server_sidebar {
        background-color: #1e1f22;
        border: none;
    }
    QPushButton#server_btn {
        background-color: #313338;
        color: #dbdee1;
        border-radius: 24px;
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#server_btn:hover {
        background-color: #5865f2;
        color: #ffffff;
        border-radius: 16px;
    }
    QPushButton#server_btn_active {
        background-color: #5865f2;
        color: #ffffff;
        border-radius: 16px;
        font-weight: bold;
    }

    QFrame#channels_sidebar {
        background-color: #2b2d31;
        border: none;
    }
    QLabel#server_header {
        font-size: 15px;
        font-weight: 800;
        color: #f2f3f5;
        padding: 14px 16px;
        border-bottom: 1px solid #1f2023;
    }
    QListWidget#channel_list {
        background-color: transparent;
        border: none;
        outline: none;
        padding: 8px;
    }
    QListWidget#channel_list::item {
        padding: 8px 10px;
        border-radius: 4px;
        color: #949ba4;
        font-weight: 600;
        margin-bottom: 2px;
    }
    QListWidget#channel_list::item:hover {
        background-color: #35373c;
        color: #dbdee1;
    }
    QListWidget#channel_list::item:selected {
        background-color: #404249;
        color: #ffffff;
    }

    QFrame#user_bar {
        background-color: #232428;
        border-top: 1px solid #1f2023;
        padding: 4px 8px;
    }
    QLabel#user_name {
        font-weight: 700;
        color: #f2f3f5;
        font-size: 13px;
    }
    QLabel#user_tag {
        color: #949ba4;
        font-size: 11px;
    }
    QPushButton#icon_btn {
        background-color: transparent;
        border: none;
        border-radius: 4px;
        color: #b5bac1;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton#icon_btn:hover {
        background-color: #35373c;
        color: #dbdee1;
    }

    QFrame#chat_header {
        background-color: #313338;
        border-bottom: 1px solid #2b2d31;
    }
    QTextEdit#chat_display {
        background-color: #313338;
        border: none;
        padding: 16px;
        font-size: 14px;
        line-height: 1.4;
    }
    QLineEdit#msg_input {
        background-color: #383a40;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        color: #dbdee1;
        font-size: 14px;
    }
    QPushButton#action_btn {
        background-color: #5865f2;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
    }
    QPushButton#action_btn:hover {
        background-color: #4752c4;
    }
    QPushButton#cancel_btn {
        background-color: #4e5058;
        border: none;
        border-radius: 6px;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
    }
    QPushButton#cancel_btn:hover {
        background-color: #6d6f78;
    }

    QFrame#members_sidebar {
        background-color: #2b2d31;
        border: none;
    }
    QLabel#member_category {
        color: #949ba4;
        font-size: 11px;
        font-weight: 700;
        padding: 16px 12px 6px 12px;
        letter-spacing: 0.5px;
    }
    QListWidget#members_list {
        background-color: transparent;
        border: none;
        outline: none;
        padding: 4px;
    }
    QListWidget#members_list::item {
        padding: 6px 8px;
        color: #949ba4;
        font-weight: 600;
        border-radius: 4px;
    }
    QListWidget#members_list::item:hover {
        background-color: #35373c;
        color: #dbdee1;
    }

    QDialog#settings_dialog {
        background-color: #313338;
    }
    QTabWidget::pane {
        border: 1px solid #2b2d31;
        background-color: #2b2d31;
        border-radius: 8px;
    }
    QTabBar::tab {
        background: #1e1f22;
        color: #949ba4;
        padding: 10px 20px;
        font-weight: bold;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
    }
    QTabBar::tab:selected {
        background: #5865f2;
        color: white;
    }
"""

def get_install_dir():
    if sys.platform == "win32":
        base_dir = Path(os.getenv("APPDATA", Path.home()))
    else:
        base_dir = Path.home() / ".local" / "share"
    return base_dir / "VerylApp"

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_dialog")
        self.setWindowTitle("Settings")
        self.resize(520, 400)
        self.setStyleSheet(DISCORD_THEME)

        layout = QVBoxLayout(self)
        
        title = QLabel("Application Settings")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #f2f3f5; margin-bottom: 10px;")
        layout.addWidget(title)

        tabs = QTabWidget()
        
        # General Settings Tab
        general_tab = QWidget()
        g_layout = QVBoxLayout(general_tab)
        self.cb_notifications = QCheckBox("Enable Desktop Notifications")
        self.cb_sounds = QCheckBox("Play Audio Notifications")
        self.cb_autoscroll = QCheckBox("Automatic Chat Scrolling")
        self.cb_autoscroll.setChecked(True)

        g_layout.addWidget(self.cb_notifications)
        g_layout.addWidget(self.cb_sounds)
        g_layout.addWidget(self.cb_autoscroll)
        g_layout.addStretch()
        tabs.addTab(general_tab, "General")

        # Developer Tab
        dev_tab = QWidget()
        d_layout = QVBoxLayout(dev_tab)
        
        dev_info = QLabel("Developer Tools & Version Control")
        dev_info.setStyleSheet("font-size: 14px; font-weight: bold; color: #f59e0b;")
        d_layout.addWidget(dev_info)

        dev_desc = QLabel("Switching to Developer Mode forces a full application reset and returns you to the installer to select custom development builds.")
        dev_desc.setWordWrap(True)
        dev_desc.setStyleSheet("color: #949ba4; font-size: 12px; margin-bottom: 10px;")
        d_layout.addWidget(dev_desc)

        run_dev_btn = QPushButton("Run in Dev Mode")
        run_dev_btn.setStyleSheet("""
            QPushButton {
                background-color: #d97706;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #b45309;
            }
        """)
        run_dev_btn.clicked.connect(self.authenticate_and_restart_dev)
        d_layout.addWidget(run_dev_btn)
        
        d_layout.addStretch()
        tabs.addTab(dev_tab, "Developer")

        layout.addWidget(tabs)

        # Dialog Buttons
        btn_box = QHBoxLayout()
        btn_box.addStretch()

        save_btn = QPushButton("Save")
        save_btn.setObjectName("action_btn")
        save_btn.clicked.connect(self.save_settings)

        close_btn = QPushButton("Close")
        close_btn.setObjectName("cancel_btn")
        close_btn.clicked.connect(self.reject)

        btn_box.addWidget(save_btn)
        btn_box.addWidget(close_btn)
        layout.addLayout(btn_box)

    def save_settings(self):
        self.accept()

    def authenticate_and_restart_dev(self):
        password, ok = QInputDialog.getText(
            self, 
            "Developer Authentication", 
            "Enter Developer Password:", 
            QLineEdit.Password
        )
        if ok and password == DEV_PASSWORD:
            QMessageBox.information(
                self, 
                "Access Granted", 
                "Authentication successful. Returning to Installer for Version Selection..."
            )
            
            # Wipe local cache to force launcher selection
            install_dir = get_install_dir()
            try:
                for item in install_dir.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            except Exception as e:
                print(f"Cleanup error: {e}")

            # Relaunch VerylApp.py launcher
            desktop_dir = Path.home() / "Desktop"
            launcher_script = desktop_dir / "VerylApp.py"

            if launcher_script.exists():
                subprocess.Popen([sys.executable, str(launcher_script), "--dev"])
            else:
                subprocess.Popen([sys.executable, "VerylApp.py", "--dev"])

            QApplication.quit()
        elif ok:
            QMessageBox.critical(self, "Access Denied", "Incorrect developer password.")


class VerylAppMain(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VerylApp")
        self.resize(1180, 720)
        self.setStyleSheet(DISCORD_THEME)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Server Sidebar
        server_sidebar = QFrame()
        server_sidebar.setObjectName("server_sidebar")
        server_sidebar.setFixedWidth(72)
        server_layout = QVBoxLayout(server_sidebar)
        server_layout.setContentsMargins(0, 12, 0, 12)
        server_layout.setAlignment(Qt.AlignTop)

        btn_home = QPushButton("V")
        btn_home.setObjectName("server_btn_active")
        btn_home.setFixedSize(48, 48)

        btn_server1 = QPushButton("Main")
        btn_server1.setObjectName("server_btn")
        btn_server1.setFixedSize(48, 48)

        server_layout.addWidget(btn_home, alignment=Qt.AlignCenter)
        server_layout.addSpacing(8)
        server_layout.addWidget(btn_server1, alignment=Qt.AlignCenter)

        # Channels Sidebar
        channels_sidebar = QFrame()
        channels_sidebar.setObjectName("channels_sidebar")
        channels_sidebar.setFixedWidth(240)
        channels_layout = QVBoxLayout(channels_sidebar)
        channels_layout.setContentsMargins(0, 0, 0, 0)

        server_header = QLabel("Veryl Network")
        server_header.setObjectName("server_header")

        self.channel_list = QListWidget()
        self.channel_list.setObjectName("channel_list")
        self.channel_list.addItems([
            "# announcements", 
            "# general", 
            "# developer-lounge", 
            "# bug-reports"
        ])
        self.channel_list.setCurrentRow(1)

        # User panel
        user_bar = QFrame()
        user_bar.setObjectName("user_bar")
        user_bar_layout = QHBoxLayout(user_bar)
        user_bar_layout.setContentsMargins(8, 6, 8, 6)

        user_info = QVBoxLayout()
        user_info.setSpacing(0)
        
        user_name_label = QLabel("Ondra")
        user_name_label.setObjectName("user_name")
        
        user_tag_label = QLabel("#8520")
        user_tag_label.setObjectName("user_tag")
        
        user_info.addWidget(user_name_label)
        user_info.addWidget(user_tag_label)

        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("icon_btn")
        settings_btn.setMinimumWidth(65)
        settings_btn.setHeight = 32
        settings_btn.clicked.connect(self.open_settings)

        user_bar_layout.addLayout(user_info)
        user_bar_layout.addStretch()
        user_bar_layout.addWidget(settings_btn)

        channels_layout.addWidget(server_header)
        channels_layout.addWidget(self.channel_list)
        channels_layout.addWidget(user_bar)

        # Main Chat Area
        chat_area = QFrame()
        chat_layout = QVBoxLayout(chat_area)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)

        chat_header = QFrame()
        chat_header.setObjectName("chat_header")
        chat_header.setFixedHeight(48)
        chat_header_layout = QHBoxLayout(chat_header)
        chat_header_layout.setContentsMargins(16, 0, 16, 0)

        self.channel_title = QLabel("# general")
        self.channel_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f2f3f5;")
        
        chat_header_layout.addWidget(self.channel_title)
        chat_header_layout.addStretch()

        self.chat_display = QTextEdit()
        self.chat_display.setObjectName("chat_display")
        self.chat_display.setReadOnly(True)
        
        self.chat_display.append("<span style='color: #22c55e; font-weight: bold;'>[System]:</span> Welcome to VerylApp Client.")
        self.chat_display.append("<b>System Bot</b> <span style='color: #949ba4; font-size: 10px;'>Today at 12:00</span><br>Application initialized successfully.<br>")

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(16, 0, 16, 20)

        self.msg_input = QLineEdit()
        self.msg_input.setObjectName("msg_input")
        self.msg_input.setPlaceholderText("Message #general...")
        self.msg_input.returnPressed.connect(self.send_message)

        send_btn = QPushButton("Send")
        send_btn.setObjectName("action_btn")
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(send_btn)

        chat_layout.addWidget(chat_header)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(input_container)

        # Members Sidebar
        members_sidebar = QFrame()
        members_sidebar.setObjectName("members_sidebar")
        members_sidebar.setFixedWidth(210)
        members_layout = QVBoxLayout(members_sidebar)
        members_layout.setContentsMargins(0, 0, 0, 0)

        online_label = QLabel("ONLINE — 3")
        online_label.setObjectName("member_category")

        self.members_list = QListWidget()
        self.members_list.setObjectName("members_list")
        
        self.members_list.addItem(QListWidgetItem("Ondra (You)"))
        self.members_list.addItem(QListWidgetItem("System Bot [BOT]"))
        self.members_list.addItem(QListWidgetItem("Administrator"))
        
        members_layout.addWidget(online_label)
        members_layout.addWidget(self.members_list)

        main_layout.addWidget(server_sidebar)
        main_layout.addWidget(channels_sidebar)
        main_layout.addWidget(chat_area)
        main_layout.addWidget(members_sidebar)

        self.channel_list.currentTextChanged.connect(self.change_channel)

    def change_channel(self, channel_name):
        self.channel_title.setText(channel_name)
        self.msg_input.setPlaceholderText(f"Message {channel_name}...")
        self.chat_display.append(f"<br><span style='color: #949ba4;'>--- Active channel changed to <b>{channel_name}</b> ---</span><br>")

    def send_message(self):
        text = self.msg_input.text().strip()
        if text:
            self.chat_display.append(f"<b>Ondra</b> <span style='color: #949ba4; font-size: 10px;'>Just now</span><br>{text}<br>")
            self.msg_input.clear()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VerylAppMain()
    window.show()
    sys.exit(app.exec_())
