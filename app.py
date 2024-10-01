import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QHBoxLayout, 
QLabel, QLineEdit, QSpacerItem, QSizePolicy , QDialog , QStackedWidget , QTabWidget , QTableWidget ,QTableWidgetItem , QHeaderView )
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
        print("Hyperlink clicked") 

class ErrorDialog(QDialog):
    def __init__(self, message,parent=None ):
        super(ErrorDialog, self).__init__(parent)

        self.setWindowTitle("Error")
        self.setFixedSize(300, 150) 
                
        self.setStyleSheet("""
            QDialog {
                background-color: #000000;  
            }
            QLabel {
                color: #FF0000;              
                font-size: 14px;           
                padding: 10px;             
            }
        """)

        layout = QVBoxLayout()

        label = QLabel(message)  
        label.setWordWrap(True) 
        layout.addWidget(label)

        self.setLayout(layout)
        self.exec_()

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  

        self.login_widget = QWidget(self)
        self.setCentralWidget(self.login_widget)

        self.setStyleSheet("""
            QMainWindow {
                border: 2px solid #663399;  
                border-radius: 18px;
                background-color: #363636 ; color: #FFFFFF; font-family: Arial, sans-serif;
            }
        """)

        self.login_widget.setStyleSheet("""
            QWidget {
                background-color: #363636 ; color: #FFFFFF; font-family: Arial, sans-serif;
                border-radius: 18px; 
            }
        """)

        self.layout = QVBoxLayout(self.login_widget)
        self.top_layout = QHBoxLayout()


        self.close_button = QPushButton()
        self.close_button.setIcon(QIcon("close.png")) 
        self.close_button.setStyleSheet("QPushButton { background-color: transparent; border: none; }")  
        self.close_button.clicked.connect(self.close)  
        

        self.top_layout.addStretch()  
        self.top_layout.addWidget(self.close_button)

        self.layout.addLayout(self.top_layout)

        self.layout.addSpacing(10) 


        self.setGeometry(100, 100, 1024 , 768)
        try :
            self.client = Client("127.0.0.1" , 50000)
        except ConnectionRefusedError as e :
            ErrorDialog(e , self)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        self.login_page = LoginPage(self, self.client)
        self.stacked_widget.addWidget(self.login_page)

        self.dashboard = DashboardPage(self , self.client , self.login_page.logged)
        self.stacked_widget.addWidget(self.dashboard)

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
        self.logged = False
        self.init_ui()
        self.client = client
        self.parent = parent
        
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
                background-color: #E8175D;
                color: #FFFFFF;
                border: 2px solid #E8175D;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #CC527A;
            }
            QPushButton:pressed {
                background-color: #CC527A;
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
        validation = self.client.login_request(self.client_id_input.text() , self.password_input.text())
        if validation == True:
            self.parent.stacked_widget.setCurrentWidget(self.parent.dashboard) 
            self.logged = True
        else :
            ErrorDialog(validation, self.parent)

class DashboardPage(QWidget):
    def __init__(self, parent , client , logged):
        super().__init__(parent)
        self.client = client
        self.tabs = QTabWidget()
        self.logged = logged
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #E8175D;
                color: #FFFFFF;
                padding: 10px 30px;
                border: 2px solid #555555;
                border-radius: 10px;
                font-size: 16px;
                min-width: 150px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #CC527A;
            }
            QTabBar::tab:hover {
                background: #CC527A;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
                top: 20px ;
            }
        """)

        self.stocks_tab = StocksTab(self.client ,self)
        self.tabs.addTab(self.stocks_tab, "Stocks")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class StocksTab(QWidget):
    def __init__(self, client, parent=None):
        super(StocksTab, self).__init__(parent)
        self.client = client
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            /* Table Header */
            QHeaderView::section {
                background-color: #E8175D; 
                color: #FFFFFF;           
                padding: 8px;              
                font-size: 14px;          
                border: 1px solid #555555; 
            }

            /* Table Cells */
            QTableWidget::item {
                background-color: #F7CAC9; 
                color: #000000;           
                padding: 5px;             
                border: none;             
            }

            /* Alternating Row Colors */
            QTableWidget::item:alternate {
                background-color: #F5E1D2; 
            }

            /* Hovered Cell */
            QTableWidget::item:hover {
                background-color: #CC527A; 
                color: #FFFFFF;           
            }

            /* Selected Cell */
            QTableWidget::item:selected {
                background-color: #CC527A; 
                color: #FFFFFF;           
            }

            /* Grid Line */
            QTableWidget {
                gridline-color: #555555;   /* Color of the grid lines */
            }
        """)

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(["Stock ID", "Entity", "Number", "Price" , "Action"])
        self.update_button = QPushButton("Update Stocks")
        self.update_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #A8A7A7 ;
                border-radius: 15px;
                padding: 10px;
                background-color: #A8A7A7;
                color: #000000;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #151D20;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background-color: #151D20;
            }
        """)
        self.update_button.clicked.connect(self.populate_table)

        if parent.logged :
            self.populate_table()

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.update_button)
        self.setLayout(layout)
    

    def populate_table(self):
        data = self.client.fetch_stocks_request()  
        self.table.setRowCount(len(data))  

        for row_index, (index, row) in enumerate(data.iterrows()):  
            for column_index, item in enumerate(row):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(item)))  
            buy_button = QPushButton("Buy")
            buy_button.clicked.connect(lambda checked, row=row_index: self.buy_stock(row_index)) 
            self.table.setCellWidget(row_index, 4, buy_button)  

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
