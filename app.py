import sys 
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication ,QMainWindow , QWidget , QVBoxLayout , QLabel , QLineEdit , QPushButton , QSpacerItem, QSizePolicy
from PyQt5.QtGui import  QIcon 

class HyperlinkLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("color: #000000; text-decoration: underline; font-size: 16px;")  
        self.setAlignment(Qt.AlignRight)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:  
            self.clicked()  

    def clicked(self):
        print("Hyperlink clicked!")  # Define your action here


class BourseApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Bourse")
        self.setGeometry(100, 100, 1024 , 768)
        self.setStyleSheet("background-color: #355C7D ; color: #FFFFFF; font-family: Arial, sans-serif;")
        self.login_page = LoginPage(self)
        self.setCentralWidget(self.login_page)

    def closeEvent(self, event):
        event.accept()

class LoginPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

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
                color: #000000;  /* Set text color to black */
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
                color: #000000;  /* Set text color to black */
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.ico'))

    sniffer_app = BourseApp()
    sniffer_app.show()
    sys.exit(app.exec_())
