from typing import Tuple
from flask import Flask, render_template, session, request
from uuid import uuid4
from captcha.image import ImageCaptcha
import os
import base64

app = Flask(__name__)
app.secret_key = os.urandom(31)

# Methods


def generate_captcha() -> Tuple[str, str]:
    image = ImageCaptcha(width=280, height=90)
    captcha_text = str(uuid4()).split("-")[0]
    data = image.generate(captcha_text)
    return (captcha_text, base64.b64encode(data.read()).decode("utf-8"))

# Routes


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("login", False):
        return index()
    if request.method == "GET":
        captcha_text, captcha_image = generate_captcha()
        captcha_image = "data:image/png;base64," + captcha_image
        session["captcha"] = captcha_text
        return render_template("login.html", captcha_image=captcha_image)
    elif request.method == "POST":
        data = request.form
        if data.get("username", "") == "asd" and data.get("password", "") == "asd":
            if data.get("captcha") == session.get("captcha", ""):
                session["login"] = True
                return index()
            session["login"] = False
            return "Failed to validate Captcha."
        else:
            session["login"] = False
            return "Incorrect username and/or password."
    else:
        return "Something went wrong."


@app.route("/", methods=["GET"])
def index():
    if session.get("login", False):
        return render_template("index.html")
    return login()


@app.route("/logout", methods=["GET"])
def logout():
    session["login"] = False
    return login()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
