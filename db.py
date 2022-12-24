import mysql.connector
# from datetime import datetime

db = mysql.connector.connect(
host="localhost",
user ="root",
passwd="486555",
database="ticket_reservations")

mycursor = db.cursor()

MAX_BROJ_KARATA = 20
MAX_BROJ_VIP_KARATA = 5

# mycursor.execute("CREATE DATABASE ticket_reservations") ovu cu da koristim

# mycursor.execute("DROP TABLE users")

# mycursor.execute("CREATE TABLE users(username VARCHAR(20) PRIMARY KEY, password VARCHAR(20), name VARCHAR(20), lastname VARCHAR(20), jmbg VARCHAR(13), email VARCHAR(20), tickets SMALLINT UNSIGNED DEFAULT 0, vipTick SMALLINT UNSIGNED DEFAULT 0)")

def insert_new_user(new_user):
    sql_query = "INSERT INTO users(username, password, name, lastname, jmbg, email, tickets, vipTick) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql_query, new_user)

    db.commit()
    print("Registrovan novi korisnik u bazu.")
    
def print_table():
    mycursor.execute("SELECT * FROM users")
    for x in mycursor:
        print(x)

def execute(string):
    mycursor.execute(string)

def get_all_tickets():
    mycursor.execute("SELECT SUM(tickets) FROM users")
    tickets = mycursor.fetchall()[0][0]
    return int(MAX_BROJ_KARATA-tickets)

def get_all_vip_tickets():
    mycursor.execute("SELECT SUM(vipTick) FROM users")
    tickets = mycursor.fetchall()[0][0]
    return int(MAX_BROJ_VIP_KARATA-tickets)

def get_tickets_by_user(username):
    mycursor.execute("SELECT tickets, vipTick FROM users WHERE username=%s",(username,))
    return int(mycursor.fetchone()[0])

def update_tickets_by_user(tickets, username):
    mycursor.execute("UPDATE users SET tickets=%s WHERE username=%s", (tickets, username))
    db.commit()
    print(username+' reserved '+str(tickets)+' tickets!')

def update_vip_tickets_by_user(tickets, username):
    mycursor.execute("UPDATE users SET vipTick=%s WHERE username=%s", (tickets, username))
    db.commit()
    print(username+' reserved '+str(tickets)+' vip tickets!')

def check_username(username):
    try:
        mycursor.execute("SELECT username FROM users WHERE username=%s",(username,))
        if mycursor.fetchone() is None:
            # print(type(mycursor.fetchone()))
            return True
        else:
            return False
    except:
        return True

def check_password(username,password):
    try:
        mycursor.execute("SELECT username FROM users WHERE username=%s AND password=%s",(username,password,))
        if mycursor.fetchone() is None:
            return False
        else:
            return True
    except:
        return False

    
# print_table()