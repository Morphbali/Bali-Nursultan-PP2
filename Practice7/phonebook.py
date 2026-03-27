import csv
from connect import connect


def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL UNIQUE
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Table is ready")


def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                cur.execute("""
                    INSERT INTO contacts (username, phone)
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING
                """, (row["username"], row["phone"]))

        conn.commit()
        print("Data imported from CSV")
    except FileNotFoundError:
        print("CSV file not found")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO contacts (username, phone)
            VALUES (%s, %s)
        """, (username, phone))
        conn.commit()
        print("Contact added")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def show_all_contacts():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found")

    cur.close()
    conn.close()


def update_contact():
    search_value = input("Enter current username or phone: ")
    print("1 - Update username")
    print("2 - Update phone")
    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    try:
        if choice == "1":
            new_username = input("Enter new username: ")
            cur.execute("""
                UPDATE contacts
                SET username = %s
                WHERE username = %s OR phone = %s
            """, (new_username, search_value, search_value))
        elif choice == "2":
            new_phone = input("Enter new phone: ")
            cur.execute("""
                UPDATE contacts
                SET phone = %s
                WHERE username = %s OR phone = %s
            """, (new_phone, search_value, search_value))
        else:
            print("Invalid choice")
            cur.close()
            conn.close()
            return

        conn.commit()
        print("Contact updated")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def query_contacts():
    print("1 - Search by name")
    print("2 - Search by phone prefix")
    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("""
            SELECT * FROM contacts
            WHERE username ILIKE %s
            ORDER BY id
        """, ('%' + name + '%',))
    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute("""
            SELECT * FROM contacts
            WHERE phone LIKE %s
            ORDER BY id
        """, (prefix + '%',))
    else:
        print("Invalid choice")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Nothing found")

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter username or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""
            DELETE FROM contacts
            WHERE username = %s OR phone = %s
        """, (value, value))

        conn.commit()

        if cur.rowcount > 0:
            print("Contact deleted")
        else:
            print("Contact not found")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Create table")
        print("2. Import from CSV")
        print("3. Add contact from console")
        print("4. Show all contacts")
        print("5. Update contact")
        print("6. Query contacts")
        print("7. Delete contact")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            show_all_contacts()
        elif choice == "5":
            update_contact()
        elif choice == "6":
            query_contacts()
        elif choice == "7":
            delete_contact()
        elif choice == "8":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


menu()