import sqlite3
import check_date
from random import randint

def make_reserv(date_in, date_out, room, cust_num):
    id_num = randint(0, 10000)
    albums = [(id_num, room, date_in, date_out, cust_num)]
    connection = sqlite3.connect('reservation.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Reservation""")
    result_set = cursor.fetchall()
    for row in result_set:
        if row[1] == room:
            if not check_date.check(row, date_in, date_out):
                print("Already exist")
                connection.commit()
                connection.close()
                return False
    cursor.executemany("""INSERT INTO Reservation
                              VALUES (?,?,?,?,?)""", albums)
    connection.commit()
    connection.close()
    return True