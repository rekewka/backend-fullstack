from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sqlite3 as sql

app = Flask(__name__)

def InitDb():
    connection = sql.connect('db.sl3')
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date_created TEXT
        )
        '''
    )
    connection.commit()
    connection.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        connection = sql.connect('db.sl3')
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO tasks (content, date_created)
            VALUES (?, ?)
            ''', 
            (task, date)
        )
        connection.commit()  
        connection.close()
    return redirect(url_for('my_tasks'))

@app.route('/direct', methods=['GET'])
def my_tasks():
    connection = sql.connect('db.sl3')
    cursor = connection.cursor()
    cursor.execute('SELECT id, content, date_created FROM tasks')
    tasks = cursor.fetchall()
    connection.close()
    return render_template('tasks.html', tasks=tasks)

if __name__ == "__main__":
    InitDb()
    app.run(debug=True)
