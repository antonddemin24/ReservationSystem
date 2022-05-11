import sqlite3


def delete_reservation(text):
    connection = sqlite3.connect('reservation.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Reservation""")
    result_set = cursor.fetchall()
    for row in result_set:
        print(row)
    id_num = int(text)
    cursor.execute("""DELETE FROM Reservation
                                  WHERE id= ?""", (id_num, ))
    connection.commit()
    connection.close()
    return True