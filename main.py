from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# создание базы данных и таблицы
def create_table():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS students (
                student_name TEXT,
                attendance INTEGER,
                lesson_theme TEXT
                )""")
    conn.commit()
    conn.close()

# добавление нового ученика
@app.route('/add_student', methods=['POST'])
def add_student():
    student_name = request.form['student_name']
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students VALUES (?, ?, ?)", (student_name, 0, ''))
    conn.commit()
    conn.close()
    return 'Success'

# удаление ученика
@app.route('/delete_student', methods=['POST'])
def delete_student():
    student_name = request.form['student_name']
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE student_name=?", (student_name,))
    conn.commit()
    conn.close()
    return 'Success'

# отметка присутствия ученика
@app.route('/mark_presence', methods=['POST'])
def mark_presence():
    student_name = request.form['student_name']
    attendance = request.form['attendance']
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("UPDATE students SET attendance=? WHERE student_name=?", (attendance, student_name))
    conn.commit()
    conn.close()
    return 'Success'

# добавление темы занятия
@app.route('/add_lesson_theme', methods=['POST'])
def add_lesson_theme():
    student_name = request.form['student_name']
    lesson_theme = request.form['lesson_theme']
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("UPDATE students SET lesson_theme=? WHERE student_name=?", (lesson_theme, student_name))
    conn.commit()
    conn.close()
    return 'Success'

# вывод списка всех учеников
@app.route('/')
def list_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('list.html', students=students)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
