from flask import Flask, flash, redirect, render_template, request, session, g
from flask_session import Session
from functools import wraps
import sqlite3


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DB = "data.db"

search_req = ""

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_connection(db_file):
    """ Create a connection to the sql database
    Parameters: 
    db_file - The name of the file
    Returns: A connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except sqlite3.Error as e:
        print(e)
    return None


def SQL(*args):
    query = str(args[0])

    conditions = []
    if len(args) > 0:
        for i in range(0, len(args), 1):
            if i != 0:
                conditions.append(args[i])

    conn = create_connection(DB)
    cur = conn.cursor()
    cur.execute(query, tuple(conditions))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result

def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route("/", methods=["GET", "POST"])
def index():
        return render_template("index.html")