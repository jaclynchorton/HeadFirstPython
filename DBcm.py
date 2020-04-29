import mysql.connector


class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

class UseDatabase:
    #The optional "None" annotation confirms that this method has no return value and the colon terminates the "def" line
    def __init__(self, config: dict) -> None: #Dunder "init" accepts a single dictionary, which we're calling "config

        self.configuration = config #The value of the "config" argument is assigned to an attribute called "configuration"

    def __enter__(self) -> 'cursor': #This annotation tells users of this class what they can expect to be returned from this method
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise CredentialsError(err)
        

    def __exit__(self, exc_type, exc_value, exc_trace) -> None: #This annotation confirms that this method has no return value; such annotations are optional but are good practice.
        self.conn.commit()
        self.cursor.close()
        self.conn.close() #The previously used attributes are used to commit unsaved data, as well as close the cursor and connection. 
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)

        
