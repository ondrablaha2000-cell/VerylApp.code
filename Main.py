import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QListWidget, QFrame, QLabel
)
from PyQt5.QtCore import Qt

STYLE_SHEET = """
    QWidget {
        background-color: #18181b;
        color: #f4f4f5;
        font-family: "Segoe UI", Arial;
    }
    QFrame#sidebar {
        background-color: #202023;
        border-right: 1px solid #303036;
    }
    QListWidget {
        background-color: transparent;
        border: none;
        outline: none;
    }
    QListWidget::item {
        padding: 12px;
        border-radius: 8px;
        color: #a1a1aa;
    }
    QListWidget::item:selected {
        background-color: #27272a;
        color: #f4f4f5;
        font-weight: bold;
    }
    QTextEdit {
        background-color: #202023;
        border: 1px solid #303036;
        border-radius: 10px;
        padding: 10px;
        font-size: 14px;
    }
    QLineEdit {
        background-color: #27272a;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        padding: 12px;
        color: #f4f4f5;
    }
    QPushButton {
        background-color: #8b5cf6;
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        padding: 12px 20px;
    }
    QPushButton:hover {
        background-color: #7c3aed;
    }
"""

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VerylChat GUI")
        self.resize(800, 500)
        self.setStyleSheet(STYLE_SHEET)
        
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)

        title = QLabel("Chats")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #f4f4f5;")
        sidebar_layout.addWidget(title)

        self.chat_list = QListWidget()
        self.chat_list.addItems(["# general", "# dev-room", "# random"])
        self.chat_list.setCurrentRow(0)
        sidebar_layout.addWidget(self.chat_list)

        # Main Chat Area
        chat_area = QWidget()
        chat_layout = QVBoxLayout(chat_area)
        chat_layout.setContentsMargins(20, 20, 20, 20)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.append("<b>System:</b> Vítej v chatu! 🚀")

        input_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Napiš zprávu...")
        self.msg_input.returnPressed.connect(self.send_message)

        send_btn = QPushButton("Odeslat")
        send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(send_btn)

        chat_layout.addWidget(self.chat_display)
        chat_layout.addLayout(input_layout)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(chat_area)

    def send_message(self):
        text = self.msg_input.text().strip()
        if text:
            self.chat_display.append(f"<b>You:</b> {text}")
            self.msg_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
