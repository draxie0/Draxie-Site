from flask import Flask,request,redirect
import sqlite3

app = Flask(__name__)

db=sqlite3.connect("draxie.db",check_same_thread=False)
cur=db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users(email TEXT,password TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS messages(text TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS visits(ip TEXT)")
db.commit()

def page(content):

    return f"""
<html>

<head>

<title>DRAXIE NETWORK</title>

<style>

body{{
background:black;
color:#00ff9f;
font-family:monospace;
text-align:center;
}}

h1{{text-shadow:0 0 20px #00ff9f}}

.box{{
border:1px solid #00ff9f;
width:300px;
margin:auto;
margin-top:20px;
padding:20px;
}}

input{{
background:black;
border:1px solid #00ff9f;
color:#00ff9f;
padding:8px;
}}

button{{
background:black;
border:1px solid #00ff9f;
color:#00ff9f;
padding:8px;
}}

</style>

</head>

<body>

<h1>DRAXIE NETWORK</h1>

{content}

</body>

</html>
"""

@app.route("/",methods=["GET","POST"])
def home():

    ip=request.remote_addr
    cur.execute("INSERT INTO visits VALUES(?)",(ip,))
    db.commit()

    return page("""

<div class=box>

<h2>Giriş</h2>

<form method=POST action="/login">

<input name=email placeholder=email><br><br>
<input name=password placeholder=şifre type=password><br><br>

<button>Giriş</button>

</form>

</div>

<div class=box>

<h2>Kayıt</h2>

<form method=POST action="/register">

<input name=email placeholder=email><br><br>
<input name=password placeholder=şifre type=password><br><br>

<button>Kayıt ol</button>

</form>

</div>

""")

@app.route("/register",methods=["POST"])
def register():

    email=request.form["email"]
    pw=request.form["password"]

    cur.execute("INSERT INTO users VALUES(?,?)",(email,pw))
    db.commit()

    return redirect("/")

@app.route("/login",methods=["POST"])
def login():

    email=request.form["email"]
    pw=request.form["password"]

    cur.execute("SELECT * FROM users WHERE email=? AND password=?",(email,pw))

    if cur.fetchone():

        return redirect("/panel")

    return "giriş başarısız"

@app.route("/panel",methods=["GET","POST"])
def panel():

    if request.method=="POST":

        msg=request.form["msg"]
        cur.execute("INSERT INTO messages VALUES(?)",(msg,))
        db.commit()

    cur.execute("SELECT * FROM messages")
    msgs=cur.fetchall()

    cur.execute("SELECT * FROM visits")
    visits=cur.fetchall()

    msg_html=""
    for m in msgs:
        msg_html+=f"<p>{m[0]}</p>"

    visit_html=""
    for v in visits[-10:]:
        visit_html+=f"<p>{v[0]}</p>"

    return page(f"""

<div class=box>

<h2>Mesaj bırak</h2>

<form method=POST>

<input name=msg>
<button>Gönder</button>

</form>

{msg_html}

</div>

<div class=box>

<h2>Son ziyaretçiler</h2>

{visit_html}

</div>

""")

app.run(host="0.0.0.0",port=10000)
