#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
import time

def config(filename='C:/Users/coler/hikaritesting/lightbulbtesting/bot/bot/utils/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """ Connect to the PostgreSQL database server """
    global conn
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        global cur
        cur = conn.cursor()
        
	# execute a statement
        cur.execute('SELECT * FROM public.users')
        # display the PostgreSQL database server version
        data = cur.fetchall()
        print(data)
       
	# close the communication with the PostgreSQL
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def close():
    cur.close()
    if conn is not None:
        conn.close()
        print('Database connection closed.')

def create_user(name: str, id: int):
    try:
        data = cur.execute(f"INSERT INTO public.users (id, name) VALUES({id}, '{name}') returning *")
        print(data)
    except psycopg2.errors.UniqueViolation as error:
        print(error)
        close()
        connect()
        return 

def get_all_data():
    cur.execute('SELECT * FROM public.users')
    data = cur.fetchall()
    print(data)
    return data

def get_user_data(id: int):
    cur.execute(f'SELECT * FROM public.users WHERE id = {id}')
    data = cur.fetchone()
    print(data)
    return data

def save():
    conn.commit()

if __name__ == '__main__':
    start_time = time.perf_counter()
    connect()
    print("Connected")
    create_user("Carberra", 385807530913169426)
    print("Created")
    get_all_data()
    print("Got all data")
    get_user_data(215061635574792192)
    print("Got user data")
    save()
    print("Saved")
    close()
    print("Closed")
    end_time = time.perf_counter()
    print(f"Finished in {end_time - start_time:0.4f}s")