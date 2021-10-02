from flask import Flask, render_template, request

app = Flask(__name__)

MUSIC_FESTIVALS = [
    "Electic Picnic",
    "Longitude",
    "Tomorrowland",
    "Reading"
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("name") or not request.form.get("musicfestival"):
        return render_template("failure.html")
    return render_template("success.html")


app.run(debug=True)
