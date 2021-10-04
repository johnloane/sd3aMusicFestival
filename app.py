from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'sd3a_music_festival'

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
    name = request.form.get("name")
    festival_chosen = request.form.get("musicfestival")
    print(festival_chosen)
    if not name or not festival_chosen or festival_chosen not in MUSIC_FESTIVALS:
        return render_template("failure.html")
    REGISTRANTS[name] = festival_chosen
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO registrant(name, festival) VALUES (%s, %s)", (name, festival_chosen))
    mysql.connection.commit()
    cur.close()
    return redirect("/registrants")


@app.route("/registrants")
def registrants():
    return render_template("registrants.html", registrants = REGISTRANTS)


app.run(debug=True)
