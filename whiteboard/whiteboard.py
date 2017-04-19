"""
Project Whiteboard
By: Srushti Patel, John Ferguson, Kris Gates, and Josh Milford
This is the code that you get after following the Flask whiteboard tutorial.
We will be heavily modifying this file!
"""

# all the imports
import os
import sqlite3
import tempfile
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

#config file start
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , whiteboard.py

# Flask's debug parameter automatically monitors for code changes
# (exchanges performance for not having to restart the app for changes)
app.run(debug = True)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'whiteboard.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('WHITEBOARD_SETTINGS', silent=True)
#config file end

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
	
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
		
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
	
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
	
@app.route('/board')
def board():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('board.html', entries=entries)
	
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    if len(request.form['text']) != 0:
        db.execute('insert into entries (title, text) values (?, ?)',
                     [request.form['title'], request.form['text']])
        db.commit()
        flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO: Execute a query to populate a dictionary of existing users.
    usersDict = {}
    # If there isn't already a user present with that user name...
    if request.form['username'] not in usersDict:
        # TODO: Insert record for new user and return confirmation page.
        pass
    # ... else, the user already exists.
    else:
        # TODO: Return an error and return the user to the registration page.
        pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('board'))
    return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
	
