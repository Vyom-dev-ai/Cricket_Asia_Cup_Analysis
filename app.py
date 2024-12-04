from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

# Database configuration
DATABASE = 'cricket_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create a route for the home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return """
    <h1>About</h1>
    <p>Source: Your CSV File</p>
    <p>Variables: Team, Opponent, Format, Ground, Year, Toss, Selection, Run Scored, Wicket Lost, Fours, Sixes, Extras, Run Rate, Avg Bat Strike Rate, Highest Score, Wicket Taken, Given Extras, Highest Individual Wicket, Player Of The Match, Result</p>
    """

@app.route('/data')
def data():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM cricket_matches")
    rows = cur.fetchall()
    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
