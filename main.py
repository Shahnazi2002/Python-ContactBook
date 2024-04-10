import sqlite3

# Connect to database
connection = sqlite3.connect('contacts.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (Name TEXT PRIMARY KEY, Email TEXT, Phone INTEGER)''')

def print_header():
    print("\nNo.  Name               Email                     Phone")
    print("-" * 64)

def incorrect_input():
    print("The entered command is not correct, please try again.")

def create_contact():
    try:
        name = input("Please enter name: ")
        email = input("Please enter email: ")
        phone = input("Please enter phone number: 0")
        cursor.execute("INSERT OR IGNORE INTO contacts VALUES (?, ?, ?)", (name, email, phone))
        connection.commit()
        print("Contact added.")
        main_menu()
    except:
        incorrect_input()
        main_menu()

def delete_contact(name):
    accepted = input("Are you sure for delete {name}? Y/N\n")
    match accepted.upper():
        case "Y":
            cursor.execute("DELETE FROM contacts WHERE Name = ?", (name,))
            connection.commit()
            print("The contact deleted.")
            display_all()
        
        case "N":
            view_contact(name)
        
        case _:
            incorrect_input()
            view_contact(name)

def view_contact(name): # View and edit contact
    cursor.execute("SELECT * FROM contacts WHERE Name = ?", (name,))
    row = cursor.fetchone()
    print_header()
    print(row)
    operation = input("Enter [E] for edit and [D] for delete contact or press Enter for return to main menu. ")

    match operation.upper():
        case "E":
            edit_case = input("Enter [N] for edit name or enter [E] for edit email and [P] for edit phone. Press ENTER to return. ")
            match edit_case.upper():
                case "":
                    view_contact(name)

                case "P":
                    new_phone = int(input("Enter new phone number: 0"))
                    cursor.execute("UPDATE contacts SET Phone = ? WHERE Name = ?", (new_phone, name))
                    connection.commit()
                    print("Contact phone number already updated.")
                    view_contact(name)
                case "E":
                    new_email = input("Enter new email address: ")
                    cursor.execute("UPDATE contacts SET Email = ? WHERE Name = ?", (new_email, name))
                    connection.commit()
                    print("Contact email already updated.")
                    view_contact(name)
                case "N":
                    new_name = input("Enter name of contact: ")
                    cursor.execute("UPDATE contacts SET Name = ? WHERE Name = ?", (new_name, name))
                    connection.commit()
                    print("Contact updated.")
                    display_all()


        case "D":
            delete_contact(name)

        case "":
            main_menu()

        case _:
            incorrect_input()
            main_menu()

def display_all():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    if len(rows)<1:
        print("(The contacts list is empty.)")
    else:
        print_header()
        for i in range(len(rows)):
            print(str(i+1).zfill(2), rows[i])
        try:
            select = int(input("Enter number of row for select the contact: "))-1
            view_contact(rows[select][0])
        except:
            incorrect_input()
            main_menu()

def main_menu():
    print("\n")
    print("------- Python Contacts Book -------")
    command = input("[C] Create a new contact\n[A] View all contacts\n[E] Exit\n")

    match command.upper():
        case "C": # Create a new contact
            create_contact()

        case "A": # View all contacts
            display_all()

        case "E": # Exit
            connection.close()

        case _:
            incorrect_input()
            main_menu()

main_menu()