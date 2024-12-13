from flask import Flask, render_template, g, jsonify
import requests # type: ignore
import sqlite3
import credentials

# Example usage:
print(credentials.cricket_api_key)
print(credentials.database_password)


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

@app.route('/cricket')##secured version
def cricket():
    api_key = credentials.cricket_api_key
    # Example endpoint for a cricket API
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q=London"
    
    # Making a request to the Cricket API
    response = requests.get(url)
    cricket_data = response.json()
    
    # Return the weather data in a safe, user-friendly way
    return jsonify(cricket_data)

@app.route('/asiacup')##pulling credentials
def asiacup():
    api_key = credentials.cricket_api_key
    return f"Your Weather API Key is: {api_key}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/data')
def data():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM cricket_matches")
    rows = cur.fetchall()
    return render_template('data.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
