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

# mycursor.execute("SHOW SCHEMAS")
# for x in mycursor:
#     print(x)

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


# insert_new_user(("username123", "12345", "Nikola", "Nikolic", "2301993290013", "email2455", "2", "0"))
# execute("UPDATE users SET tickets='2',vip_tickets='2' WHERE username='username123'")
# db.commit()
# print_table()

# execute("DELETE FROM users WHERE username='sdfhs'")
# db.commit()

def get_all_tickets():
    mycursor.execute("SELECT SUM(tickets) FROM users")
    # print(type(tickets))
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
    print(username)
    try:
        mycursor.execute("SELECT username FROM users WHERE username=%s",(username,))
        if mycursor.fetchone() is None:
            print(type(mycursor.fetchone()))
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
# username = 'dfhdssdsdh'
# mycursor.execute("SELECT username FROM users WHERE username=%s",(username,))
# print(type(mycursor.fetchone()))

# get_all_tickets()

# mycursor.execute("DESCRIBE users")
# for x in mycursor:
#     print(x)

# users = [("tim", "techwithtim"),
#         ("joe", "joey123"),
#         ("Sarah", "Sarah1234")]

# user_scores = [(45,100),
#                 (30,200),
#                 (46,124)]

# mycursor = db.cursor()

# Q1 = "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50), passwd VARCHAR(50))"

# Q2 = "CREATE TABLE Scores (userID int PRIMARY KEY, FOREIGN KEY(userID) REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0)"

# # mycursor.execute(Q1)
# # mycursor.execute(Q2)

# # mycursor.execute("SHOW TABLES")
# # for x in mycursor:
# #     print(x)

# Q3 = "INSERT INTO Users (name, passwd) VALUES (%s,%s)"
# Q4 = "INSERT INTO Scores (userID, game1, game2) VALUES (%s,%s,%s)"

# for x,user in enumerate(users):
#     mycursor.execute(Q3, user)
#     last_id = mycursor.lastrowid
#     mycursor.execute(Q4, (last_id,) + user_scores[x])

# db.commit()

# mycursor.execute("SELECT * FROM Scores")
# for x in mycursor:
#     print(x)

# mycursor.execute("SELECT * FROM Users")
# for x in mycursor:
#     print(x)
# # mycursor.execute("CREATE DATABASE testdatabase") naziv baze "testdatabase" se doda gore u connector posle sto se prvi put izvrsi

# # mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

# # mycursor.execute("DESCRIBE Person") ovo printuje sve iz Person-a

# # for x in mycursor:
# #     print(x)

# # mycursor.execute("INSERT INTO Person (name, age) VALUES (%s, %s)",("Anne", 20)) ovo zajedno sa ovim db.commit dodaje u tabelu


# # db.commit()

# # mycursor.execute("SELECT * FROM Person")

# # for x in mycursor:
# #     print(x)

# # mycursor.execute("CREATE TABLE Test (name varchar(50) NOT NULL, created datetime NOT NULL, gender ENUM('M','F','O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

# # mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s,%s,%s)",("JOEY", datetime.now(), "F"))

# # db.commit()

# # mycursor.execute("SELECT id, name FROM Test WHERE gender = 'M' ORDER BY id DESC")
# # for x in mycursor:
# #     print(x)

# # mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")
# # mycursor.execute("ALTER TABLE Test DROP food") ovo brise kolonu
# # mycursor.execute("ALTER TABLE Test CHANGE name first_name VARCHAR(50)") mijenja naziv name u first_name
# # mycursor.execute("ALTER TABLE Test CHANGE first_name first_name VARCHAR(4)")

# # mycursor.execute("DESCRIBE Test")
# # # print(mycursor.fetchone())
# # for x in mycursor:
# #     print(x)

