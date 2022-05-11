import sqlite3

def show_all():
    connection = sqlite3.connect('reservation.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM Reservation""")
    result_set = cursor.fetchall()
    for row in result_set:
        print(row)