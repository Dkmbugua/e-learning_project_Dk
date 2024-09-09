import sqlite3
import click
from flask import current_app, g


def get_db():
    #checks if a database connection is already stored in 'g'
    if 'db'not in g:
        #creates a new connection to the sqlite database
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], #path to the sqlite databasefile
            detect_types=sqlite3.PARSE_DECLTYPES #parse types for better handling
        )
        #use dict_like rowsfor easier access by column name 
        g.db.row_factory = sqlite3.Row

    return g.db #returns database connection

def close_db(e=None):
    #retrieve and remove connection from 'g'
    db =g.pop('db', None)

    if db is not None:
        #closes the database connection idf it exist
        db.close()

def init_db():
    #get a connection to the database
    db = get_db()

    #open the schema file and execute its contents to create tables
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """clear the existing tables and create new table"""

    #call the init_db function to initialize the database
    init_db()
    #output the message to indicatethe database was initialized
    click.echo('initialized the database.')

def init_app(app):
    """register unctions with app instance"""
    app.teardown_appcontext(close_db)#close the database connection after each request
    app.cli.add_command(init_db_command) #add 'init-db as a cli command'




    