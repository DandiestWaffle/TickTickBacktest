import pymysql
from sql_client import SqlClient

class MysqlClient(SqlClient):
    """
    Sqlite client
    """
    def __init__(self, logger):
        """
        Constructor
        """
        SqlClient.__init__(self, logger)

    def connect(self, **kwargs):
        """
        Connect
        :param path: sqlite file to connect
        """
        host = kwargs['host']
        port = kwargs['port']
        user = kwargs['user']
        pwd = kwargs['pwd']
        schema = kwargs['schema']
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=pwd,
                                    db=schema,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.SSDictCursor)
        self.cursor = self.conn.cursor()
        return self.conn is not None and self.cursor is not None

    def execute(self, sql):
        """
        Execute the sql command
        :param sql: SQL command
        """
        self.cursor.execute(sql)

    def commit(self):
        """
        Commit
        """
        self.conn.commit()

    def fetchone(self):
        """
        Fetch one record
        :return Record
        """
        return self.cursor.fetchone()

    def fetchall(self):
        """
        Fetch all records
        :return Record
        """
        return self.cursor.fetchall()

    def select(self, table, columns=['*'], condition='', orderby='', limit=0, isFetchAll=True):
        """
        Select rows from the table
        :param table: Table name
        :param columns: Selected columns
        :param condition: Where condition
        :param orderby: Order by condition
        :param limit: Rows limit
        :param isFetchAll: Indicator of fetching all
        :return Result rows
        """
        ret = SqlClient.select(self, table, columns, condition, orderby, limit, isFetchAll)
        if isinstance(ret, list):
            return [list(e.values()) for e in ret]
        else:
           return ret

    def close(self):
        """
        Close connnection
        """
        self.cursor.close()
        self.conn.close()