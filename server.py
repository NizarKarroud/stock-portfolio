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
            'sell': (re.compile(r'sell id\s*:\s*(\S+)\s*stockid\s*:\s*(\S+)\s*number\s*:\s*(\S+)'), self.requests_references['sell']),
            'buy': (re.compile(r'buy id\s*:\s*(\S+)\s*stockid\s*:\s*(\S+)\s*number\s*:\s*(\S+)'), self.requests_references['buy']),
            "owned number": (re.compile(r'owned number id\s*:\s*(\S+)'), self.requests_references["owned number"])
        }

    def parse_message(self, message):
        for message_type, (pattern, func) in self.messages_patterns.items():
            match = pattern.match(message)
            if match:
                arguments = match.groups()
                response = func(arguments) if arguments else func()
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
                server_response = self.parse_message(message).encode("utf-8")
                if "fetch" in message:
                    client_socket.sendall(f"{len(server_response)}".encode("utf-8"))
                client_socket.sendall(server_response)
                logging.info(f"Sent response of {len(server_response)} bytes")

        except Exception as err:
            logging.error(f"Error handling client: {err}")
        finally:
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

    def validate_login(self, arguments):
        id, password = arguments
        try: 
            self.database_cursor.execute(f"SELECT password FROM client WHERE idclient={id}")
            result = self.database_cursor.fetchone()  
            if result and password == result[0]:
                logging.info(f"Login successful for user ID: {id}")
                return "Login request accepted"
            else: 
                logging.warning(f"Login denied for user ID: {id} - No match found")
                return "Login request denied : no match found"                        
        except Exception as err:
            logging.error(f"Error validating login for ID {id}: {err}")
            return "Login request failed"

    def buy_request(self, arguments):
        logging.info(f"Buy request with arguments: {arguments}")
        return "Buy request processed"

    def sell_request(self, arguments):
        logging.info(f"Sell request with arguments: {arguments}")
        return "Sell request processed"

    def fetch_profile(self, arguments):
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

    def owned_number(self, arguments):
        id = arguments[0]
        try:
            self.database_cursor.execute(f"SELECT COUNT(*) FROM actions_client WHERE idclient={id};")
            number = self.database_cursor.fetchone()
            logging.info(f"Number of owned stocks for user ID {id}: {number[0]}")
            return str(number[0])
        except Exception as err:
            logging.error(f"Error counting owned stocks for ID {id}: {err}")

    def fetch_owned(self, arguments):
        id = arguments[0]
        try:
            self.database_cursor.execute(f"SELECT * FROM owned_stocks WHERE idclient={id};")
            owned_stocks = self.database_cursor.fetchall()
            logging.info(f"Fetched owned stocks for user ID {id}")
            return owned_stocks
        except Exception as err:
            logging.error(f"Error fetching owned stocks for ID {id}: {err}")

if __name__ == "__main__":
    server = AsyncServer("127.0.0.1", 50000)
    asyncio.run(server.accept_connections())
