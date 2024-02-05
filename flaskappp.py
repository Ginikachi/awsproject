import sqlite3

from flask import Flask , request , g , render_template
from flask import *
app = Flask(__name__)


@app.route('/')
def home():
  return render_template('login.html')



if __name__ == '__main__':
  app.run()


DATABASE = 'users.db'

app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


@app.route("/viewdb")
def viewdb():
    rows = execute_query("""SELECT * FROM users""")
    return '<br>'.join(str(row) for row in rows)

@app.route('/signup')
def signup():
    return render_template('register.html')


@app.route('/Login')
def Login():
    return render_template("login.html")


@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("you successfully logged out")
   return redirect(url_for('home'))

def get_user_info(user_name):
    con = connect_to_database()
    cur = con.cursor()
    cur.execute("SELECT * FROM users where username = (?)" , [user_name])
    data = cur.fetchall()
    return data

    
@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        data = get_user_info(username)
        for item in data:
            username = request.form['username']
            if password != item[4]:
                error = "invalid password"
            elif username != item[3]:
                error = "username don't have account"

            else:
                msg = "you are successfuly logged in"
                session[username] = username
                return render_template('index.html' , data= data, msg = msg )
        return render_template('login.html',error = error)


app.secret_key = "secret"

@app.route("/register" , methods =["GET", "POST"])
def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            con = connect_to_database()
            cur = con.cursor()
            cur.execute("INSERT INTO users(firstname,lastname,email, username, password) VALUES (?,?,?,?,?)",(firstname,lastname,email, username , password) )
            con.commit()
            msg = "successfully registered"
            data = get_user_info(username)
        return render_template('result.html' , data= data, msg = msg )



