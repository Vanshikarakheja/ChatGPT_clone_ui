import sqlite3

def create_user(email, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (email, password)
            VALUES (?, ?)
            """,
            (email, password)
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()