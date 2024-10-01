import asyncio
import socket
import re
from database import MySQL_connection

class AsyncServer:
    def __init__(self , ip , port ) -> None:
        self.server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.server_socket.bind((ip,port))
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
            "fetch owned": self.fetch_owned
        }

        self.messages_patterns = {
            'login': (re.compile(r'login id\s*:\s*(\S+)\s*password\s*:\s*(\S+)'), self.requests_references['login']),
            'fetch_stocks': (re.compile(r'fetch stocks'), self.requests_references['fetch stocks']),
            'fetch_profile': (re.compile(r'fetch profile id\s*:\s*(\S+)'), self.requests_references['fetch profile']),
            'fetch_owned': (re.compile(r'fetch owned id\s*:\s*(\S+)'), self.requests_references['fetch owned']),
            'sell': (re.compile(r'sell id\s*:\s*(\S+)\s*stockid\s*:\s*(\S+)\s*number\s*:\s*(\S+)'), self.requests_references['sell']),
            'buy': (re.compile(r'buy id\s*:\s*(\S+)\s*stockid\s*:\s*(\S+)\s*number\s*:\s*(\S+)'), self.requests_references['buy'])
        }

    def parse_message(self , message):
        for message_type, (pattern, func) in self.messages_patterns.items():
            match = pattern.match(message)
            if match:
                data = match.groups()
                if data :
                    response = func(data)  
                else:
                    response = func()
                return response
        
    async def handle_client(self , client_socket):
        loop = asyncio.get_running_loop()
        try : 
            while True :
                data = await loop.run_in_executor(None, client_socket.recv, 1024)
                message = data.decode("utf-8")
                server_response = self.parse_message(message)
                client_socket.sendall(server_response.encode("utf-8"))

        except Exception as err :
            return err
        

    async def accept_connections(self):
        loop = asyncio.get_running_loop()

        while True:
            try:
                client_socket, client_address = await loop.run_in_executor(None, self.server_socket.accept)
                asyncio.create_task(self.handle_client(client_socket))  
            except Exception as e:
                print(e)

    def validate_login(self , data ):
        id , password = data
        try : 
            self.database_cursor.execute(f"SELECT password FROM client WHERE idclient ={id}")
            result = self.database_cursor.fetchone()  
            print(result)
            if result and password == result[0]:
                return "Login request accepted"
            else : 
                return "login request denied no match found"                        
        except Exception as err:
            print(f"Error: {err}")
    
    def buy_request(self , data):
        pass
   
    def sell_request(self , data):
        pass

    def fetch_profile(self , data):
        pass

    def fetch_stocks(self ):
        pass

    def fetch_owned(self , data):
        pass


if __name__ == "__main__":

    server = AsyncServer("127.0.0.1" ,50000 )
    asyncio.run(server.accept_connections())