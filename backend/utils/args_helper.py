'''
    This file contains all functions executed if args are passed
'''

def show_all_books(connect_to):
    cursor = connect_to.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


