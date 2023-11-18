"""Skript zur Interaktion mit der 'users'-Datenbank"""


import sqlite3


PATH = "database/users.db"


def check_user(user: str, password: str) -> bool:
    """Prüfe ob die Einwahldaten eines Nutzers vorhanden sind"""

    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT user, password FROM USERS WHERE user = ?", (user,))
    try:
        entry = cursor.fetchall()[0]
    except IndexError:
        return False

    connection.commit()
    connection.close()

    if user == entry[0] and password == entry[1]:
        return True
    return False
