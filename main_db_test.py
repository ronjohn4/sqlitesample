import main_db
import os
import unittest


class TestStringMethods(unittest.TestCase):
    database = 'main_db_test.db'
    class_instance = None

    def setUp(self):
        # Delete previous instances of the DB that weren't cleaned up
        try:
            os.remove(self.database)
            print('Previous database file deleted: {0}'.format(self.database))
        except Exception as e:
            print(e)

        self.class_instance = main_db.DB(self.database)

    def tearDown(self):
        del self.class_instance

        # Only clean up db file if not needed for offline manual checking
        # try:
        #     os.remove(self.database)
        # except Exception as e:
        #     print(e)


    def test_conn(self):
        self.assertIsNotNone(self.class_instance.conn)

    def test_database(self):
        self.assertEqual(self.class_instance.database, self.database)

    def test_close(self):
        self.class_instance.close()
        self.assertIsNone(self.class_instance.conn)

    def test_project_insert(self):
        project = main_db.project
        project.id = None
        project.begin_date = '2017-12-01'
        project.end_date = '2018-01-01'
        project.name = 'test project'
        cur_pos = self.class_instance.projects.insert(project)
        self.assertIsNotNone(cur_pos)





if __name__ == '__main__':
    unittest.main()
