from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="steamuser",
    password="mypassword",
    database="steamdata"
)

@app.route('/', methods=['GET'])
def index():
    cursor = conn.cursor(dictionary=True)
    keyword = request.args.get('keyword')

    if keyword:
        cursor.execute("""
            SELECT sg.* FROM steam_games sg
            INNER JOIN (
                SELECT Game, MAX(Date) AS MaxDate
                FROM steam_games
                WHERE Game LIKE %s
                GROUP BY Game
            ) latest ON sg.Game = latest.Game AND sg.Date = latest.MaxDate
            ORDER BY sg.HeatRatio DESC
            LIMIT 100
        """, (f"%{keyword}%",))
    else:
        cursor.execute("""
            SELECT sg.* FROM steam_games sg
            INNER JOIN (
                SELECT Game, MAX(Date) AS MaxDate
                FROM steam_games
                GROUP BY Game
            ) latest ON sg.Game = latest.Game AND sg.Date = latest.MaxDate
            ORDER BY sg.HeatRatio DESC
            LIMIT 100
        """)

    results = cursor.fetchall()
    cursor.close()
    return render_template("index.html", results=results, keyword=keyword or '')

if __name__ == '__main__':
    app.run(debug=True)
