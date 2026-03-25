
from flask import Flask, render_template, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secretkey"

def db():
    return sqlite3.connect("database.db")

def init():
    if not os.path.exists("database.db"):
        conn = db()
        c = conn.cursor()
        c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
        c.execute("INSERT INTO users (username,password,role) VALUES ('admin','admin','admin')")
        c.execute("CREATE TABLE leads (id INTEGER PRIMARY KEY, company TEXT, value REAL, status TEXT)")
        c.execute("CREATE TABLE pharmacies (id INTEGER PRIMARY KEY, name TEXT, area TEXT)")
        c.execute("CREATE TABLE influencers (id INTEGER PRIMARY KEY, name TEXT, platform TEXT)")
        conn.commit()
        conn.close()

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=request.form["username"]
        p=request.form["password"]
        conn=db()
        res=conn.execute("SELECT * FROM users WHERE username=? AND password=?",(u,p)).fetchone()
        if res:
            session["user"]=u
            session["role"]=res[3]
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/leads", methods=["GET","POST"])
def leads():
    conn=db()
    if request.method=="POST":
        conn.execute("INSERT INTO leads (company,value,status) VALUES (?,?,?)",
        (request.form["company"],request.form["value"],request.form["status"]))
        conn.commit()
    data=conn.execute("SELECT * FROM leads").fetchall()
    return render_template("leads.html",data=data)

@app.route("/pharmacies", methods=["GET","POST"])
def pharmacies():
    conn=db()
    if request.method=="POST":
        conn.execute("INSERT INTO pharmacies (name,area) VALUES (?,?)",
        (request.form["name"],request.form["area"]))
        conn.commit()
    data=conn.execute("SELECT * FROM pharmacies").fetchall()
    return render_template("pharmacies.html",data=data)

@app.route("/influencers", methods=["GET","POST"])
def influencers():
    conn=db()
    if request.method=="POST":
        conn.execute("INSERT INTO influencers (name,platform) VALUES (?,?)",
        (request.form["name"],request.form["platform"]))
        conn.commit()
    data=conn.execute("SELECT * FROM influencers").fetchall()
    return render_template("influencers.html",data=data)

if __name__=="__main__":
    init()
    app.run(host="0.0.0.0", port=10000)
