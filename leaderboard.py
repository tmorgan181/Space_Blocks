# CS 3100 Team 8
# Spring 2021
#
# This file initializes the leaderboard database file to store high scores.
# It also provides several access functions to read from and modify the database.

#Import sqlite3 database tools
import sqlite3

def init_database():
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    #Table is created only on the first run of the app
    try:
        c.execute("""
        CREATE TABLE Leaderboard (
        entry_ID Integer PRIMARY KEY,
        player_initials Text,
        score Integer
        )
        """)

        print("Table \'Leaderboard\' successfully created.")

    except sqlite3.OperationalError:
        print("Table \'Leaderboard\' already exists.")

    #Commit changes
    conn.commit()
    #Close connection
    conn.close()

    return

def add_entry(name, score):
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    entry_data = (name, score)
    c.execute("""INSERT INTO Leaderboard(player_initials, score) VALUES
                (?, ?)""", entry_data)

    # Commit changes
    conn.commit()
    #Close connection
    conn.close()
    return

def print_all_scores():
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    c.execute("SELECT entry_ID FROM Leaderboard")
    ID_list = c.fetchall()

    for x in ID_list:
        c.execute("SELECT * FROM Leaderboard WHERE entry_ID=?", x)
        info = c.fetchone()
        print(info)

    #Close connection
    conn.close()

    return

def return_top_ten():
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    c.execute("SELECT entry_ID FROM Leaderboard ORDER BY score DESC")
    ID_list = c.fetchall()

    # Append each entry to a new list
    entries = []
    for i in range(10):
        if i < len(ID_list):
            c.execute("SELECT * FROM Leaderboard WHERE entry_ID=?", ID_list[i])
            info = c.fetchone()
            entries.append(info)

    #Close connection
    conn.close()

    return entries

def return_top_five():
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    c.execute("SELECT entry_ID FROM Leaderboard ORDER BY score DESC")
    ID_list = c.fetchall()

    # Append each entry to a new list
    entries = []
    for i in range(5):
        if i < len(ID_list):
            c.execute("SELECT * FROM Leaderboard WHERE entry_ID=?", ID_list[i])
            info = c.fetchone()
            entries.append(info)

    #Close connection
    conn.close()

    return entries

def erase_nones():
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    c.execute("SELECT entry_ID FROM Leaderboard WHERE player_initials='none'")
    ID_list = c.fetchall()
    print(ID_list)

    for x in ID_list:
        print(x)
        c.execute("DELETE FROM Leaderboard WHERE entry_ID=?", x)

    #Close connection
    conn.close()

    return

def erase_entry(name):
    #Connect to database info file
    conn = sqlite3.connect("leaderboard.db")
    #Create database cursor
    c = conn.cursor()

    c.execute("SELECT entry_ID FROM Leaderboard WHERE player_initials=?", name)
    ID_list = c.fetchall()
    print(ID_list)

    for x in ID_list:
        print(x)
        c.execute("DELETE FROM Leaderboard WHERE entry_ID=?", x)

    #Close connection
    conn.close()

    return