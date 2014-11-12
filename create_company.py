import sqlite3


def make_sql(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS employee
                 (id integer primary key, name text,
                 monthly_salary integer, yearly_bonus integer, position text)''')


def insert_in_employee(conn):
    name = input("Name: ")
    salary = input("Salary: ")
    bonuses = input("Bonuses: ")
    position = input("Position: ")
    conn.execute('''INSERT INTO employee(name, monthly_salary, yearly_bonus,
                                       position)
                    VALUES(?, ?, ?, ?)''', (name, salary, bonuses, position))
