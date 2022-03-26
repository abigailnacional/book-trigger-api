from flask import render_template
from appmodels import create_app
from appmodels.models import Book
from scraper import scrapeWikiArticle
import os
from flask_sqlalchemy import SQLAlchemy
import sys
import urllib.parse
import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction

app = create_app()


def create_book(session, someBook):
     session.add(someBook)


@app.route("/")
def index():
     return render_template("index.html")


if __name__ == '__main__':
     conn_string = sys.argv[1]

     try:
          db_uri = os.path.expandvars(conn_string)
          db_uri = urllib.parse.unquote(db_uri)

          psycopg_uri = db_uri.replace(
               'postgresql://', 'cockroachdb://').replace(
               'postgres://', 'cockroachdb://').replace(
                    '26257?', '26257/bank?')
          # The "cockroachdb://" prefix for the engine URL indicates that we are
          # connecting to CockroachDB using the 'cockroachdb' dialect.
          # For more information, see
          # https://github.com/cockroachdb/sqlalchemy-cockroachdb.
          engine = create_engine(psycopg_uri)
     except Exception as e:
        print('Failed to connect to database.')
        print('{0}'.format(e))

     newBook = scrapeWikiArticle('https://booktriggerwarnings.com/index.php?title=%27Salem%27s_Lot_by_Stephen_King')
     run_transaction(sessionmaker(bind=engine),
                    lambda s: create_book(s, newBook))

