from flask import Flask, jsonify
import cx_Oracle

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = cx_Oracle.connect(
        user="sytem",  
        password="root",  
       dsn = "localhost:1521/ORCL"
    )
    return connection

@app.route('/')
def hello_world():
    return 'Hello, World!'

# API to get leaderboard based on runs scored
@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT p.name, SUM(perf.runs_scored) AS total_runs
        FROM Performance perf
        JOIN Player p ON perf.player_id = p.player_id
        GROUP BY p.name
        ORDER BY total_runs DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()

    leaderboard = []
    for row in result:
        leaderboard.append({
            'player': row[0],
            'runs': row[1]
        })
    
    cursor.close()
    connection.close()
    return jsonify(leaderboard)

# API to get performance report of a specific player
@app.route('/performance/<int:player_id>', methods=['GET'])
def get_performance(player_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT m.match_date, perf.runs_scored, perf.wickets_taken
        FROM Performance perf
        JOIN Match m ON perf.match_id = m.match_id
        WHERE perf.player_id = :player_id
    """
    cursor.execute(query, player_id=player_id)
    result = cursor.fetchall()

    performance_report = []
    for row in result:
        performance_report.append({
            'match_date': row[0],
            'runs_scored': row[1],
            'wickets_taken': row[2]
        })
    
    cursor.close()
    connection.close()
    return jsonify(performance_report)

if __name__ == '__main__':
    app.run(debug=True)

