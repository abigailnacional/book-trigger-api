from flask import Flask, render_template
from appmodels import create_app
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm

app = create_app()
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

@app.route("/")
def index():
     return render_template("index.html")

if __name__ == "__main__":
  app.run()