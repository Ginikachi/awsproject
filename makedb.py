
import sqlite3
conn = sqlite3.connect("users.db")
cur = conn.cursor()
conn.execute("CREATE TABLE users (firstname text , lastname text , email text , username text unique , password text)")
print("database successfully created")
conn.commit()
conn.close()
