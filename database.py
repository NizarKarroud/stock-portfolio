import mysql.connector
import pandas as pd
import warnings


class MySQL_connection:

    def __init__(self, ):
        self.__hostname = "localhost"
        self.__username = "root"
        self.__pwd = "root"
        self.__db = "bourse"
        self.__port = 3306
        self.__auth_plugin = 'mysql_native_password'

        self.connect()
        self.mysql_cursor()

    def connect(self) :
        try : 
            self.__connection = mysql.connector.connect(
                host=self.__hostname ,
                user=self.__username ,
                password=self.__pwd  , 
                port=self.__port ,
                database=self.__db, 
                auth_plugin=self.__auth_plugin)   
            self.__connected = True
        except Exception as err:
            self.__connected = False

    def mysql_cursor(self):
        try :
            if self.__connected :
                self.__cursor = self.__connection.cursor(buffered=True)
        except Exception as err : 
            pass

    def kill_connection(self) :
        if self.__connection :
            self.__connection.close()
    
    def kill_cursor(self):
        if self.__cursor:
            self.__cursor.close()

    def dataframe_query(self, query):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            self.__connection.commit()  
            return pd.read_sql_query(query, self.__connection)


    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self):
        return self.__cursor
    
    @property
    def hostname(self):
        return self.__hostname

    @property
    def username(self):
        return self.__username

    @property
    def pwd(self):
        return self.__pwd

    @property
    def port(self):
        return self.__port

    @property
    def db(self):
        return self.__db

    @property
    def auth_plugin(self):
        return self.__auth_plugin
    @property
    def connected(self):
        return self.__connected




            



