from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "taskmanager"

# Create Database
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        status TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home
@app.route('/')
def home():
    if "user" in session:
        return redirect('/dashboard')
    return redirect('/login')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )
            conn.commit()
            flash("Registration Successful")
            return redirect('/login')
        except:
            flash("Username already exists")

        conn.close()

    return render_template("register.html")

# Login
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method=="POST":

        username=request.form['username']
        password=request.form['password']

        conn=sqlite3.connect("database.db")
        cur=conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username,password)
        )

        user=cur.fetchone()

        if user:
            session["user"]=user[0]
            return redirect('/dashboard')

        flash("Invalid Login")

    return render_template("login.html")

# Dashboard
@app.route('/dashboard')
def dashboard():

    if "user" not in session:
        return redirect('/login')

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user"],)
    )

    tasks=cur.fetchall()

    return render_template("dashboard.html",tasks=tasks)

# Add Task
@app.route('/add',methods=['POST'])

def add():

    title=request.form['title']
    description=request.form['description']

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute(
        "INSERT INTO tasks(title,description,status,user_id) VALUES(?,?,?,?)",
        (title,description,"Pending",session["user"])
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# Complete Task
@app.route('/complete/<int:id>')

def complete(id):

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute(
        "UPDATE tasks SET status='Completed' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# Delete Task
@app.route('/delete/<int:id>')

def delete(id):

    conn=sqlite3.connect("database.db")
    cur=conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# Logout
@app.route('/logout')

def logout():

    session.pop("user",None)

    return redirect('/login')

if __name__=="__main__":
    app.run(debug=True)
