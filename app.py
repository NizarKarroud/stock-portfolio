import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QHBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy)
from client import Client

class HyperlinkLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: #000000; text-decoration: underline; font-size: 16px;")  
        self.setAlignment(Qt.AlignRight)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  
            self.clicked()  

    def clicked(self):
        print("Hyperlink clicked!") 


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet("""
            QMainWindow {
                border: 2px solid #663399;  
                border-radius: 18px;
                background-color: #355C7D ; color: #FFFFFF; font-family: Arial, sans-serif;
            }
        """)

        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: #355C7D ; color: #FFFFFF; font-family: Arial, sans-serif;
                border-radius: 18px; 
            }
        """)

        layout = QVBoxLayout(self.central_widget)
        top_layout = QHBoxLayout()

        close_button = QPushButton()
        close_button.setIcon(QIcon("close.png")) 
        close_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")  
        close_button.clicked.connect(self.close)  
        top_layout.addStretch()  
        top_layout.addWidget(close_button)

        layout.addLayout(top_layout)

        layout.addStretch()

        self.setGeometry(100, 100, 1024 , 768)

        self.client = Client("127.0.0.1" , 50000)
        self.login_page = LoginPage(self, self.client)
        layout.addWidget(self.login_page)

        self.startPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            self.move(self.pos() + event.pos() - self.startPos)

    def mouseReleaseEvent(self, event):
        self.startPos = None

class LoginPage(QWidget):
    def __init__(self, parent , client):
        super().__init__(parent)
        self.init_ui()
        self.client = client

    def init_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.login_layout = QVBoxLayout()

        self.hyperlink_label = HyperlinkLabel("Register")

        self.login_label = QLabel("Login")
        self.login_label.setStyleSheet("font-size: 80px; font-weight: bold; margin: 20px;")
        self.login_label.setAlignment(Qt.AlignCenter) 
        self.client_id_label = QLabel("Client ID")
        self.client_id_label.setStyleSheet("font-size: 20px; margin: 10px;")
        self.client_id_label.setAlignment(Qt.AlignCenter)  

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.vertical_login_spacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.horizontal_login_spacer = QSpacerItem(40, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Enter Your ID")
        self.client_id_input.setFixedSize(250, 40)
        self.client_id_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 10px;
                background-color: #FFFFFF;
                color: #000000; 
                font-size: 16px;
            }
        """)
        self.client_id_input.setAlignment(Qt.AlignCenter)

        self.password_label = QLabel("Password")
        self.password_label.setStyleSheet("font-size: 20px; margin: 10px;")
        self.password_label.setAlignment(Qt.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Your password")
        self.password_input.setFixedSize(250, 40)
        self.password_input.setEchoMode(QLineEdit.Password)  
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #555555;
                border-radius: 10px;
                padding: 10px;
                background-color: #FFFFFF;
                color: #000000; 
                font-size: 16px;
            }
        """)
        self.password_input.setAlignment(Qt.AlignCenter)
        
        self.login_button = QPushButton("Login") 
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #6C5B7B;
                color: #FFFFFF;
                border: 2px solid #6C5B7B;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #C06C84;
            }
            QPushButton:pressed {
                background-color: #C06C84;
            }
        """)
        self.login_button.setFixedSize(250, 40)
        self.login_button.clicked.connect(self.login)
        self.login_layout.addWidget(self.login_label)
        self.login_layout.addItem(self.vertical_login_spacer)

        self.login_layout.addWidget(self.client_id_label)
        self.login_layout.addWidget(self.client_id_input)
        self.login_layout.addWidget(self.password_label)
        self.login_layout.addWidget(self.password_input)
        self.login_layout.addItem(self.vertical_spacer)
        self.login_layout.addWidget(self.login_button)

        self.login_layout.addItem(self.horizontal_login_spacer)
        self.login_layout.addWidget(self.hyperlink_label)
        
        self.main_layout.addLayout(self.login_layout)
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.main_layout)

    def login(self) :
        self.client.login_request(self.client_id_input.text() , self.password_input.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
