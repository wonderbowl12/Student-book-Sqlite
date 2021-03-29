import sqlite3

connection = sqlite3.connect('phonebook.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

#Add password system
#Add more features for ease of access
#Clean up repetitive code
#GUI?


#Function adds a new student
def add_student():
    name = input('Name of Student you would like to add: ')
    phone = input('Phone number?: ')
    school_id = input('School ID: ')
    # id = input('id?')

    confirm = confirm_action()
    if confirm is True:
        cursor.execute('INSERT INTO name(school,name,phone) VALUES(?,?,?)', (school_id.capitalize(), name, phone))
        connection.commit()
        menu()
    if confirm is False:
        add_student()

#Finds student
def find_student():
    try:
        school_id = input('Input student ID: ')
        cursor.execute('SELECT*FROM name WHERE school=?', (school_id,))
        row = cursor.fetchone()
        grab_information(row)
        another = input('Want to look up another student? (Yes or No): ')
        if another.lower() is 'yes':
            find_student()
        elif another.lower() is 'no':
            menu()
    except:
        x = input('Sorry the student was not found, do you want to try again? ')
        if x.lower() == 'yes':
            find_student()
        elif x.lower() == 'no':
            menu()
        else:
            print('Not sure what you mean...  \n')
            find_student()


def update_information():
    id_input = input('What is the entry you want to update? (Student ID): \n')

    update_choice = int(input('What do you want to update? '
                              '\n 1. Names'
                              '\n 2. Phone Number'
                              '\n 3. School ID'
                              '\n'))
    cursor.execute('SELECT*FROM name WHERE school=?', (id_input,))
    row = cursor.fetchone()
    found_name = row['name']
    found_num = row['phone']
    found_id = row['school']
    if update_choice == 1:
        cursor.execute('UPDATE name SET name = ? WHERE name = ?', (input('New Name:  '), found_name))
        connection.commit()
        print('Name has been updated! \n')
        menu()
    elif update_choice == 2:
        cursor.execute('UPDATE name SET phone = ? WHERE phone = ?', (input('New Number: '), found_num))
        connection.commit()
        print('Number has been updated! \n')
        menu()
    elif update_choice == 3:
        cursor.execute('UPDATE name SET school = ? WHERE school = ?', (input('New ID: '), found_id))
        connection.commit()
        print('ID has been updated! \n')
        menu()
    else:
        print('Error')
        update_information()


def delete_student():
    school_id = input('Enter student ID to delete: ')
    cursor.execute('SELECT*FROM name WHERE school=?', (school_id,))
    row = cursor.fetchone()
    grab_information(row)
    confirm = confirm_action()
    if confirm is True:
        cursor.execute('DELETE FROM name WHERE school=?', (school_id,))
        connection.commit()
        menu()
    if confirm is False:
        delete_student()

#Delete all and list all use the same loop, creates cursor and uses fetchall to collect all objects.
#Loop appends objects to id_db which is then used in another loop to get objects from database

def delete_all_students():
    cursor.execute('SELECT*FROM name')
    rows = cursor.fetchall()
    id_db = []
    for row in rows:
        id_db.append(row[0])
    for id in id_db:
        cursor.execute('SELECT*FROM name WHERE id=?', (id,))
        row = cursor.fetchone()
        grab_information(row)
        confirm = confirm_action()
        if confirm is True:
            for id in id_db:
                cursor.execute('DELETE FROM name WHERE id=?', (id,))
                connection.commit()
                print('All entries were deleted.\n')
        elif confirm is False:
            menu()



def list_all():
    cursor.execute('SELECT*FROM name')
    rows = cursor.fetchall()
    id_db = []
    for row in rows:
        id_db.append(row[0])
    if len(id_db) == 0:
        print('There are no entries.\n')
        menu()
    else:
        for id in id_db:
            cursor.execute('SELECT*FROM name WHERE id=?', (id,))
            row = cursor.fetchone()
            grab_information(row)

    menu()

def grab_information(row):
    id = row['id']
    school = row['school']
    name = row['name']
    phone = row['phone']
    print('\n')
    print('ID:' + str(id))
    print("School ID: " + str(school))
    print("Name: " + str(name))
    print("Phone number: " + str(phone))

def confirm_action():
    confirm = input('Are you sure? (Yes or No) ')
    if confirm.lower() == 'yes' or 'y':
        return True
    elif confirm.lower() == 'no' or 'n':
        return False

def menu():
    print('\n')
    print('Welcome to da STUDENT PHONEBOOK, what do you want?\n'
          '\n 1. Find a Student'
          '\n 2. Add a Student'
          '\n 3. Update Student Information'
          '\n 4. Delete a Student'
          '\n 5. List all Students'
          '\n 6. Delete all Students'
          '\n END. End Program', "\r")
    menu_choice = input()
    if menu_choice == '1':
        find_student()
    if menu_choice == '2':
        add_student()
    if menu_choice == '3':
        update_information()
    if menu_choice == '4':
        delete_student()
    if menu_choice == '5':
        list_all()
    if menu_choice == '6':
        delete_all_students()
    if menu_choice == 'END':
        quit()


menu()
