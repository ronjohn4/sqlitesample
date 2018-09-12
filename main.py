# Ron Johnson
# 9/8/2018
#
# Sample of DB operations typically needed against sqlite3.
# Most of this code came from somewhere else, see urls below.
#
# Won't get into modifying table structures other than creating the tables
#
# http://www.sqlitetutorial.net

import sqlite3
import os

database = "pythonsqlite.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file.  The database will be created if it doesn't exist.
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def create_tasks_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    create_table_sql = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        priority integer,
                                        status_id integer NOT NULL,
                                        project_id integer NOT NULL,
                                        begin_date text NOT NULL,
                                        end_date text NOT NULL,
                                        FOREIGN KEY (project_id) REFERENCES projects (id)
                                    );"""
    create_table(conn, create_table_sql)


def create_projects_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    create_table_sql = """ CREATE TABLE IF NOT EXISTS projects (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            begin_date text,
                                            end_date text
                                        ); """

    create_table(conn, create_table_sql)


def insert_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date) VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def insert_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date) VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


if __name__ == "__main__":
    # 1. Delete database
    try:
        os.remove(database)
    except Exception as e:
        print(e)
    print('database file deleted (if it existed): {0}'.format(database))

    # 2. Create connection (which will create a db if it doesn't exit)
    conn = create_connection(database)
    print('connection created')

    # with conn:

    # 3. Close connection
    # conn.close()
    # print('connection closed')

    # 4. Create connection (prove that it will open when db already exists)
    # conn = create_connection(database)
    # print('connection created (second time)')

    # 5. Create tables
    create_projects_table(conn)
    create_tasks_table(conn)
    print('tables created')

    # 6. Insert
    project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    project_id = insert_project(conn, project)

    # task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
    # task_id = insert_task(conn, task_1)

    # task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
    # task_id = insert_task(conn, task_2)

    print('rows inserted')

    conn.close()
    print('database closed')

        # 7. Read
        # 8. Close / Open connection
        # 9. Read (prove persistence)
        # 10. Update
        # 11. Delete

