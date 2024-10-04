import socket
import threading 

class Client:
    def __init__(self , server_ip :str , server_port : int) -> None:
        self.client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.connect_server()
        self.response_event = threading.Event()
        self.response_data = None  
        self.recv_thread = threading.Thread(target=self.client_recv)
        self.recv_thread.start()

    def connect_server(self):
        try:
            self.client_socket.connect((self.server_ip , self.server_port))
            self.connected = True
        except ConnectionRefusedError as err:
            self.connected = False
            raise ConnectionRefusedError(f"Could not connect to server at {self.server_ip}:{self.server_port}")

    def client_recv(self):
        """ Continuously listen for responses from the server """
        while True:
            try:
                response = self.client_socket.recv(5000).decode("utf-8")
                if response:
                    self.response_data = response
                    self.response_event.set()  
            except ConnectionError:
                break  

    def send_and_wait(self, message):
        """ Helper method to send a message and wait for the response """
        self.response_event.clear()  
        self.client_socket.sendall(message.encode("utf-8"))
        self.response_event.wait()  #wait for the event to be set , meaning a response came

        try:
            return self.response_data
        except Exception as err:
            return f"Error in fetching data: {str(err)}"
 

    def login_request(self, id: int, password: str):
        try : 
            id = int(id)
        except ValueError :
            return "Error: ID must be an integer."

        if self.connected:
            login_msg = f"login id : {id} password : {password.strip()}"
            try:
                response = self.send_and_wait(login_msg)
                if response != "Login request accepted":
                    return response
                else:
                    return "Login request accepted"
            except Exception as err:
                return str(err)

    def fetch_stocks_request(self):
        if self.connected:
            fetch_stocks_msg = "fetch stocks"
            try:
                response = self.send_and_wait(fetch_stocks_msg)
                return response
            except Exception as err:
                return str(err)

    def fetch_owned_stocks(self, id: int):
        if self.connected:
            fetch_owned_msg = f"fetch owned id : {id}"
            try:
                response = self.send_and_wait(fetch_owned_msg)
                return response
            except Exception as err:
                return str(err)

    def fetch_profile(self, id: int):
        if self.connected:
            fetch_profile_msg = f"fetch profile id : {id}"
            try:
                response = self.send_and_wait(fetch_profile_msg)
                return response
            except Exception as err:
                return str(err)

    def fetch_owned_number(self, id: int):
        if self.connected:
            fetch_owned_number_msg = f"owned number id : {id}"
            try:
                response = self.send_and_wait(fetch_owned_number_msg)
                return response
            except Exception as err:
                return str(err)

    def buy_request(self, id: int, stock_id: int, number: int, price: float):
        if self.connected:
            buy_request_msg = f"buy id : {id} stockid : {stock_id} number : {number} price : {int(price)}"
            try:
                response = self.send_and_wait(buy_request_msg)
                return response
            except Exception as err:
                return str(err)

    def sell_request(self, id: int, stock_id: int, number: int, entity: str, price: float):
        if self.connected:
            sell_request_msg = f"sell id : {id} stockid : {stock_id} number : {number} entity : {entity} price : {int(price)}"
            try:
                response = self.send_and_wait(sell_request_msg)
                return response
            except Exception as err:
                return str(err)

if __name__ == "__main__":
    client = Client("127.0.0.1", 50000)
    client.connect_server()
