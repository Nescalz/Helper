from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import filedialog

# Подключаемся к базе данных
connection = sqlite3.connect('database_server.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tema (
id INTEGER PRIMARY KEY,
name TEXT,
tema TEXT,
predmet TEXT
)
''')

#Создаем таблицу для к/р
cursor.execute('''
CREATE TABLE IF NOT EXISTS kr (
id INTEGER PRIMARY KEY,
name TEXT,
kr TEXT
)
''')
#
cursor.execute('''
CREATE TABLE IF NOT EXISTS lr (
id INTEGER PRIMARY KEY,
name TEXT,
lr TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
tema TEXT,
comm TEXT,
ocenc REAL
)
''')

# Создаем таблицу для заданий учителя
cursor.execute('''
CREATE TABLE IF NOT EXISTS teacher_tm (
id INTEGER PRIMARY KEY,
tema TEXT,
assignment TEXT
)
''')

#Функия настройки фрейма для тем
def new_window2(text1, text_windows, obzec, gui):
    guis2 = Tk()
    guis2.title(text1)
    guis2.geometry("1000x750")
    
    kn = Button(guis2, text="Закрыть.", command=guis2.destroy)
    kn.place(x=500, y=600, width=100, height=30)
    
    label1 = Label(guis2, text="Название темы:")
    label1.pack()
    
    entry_names = Entry(guis2, width=50)
    entry_names.pack()
    
    label2 = Label(guis2, text=text_windows)
    label2.pack()
    
    texta = Text(guis2, width=50, height=10)
    texta.pack()
    
    button = Button(guis2, text="Добавить тему", command=lambda: dob_tema(entry_names.get(), texta.get("1.0", END), obzec))
    button.pack()

#Функция сообщения о теме
def dob_tema(names, tema, obzec):
    cursor.execute('INSERT INTO tema (name, tema, predmet) VALUES (?, ?, ?)', (names, tema, obzec))
    connection.commit()
    messagebox.showinfo("Успех", "Тема успешно добавлена.")

#Функция коментирования
def com():
    def rate_comment(rating, comment_id):
        cursor.execute('INSERT INTO comments (tema, comm, ocenc) VALUES (?, ?, ?)', (comment[0], comment[1], rating))
        connection.commit()
        messagebox.showinfo("Оценка комментария", f"Комментарий ID {comment_id} оценен на {rating}.")


    comss = Tk()
    comss.title("Комментарии учеников")
    comss.geometry("600x400")

    kole = Scrollbar(comss)
    kole.pack(side=RIGHT, fill=Y)

    comments_text = Text(comss, yscrollcommand=kole.set)
    comments_text.pack(fill=BOTH, expand=YES)

    kole.config(command=comments_text.yview)

    cursor.execute('SELECT * FROM comments')
    comments = cursor.fetchall()
    for idx, comment in enumerate(comments):
        comments_text.insert(END, f"Тема: {comment[0]}\nКомментарий: {comment[1]}\n")
        rating_frame = Frame(comss)
        rating_frame.pack()
        for rating_value in range(5, 1, -1):  # Создаем кнопки рейтинга от 5 до 2
            rate_button = Button(rating_frame, text=str(rating_value), command=lambda rating=rating_value, id=idx+1: rate_comment(rating, id))
            rate_button.pack(side=LEFT)
        comments_text.insert(END, "\n")
    comments_text.config(state=DISABLED)
#Функция удаления задания
def deliteeeeee(assignment_id, frame):
    cursor.execute('DELETE FROM teacher_tm WHERE id=?', (assignment_id,))
    connection.commit()
    messagebox.showinfo("Успех", "Задание успешно удалено.")
    frame.destroy() 
#Функия заданий
def zadan():
    okno = Tk()
    okno.title("Задания учителя")
    okno.geometry("600x400")

    kole = Scrollbar(okno)
    kole.pack(side=RIGHT, fill=Y)

    txt = Text(okno, yscrollcommand=kole.set)
    txt.pack(fill=BOTH, expand=YES)

    kole.config(command=txt.yview)

    cursor.execute('SELECT * FROM teacher_tm')
    tm = cursor.fetchall()
    for assignment in tm:
        frame = Frame(okno)
        frame.pack()
        
        label = Label(frame, text=f"ID: {assignment[0]}\nТема: {assignment[1]}\nЗадание: {assignment[2]}\n")
        label.pack(side=LEFT)
        
        del_kn = Button(frame, text="Удалить задание", command=lambda id=assignment[0], f=frame: deliteeeeee(id, f))
        del_kn.pack(side=RIGHT)
        
        txt.window_create(END, window=frame)
        txt.insert(END, "\n")
        
    txt.config(state=DISABLED)

#функия добавления тем
def temas(obz):
    new_window2("Добавить тему", "", obz, gui)

#Функция опредеения вызова нужной функции
def gl(text):
    if text == "Комментарии/работы ученика":
        com()
    elif text == "Задания ученика":
        zadan()
    else:
        temas(text)

#Настройка кнопок
gui = Tk()
gui.title("Помощник учителя")
gui.geometry("800x550")

pred = ["Математика", "Информатика", "Физика", "Русский язык", "Химия", "Геометрия", "Философия"]

row = 0
for щи in pred:
    kn222 = Button(gui, text=щи, command=lambda s=щи: gl(s))
    kn222.grid(row=row, column=0, padx=10, pady=10)
    row += 1

kn1 = Button(gui, text="Комментарии ученика", command=lambda: gl("Комментарии/работы ученика"))
kn1.grid(row=row, column=0, padx=10, pady=10)

gui.mainloop()
