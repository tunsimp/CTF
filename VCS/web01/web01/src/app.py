import os
from flask import Flask, request, session, Response, url_for, redirect
import hashlib
import uuid
import db

with open("/flag1.txt", "r") as f:
    FLAG1 = f.read().strip()
with open("/flag2.txt", "r") as f:
    FLAG2 = f.read().strip()
os.system("rm /flag1.txt /flag2.txt")

db.init_db()

app = Flask(__name__, static_url_path="")
app.config["SECRET_KEY"] = os.urandom(42)


@app.route("/")
def source():
    return open(__file__).read()


@app.route("/meme")
def meme():
    meme = request.args.get("id", None)
    try:
        uuid.UUID(str(meme))
    except ValueError:
        return "Invalid meme id", 400
    
    meme = db.get_meme(meme)
    if meme is None:
        return "Meme not found", 404
    filename = meme[0]

    try:
        file_data = open(f"./meme/{filename}", "rb").read()
        response = Response(file_data)
        response.headers["Content-Type"] = "image/png"
        return response
    except FileNotFoundError:
        return "File not found", 404


@app.route("/freeflag")
def index():
    segcret = request.args.get("segcret", None)

    if segcret is None:
        return "Please provide a secret key!"

    session["flag"] = FLAG1
    if segcret == app.config["SECRET_KEY"]:
        return session["flag"]
    else:
        return "Incorrect secret key!"


@app.route("/login")
def login():
    username = request.args.get("username", None)
    password = request.args.get("password", None)
    if username is None or password is None:
        return "Please provide username and password!"

    user = db.get_user(username)
    if user is None:
        return "User not found", 403

    hashed_password = hashlib.md5(password.encode()).hexdigest()
    if user[1] == hashed_password:
        session["username"] = user[0]
        return "Login successful!"
    else:
        return "Incorrect password!", 403


@app.route("/admin")
def admin():
    if session.get("username") != "admin":
        return "You are not admin!", 403

    return f"Welcome admin! Here is your flag: {FLAG2}"


@app.route("/upload-meme", methods=["POST"])
def upload_meme():
    meme = request.files.get("meme", None)
    title = request.form.get("title", None)
    if meme is None or title is None:
        return "Please provide a meme and title!", 400

    filename = meme.filename
    if ".." in filename or "/" in filename:
        # I gave you a chance to upload a meme, but you tried to do something else
        filename = f"{uuid.uuid4()}.png"

    id=str(uuid.uuid4())
    meme.save(f"./meme/{filename}")
    res = db.add_meme(title, filename, id)
    if res == True:
        return redirect(url_for("meme", id=id))
    else:
        return f"Failed to upload meme!\n{res}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
