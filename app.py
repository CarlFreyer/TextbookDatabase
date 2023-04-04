import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('maintextbooks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM textbooks where textbook_title = "hello"')
    textbooks = [{'textbook_id': row[0], 'textbook_title': row[1], 'textbook_description': row[2]} for row in c.fetchall()]
    conn.close()
    return render_template('home.html', textbooks=textbooks)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        textbook_id = request.form['textbook_id']
        conn = sqlite3.connect('maintextbooks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM textbooks WHERE textbook_title = ?', (textbook_id,))
        row = c.fetchone()
        conn.close()
        if row is not None:
            textbook_title = row[1]
            textbook_description = row[2]
            return render_template('textbook.html', textbook_id=textbook_id, textbook_title=textbook_title, textbook_description=textbook_description)
        else:
            return render_template('notFound.html', textbook_id=textbook_id)

@app.route('/searchClass', methods=['GET', 'POST'])
def searchClass():
    if request.method == "POST":
        textbook_id = request.form['textbook_id']
        print(textbook_id)
        conn = sqlite3.connect('maintextbooks.db')
        c = conn.cursor()
        c.execute('SELECT * FROM textbooks WHERE textbook_title = ?', (textbook_id,))
        row = c.fetchone()
        conn.close()
        if row is not None:
            textbook_title = row[1]
            textbook_description = row[2]
            return render_template('textbook.html', textbook_id=textbook_id, textbook_title=textbook_title, textbook_description=textbook_description)
        else:
            return render_template('notFound.html', textbook_id=textbook_id)

@app.route('/textbook', methods=['GET', 'POST'])
def click():
    textbook_id = request.args.get('bookName', default = 'n/a', type = str)
    print(textbook_id + "\n\n\n\n\n\n\n\n\n")
    if textbook_id == 'n/a':
        return render_template('notFound.html', textbook_id=textbook_id)
    conn = sqlite3.connect('maintextbooks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM textbooks WHERE textbook_title = ?', (textbook_id,))
    row = c.fetchone()
    conn.close()
    if row is not None:
        textbook_title = row[1]
        textbook_description = row[2]
        return render_template('textbook.html', textbook_id=textbook_id, textbook_title=textbook_title, textbook_description=textbook_description)
    else:
        return render_template('notFound.html', textbook_id=textbook_id)

