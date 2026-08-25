import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QListWidget, QFrame, 
    QLabel, QListWidgetItem, QScrollArea
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

DISCORD_STYLE = """
    QWidget {
        background-color: #313338;
        color: #dbdee1;
        font-family: "gg sans", "Segoe UI", Arial;
    }
    
    /* 1. Server List Sidebar */
    QFrame#server_sidebar {
        background-color: #1e1f22;
        border: none;
    }
    QPushButton#server_btn {
        background-color: #313338;
        color: #dbdee1;
        border-radius: 24px;
        font-size: 16px;
        font-weight: bold;
    }
    QPushButton#server_btn:hover {
        background-color: #5865f2;
        color: white;
        border-radius: 16px;
    }

    /* 2. Channels Sidebar */
    QFrame#channels_sidebar {
        background-color: #2b2d31;
        border: none;
    }
    QLabel#server_header {
        font-size: 15px;
        font-weight: bold;
        color: #f2f3f5;
        padding: 12px;
        border-bottom: 1px solid #1f2023;
    }
    QListWidget#channel_list {
        background-color: transparent;
        border: none;
        outline: none;
        padding: 8px;
    }
    QListWidget#channel_list::item {
        padding: 8px;
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

    /* User Bar */
    QFrame#user_bar {
        background-color: #232428;
        padding: 6px;
    }
    QLabel#user_name {
        font-weight: bold;
        color: #f2f3f5;
        font-size: 13px;
    }
    QLabel#user_tag {
        color: #949ba4;
        font-size: 11px;
    }

    /* 3. Main Chat Area */
    QFrame#chat_header {
        background-color: #313338;
        border-bottom: 1px solid #2b2d31;
    }
    QTextEdit#chat_display {
        background-color: #313338;
        border: none;
        padding: 15px;
        font-size: 14px;
    }
    QLineEdit#msg_input {
        background-color: #383a40;
        border: none;
        border-radius: 8px;
        padding: 12px 15px;
        color: #dbdee1;
        font-size: 14px;
    }
    QPushButton#send_btn {
        background-color: #5865f2;
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        padding: 10px 18px;
    }
    QPushButton#send_btn:hover {
        background-color: #4752c4;
    }

    /* 4. Members Sidebar */
    QFrame#members_sidebar {
        background-color: #2b2d31;
        border: none;
    }
    QLabel#member_category {
        color: #949ba4;
        font-size: 12px;
        font-weight: bold;
        padding: 15px 10px 5px 10px;
    }
    QListWidget#members_list {
        background-color: transparent;
        border: none;
        outline: none;
        padding: 5px;
    }
    QListWidget#members_list::item {
        padding: 6px;
        color: #949ba4;
        font-weight: 500;
    }
"""

class DiscordGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VerylApp - Discord Edition 💬")
        self.resize(1100, 680)
        self.setStyleSheet(DISCORD_STYLE)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ----------------------------------------------------
        # 1. SERVERS SIDEBAR (Nejvíc vlevo)
        # ----------------------------------------------------
        server_sidebar = QFrame()
        server_sidebar.setObjectName("server_sidebar")
        server_sidebar.setFixedWidth(72)
        server_layout = QVBoxLayout(server_sidebar)
        server_layout.setContentsMargins(0, 12, 0, 12)
        server_layout.setAlignment(Qt.AlignTop)

        # Tlačítka serverů
        btn_home = QPushButton("V")
        btn_home.setObjectName("server_btn")
        btn_home.setFixedSize(48, 48)

        btn_server1 = QPushButton(" Veryl ")
        btn_server1.setObjectName("server_btn")
        btn_server1.setFixedSize(48, 48)

        btn_server2 = QPushButton(" Dev ")
        btn_server2.setObjectName("server_btn")
        btn_server2.setFixedSize(48, 48)

        server_layout.addWidget(btn_home, alignment=Qt.AlignCenter)
        server_layout.addSpacing(10)
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

        server_header = QLabel("Veryl Community 🔥")
        server_header.setObjectName("server_header")

        self.channel_list = QListWidget()
        self.channel_list.setObjectName("channel_list")
        self.channel_list.addItems([
            "# welcome", 
            "# general", 
            "# dev-chat", 
            "# memes", 
            "# releases"
        ])
        self.channel_list.setCurrentRow(1)

        # User profile bar dole
        user_bar = QFrame()
        user_bar.setObjectName("user_bar")
        user_bar_layout = QHBoxLayout(user_bar)
        user_bar_layout.setContentsMargins(10, 8, 10, 8)

        user_info = QVBoxLayout()
        user_name = QLabel("Ondra")
        user_name.setObjectName("user_name")
        user_tag = QLabel("#8520")
        user_tag.setObjectName("user_tag")
        user_info.addWidget(user_name)
        user_info.addWidget(user_tag)

        user_bar_layout.addLayout(user_info)
        user_bar_layout.addStretch()

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

        self.channel_title = QLabel("# general")
        self.channel_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #f2f3f5;")
        chat_header_layout.addWidget(self.channel_title)

        # Chat History
        self.chat_display = QTextEdit()
        self.chat_display.setObjectName("chat_display")
        self.chat_display.setReadOnly(True)
        
        # Předpřipravené zprávy
        self.chat_display.append("<span style='color: #23a55a; font-weight: bold;'>[System]:</span> Vítej na serveru Veryl! 🚀")
        self.chat_display.append("<br><b>DevBot</b> <span style='color: #949ba4; font-size: 10px;'>dnes v 18:30</span><br>Nová verze VerylApp byla úspěšně nasazena! 🎉<br>")

        # Input Area
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(16, 0, 16, 20)

        self.msg_input = QLineEdit()
        self.msg_input.setObjectName("msg_input")
        self.msg_input.setPlaceholderText("Napiš zprávu v #general...")
        self.msg_input.returnPressed.connect(self.send_message)

        send_btn = QPushButton("Odeslat")
        send_btn.setObjectName("send_btn")
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(send_btn)

        chat_layout.addWidget(chat_header)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addWidget(input_container)

        # ----------------------------------------------------
        # 4. MEMBERS SIDEBAR (Vpravo)
        # ----------------------------------------------------
        members_sidebar = QFrame()
        members_sidebar.setObjectName("members_sidebar")
        members_sidebar.setFixedWidth(200)
        members_layout = QVBoxLayout(members_sidebar)
        members_layout.setContentsMargins(0, 0, 0, 0)

        online_label = QLabel("ONLINE — 3")
        online_label.setObjectName("member_category")

        self.members_list = QListWidget()
        self.members_list.setObjectName("members_list")
        
        # Členové
        item1 = QListWidgetItem("🟢 Ondra (You)")
        item2 = QListWidgetItem("🟢 DevBot [BOT]")
        item3 = QListWidgetItem("🟢 Bradar")
        item4 = QListWidgetItem("🔴 OfflineUser")
        
        self.members_list.addItem(item1)
        self.members_list.addItem(item2)
        self.members_list.addItem(item3)
        self.members_list.addItem(item4)

        members_layout.addWidget(online_label)
        members_layout.addWidget(self.members_list)

        # Add all to main layout
        main_layout.addWidget(server_sidebar)
        main_layout.addWidget(channels_sidebar)
        main_layout.addWidget(chat_area)
        main_layout.addWidget(members_sidebar)

        # Event connections
        self.channel_list.currentTextChanged.connect(self.change_channel)

    def change_channel(self, channel_name):
        self.channel_title.setText(channel_name)
        self.msg_input.setPlaceholderText(f"Napiš zprávu v {channel_name}...")
        self.chat_display.append(f"<br><span style='color: #949ba4;'>--- Přepnuto do kanálu <b>{channel_name}</b> ---</span><br>")

    def send_message(self):
        text = self.msg_input.text().strip()
        if text:
            self.chat_display.append(f"<b>Ondra</b> <span style='color: #949ba4; font-size: 10px;'>Právě teď</span><br>{text}<br>")
            self.msg_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiscordGUI()
    window.show()
    sys.exit(app.exec_())
