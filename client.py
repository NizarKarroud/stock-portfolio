import socket

class Client:
    def __init__(self , server_ip :str , server_port : int) -> None:
        self.client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.server_port = server_port
        self.connect_server()
    
    def connect_server(self):
        try :
            self.client_socket.connect((self.server_ip , self.server_port))
            self.connected = True
        except ConnectionRefusedError as err :
            self.connected = False
            raise ConnectionRefusedError(f"Could not connect to server at {self.server_ip}:{self.server_port}")

        
    def login_request(self , id : int , password : str):
        if not id.isdigit() :
            return "Error: ID must be an integer."
        
        if self.connected :
            self.login_msg = f"login id : {id} password : {password.strip()}"
            try :
                self.client_socket.sendall(self.login_msg.encode("utf-8"))
                self.login_response = self.client_socket.recv(1024).decode("utf-8")  
                if self.login_response !=  "Login request accepted":
                    return self.login_response                                                                   
                else :
                    return  "Login request accepted"      
            except Exception as err:
                return err
            
    def fetch_stocks_request(self):
        if self.connected :
            self.fetch_stocks_msg = "fetch stocks"
            try :
                self.client_socket.sendall(self.fetch_stocks_msg.encode("utf-8"))
                self.data_len = self.client_socket.recv(1024).decode("utf-8")
                if self.data_len :
                    self.fetch_stocks_response = self.client_socket.recv(int(self.data_len)).decode("utf-8")  
                    return self.fetch_stocks_response         
            except Exception as err:
                return err
            
    def fetch_owned_stocks(self, id : int):
        if self.connected :
            self.fetched_owned_msg = f"fetch owned id : {id}"
        try :
            self.client_socket.sendall(self.fetched_owned_msg.encode("utf-8"))
            self.data_len = self.client_socket.recv(1024).decode("utf-8")
            if self.data_len :
                self.fetch_owned_response = self.client_socket.recv(int(self.data_len)).decode("utf-8")  
                return self.fetch_owned_response         
        except Exception as err:
                return err
        
    def fetch_profile(self , id :int):
        if self.connected :
            self.fetch_profile_msg = f"fetch profile id : {id}"
        try :
            self.client_socket.sendall(self.fetch_profile_msg.encode("utf-8"))
            self.data_len = self.client_socket.recv(255).decode("utf-8")
            if self.data_len :
                self.fetch_profile_response = self.client_socket.recv(int(self.data_len)).decode("utf-8")  
                return self.fetch_profile_response         
        except Exception as err:
                return err
    
    def fetch_owned_number(self, id : int):
        if self.connected :
            self.fetch_owned_number_msg = f"owned number id : {id}"
        try :
            self.client_socket.sendall(self.fetch_owned_number_msg.encode("utf-8"))
            self.fetch_owned_number_response = self.client_socket.recv(1024).decode("utf-8")  
            return self.fetch_owned_number_response         
        except Exception as err:
                return err            
            
if __name__ == "__main__":
    client = Client("127.0.0.1" , 50000)
    client.connect_server()