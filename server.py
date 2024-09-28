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
        
    async def handle_client(self ,client_socket, client_address):
            await asyncio.sleep(5)
    
    async def accept_connections(self):
        loop = asyncio.get_running_loop()

        while True:
            try:
                client_socket, client_address = await loop.run_in_executor(
                    None, self.server_socket.accept
                )
                asyncio.create_task(self.handle_client(client_socket, client_address))  
                tasks = asyncio.all_tasks()
                print(f"Current coroutines in the loop: {len(tasks)}")
                for task in tasks:
                    print(task)
            except Exception as e:
                print(e)


if __name__ == "__main__":

    server = AsyncServer("127.0.0.1" ,50000 )
    asyncio.run(server.accept_connections())