
from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "finalsecret"

def db():
    return sqlite3.connect("database.db")

def init():
    if not os.path.exists("database.db"):
        conn = db()
        c = conn.cursor()
        c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
        c.execute("INSERT INTO users (username,password,role) VALUES ('admin','admin','admin')")
        c.execute("CREATE TABLE leads (id INTEGER PRIMARY KEY, name TEXT, status TEXT)")
        c.execute("CREATE TABLE settings (id INTEGER PRIMARY KEY, company TEXT, theme TEXT)")
        c.execute("INSERT INTO settings (company,theme) VALUES ('Medical Growth System','light')")
        conn.commit()
        conn.close()

@app.route("/")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    conn=db()
    leads=conn.execute("SELECT COUNT(*) FROM leads").fetchone()[0]
    users=conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    return render_template("dashboard.html",leads=leads,users=users)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        conn=db()
        res=conn.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p)).fetchone()
        if res:
            session["user"]=u
            session["role"]=res[3]
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/users",methods=["GET","POST"])
def users():
    if session.get("role")!="admin":
        return redirect("/")
    conn=db()
    if request.method=="POST":
        conn.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
        (request.form["username"],request.form["password"],request.form["role"]))
        conn.commit()
    data=conn.execute("SELECT * FROM users").fetchall()
    return render_template("users.html",data=data)

@app.route("/settings",methods=["GET","POST"])
def settings():
    conn=db()
    if request.method=="POST":
        conn.execute("UPDATE settings SET company=?, theme=? WHERE id=1",
        (request.form["company"],request.form["theme"]))
        conn.commit()
    data=conn.execute("SELECT * FROM settings").fetchone()
    return render_template("settings.html",data=data)

if __name__=="__main__":
    init()
    app.run(host="0.0.0.0",port=10000)
