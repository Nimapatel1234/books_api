from django.db import connection

def list_books():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books LIMIT 10;")
        results = cursor.fetchall()
        for row in results:
            print(row)
