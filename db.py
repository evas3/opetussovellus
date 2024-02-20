from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SEC_KEY")
db = SQLAlchemy(app)
