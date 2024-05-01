import json
import secrets
import string

from flask import jsonify, render_template, request, url_for, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.sql import text
from flask_login import login_user, login_required, logout_user, current_user
from app import app
from app import db
from app import login_manager
from app.models.authuser import AuthUser


# from app import oauth

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our
    # user table, use it in the query for the user
    return AuthUser.query.get(int(user_id))


@app.route("/")
def home():
    return "Flask says 'Hello world!'"


@app.route("/crash")
def crash():
    return 1 / 0


@app.route("/db")
def db_connection():
    try:
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return "<h1>db works.</h1>"
    except Exception as e:
        return "<h1>db is broken.</h1>" + str(e)


def gen_avatar_url(email, name):
    bgcolor = generate_password_hash(email, method="sha256")[-6:]
    color = hex(int("0xffffff", 0) - int("0x" + bgcolor, 0)).replace("0x", "")
    lname = ""
    temp = name.split()
    fname = temp[0][0]
    if len(temp) > 1:
        lname = temp[1][0]

    avatar_url = (
            "https://ui-avatars.com/api/?name="
            + fname
            + "+"
            + lname
            + "&background="
            + bgcolor
            + "&color="
            + color
    )
    return avatar_url
