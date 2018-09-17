# sqlitesample

It's exactly that, a sample of common DB operations in Python against sqlite.

1. Delete database
2. Create connection (which will create a db if it doesn't exit)
3. Close connection
4. Create connection (prove that it will open when db already exists)
5. Create tables
6. Insert
7. Read all
8. Read by key
9. Update
10. Delete
11. Commit and close

## Credits
Most (all?) the code here has been pulled from various sources and tested.

http://www.sqlitetutorial.net/sqlite-python


# main_db.py
This is a python class that encapulates all the above into a.... python class.
This class is not generic but implementation specific which makes this a sample template.