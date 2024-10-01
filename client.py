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
            print(err)

    def login_request(self , id : int , password : str):
        if self.connected :
            self.login_msg = f"login id : {id} password : {password.strip()}"
            print(self.login_msg)
            try :
                self.client_socket.sendall(self.login_msg.encode("utf-8"))
                self.login_response = self.client_socket.recv(1024).decode("utf-8")  
                """login request denied no match found
                    login request accepted   """
                print(self.login_response )                                                                        
                
            except Exception as err:
                return err
            
    def fetch_stocks_request(self):
        pass

    def fetch_owned_stocks(self):
        pass

    def fetch_profile(self):
        pass
if __name__ == "__main__":
    client = Client("127.0.0.1" , 50000)
    client.connect_server()