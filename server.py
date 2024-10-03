import asyncio
import socket
import re
import logging
from database import MySQL_connection
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AsyncServer:
    def __init__(self, ip, port) -> None:
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()
        self.database_object = MySQL_connection()
        self.database_cursor = self.database_object.cursor
        self.database_connection = self.database_object.connection   
        self.active_sessions = {}

        self.requests_references = {
            "login": self.validate_login,
            "buy": self.buy_request,
            "sell": self.sell_request,
            "fetch profile": self.fetch_profile,
            "fetch stocks": self.fetch_stocks,
            "fetch owned": self.fetch_owned,
            "owned number": self.owned_number
        }

        self.messages_patterns = {
            'login': (re.compile(r'login id\s*:\s*(\S+)\s*password\s*:\s*(\S+)'), self.requests_references['login']),
            'fetch_stocks': (re.compile(r'fetch stocks'), self.requests_references['fetch stocks']),
            'fetch_profile': (re.compile(r'fetch profile id\s*:\s*(\S+)'), self.requests_references['fetch profile']),
            'fetch_owned': (re.compile(r'fetch owned id\s*:\s*(\S+)'), self.requests_references['fetch owned']),
            'sell': (re.compile(r'sell id\s*:\s*(\S+)\s*stockid\s*:\s*(\S+)\s*number\s*:\s*(\S+)\s*entity\s*:\s*(.+?)\s*price\s*:\s*(\S+)'), self.requests_references['sell']),
            'buy': (re.compile(r'buy id\s*:\s*(\S+)\s*stockid\s*:\s*(\S+)\s*number\s*:\s*(\S+)\s*price\s*:\s*(\S+)'), self.requests_references['buy']),
            "owned number": (re.compile(r'owned number id\s*:\s*(\S+)'), self.requests_references["owned number"])
        }

    def parse_message(self, message , client_socket):
        for message_type, (pattern, func) in self.messages_patterns.items():
            match = pattern.match(message)
            if match:
                arguments = match.groups()
                response = func(arguments , client_socket) if arguments else func()
                return response
        logging.warning(f"Unknown message format: {message}")
        return "Unknown command"

    async def handle_client(self, client_socket , client_address):
        loop = asyncio.get_running_loop()
        try: 
            logging.info("Handling new client connection")
            while True:
                data = await loop.run_in_executor(None, client_socket.recv, 1024)
                if not data:
                    break 
                message = data.decode("utf-8")
                logging.info(f"Received message: {message}")
                server_response = self.parse_message(message , client_socket).encode("utf-8")
                if "fetch" in message:
                    client_socket.sendall(f"{len(server_response)}".encode("utf-8"))
                client_socket.sendall(server_response)
                logging.info(f"Sent response of {len(server_response)} bytes")

        except Exception as err:
            logging.error(f"Error handling client: {err}")
        finally:
            for key in self.active_sessions.keys():
                if self.active_sessions[key] == client_socket:
                    del  self.active_sessions[key]
                    break            
            client_socket.close()
            logging.info(f"Closed connection with client {client_address}")
    
    async def accept_connections(self):
        loop = asyncio.get_running_loop()
        while True:
            try:
                logging.info("Waiting for new client connections")
                client_socket, client_address = await loop.run_in_executor(None, self.server_socket.accept)
                logging.info(f"Accepted connection from {client_address}")
                asyncio.create_task(self.handle_client(client_socket , client_address))  
            except Exception as err:
                logging.error(f"Error accepting connections: {err}")

    def validate_login(self, arguments , client_socket):
        id, password = arguments
        try:
            if id in self.active_sessions:
                logging.warning(f"Login denied for user ID {id}: User is already logged in on another connection.")
                return "Login request denied: User is already logged in."

            self.database_cursor.execute(f"SELECT password FROM client WHERE idclient={id}")
            result = self.database_cursor.fetchone()  
            if result and password == result[0] :
                print("here")
                self.active_sessions[id] = client_socket
                print("here2")
                logging.info(f"Login successful for user ID: {id}")
                return "Login request accepted"
            else: 
                logging.warning(f"Login denied for user ID: {id} - No match found")
                return "Login request denied : no match found"                        
        except Exception as err:
            logging.error(f"Error validating login for ID {id}: {err}")
            return "Login request failed"

    def buy_request(self, arguments , client_socket):
        user_id, stock_id, number, price = map(int, arguments[:])
        try :
            self.database_cursor.execute(f"SELECT nombre FROM action WHERE idaction={stock_id};")
            available_number = self.database_cursor.fetchone()
            if available_number[0] :
                self.database_cursor.execute(f"SELECT solde FROM client WHERE idclient={user_id};")
                user_balance = self.database_cursor.fetchone()
                if user_balance[0] >= price :
                    new_balance = user_balance[0] - price
                    self.database_cursor.execute(f"UPDATE client SET solde={new_balance} WHERE idclient={user_id};")
                    
                    remaining_stocks = available_number[0] - number
                    if remaining_stocks > 0:
                        self.database_cursor.execute(f"UPDATE action SET nombre={remaining_stocks} WHERE idaction={stock_id};")
                    else:
                        self.database_cursor.execute(f"UPDATE action SET nombre=0 WHERE idaction={stock_id};")
                    self.database_cursor.execute(f"SELECT nombre FROM actions_client WHERE idclient={user_id} AND idaction={stock_id};")
                    owned_stocks = self.database_cursor.fetchone()
                    
                    if owned_stocks:
                        new_owned_number = owned_stocks[0] + number
                        self.database_cursor.execute(f"UPDATE actions_client SET nombre={new_owned_number} WHERE idclient={user_id} AND idaction={stock_id};")
                    else:
                        self.database_cursor.execute(f"INSERT INTO actions_client (idclient, idaction, nombre) VALUES ({user_id}, {stock_id}, {number});")
                    
                    self.database_connection.commit()  
                    logging.info(f"Buy request successful: User {user_id} bought {number} stocks of {stock_id}")
                    return f"Buy request successful: Purchased {number} of stock {stock_id}."
                else:
                    logging.warning(f"Buy request denied: Insufficient balance for user {user_id}")
                    return "Buy request denied: Insufficient balance."
            else:
                logging.warning(f"Buy request denied: Not enough stocks available for stock {stock_id}")
                return "Buy request denied: Not enough stocks available"
    
        except Exception as err:
            logging.error(f"Error processing buy request for user {user_id}: {err}")
            self.database_connection.rollback()  
            return "Error processing buy request."
    
    def sell_request(self, arguments , client_socket):
        user_id, stock_id, number, entity,price = arguments
        price = int(price)
        sold_number = int(number)
        single_price = price // sold_number
        try :
            self.database_cursor.execute(f"SELECT nombre FROM actions_client WHERE idaction={stock_id};")
            owned_number = self.database_cursor.fetchone()
            if sold_number < owned_number[0] :
                new_owned =  owned_number[0]- sold_number
                self.database_cursor.execute(f"UPDATE actions_client SET nombre={new_owned} WHERE idclient={user_id} AND idaction={stock_id};")
            else :
                self.database_cursor.execute(f"DELETE FROM actions_client WHERE idaction={stock_id} AND idaction={stock_id};")
            
            self.database_cursor.execute(f"SELECT idaction , nombre FROM action WHERE idaction={stock_id};")
            available_stock = self.database_cursor.fetchone()
            if available_stock[0]:
                new_action_number = int(available_stock[1]) +sold_number
                self.database_cursor.execute(f"UPDATE action SET nombre={new_action_number} WHERE idaction={available_stock[0]};")
            else :
                self.database_cursor.execute(f"INSERT INTO action (idaction, nombre, prix,societe) VALUES ({stock_id},{sold_number},{single_price} , {entity});")
            self.database_cursor.execute(f"SELECT solde FROM client WHERE idclient={user_id}")
            user_solde = self.database_cursor.fetchone()
            updated_solde = int(user_solde[0]) + price
            self.database_cursor.execute(f"UPDATE client SET solde={updated_solde} WHERE idclient={user_id} ;")
            logging.info(f"Sale request successful: User {user_id} solde {sold_number} stocks of {stock_id}")
            return f"Sale request successful"
        except Exception as err:
            logging.error(f"Error processing Sale request for user {user_id}: {err}")
            self.database_connection.rollback()  
            return "Error processing sale request."

    def fetch_profile(self, arguments , client_socket):
        id = arguments[0]
        try:
            df = self.database_object.dataframe_query(f"SELECT * FROM client WHERE idclient={id}")
            data = df.to_json(orient="records")
            logging.info(f"Fetched profile data for user ID: {id}")
            return data
        except Exception as err:
            logging.error(f"Error fetching profile for ID {id}: {err}")

    def fetch_stocks(self):
        try: 
            df = self.database_object.dataframe_query("SELECT * FROM action")
            data = df.to_json(orient="records")
            logging.info("Fetched stocks data")
            return data
        except Exception as err:
            logging.error(f"Error fetching stocks: {err}")

    def owned_number(self, arguments , client_socket):
        id = arguments[0]
        try:
            self.database_cursor.execute(f"SELECT COUNT(*) FROM actions_client WHERE idclient={id};")
            number = self.database_cursor.fetchone()
            logging.info(f"Number of owned stocks for user ID {id}: {number[0]}")
            return str(number[0])
        except Exception as err:
            logging.error(f"Error counting owned stocks for ID {id}: {err}")

    def fetch_owned(self, arguments , client_socket):
        id = arguments[0]
        try:
            df = self.database_object.dataframe_query(f"SELECT idaction , nombre FROM actions_client WHERE idclient={id};")
            idactions = df['idaction'].tolist()
            idactions_str = ','.join([str(action) for action in idactions])  
            prices_df = self.database_object.dataframe_query(
                f"SELECT idaction, societe,prix FROM action WHERE idaction IN ({idactions_str});"
            )

            df = df.merge(prices_df, on='idaction', how='left') 

            owned_stocks = df.to_json(orient="records")
            print(owned_stocks)
            logging.info(f"Fetched owned stocks for user ID {id}")
            return owned_stocks
        except Exception as err:
            logging.error(f"Error fetching owned stocks for ID {id}: {err}")

if __name__ == "__main__":
    server = AsyncServer("127.0.0.1", 50000)
    asyncio.run(server.accept_connections())
