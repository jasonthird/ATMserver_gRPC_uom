import string
import sys
from decimal import Decimal
import random
import mariadb
import json


class Sql:
    def __init__(self):
        # get credentials from json file
        with open('sqlConfig.json') as f:
            data = json.load(f)
            self.host = data['host']
            self.user = data['user']
            self.password = data['password']
            self.database = data['database']
            self.port = int(data['port'])

    def connect(self):
        try:
            conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return e

    def dbConnectAndExecute(self, query, args):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(query, args)
            conn.commit()
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()

    def createDb(self):
        try:
            conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            cur = conn.cursor()
            cur.execute("CREATE DATABASE IF NOT EXISTS " + self.database)
            conn.commit()
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()

    def createTables(self):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username char(40) not null unique,
                    pin int not null
                    )
                        collate utf8mb3_unicode_ci;
                    """)
            cur.execute(""" 
                CREATE TABLE IF NOT EXISTS authCode (
                    owner_id int not null,
                    AuthCode char(40) null unique,
                    constraint authCode_users_null_fk
                        foreign key (owner_id) references users (id)
                )""")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS balances (
                    id       int auto_increment
                    primary key,
                    owner_id int            not null comment 'the one from users',
                    balance  decimal(13, 4) not null comment 'In euro',
                    constraint balances_users_null_fk
                        foreign key (owner_id) references users (id)
                )""")
            conn.commit()
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()

    def insertUser(self, username, pin):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, pin) VALUES (?, ?)", (username, pin))
            conn.commit()
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()

    def insertAuthCode(self, owner_id, authCode):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO authCode (owner_id, AuthCode) VALUES (?, ?)", (owner_id, authCode))
            conn.commit()
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()

    def insertBalance(self, owner_id, balance):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO balances (owner_id, balance) VALUES (?, ?)", (owner_id, balance))
            conn.commit()
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str
    def get_random_number(self, length):
        resultInt = random.randint(10**(length-1), (10**length)-1)
        return resultInt
    def getUserId(self,user):
        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = ?", (user,))
            return cur.fetchone()[0]
        except mariadb.Error as e:
            return e
        finally:
            conn.close()
    def insertTestData(self):
        try:
            conn = self.connect()
            cur = conn.cursor()
            users = dict()
            for i in range(10):
                username = "user" + self.get_random_string(5)
                pin = self.get_random_number(4)
                users[username] = pin
            for user in users:
                self.insertUser(user, users[user])
                self.insertBalance(self.getUserId(user), Decimal(self.get_random_number(4)+self.get_random_number(2)/100))
                self.insertAuthCode(self.getUserId(user), self.get_random_string(40))
                print("Inserted user: " + user + " with pin: " + str(users[user]))
            return cur
        except mariadb.Error as e:
            return e
        finally:
            conn.close()
