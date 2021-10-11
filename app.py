from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import os

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sd3a_music_festival'

app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)




MUSIC_FESTIVALS = [
    "Electricpicnic",
    "Longitude",
    "Tomorrowland",
    "Reading"
]

REGISTRANTS = {}


@app.route("/")
def index():
    return render_template("index.html", festivals = MUSIC_FESTIVALS)


@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    festival_chosen = request.form.get("musicfestival")
    print(email)
    print(festival_chosen)
    if not email or not festival_chosen or festival_chosen not in MUSIC_FESTIVALS:
        return render_template("failure.html")
    REGISTRANTS[email] = festival_chosen
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO registrant(name, festival) VALUES (%s, %s)", (email, festival_chosen))
    mysql.connection.commit()
    cur.close()
    message = Message("You are registered", recipients=[email])
    mail.send(message)
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    cur = mysql.connection.cursor()
    cur.execute("select name, festival from registrant")
    registrants = cur.fetchall()
    return render_template("registrants.html", registrants = registrants)


app.run(debug=True)
