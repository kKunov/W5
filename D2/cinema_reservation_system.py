import sqlite3


def create_db(db):
    db.execute('''CREATE TABLE IF NOT EXISTS movies
                  (id INTEGER PRIMARY KEY,
                   name text, rating REAL)''')

    db.execute('''CREATE TABLE IF NOT EXISTS projections
                  (id INTEGER PRIMARY KEY,
                   movie_id INTEGER REFERENCES movies(id),
                   type INTEGER,
                   date_and_time DATE)''')

    db.execute('''CREATE TABLE IF NOT EXISTS reservations
                  (id INTEGER PRIMARY KEY,
                   username TEXT,
                   projection_id INTEGER REFERENCES projections(id),
                   row INTEGER(2), sit INTEGER(2))''')
    db.commit()


def add_movies(db):
    name = input("Name of the Movie: ")
    rating = input("Rating of the Movie: ")
    db.execute('''INSERT INTO movies(name, rating)
                  VALUES(?,?)''', (name, rating))
    db.commit()


def add_projection(db):
    movie_id = input("Movie ID: ")
    type_movie = input("Type: ")
    date_and_time = input("Date and time: ")
    db.execute('''INSERT INTO projections(movie_id, type, date_and_time)
                  VALUES(?, ?, ?)''', (movie_id, type_movie, date_and_time))
    db.commit()


def show_movies(db):
    list_of_movies = db.execute('''SELECT *
                                   FROM movies
                                   ORDER BY rating desc''')
    for raw in list_of_movies:
        print("ID:{0} Movie: '{1}' Rating: {2}".format(raw[0], raw[1], raw[2]))


def show_movies_projections(db, movie_id):
    list_of_projections = db.execute('''SELECT projections.id,
                                        projections.type,
                                        projections.date_and_time
                                        FROM projections
                                        WHERE projections.movie_id = ?''',
                                     (movie_id,))
    name_of_the_movie = db.execute('''SELECT name
                                      FROM movies
                                      WHERE id = ?''', (movie_id,)).fetchone()
    print("{}".format(name_of_the_movie[0]))
    for raw in list_of_projections:
        print("ID: {0}, Type: {1}, Date and time: {2}".format(raw[0], raw[1],
              raw[2]))


def is_valid_movie(db, movie_id):
    movie_check = db.execute('''SELECT name
                                FROM movies
                                WHERE id = ?''', (movie_id,))
    if movie_check == "":
        return False
    else:
        return True


def check_free_sits(db, num_of_tickets, proj_id):
    free_sits = db.execute('''SELECT 100 - count(id)
                              FROM reservations
                              WHERE projection_id = ?''',
                           (proj_id,)).fetchone()
    return free_sits[0]


def is_sit_is_free(db, row, sit):
    is_it_free = db.execute('''SELECT row, sit
                               FROM reservations
                               where row = ? and sit = ?''',
                            (row, sit)).fetchone()
    if is_it_free is None:
        return True
    else:
        return False


def print_sits(db, proj_id):
    rows = []
    sits = []
    r = db.execute('''SELECT row, sit
                      FROM reservations''').fetchone()
    s = db.execute('''SELECT sit
                      FROM reservations''').fetchone()
    for row in r:
        rows.append(row)
    for sit in s:
        sits.append(sit)
    for row2 in range(10):
        for sit in range(10):
            if [row2, sit] in row:
                print("x")
            else:
                print(".")


def add_reservation(db, name, proj_id, row, sit):
    db.execute('''INSERT INTO reservations(username, projection_id,
                              row, sit)
                  VALUES(?, ?, ?, ?)''', (name, proj_id, row, sit))


def check_projection(db, proj_id):
    is_it_valid = db.execute('''SELECT id
                                FROM projections
                                WHERE id = ?''', (proj_id,))
    if is_it_valid == "":
        return False
    else:
        return True


def make_reservation(db):
    name = input("Name: ")
    show_movies(db)
    movie_id = input("Select movie Id: ")
    while is_valid_movie(db, movie_id) is False:
        print("Its not a Valid ID, TRY AGAIN!")
        movie_id = input("Select movie Id: ")
    show_movies_projections(db, movie_id)
    proj_id = input("Select projection Id: ")
    while check_projection(db, proj_id) is False:
        print("Its not a Valid ID, TRY AGAIN!")
        proj_id = input("Select projection Id: ")
    num_of_tickets = input("How many tickets: ")
    '''while check_free_sits(db, num_of_tickets, proj_id)[0] <= num_of_tickets:
        print("Too many sits, Try AGAIN!!!")
        num_of_tickets = input("How many tickets: ")'''
    rows = []
    sits = []
    print_sits(db, proj_id)
    for index in range(int(num_of_tickets)):
        row = input("Select the row: ")
        sit = input("Select the sit")
        while (int(row) < 1 or int(row) > 10 or int(sit) > 10 or
               int(sit) < 1 or is_sit_is_free(db, row, sit) is False):
            print("Bad input, check if the sit is free and exists!")
            row = input("Select the row: ")
            sit = input("Select the sit: ")
        rows.append(int(row))
        sits.append(int(sit))
    for index in range(int(num_of_tickets)):
        add_reservation(db, name, proj_id, rows[index], sits[index])
    db.commit


def main():
    db = sqlite3.connect("cinema_reservation_system.db")
    create_db(db)
    make_reservation(db)
    db.commit()

if __name__ == '__main__':
    main()
