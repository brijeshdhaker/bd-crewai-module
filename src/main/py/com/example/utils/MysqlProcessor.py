import itertools
import mysql.connector


class MysqlProcessor(object):

    connection = None

    # The init method or constructor
    def __init__(self, uuid=None):
        try:
            #
            MysqlProcessor.connection = mysql.connector.connect(
                user="operate",
                password="paSSW0rd",
                host="mysqlserver",
                port="3306",
                database="SANDBOXDB",
                autocommit=False
            )
        except Exception as e:
            # Print any error messages to stdout
            print(f"An error occurred: {e}")
        finally:
            pass
    
    #
    def insert(self, sql = None, values = None):

        if not sql:
            raise Exception("sql string is empty.")

        if not isinstance(values, list):
            raise TypeError("Only list are allowed.")

        cursor = self.connection.cursor()
        cursor.executemany(sql, values)
        self.commit()
        return cursor.rowcount

    #
    def saveAndCommit(self, sql = None, value = None):
        cursor = self.connection.cursor()
        #sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
        #value = ("John", "Highway 21")
        cursor.execute(sql, value)
        self.commit()
        print(cursor.rowcount, "record inserted.")

    #
    #@staticmethod
    def fetchOne(self, sql:str = None, isdict= False):
        if isdict :
            cursor = MysqlProcessor.connection.cursor(dictionary=True)
        else:
            cursor = MysqlProcessor.connection.cursor()
        cursor.execute(sql)
        #cursor.fetchone()
        return cursor.fetchall()[0]
    
    #
    def fetchAll(self, sql = None, isdict= False):
        if isdict :
            cursor = MysqlProcessor.connection.cursor(dictionary=True)
        else:
            cursor = MysqlProcessor.connection.cursor()
        
        cursor.execute(sql)
        return cursor.fetchall()

    #
    def execute(self, sql = None):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        _cnt = cursor.rowcount
        self.commit()
        return _cnt

    #
    def commit(self):
        # Disconnecting from the server
        self.connection.commit()

    #
    def close(self):
        # Disconnecting from the server
        self.connection.close()

    #
    def __convertAsDict(self, cursor):
        #
        _col_desc = cursor.description
        #
        column_names = [col[0] for col in _col_desc]
        results = [dict(zip(column_names, row)) for row in cursor.fetchall()]
        return results
    