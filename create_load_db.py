import pandas as pd
import sqlite3

# Read the dataset
csv_file = 'C:\\Users\\orbit\\OneDrive\\Documents\\flask_python_cricproject\\data\\asiacup.csv'  # Specify the path to your CSV file
df = pd.read_csv(csv_file)

# Print the DataFrame column names and count
print("DataFrame Columns:", df.columns)
print("Number of columns in DataFrame:", len(df.columns))

# Clean column names by stripping leading/trailing whitespace
df.columns = df.columns.str.strip()


# Fill missing values for all columns with appropriate defaults
df = df.fillna({
    'Team': 'Unknown',
    'Opponent': 'Unknown',
    'Format': 'Unknown',
    'Ground': 'Unknown',
    'Year': 0,
    'Toss': 'Unknown',
    'Selection': 'Unknown',
    'Run Scored': 0, 
    'Wicket Lost': 0,
    'Fours': 0,
    'Sixes': 0,
    'Extras': 0,
    'Run Rate': 0.0,
    'Avg Bat Strike Rate': 0.0,
    'Highest Score': 0,
    'Wicket Taken': 0,
    'Given Extras': 0,
    'Highest Individual wicket': 0,
    'Player Of The Match': 'Unknown',
    'Result': 'Unknown'
})

# Print the DataFrame to verify the changes
print("Cleaned DataFrame Columns:", df.columns)
print("DataFrame after filling missing values:")
print(df.head())

# Connect to SQLite database (it will create a new DB if it doesn't exist)
conn = sqlite3.connect('cricket_data.db')
cursor = conn.cursor()

# Create table for cricket match data
cursor.execute('''
CREATE TABLE IF NOT EXISTS cricket_matches (
    Team TEXT,
    Opponent TEXT,
    Format TEXT,
    Ground TEXT,
    Year INTEGER,
    Toss TEXT,
    Selection TEXT,
    Run_Scored INTEGER,
    Wicket_Lost INTEGER,
    Fours INTEGER,
    Sixes INTEGER,
    Extras INTEGER,
    Run_Rate REAL,
    Avg_Bat_Strike_Rate REAL,
    Highest_Score INTEGER,
    Wicket_Taken INTEGER,
    Given_Extras INTEGER,
    Highest_Individual_wicket INTEGER,
    Player_Of_The_Match TEXT,
    Result TEXT
)
''')

# Loop through each row of the DataFrame and insert data into the database
for index, row in df.iterrows():
    print(f"Inserting row with values: {row.to_dict()}")
    cursor.execute('''
    INSERT INTO cricket_matches (Team, Opponent, Format, Ground, Year, Toss, Selection, Run_Scored, 
                         Wicket_Lost, Fours, Sixes, Extras, Run_Rate, Avg_Bat_Strike_Rate, 
                         Highest_Score, Wicket_Taken, Given_Extras, Highest_Individual_wicket, 
                         Player_Of_The_Match, Result)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (row['Team'], row['Opponent'], row['Format'], row['Ground'], row['Year'], row['Toss'],
          row['Selection'], int(row['Run Scored']), int(row['Wicket Lost']), int(row['Fours']),
          int(row['Sixes']), int(row['Extras']), float(row['Run Rate']), float(row['Avg Bat Strike Rate']),
          int(row['Highest Score']), int(row['Wicket Taken']), int(row['Given Extras']),
          int(row['Highest Individual wicket']), row['Player Of The Match'], row['Result']))

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into the database.")
