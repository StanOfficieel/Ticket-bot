import mysql.connector
import yaml

config = yaml.safe_load(open("config.yml", 'r', encoding="utf-8")).get("database")


class Database:
    """Class for easier work with database"""
    def __init__(self, print_out_state=True):
        try:
            self.get_connection()
            self.db.close()
            if print_out_state:
                print("Database connected, tables created!")
        except Exception as exc:
            if print_out_state:
                print("Something went wrong with database! See the error below:")
            print(exc)

    def get_connection(self):
        """Establish a new connection to the database"""
        self.db = mysql.connector.connect(
            host=config.get("host"),
            user=config.get("user"),
            password=config.get("password"),
            database=config.get("databaseName"),
            port=config.get("port")
        )
        self.cursor = self.db.cursor()

    def close_connection(self):
        """Close the connection with database"""
        self.cursor.close()
        self.db.close()

    def check_create_table(self, tbname, columns):
        """Handles table creation"""
        self.get_connection()
        self.cursor.execute(f"create table if not exists {tbname} ({columns});")
        self.close_connection()

    def get_boolean(self, tbname, column, id):
        """Gets true/false from the database based on the args"""
        self.get_connection()
        self.cursor.execute(f"select {column} from {tbname} where {id}=1;")
        result = self.cursor.fetchall()
        self.close_connection()
        if len(result):
            return True
        return False

    def check_contains(self, tbname, column, value):
        """Return true/false based on if the database contains specific value"""
        self.get_connection()
        self.cursor.execute(f"select * from {tbname} where {column}={value};")
        result = self.cursor.fetchall()
        self.close_connection()
        if len(result):
            return True
        return False

    def insert(self, tbname, columns, values):
        """Handles database new data insertion"""
        self.get_connection()
        self.cursor.execute(f"insert into {tbname} ({columns}) values ({values});")
        self.db.commit()
        self.close_connection()

    def get_next_auto_increment(self, tbname):
        """Gets next auto increment of certain table"""
        self.get_connection()
        self.cursor.execute(f"SHOW TABLE STATUS LIKE '{tbname}';")
        result = self.cursor.fetchone()
        self.close_connection()
        return result[10]

    def get_count(self, tbname, condition):
        """Gets count of records that match certain condition"""
        self.get_connection()
        self.cursor.execute(f"select count(*) from {tbname} where {condition}")
        result = self.cursor.fetchone()
        self.close_connection()
        return result[0]

    def get_id(self, tbname, condition):
        """Gets id of object with certain properties from the database"""
        self.get_connection()
        self.cursor.execute(f"select id from {tbname} where {condition}")
        result = self.cursor.fetchone()
        self.close_connection()
        return result[0]

    def update_data(self, tbname, column, value, condition):
        """Handles database data updating"""
        self.get_connection()
        self.cursor.execute(f"update {tbname} set {column}={value} where {condition}")
        self.db.commit()
        self.close_connection()

    def get_value_general(self, tbname, column, condition):
        """Gets some value from the database based on the given condition"""
        self.get_connection()
        self.cursor.execute(f"select {column} from {tbname} where {condition};")
        result = self.cursor.fetchone()
        self.close_connection()
        return result[0]

    def delete_value_general(self, table_name, condition):
        """Removes line from the database depending on condition"""
        self.get_connection()
        self.cursor.execute(f"delete from {table_name} where {condition}")
        self.db.commit()
        self.close_connection()
