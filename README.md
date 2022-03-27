# book-trigger-api
Code for the Book Trigger API project for MLH's Hack Empowered Hackathon. [Here is the Devpost page.](https://devpost.com/software/book-trigger-warnings-api)

# Acknowledgements
Code for connecting the Flask app to CockroachDB is based off of [this repository](https://github.com/cockroachlabs/example-app-python-sqlalchemy) and [this tutorial](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html).

Basic Flask boilerplate comes from [this repository](https://github.com/abigailnacional/flask-boilerplate).

The information about triggers from certain books is from [this website](https://booktriggerwarnings.com/).

I used [this tutorial](https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/) to learn about how to web scrape Wiki articles and [this tutorial](https://rapidapi.com/blog/how-to-build-an-api-in-python/) in order to learn about how to build an API in Python with RapidAPI.

# Installation/Running the Code

1. Clone the repo
   ```sh
   git clone https://github.com/abigailnacional/book-trigger-api.git
   ```
2. Navigate to the folder
   ```sh
   cd book-trigger-api
   ```
3. Run install.sh by dragging the file into your terminal.

4. To initialize the database, use the cockroach sql command to execute the SQL statements in the dbinit.sql file:
   ```sh
   cat dbinit.sql | cockroach sql --url "<connection-string>"
   ```
   Where connection-string is the connection string provided in the Connection info window of the CockroachDB Cloud Console.

   Note that you need to provide a SQL user password in order to securely connect to a CockroachDB Cloud cluster. The connection string should have a placeholder for the password (ENTER-PASSWORD).

5. Run the following commands in your terminal:
   ```sh
   export FLASK_ENV=‘development’
   . env/bin/activate
   python3 app.py '<connection_string>'
   ```

6. Type "localhost:5000" into your browser's URL bar and press enter.
