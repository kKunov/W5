import sqlite3
from create_company import make_sql
from create_company import insert_in_employee


def print_commands():
    print("Available commands:")
    print("1. list_employees")
    print("2. monthly_spending")
    print("3. yearly_spending")
    print("4. add_employee")
    print("5. delete_employee")
    print("6. update_employee")
    print("7. exit")


def ask_for_command():
    command = input("Chose command: ")
    return command


def check_command(command):
    if (command == "list_employees" or command == "monthly_spending" or
        command == "yearly_spending" or command == "add_employee" or
        command == "delete_employee" or command == "update_employee" or
        command == "exit"):
        return True
    else:
        return False


def list_employees(conn):
    list_of_emplo = conn.execute('''SELECT id, name, position
                                    FROM employee''')
    for raw in list_of_emplo:
        print("%s - %s - %s" % (raw[0], raw[1], raw[2]))


def delete_employee(conn, i_d):
    conn.execute('''DELETE FROM employee
                    WHERE id = ?''', (i_d,))


def monthly_spending(conn):
    spending = conn.execute('''SELECT SUM(monthly_salary)
                               FROM employee''').fetchone()
    print("The company is spending ${0} every month!".format(spending[0]))


def yearly_spending(conn):
    spending = conn.execute('''SELECT (SUM(monthly_salary) * 12) + SUM(yearly_bonus)
                               FROM employee''').fetchone()
    print("The company is spending ${0} every year!".format(spending[0]))


def update_employee(conn):
    check = 0
    while check == 0:
        print('''You must put a ID for update, what do you want to change
                and to what to change it!''')
        print("You can change name, salary, bonus or position")
        i_d = input("Tipe ID:")
        type_of_data = input("What do you want to change: ")
        new_data = input("change to: ")
        if type_of_data == "name":
            conn.execute('''UPDATE employee
                            SET name = ? WHERE id = ?''', (new_data, i_d))
            check += 1
        elif type_of_data == "salary":
            conn.execute('''UPDATE employee
                            SET monthly_salary = ? WHERE id = ?''', (new_data, i_d))
            check += 1
        elif type_of_data == "bonus":
            conn.execute('''UPDATE employee
                            SET yearly_bonus = ? WHERE id = ?''', (new_data, i_d))
            check += 1
        elif type_of_data == "position":
            conn.execute('''UPDATE employee
                            SET position = ? WHERE id = ?''', (new_data, i_d))
            check += 1


def what_to_do(command, conn):
    if command == "add_employee":
        insert_in_employee(conn)
    elif command == "list_employees":
        list_employees(conn)
    elif command == "delete_employee":
        i_d = input("Type the ID of employee you want to delete: ")
        delete_employee(conn, i_d)
    elif command == "monthly_spending":
        monthly_spending(conn)
    elif command == "yearly_spending":
        yearly_spending(conn)
    elif command == "update_employee":
        update_employee(conn)


def main():
    conn = sqlite3.connect("company.db")
    make_sql(conn)
    print_commands()
    command = ask_for_command()
    while check_command(command) is False:
        print("Wrong command! Try again!")
        command = ask_for_command()
    what_to_do(command, conn)
    conn.commit()


if __name__ == '__main__':
    main()

