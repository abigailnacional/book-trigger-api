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
from flask_restful import Api, Resource, reqparse #not used yet because functions cannot yet be called with the standard API request format
import uuid

app = create_app()
api = Api(app)

#Create function, use when given url to BookTriggerWarnings page
def create_book_from_url(session, url):
     aBook = scrapeWikiArticle(url)
     create_book(session, aBook)

#Create function, use when given a Book object. Should only be used by the API, not a human.
def create_book(session, someBook):
     session.add(someBook)
     print("Added book to database.")
     print("ID:", str(someBook.id))
     print("Title:", someBook.title)
     print("Author(s):", someBook.authors)
     print("Genre(s):", someBook.genres)
     print("Trigger(s):", someBook.triggers)
     print("Age group:", someBook.age_group)
     print("Publish date:", someBook.published)
     print("Publisher:", someBook.publisher)
     return someBook, 200

#Read function (getter). Use when given a book title.
def get_book_from_title(session, someTitle):
     found = session.query(Book).filter(Book.title==someTitle).first()
     if found != None:
          print("ID:", str(found.id))
          print("Title:", found.title)
          print("Author(s):", found.authors)
          print("Genre(s):", found.genres)
          print("Trigger(s):", found.triggers)
          print("Age group:", found.age_group)
          print("Publish date:", found.published)
          print("Publisher:", found.publisher)
          return found, 200
     else:
          print("Record not found.")
          return "Record not found", 404

#Read function (getter). Use when given a Book ID.
def get_book_from_ID(session, someID):
     found = session.query(Book).filter(Book.id==someID).first()
     if found != None:
          print("ID:", str(found.id))
          print("Title:", found.title)
          print("Author(s):", found.authors)
          print("Genre(s):", found.genres)
          print("Trigger(s):", found.triggers)
          print("Age group:", found.age_group)
          print("Publish date:", found.published)
          print("Publisher:", found.publisher)
          return found, 200
     else:
          print("Record not found.")
          return "Record not found", 404

#Update function. Deletes old Book record and replaces it with the updated version, but keeps the same ID.
def update_book(session, someTitle, someAuthors, someGenres, someTriggers, someAgeGroup, somePubDate, somePublisher):
     outdated = session.query(Book).filter(Book.title==someTitle).first()
     if outdated != None:
          print("Old record:")
          print("ID:", str(outdated.id))
          print("Title:", outdated.title)
          print("Author(s):", outdated.authors)
          print("Genre(s):", outdated.genres)
          print("Trigger(s):", outdated.triggers)
          print("Age group:", outdated.age_group)
          print("Publish date:", outdated.published)
          print("Publisher:", outdated.publisher)
          updated = Book(
                    id=outdated.id, #Keep the same ID
                    title=someTitle,
                    authors=someAuthors,
                    genres=someGenres,
                    triggers=someTriggers,
                    age_group=someAgeGroup,
                    published=somePubDate,
                    publisher=somePublisher)
          delete_book(session, outdated)
          print("\nNew record:")
          create_book(session, updated)
          return updated, 200
     else:
          updated = Book(
                    id=uuid.uuid4(), #Need to make an ID since there is no old one to reuse
                    title=someTitle,
                    authors=someAuthors,
                    genres=someGenres,
                    triggers=someTriggers,
                    age_group=someAgeGroup,
                    published=somePubDate,
                    publisher=somePublisher)
          print("Old record not found, creating new record.")
          print("New record:")
          create_book(session, updated)
          return updated, 201
          
#Delete function, use when given only a title.
def delete_book_given_title(session, someTitle):
     tbdeleted = session.query(Book).filter(Book.title==someTitle).first()
     if tbdeleted != None:
          delete_book(session, tbdeleted)
     else:
          print("Record not found.")
          return "Record not found", 404

#Delete function, use when given a book ID.
def delete_book_given_ID(session, someID):
     tbdeleted = session.query(Book).filter(Book.id==someID).first()
     if tbdeleted != None:
          delete_book(session, tbdeleted)
     else:
          print("Record not found.")
          return "Record not found", 404

#Delete function, use when given a Book object. Never used by a human, only by the API.
def delete_book(session, aBook):
     print("Deleted", aBook.title, "from database.")
     session.delete(aBook)
     return 200

#@app.route("/")
#def index():
#     return render_template("index.html")

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
     
     #print("Checking create_book_from_url.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: create_book_from_url(s, "https://booktriggerwarnings.com/index.php?title=A_Sea_of_Pearls_%26_Leaves_by_Rosalyn_Briar"))
     #print("Checking get_book_from_title.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: get_book_from_title(s, "A Sea of Pearls & Leaves"))
     #print("Checking get_book_from_ID.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: get_book_from_ID(s, "357ee79c-8672-4bcc-9760-81640c960699"))
     #print("Checking update_book when the book is in the database.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: update_book(s, "HEY UPDATED", "Dad", "Horror", "Gore", "Adult", "Today", "House Pubs"))
     #print("Checking update_book when the book is NOT in the database.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: update_book(s, "HEY UPDATED", "Dad", "Horror", "Gore", "Adult", "Today", "House Pubs"))
     #print("Checking delete_book_given_title.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: delete_book_given_title(s, "A Sea of Pearls & Leaves"))
     #print("Checking delete_book_given_ID.")
     #run_transaction(sessionmaker(bind=engine),
     #               lambda s: delete_book_given_title(s, "A Sea of Pearls & Leaves"))
     
     
     

