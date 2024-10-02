import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon , QKeySequence
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,QHBoxLayout, 
QLabel, QLineEdit, QSpacerItem, QSizePolicy , QDialog , QStackedWidget , QTabWidget , QTableWidget ,QTableWidgetItem , QHeaderView , QShortcut)
from client import Client
import json

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
        self.close_button.clicked.connect(lambda : self.close_app(self))  
        

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


        self.startPos = None

    def close_app(self , app):
        try :
            self.client.client_socket.close()
            app.close()
        except Exception as err :
            ErrorDialog(err , self)
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
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Return), self) 
        self.shortcut.activated.connect(self.login)  
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
        if validation == "Login request accepted":
            self.parent.dashboard = DashboardPage(self , self.client , self.client_id_input.text() )
            self.parent.stacked_widget.addWidget(self.parent.dashboard)
            self.parent.stacked_widget.setCurrentWidget(self.parent.dashboard) 
        else :
            ErrorDialog(validation, self.parent)

class DashboardPage(QWidget):
    def __init__(self, parent , client , id):
        super().__init__(parent)
        self.client = client
        self.tabs = QTabWidget()
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
            QTabBar::tab:focus {
                outline: none;
            }
            QTabBar::tab:hover {
                background: #CC527A;
            }
            QTabWidget::pane {
                border: 1px solid #444444;
                top: 20px ;
            }
        """)

        self.stocks_tab = StocksTab(self.client , id ,self) 
        self.tabs.addTab(self.stocks_tab, "Stocks")
        
        self.sales_tab = SalesTab(self.client , id ,self) 
        self.tabs.addTab(self.sales_tab, "Sales")
        
        self.profile_tab = ProfileTab(self.client ,id , self)
        self.tabs.addTab(self.profile_tab, "Profile")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class StocksTab(QWidget):
    def __init__(self, client,id,parent=None):
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
                                 
            QScrollBar:vertical {
                border: 1px solid #555555;
                background: #2A363B;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #777777;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical {
                border: 1px solid #555555;
                background: #2A363B;
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                border: 1px solid #555555;
                background: #2A363B;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #2A363B;
            }

            QScrollBar:horizontal {
                border: 1px solid #555555;
                background: #2A363B;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background: #777777;
                border-radius: 6px;
            }
            QScrollBar::add-line:horizontal {
                border: 1px solid #555555;
                background: #2A363B;
                width: 0px;
            }
            QScrollBar::sub-line:horizontal {
                border: 1px solid #555555;
                background: #2A363B;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: #2A363B;
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

        self.populate_table()

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.update_button)
        self.setLayout(layout)
    

    def populate_table(self):
        self.table.clearContents()  
        self.table.setRowCount(0)
        data = json.loads(self.client.fetch_stocks_request())
        self.table.setRowCount(len(data))  

        for row_index , row in enumerate(data):  
            for col_index, (column,value) in enumerate(row.items()):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))  
            buy_button = QPushButton("Buy")
            buy_button.clicked.connect(lambda row=row_index: self.buy_stock(row_index)) 
            self.table.setCellWidget(row_index, 4, buy_button)  

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

    def buy_stock(self , row_index):
        pass

class SalesTab(QWidget):
    def __init__(self,  client, id, parent=None):
        super(SalesTab, self).__init__(parent)
        
class ProfileTab(QWidget):
    def __init__(self, client, id, parent=None):
        super(ProfileTab, self).__init__(parent)

        data = json.loads(client.fetch_profile(id))[0]
        owned_stocks = client.fetch_owned_number(id)

        self.profile_widget = QWidget(self)
        self.profile_widget.setFixedWidth(450)
        self.profile_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.profile_widget.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E; 
                border-radius: 15px;
                padding: 20px;
            }
        """)

        self.profile_layout = QVBoxLayout(self.profile_widget)

        self.profile_label = QLabel("Profile")
        self.id_label = QLabel(f"ID: {data['idclient']}")
        self.name_label = QLabel(f"Name: {data['nom_client']}")

        self.apply_label_styles(self.profile_label, font_size=28, color="#FFFFFF", bold=True)
        self.apply_label_styles(self.id_label, font_size=20, color="#FFFFFF", bold=False)      
        self.apply_label_styles(self.name_label, font_size=20, color="#FFFFFF", bold=False)    

        self.profile_layout.addWidget(self.profile_label, alignment=Qt.AlignCenter) 
        self.profile_layout.addWidget(self.id_label, alignment=Qt.AlignCenter)  
        self.profile_layout.addWidget(self.name_label, alignment=Qt.AlignCenter) 

        self.vertical_layout = QVBoxLayout()

        self.info_top_widget = QWidget()
        self.info_top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.info_top_widget.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E; 
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 10px;  /* Space between top and bottom widgets */
            }
        """)

        self.top_layout = QVBoxLayout(self.info_top_widget)
        self.balance_label = QLabel("Balance")
        self.balance_value_label = QLabel(f"{data['solde']} DH")

        self.apply_label_styles(self.balance_label, font_size=24, color="#FFFFFF", bold=True)  
        self.apply_label_styles(self.balance_value_label, font_size=22, color="#A0A0A0", bold=False) 

        self.top_layout.addWidget(self.balance_label, alignment=Qt.AlignCenter)  
        self.top_layout.addWidget(self.balance_value_label, alignment=Qt.AlignCenter)  

        self.info_bottom_widget = QWidget()
        self.info_bottom_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.info_bottom_widget.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E; 
                border-radius: 10px;
                padding: 20px;
            }
        """)

        self.bottom_layout = QVBoxLayout(self.info_bottom_widget)
        self.owned_title = QLabel("Owned Stocks")
        self.owned_number = QLabel(f"{owned_stocks}")

        self.apply_label_styles(self.owned_title, font_size=24, color="#FFFFFF", bold=True)  
        self.apply_label_styles(self.owned_number, font_size=22, color="#A0A0A0", bold=False)  

        self.bottom_layout.addWidget(self.owned_title, alignment=Qt.AlignCenter)  
        self.bottom_layout.addWidget(self.owned_number, alignment=Qt.AlignCenter) 

        self.vertical_layout.addWidget(self.info_top_widget)
        self.vertical_layout.addWidget(self.info_bottom_widget)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.addWidget(self.profile_widget)
        self.horizontal_spacer = QSpacerItem(40, 40, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.horizontal_layout.addItem(self.horizontal_spacer)
        self.horizontal_layout.addLayout(self.vertical_layout) 
        
        self.setLayout(self.horizontal_layout)

    def apply_label_styles(self, label, font_size=12, color="#FFFFFF", bold=False):
        """Apply styles to QLabel."""
        font_weight = "bold" if bold else "normal"
        label.setStyleSheet(f"""
            QLabel {{
                font-size: {font_size}px;
                color: {color};
                font-weight: {font_weight};
                text-align: center; 
                margin: 10px 0;  
                padding: 5px;  
            }}
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
