from werkzeug.urls import url_fix
from secrets import token_urlsafe
from flask import Flask, request, abort, render_template, redirect, url_for
from unidecode import unidecode
import os, re

app = Flask(__name__)
app.config['FLAG'] = os.environ['FLAG']



def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

bad_chars = "'_#&;+"
bad_cmds = ['import', 'os', 'popen', 'subprocess', 'env', 'print env']

@app.route("/")
def index():
    return render_template("index.html", error=request.args.get("error"))       

@app.route('/admin', methods=['GET'])
def admin():
    return abort(403)

@app.route("/feedback", methods=["POST"])
def create():
    username = request.form.get("username", "")
    subject = request.form.get("subject", "")
    content = request.form.get("content", "")
    if len(subject) > 128 or "_" in subject or "/" in subject:
        return redirect(url_for("index", error="subject_error"))
    if "_" in content or "." in content or len(content) > 512:
        return redirect(url_for("index", error="content_error"))
    if any(char in bad_chars for char in content):
        return redirect(url_for("index", error="content_error"))
    for cmd in bad_cmds:
        if findWholeWord(cmd)(content):
            return redirect(url_for("index", error="content_error"))
    name = "static/feedbacks/" + url_fix(unidecode(subject).replace(" ", ""))  + token_urlsafe(16) + ".html"
    with open(name, "w") as f:
        feedback = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Feedback Form</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous"/>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js" integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN" crossorigin="anonymous"></script>
  </head>
  <body>
    <!-- Responsive navbar-->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/admin">Admin Panel</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <div class="text-center mt-5">
        <h1>From {username}</h1>
        <p class="lead">{subject}</p>
      </div>
      <div class="container">
        <div class="alert alert-error" role="alert">
          <p>{content}</p>
        </div>
      </div>       
      <div class="container">
        <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
        </footer>
      </div>
    </div>          
  </body>
</html>'''
        f.write(feedback)
    return redirect(name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])
