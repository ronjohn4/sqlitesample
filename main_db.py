import sqlite3

database = "pythonsqlite.db"

class DB():
    database = None
    conn = None
    projects = None
    tasks = None

    def __init__(self, database):
        self.database = database
        self.conn = self._create_connection()
        self.projects = projects(self.conn)
        self.tasks = tasks(self.conn)

    def close(self):
        self.conn.close()
        self.database = None
        self.conn = None
        del self.projects
        del self.tasks

    def _create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file.  The database will be created if it doesn't exist.
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except sqlite3.Error as e:
            print(e)

        return None


class projects():
    conn = None

    def __init__(self, conn):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :return:
        """

        self.conn = conn

        create_table_sql = """ CREATE TABLE IF NOT EXISTS projects (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                begin_date text,
                                                end_date text
                                            ); """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)


    def insert(self, project):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = ''' INSERT INTO projects(name,begin_date,end_date) VALUES(?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, project.insert_list())
        return cur.lastrowid


class tasks():
    conn = None

    def __init__(self, conn):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :return:
        """

        self.conn = conn

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
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)







class project():
    id = None
    name = None
    begin_date = None
    end_date = None

    def __init__(self):
        pass

    def insert_list(self):
        return (self.id, self.name, self.begin_date, self.end_date)









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


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()
    return rows


def select_project_by_id(conn, project_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE id=?", (project_id,))

    rows = cur.fetchall()
    return rows


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid


def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))


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


    # 3. Close connection
    conn.close()
    print('connection closed')


    # 4. Create connection (prove that it will open when db already exists)
    conn = create_connection(database)
    print('connection created (second time)')


    # 5. Create tables
    create_projects_table(conn)
    create_tasks_table(conn)
    print('tables created')


    # 6. Insert
    project = ('A first project', '2015-01-01', '2015-01-30');
    project_id = insert_project(conn, project)

    project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
    project_id = insert_project(conn, project)

    print('project added')

    task = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
    task_id = insert_task(conn, task)

    task = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
    task_id = insert_task(conn, task)

    print('tasks added')


    # 7. Read all
    rows = select_all_tasks(conn)
    project_id_for_read = rows[0][0]  #save id of first project for next step

    for row in rows:
        print(row)

    print('all tasks printed')


    # 8. Read by key
    rows = select_project_by_id(conn, project_id_for_read)
    for row in rows:
        print(row)

    print('specific project printed')


    # 9. Update
    task_with_id = (2, '2015-01-04', '2015-01-06',2)
    task_id = update_task(conn,task_with_id)

    print('task updated')


    # 10. Delete
    delete_task(conn, task_id)
    print('task deleted')


    # 11. Commit and close
    conn.commit()
    print('connection commit()')

    conn.close()
    print('database closed')
