import json
import csv
from connect import connect


def setup_db():
    conn = connect()
    cur = conn.cursor()

    with open("schema.sql", "r") as f:
        cur.execute(f.read())

    with open("procedures_extended.sql", "r") as f:
        cur.execute(f.read())

    conn.commit()
    cur.close()
    conn.close()
    print("DB Ready")


def add_contact():
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    res = cur.fetchone()

    if res:
        gid = res[0]
    else:
        cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (group,))
        gid = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO contacts(username,email,birthday,group_id)
        VALUES(%s,%s,%s,%s)
    """, (name, email, birthday, gid))

    conn.commit()
    cur.close()
    conn.close()


def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    t = input("Type(home/work/mobile): ")

    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, t))
    conn.commit()
    cur.close()
    conn.close()


def search():
    q = input("Search: ")
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def filter_group():
    g = input("Group: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.username, c.email
        FROM contacts c
        JOIN groups g ON c.group_id=g.id
        WHERE g.name=%s
    """, (g,))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def export_json():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.username,c.email,c.birthday,g.name,p.phone,p.type
        FROM contacts c
        LEFT JOIN groups g ON c.group_id=g.id
        LEFT JOIN phones p ON c.id=p.contact_id
    """)

    data = cur.fetchall()

    with open("export.json","w") as f:
        json.dump(data, f, indent=4, default=str)

    cur.close()
    conn.close()


def import_json():
    with open("export.json") as f:
        data = json.load(f)

    conn = connect()
    cur = conn.cursor()

    for row in data:
        name,email,bday,group,phone,ptype = row

        cur.execute("SELECT id FROM contacts WHERE username=%s",(name,))
        if cur.fetchone():
            choice = input(f"{name} exists skip/overwrite? ")
            if choice=="skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE username=%s",(name,))

        cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT DO NOTHING",(group,))
        cur.execute("SELECT id FROM groups WHERE name=%s",(group,))
        gid = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO contacts(username,email,birthday,group_id)
            VALUES(%s,%s,%s,%s)
            RETURNING id
        """,(name,email,bday,gid))

        cid = cur.fetchone()[0]

        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id,phone,type)
                VALUES(%s,%s,%s)
            """,(cid,phone,ptype))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    while True:
        print("""
1.Setup DB
2.Add contact
3.Add phone
4.Search
5.Filter by group
6.Export JSON
7.Import JSON
8.Exit
""")
        c = input()

        if c=="1": setup_db()
        elif c=="2": add_contact()
        elif c=="3": add_phone()
        elif c=="4": search()
        elif c=="5": filter_group()
        elif c=="6": export_json()
        elif c=="7": import_json()
        elif c=="8": break


menu()