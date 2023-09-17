import os
from flask import Flask
import mysql.connector
import json


class DBManager:
    def __init__(self, database='outfit', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user,
            password=pf.read(),
            host=host,  # name of the MySQL service as set in the Docker Compose file
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()

    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS products')
        self.cursor.execute(
            'CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, code INT NOT NULL, date VARCHAR(10), store VARCHAR(255), product VARCHAR(255), qty INT NOT NULL, price INT NOT NULL)')
        self.cursor.execute(
            "INSERT INTO products VALUE(0, 65014, '2019-01-12', 'Shopping Morumbi', 'Aster Pants', 5, 114)")
        self.cursor.execute(
            "INSERT INTO products VALUE(0, 65014, '2019-01-12', 'Shopping Morumbi', 'Trench Coat', 1, 269)")
        self.cursor.execute(
            "INSERT INTO products VALUE(0, 65016, '2019-01-12', 'Iguatemi Campinas', 'Peter Pan Collar', 3, 363)")
        self.connection.commit()

    def query_titles(self):
        self.cursor.execute('SELECT * FROM products')
        result = self.cursor.fetchall()  # Fetch all rows from the database

        # Convert the result to a list of dictionaries
        rows = [dict(zip([column[0] for column in self.cursor.description], row))
                for row in result]

        return rows


server = Flask(__name__)
conn = None


@server.route('/')
def listBlog():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    res = conn.query_titles()

    # Convert the result to a JSON response
    return json.dumps(res)


if __name__ == '__main__':
    server.run()
