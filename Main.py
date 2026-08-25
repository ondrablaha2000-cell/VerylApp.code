import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QListWidget, QFrame, 
    QLabel, QListWidgetItem, QDialog, QCheckBox, QTabWidget,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont

ULTIMATE_DISCORD_STYLE = """
    QWidget {
        background-color: #313338;
        color: #dbdee1;
        font-family: "gg sans", "Segoe UI", Arial, sans-serif;
    }
    
    /* 1. SERVER SIDEBAR */
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

    /* 2. CHANNELS SIDEBAR */
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

    /* USER PANEL AT BOTTOM */
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
        font-size: 16px;
    }
    QPushButton#icon_btn:hover {
        background-color: #35373c;
        color: #dbdee1;
    }

    /* 3. MAIN CHAT AREA */
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
    QPushButton#send_btn {
        background-color: #5865f2;
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
    }
    QPushButton#send_btn:hover {
        background-color: #4752c4;
    }

    /* 4. MEMBERS SIDEBAR */
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

    /* SETTINGS DIALOG */
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

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_dialog")
        self.setWindowTitle("VerylApp Settings")
        self.resize(500, 380)
        self.setStyleSheet(ULTIMATE_DISCORD_STYLE)

        layout = QVBoxLayout(self)
        
        title = QLabel("Application Settings")
        title.setStyleSheet("font-size: 20px; font-weight: 800; color: #f2f3f5; margin-bottom: 10px;")
        layout.addWidget(title)

        tabs = QTabWidget()
        
        # General Tab
        general_tab = QWidget()
        g_layout = QVBoxLayout(general_tab)
        g_layout.addWidget(QCheckBox("Enable Desktop Notifications"))
        g_layout.addWidget(QCheckBox("Play Sound on New Message"))
        g_layout.addWidget(QCheckBox("Auto-scroll to bottom on message"))
        g_layout.addStretch()
        tabs.addTab(general_tab, "General")

        # Developer Settings Tab
        dev_tab = QWidget()
        d_layout = QVBoxLayout(dev_tab)
        
        dev_info = QLabel("Developer Tools & Mode")
        dev_info.setStyleSheet("font-size: 14px; font-weight: bold; color: #eab308;")
        d_layout.addWidget(dev_info)

        self.dev_mode_checkbox = QCheckBox("Enable Developer Mode (Verbose Logs & Console)")
        self.dev_mode_checkbox.setChecked(getattr(parent, 'is_dev_mode', False))
        d_layout.addWidget(self.dev_mode_checkbox)

        run_dev_btn = QPushButton("🚀 RUN AS DEV (Hot Reload Environment)")
        run_dev_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                font-weight: bold;
                padding: 12px;
                border: none;
                border-radius: 6px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #16a34a;
            }
        """)
        run_dev_btn.clicked.connect(self.run_as_dev_action)
        d_layout.addWidget(run_dev_btn)
        
        d_layout.addStretch()
        tabs.addTab(dev_tab, "Developer")

        layout.addWidget(tabs)

        # Close button
        close_btn = QPushButton("Save & Close")
        close_btn.setObjectName("send_btn")
        close_btn.clicked.connect(self.save_and_close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

    def run_as_dev_action(self):
        if self.parent():
            self.parent().enable_dev_mode()
        self.accept()

    def save_and_close(self):
        if self.parent():
            self.parent().is_dev_mode = self.dev_mode_checkbox.isChecked()
            self.parent().update_dev_ui()
        self.accept()


class UltimateDiscordGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dev_mode = False
        
        self.setWindowTitle("VerylApp — Discord Edition ⚡")
        self.resize(1180, 720)
        self.setStyleSheet(ULTIMATE_DISCORD_STYLE)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----------------------------------------------------
        # 1. SERVERS SIDEBAR
        # ----------------------------------------------------
        server_sidebar = QFrame()
        server_sidebar.setObjectName("server_sidebar")
        server_sidebar.setFixedWidth(72)
        server_layout = QVBoxLayout(server_sidebar)
        server_layout.setContentsMargins(0, 12, 0, 12)
        server_layout.setAlignment(Qt.AlignTop)

        btn_home = QPushButton("V")
        btn_home.setObjectName("server_btn_active")
        btn_home.setFixedSize(48, 48)

        btn_server1 = QPushButton(" Veryl ")
        btn_server1.setObjectName("server_btn")
        btn_server1.setFixedSize(48, 48)

        btn_server2 = QPushButton(" Dev ")
        btn_server2.setObjectName("server_btn")
        btn_server2.setFixedSize(48, 48)

        server_layout.addWidget(btn_home, alignment=Qt.AlignCenter)
        server_layout.addSpacing(8)
        server_layout.addWidget(btn_server1, alignment=Qt.AlignCenter)
        server_layout.addWidget(btn_server2, alignment=Qt.AlignCenter)

        # ----------------------------------------------------
        # 2. CHANNELS SIDEBAR
        # ----------------------------------------------------
        channels_sidebar = QFrame()
        channels_sidebar.setObjectName("channels_sidebar")
        channels_sidebar.setFixedWidth(240)
        channels_layout = QVBoxLayout(channels_sidebar)
        channels_layout.setContentsMargins(0, 0, 0, 0)

        server_header = QLabel("Veryl Network 🚀")
        server_header.setObjectName("server_header")

        self.channel_list = QListWidget()
        self.channel_list.setObjectName("channel_list")
        self.channel_list.addItems([
            "# welcome-and-rules", 
            "# general-chat", 
            "# dev-lounge", 
            "# bug-reports", 
            "# announcements"
        ])
        self.channel_list.setCurrentRow(1)

        # User profile bar
        user_bar = QFrame()
        user_bar.setObjectName("user_bar")
        user_bar_layout = QHBoxLayout(user_bar)
        user_bar_layout.setContentsMargins(8, 6, 8, 6)

        user_info = QVBoxLayout()
        user_info.setSpacing(0)
        
        self.user_name_label = QLabel("Ondra")
        self.user_name_label.setObjectName("user_name")
        
        self.user_tag_label = QLabel("#8520")
        self.user_tag_label.setObjectName("user_tag")
        
        user_info.addWidget(self.user_name_label)
        user_info.addWidget(self.user_tag_label)

        # Settings button (Gear Icon)
        settings_btn = QPushButton("⚙️")
        settings_btn.setObjectName("icon_btn")
        settings_btn.setFixedSize(32, 32)
        settings_btn.setToolTip("Settings & Dev Mode")
        settings_btn.clicked.connect(self.open_settings)

        user_bar_layout.addLayout(user_info)
        user_bar_layout.addStretch()
        user_bar_layout.addWidget(settings_btn)

        channels_layout.addWidget(server_header)
        channels_layout.addWidget(self.channel_list)
        channels_layout.addWidget(user_bar)

        # ----------------------------------------------------
        # 3. MAIN CHAT AREA
        # ----------------------------------------------------
        chat_area = QFrame()
        chat_layout = QVBoxLayout(chat_area)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(0)

        # Chat Header
        chat_header = QFrame()
        chat_header.setObjectName("chat_header")
        chat_header.setFixedHeight(48)
        chat_header_layout = QHBoxLayout(chat_header)
        chat_header_layout.setContentsMargins(16, 0, 16, 0)

        self.channel_title = QLabel("# general-chat")
        self.channel_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #f2f3f5;")
        
        self.dev_badge = QLabel("DEV MODE ACTIVE 🛠️")
        self.dev_badge.setStyleSheet("color: #eab308; font-weight: bold; font-size: 12px;")
        self.dev_badge.hide()

        chat_header_layout.addWidget(self.channel_title)
        chat_header_layout.addStretch()
        chat_header_layout.addWidget(self.dev_badge)

        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setObjectName("chat_display")
        self.chat_display.setReadOnly(True)
        
        self.chat_display.append("<span style='color: #23a55a; font-weight: bold;'>[System]:</span> Welcome to VerylApp Network! 🔥")
        self.chat_display.append("<b>VerylBot</b> <span style='color: #949ba4; font-size: 10px;'>Today at 18:45</span><br>Application updated to Ultimate Edition! Enjoy the new UI.<br>")

        # Input Box
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(16, 0, 16, 20)

        self.msg_input = QLineEdit()
        self.msg_input.setObjectName("msg_input")
        self.msg_input.setPlaceholderText("Message #general-chat...")
        self.msg_input.returnPressed.connect(self.send_message)

        send_btn = QPushButton("Send")
        send_btn.setObjectName("send_btn")
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(send_btn)

        chat_layout.addWidget(chat_header)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(input_container)

        # ----------------------------------------------------
        # 4. MEMBERS SIDEBAR
        # ----------------------------------------------------
        members_sidebar = QFrame()
        members_sidebar.setObjectName("members_sidebar")
        members_sidebar.setFixedWidth(210)
        members_layout = QVBoxLayout(members_sidebar)
        members_layout.setContentsMargins(0, 0, 0, 0)

        online_label = QLabel("ONLINE — 4")
        online_label.setObjectName("member_category")

        self.members_list = QListWidget()
        self.members_list.setObjectName("members_list")
        
        self.members_list.addItem(QListWidgetItem("🟢 Ondra (You)"))
        self.members_list.addItem(QListWidgetItem("🟢 VerylBot [BOT]"))
        self.members_list.addItem(QListWidgetItem("🟡 Bradar"))
        self.members_list.addItem(QListWidgetItem("🔴 DevAdmin"))
        
        members_layout.addWidget(online_label)
        members_layout.addWidget(self.members_list)

        # Assembly
        main_layout.addWidget(server_sidebar)
        main_layout.addWidget(channels_sidebar)
        main_layout.addWidget(chat_area)
        main_layout.addWidget(members_sidebar)

        self.channel_list.currentTextChanged.connect(self.change_channel)

    def change_channel(self, channel_name):
        self.channel_title.setText(channel_name)
        self.msg_input.setPlaceholderText(f"Message {channel_name}...")
        self.chat_display.append(f"<br><span style='color: #949ba4;'>--- Switched to <b>{channel_name}</b> ---</span><br>")

    def send_message(self):
        text = self.msg_input.text().strip()
        if text:
            prefix = "<span style='color: #eab308; font-weight: bold;'>[DEV]</span> " if self.is_dev_mode else ""
            self.chat_display.append(f"<b>{prefix}Ondra</b> <span style='color: #949ba4; font-size: 10px;'>Just now</span><br>{text}<br>")
            self.msg_input.clear()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def enable_dev_mode(self):
        self.is_dev_mode = True
        self.update_dev_ui()
        self.chat_display.append("<br><span style='color: #22c55e; font-weight: bold;'>[SYSTEM]: Developer Mode has been turned ON 🚀</span><br>")

    def update_dev_ui(self):
        if self.is_dev_mode:
            self.dev_badge.show()
            self.user_name_label.setText("Ondra [DEV]")
            self.user_name_label.setStyleSheet("font-weight: 700; color: #eab308; font-size: 13px;")
        else:
            self.dev_badge.hide()
            self.user_name_label.setText("Ondra")
            self.user_name_label.setStyleSheet("font-weight: 700; color: #f2f3f5; font-size: 13px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UltimateDiscordGUI()
    window.show()
    sys.exit(app.exec_())
