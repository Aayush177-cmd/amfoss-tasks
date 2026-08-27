import sqlite3

DATABASE_NAME = "data/berry_broker.db"


SHIP_DATA = {
        "Dinghy": {
            "health": 100,
            "attack": 10
        },
        "Going Merry": {
            "health": 300,
            "attack": 40
        },
        "Thousand Sunny": {
            "health": 600,
            "attack": 80
        }
}

def get_connection():
        connection = sqlite3.connect(DATABASE_NAME)
        connection.row_factory = sqlite3.Row
        return connection


def initialize_database():

        print("INITIALIZING DATABASE")

        connection = get_connection()
        cursor = connection.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                wallet INTEGER NOT NULL DEFAULT 500,
                bank INTEGER NOT NULL DEFAULT 0,
                bounty INTEGER NOT NULL DEFAULT 0,
                last_daily INTEGER NOT NULL DEFAULT 0,
                last_raid INTEGER NOT NULL DEFAULT 0
            )
        """)

        print("USERS TABLE CREATED")

        # Shop items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                price INTEGER,
                description TEXT
            )
        """)

        print("ITEMS TABLE CREATED")

        # Inventory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                user_id INTEGER,
                item_name TEXT,
                quantity INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, item_name)
            )
        """)

        print("INVENTORY TABLE CREATED")

        # Crews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crews (
                crew_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                captain_id INTEGER
            )
        """)

        print("CREWS TABLE CREATED")

        # Crew members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crew_members (
                crew_id INTEGER,
                user_id INTEGER,
                PRIMARY KEY (crew_id, user_id)
            )
        """)

        print("CREW MEMBERS TABLE CREATED")

        # Devil fruits table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devil_fruits (
                user_id INTEGER PRIMARY KEY,
                fruit_name TEXT
            )
        """)

        print("DEVIL FRUITS TABLE CREATED")

        # Ships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ships (
                user_id INTEGER PRIMARY KEY,
                ship_name TEXT,
                health INTEGER,
                attack INTEGER
            )
        """)

        print("SHIPS TABLE CREATED")

        connection.commit()
        connection.close()

        print("DATABASE INITIALIZATION COMPLETE")

def get_or_create_user(user_id, username):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
        )

        user = cursor.fetchone()

        if user is None:
            cursor.execute(
            """
            INSERT INTO users (user_id, username)
            VALUES (?, ?)
            """,
            (user_id, username)
            )

            connection.commit()

            cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
            )

            user = cursor.fetchone()

        connection.close()

        return user

def update_wallet(user_id, new_wallet):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET wallet = ?
            WHERE user_id = ?
            """,
            (new_wallet, user_id)
        )

        connection.commit()
        connection.close()

def update_last_daily(user_id, timestamp):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET last_daily = ?
            WHERE user_id = ?
            """,
            (timestamp, user_id)
        )

        connection.commit()
        connection.close()

def get_user(user_id):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        user = cursor.fetchone()

        connection.close()

        return user



def transfer_berries(sender_id, receiver_id, amount):

        sender = get_user(sender_id)
        receiver = get_user(receiver_id)

        sender_wallet = sender["wallet"] - amount
        receiver_wallet = receiver["wallet"] + amount

        update_wallet(sender_id, sender_wallet)
        update_wallet(receiver_id, receiver_wallet)



def initialize_shop():

        items = [
            ("Log Pose", 500, "Helps navigate the Grand Line."),
            ("Den Den Mushi", 1000, "Communication snail."),
            ("Devil Fruit", 5000, "Mysterious power.")
        ]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO items
            (name, price, description)
            VALUES (?, ?, ?)
            """,
            items
        )

        connection.commit()
        connection.close()


def get_shop_items():
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM items")

        items = cursor.fetchall()

        connection.close()

        return items


def get_item(item_name):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM items
            WHERE name = ?
            """,
            (item_name,)
        )

        item = cursor.fetchone()

        connection.close()

        return item

def add_item_to_inventory(user_id, item_name):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO inventory (user_id, item_name, quantity)
            VALUES (?, ?, 1)

            ON CONFLICT(user_id, item_name)
            DO UPDATE SET quantity = quantity + 1
            """,
            (user_id, item_name)
        )

        connection.commit()
        connection.close()


def get_inventory(user_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT item_name, quantity
            FROM inventory
            WHERE user_id = ?
            """,
            (user_id,)
        )

        items = cursor.fetchall()

        connection.close()

        return items    



def update_last_raid(user_id, timestamp):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET last_raid = ?
            WHERE user_id = ?
            """,
            (timestamp, user_id)
        )

        connection.commit()
        connection.close()

def create_crew(name, captain_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO crews(name, captain_id)
            VALUES (?, ?)
            """,
            (name, captain_id)
        )

        crew_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO crew_members(crew_id, user_id)
            VALUES (?, ?)
            """,
            (crew_id, captain_id)
        )

        connection.commit()
        connection.close()

def get_top_crews():

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT crews.name,
                COUNT(crew_members.user_id) AS members
            FROM crews
            LEFT JOIN crew_members
            ON crews.crew_id = crew_members.crew_id
            GROUP BY crews.crew_id
            ORDER BY members DESC
            LIMIT 5
            """
        )

        crews = cursor.fetchall()

        connection.close()

        return crews



def give_fruit(user_id, fruit_name):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO devil_fruits
            VALUES (?, ?)
            """,
            (user_id, fruit_name)
        )

        connection.commit()
        connection.close()


def get_fruit(user_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT fruit_name
            FROM devil_fruits
            WHERE user_id = ?
            """,
            (user_id,)
        )

        fruit = cursor.fetchone()

        connection.close()

        return fruit

def remove_fruit(user_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM devil_fruits
            WHERE user_id = ?
            """,
            (user_id,)
        )

        connection.commit()
        connection.close()

def create_ship(user_id, ship_name):

        ship = SHIP_DATA[ship_name]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO ships
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                ship_name,
                ship["health"],
                ship["attack"]
            )
        )

        connection.commit()
        connection.close()

def get_ship(user_id):

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM ships
            WHERE user_id = ?
            """,
            (user_id,)
        )

        ship = cursor.fetchone()

        connection.close()

        return ship


def update_bounty(user_id, amount):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET bounty = ?
        WHERE user_id = ?
        """,
        (amount, user_id)
    )

    connection.commit()
    connection.close()


def get_bounty(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT bounty
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    bounty = cursor.fetchone()

    connection.close()

    return bounty


def join_crew(crew_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO crew_members
        VALUES (?, ?)
        """,
        (crew_id, user_id)
    )

    connection.commit()
    connection.close()

def update_bank(user_id, new_bank):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET bank = ?
            WHERE user_id = ?
            """,
            (new_bank, user_id)
        )

        connection.commit()
        connection.close()


def get_top_users():

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT username, wallet, bank
            FROM users
            ORDER BY wallet + bank DESC
            LIMIT 5
            """
        )

        users = cursor.fetchall()

        connection.close()

        return users

