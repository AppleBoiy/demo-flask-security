import os
from flask import Flask
from flask_mailman import Mail

from flask_security import SQLAlchemySessionUserDatastore, Security, login_required

from dotenv import load_dotenv
from database import db
from models.auth import User, Role

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "0aedgaii451cef0af8bd6432ec4b317c8999a9f8g77f5f3cb49fb9a8acds51d"
)
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get(
    "SECURITY_PASSWORD_SALT",
    "ab3d3a0f6984c4f5hkao41509b097a7bd498e903f3c9b2eea667h16",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECURITY_REGISTERABLE"] = True
app.config["SECURITY_CONFIRMABLE"] = True

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
mail = Mail(app)

uri = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = uri
db.init_app(app)
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.route("/")
def home():
    return "Hello, world!"


# At bottom of file
@app.route("/protected")
@login_required
def protected():
    return "You're logged in!"


if __name__ == '__main__':
    app.run(debug=True)
