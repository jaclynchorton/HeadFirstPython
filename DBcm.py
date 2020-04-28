import mysql.connector


class UseDatabase:
    #The optional "None" annotation confirms that this method has no return value and the colon terminates the "def" line
    def __init__(self, config: dict) -> None: #Dunder "init" accepts a single dictionary, which we're calling "config

        self.configuration = config #The value of the "config" argument is assigned to an attribute called "configuration"

    def __enter__(self) -> 'cursor': #This annotation tells users of this class what they can expect to be returned from this method
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None: #This annotation confirms that this method has no return value; such annotations are optional but are good practice.
        self.conn.commit()
        self.cursor.close()
        self.conn.close() #The previously used attributes are used to commit unsaved data, as well as close the cursor and connection. 
        
