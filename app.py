import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('maintextbooks.db')
    c = conn.cursor()
    c.execute('SELECT title, cost FROM textbooks order by cost desc')
    cost = [{'title': row[0], 'cost': row[1]} for row in c.fetchmany(10)]
    c.execute("select title, count(*) as genderCount from (select title, gender from textbooks natural join authors where gender='female') group by title order by count() desc")
    gender = [{'title': row[0], 'femaleNum': row[1]} for row in c.fetchmany(10)]
    c.execute("select title, course from textbooks left outer join (select * from authors where gender = 'female') b on textbooks.isbn=b.isbn where authorFirst is null;")
    onlyMale = [{'title': row[0], 'course': row[1]} for row in c.fetchmany(10)]
    c.execute("select university, count(*) as uniCount from (select title, university from textbooks natural join authors) group by university order by count() desc")
    university = [{'university': row[0], 'uniCount': row[1]} for row in c.fetchmany(10)]
    conn.close()
    return render_template('home.html', cost=cost, gender = gender, university = university, onlyMale = onlyMale)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        textbook_id = request.form['textbook_id']
        conn = sqlite3.connect('maintextbooks.db')
        c = conn.cursor()
        c.execute('SELECT title, course, isbn FROM textbooks WHERE title = ?', (textbook_id,))
        textbooks = [{'title': row[0], 'course': row[1], 'isbn': row[2]} for row in c.fetchall()]
        conn.close()
        if len(textbooks) is not 0:
            return render_template('search.html', textbooks=textbooks)
        else:
            return render_template('notFound.html', textbook_id=textbook_id)

@app.route('/course', methods=['GET', 'POST'])
def course():
    if request.method == "POST":
        textbook_id = request.form['class_id']
        conn = sqlite3.connect('maintextbooks.db')
        c = conn.cursor()
        c.execute('SELECT title, course, isbn FROM textbooks WHERE title = ?', (textbook_id,))
        textbooks = [{'title': row[0], 'course': row[1], 'isbn': row[2]} for row in c.fetchall()]
        conn.close()
        if len(textbooks) is not 0:
            return render_template('search.html', textbooks=textbooks)
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
    c.execute('SELECT * FROM textbooks WHERE title = ?', (textbook_id,))
    row = c.fetchone()
    conn.close()
    if row is not None:
        textbook_title = row[1]
        textbook_description = row[2]
        return render_template('textbook.html', textbook_id=textbook_id, textbook_title=textbook_title, textbook_description=textbook_description)
    else:
        return render_template('notFound.html', textbook_id=textbook_id)

