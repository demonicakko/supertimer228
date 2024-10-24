from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (date TEXT PRIMARY KEY, note TEXT)''')
    conn.commit()
    conn.close()

# Функция для сохранения заметки
def save_note(date, note):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute("REPLACE INTO notes (date, note) VALUES (?, ?)", (date, note))
    conn.commit()
    conn.close()

# Функция для получения заметки для конкретной даты
def get_note(date):
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute("SELECT note FROM notes WHERE date=?", (date,))
    note = c.fetchone()
    conn.close()
    return note[0] if note else ""

# Функция для получения всех дат с заметками
def get_all_notes():
    conn = sqlite3.connect('calendar.db')
    c = conn.cursor()
    c.execute("SELECT date FROM notes")
    dates = c.fetchall()
    conn.close()
    return [date[0] for date in dates]

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('calendar_with_notes_sidebar.html')

# Маршрут для сохранения заметки
@app.route('/save_note', methods=['POST'])
def save_note_route():
    data = request.get_json()
    date = data['date']
    note = data['note']
    save_note(date, note)
    return jsonify({'status': 'success'})

# Маршрут для получения заметки для конкретной даты
@app.route('/get_note/<date>', methods=['GET'])
def get_note_route(date):
    note = get_note(date)
    return jsonify({'note': note})

# Маршрут для получения всех дат с заметками
@app.route('/get_all_notes', methods=['GET'])
def get_all_notes_route():
    notes = get_all_notes()
    return jsonify({'dates': notes})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)




""""from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import threading

app = Flask(__name__)

timer_data = {
    'duration': 0,
    'remaining': 0,
    'active': False
}

def timer_thread():
    while timer_data['remaining'] > 0:
        time.sleep(1)
        timer_data['remaining'] -= 1
    timer_data['active'] = False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        duration = int(request.form['duration'])
        timer_data['duration'] = duration
        timer_data['remaining'] = duration
        timer_data['active'] = True

        threading.Thread(target=timer_thread).start()

        return redirect(url_for('index'))

    return render_template('index.html', timer=timer_data)

@app.route('/clock')
def clock():
    return render_template('clock.html')


@app.route('/status')
def status():
    return jsonify(timer_data)

@app.route('/world-time')
def world_time():
    return render_template('world_time.html')

#@app.route('/calendar')
#def calendar():
#    return render_template('calendar.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar_with_notes.html')

if __name__ == '__main__':
    app.run(debug=True)"""""