import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    conn = sqlite3.connect('maintextbooks.db')
    c = conn.cursor()
    c.execute('SELECT title, cost FROM textbooks order by cost desc')
    cost = [{'title': row[0], 'cost': '{0:.2f}'.format(row[1])} for row in c.fetchmany(8)]
    c.execute("select title, count(*) as genderCount from (select title, gender from textbooks natural join authors where gender='female') group by title order by count() desc")
    gender = [{'title': row[0], 'femaleNum': row[1]} for row in c.fetchmany(8)]
    c.execute("select title, course from textbooks left outer join (select * from authors where gender = 'female') b on textbooks.isbn=b.isbn where authorFirst is null;")
    onlyMale = [{'title': row[0], 'course': row[1]} for row in c.fetchmany(8)]
    c.execute("select university, count(*) as uniCount from (select title, university from textbooks natural join authors) group by university order by count() desc")
    university = [{'university': row[0], 'uniCount': row[1]} for row in c.fetchmany(8)]
    conn.close()
    return render_template('home.html', cost=cost, gender = gender, university = university, onlyMale = onlyMale)

@app.route('/list', methods=['GET'])
def list():
    conn = sqlite3.connect('maintextbooks.db')
    c = conn.cursor()
    c.execute('SELECT title, course, isbn FROM textbooks')
    textbooks = [{'title': row[0], 'course': row[1], 'isbn': row[2]} for row in c.fetchall()]
    conn.close()
    if len(textbooks) is not 0:
        return render_template('search.html', textbooks=textbooks)
    else:
        return render_template('notFound.html', textbook_id=textbook_id)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        textbook_id = request.form['textbook_id']
        conn = sqlite3.connect('maintextbooks.db')
        c = conn.cursor()
        if textbook_id == "all":
            c.execute('SELECT title, course, isbn FROM textbooks')
        else:
            c.execute('SELECT title, course, isbn FROM search WHERE search match ?', (textbook_id,))
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
        c.execute('SELECT title, course, isbn FROM textbooks WHERE course = ?', (textbook_id,))
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
    c.execute('SELECT isbn, title, publisher, pubYear, dei, course, cost FROM textbooks WHERE title = ?', (textbook_id,))
    row = c.fetchone()
    c.execute('SELECT authorFirst, authorLast, university, education, gender, ethnicity, link FROM authors WHERE isbn = ?', (row[0],))
    authors = [{'first': row[0], 'last': row[1], 'university': row[2], 'education': row[3], 'gender': row[4], 'ethnicity': row[5], 'link': row[6]} for row in c.fetchall()]
    conn.close()
    if row is not None:
        isbn = row[0]
        title = row[1]
        publisher = row[2]
        year = row[3]
        dei = row[4]
        course = row[5]
        cost = '{0:.2f}'.format(row[6])
        return render_template('textbook.html', isbn=isbn, title=title, pub=publisher, year=year, dei = dei, course = course, cost = cost, authors = authors)
    else:
        return render_template('notFound.html', textbook_id=textbook_id)

