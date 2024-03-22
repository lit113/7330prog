import csv
import mysql
from mysql.connector import connect, Error, connection


def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='cs5330',
            password='pw5330',
            database='dbprog'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None


db_connection = create_db_connection()


def process_csv_file(file_name):
    with open(file_name, mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            process_command(line)

def process_command(command_line):
    command = command_line[0]
    params = command_line[1:]
    params = [x.strip() for x in params if x != '']

    print(command)
    print(params)
    if command == 'e':
        check_or_create_tables(db_connection)
    elif command == 'r':
        clear_data(db_connection)
    elif command == 'p':
        add_new_player(db_connection, params)
    elif command == 'm':
        add_completed_match(db_connection, params)
    elif command == 'n':
        add_future_match(db_connection, params)


def check_or_create_tables(connection):
    # global player_table_query, matches_table_query
    if connection is not None:
        cursor = connection.cursor()
        player_table_query = """
        CREATE TABLE IF NOT EXISTS Player (
            ID INT PRIMARY KEY,
            Name VARCHAR(255) UNIQUE,
            Birthdate DATE,
            Rating INT,
            State CHAR(2)
        );
        """
        matches_table_query = """
        CREATE TABLE IF NOT EXISTS Matches (
            HostID INT,
            GuestID INT,
            Start DATETIME,
            End DATETIME,
            Hostwin INT,
            PreRatingHost INT,
            PostRatingHost INT,
            PreRatingGuest INT,
            PostRatingGuest INT
        );
        """
    try:
        cursor.execute(player_table_query)
        cursor.execute(matches_table_query)
        connection.commit()
        print("Tables checked/created successfully.")
    except Error as e:
        print("Error while creating tables", e)
    finally:
        if cursor:
            cursor.close()


def clear_data(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM Matches;")
        cursor.execute("DELETE FROM Player;")
        connection.commit()
        print("Data cleared successfully.")
    except Error as e:
        print("Error while clearing data", e)
    finally:
        if cursor:
            cursor.close()


def add_new_player(connection, player_data):
    cursor = connection.cursor()
    add_player_query = """
    INSERT INTO Player (ID, Name, Birthdate, Rating, State)
    VALUES (%s, %s, STR_TO_DATE(%s, '%Y%m%d'), %s, %s);
    """
    try:
        cursor.execute(add_player_query, player_data)
        connection.commit()
        print("New player added successfully.")
    except Error as e:
        print("Error while adding a new player", e)
    finally:
        if cursor:
            cursor.close()


def add_completed_match(connection, match_data):
    cursor = connection.cursor()
    add_match_query = """
    INSERT INTO Matches (HostID, GuestID, Start, End, HostWin, PreRatingHost, PostRatingHost, PreRatingGuest, \
                        PostRatingGuest)
    VALUES (%s, %s, STR_TO_DATE(%s, '%Y%m%d:%H:%i:%s'), STR_TO_DATE(%s, '%Y%m%d:%H:%i:%s'), %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(add_match_query, match_data)
        connection.commit()
        print("Completed match added successfully.")
    except Error as e:
        print("Error while adding completed match", e)
    finally:
        if cursor:
            cursor.close()


def add_future_match(connection, match_data):
    cursor = connection.cursor()
    add_future_match_query = """
    INSERT INTO Matches (HostID, GuestID, Start)
    VALUES (%s, %s, STR_TO_DATE(%s, '%Y%m%d:%H:%i:%s'));
    """
    try:
        cursor.execute(add_future_match_query, match_data)
        connection.commit()
        print("Future match added successfully.")
    except Error as e:
        print("Error while adding future match", e)
    finally:
        if cursor:
            cursor.close()

