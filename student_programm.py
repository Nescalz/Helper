# Подключаем библиотеки
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import filedialog

# Подключаемся к базе данных
connection = sqlite3.connect('database_server.db')
cursor = connection.cursor()

# Создаем таблицу для тем
cursor.execute('''
CREATE TABLE IF NOT EXISTS tema (
id INTEGER PRIMARY KEY,
name TEXT,
tema TEXT,
predmet TEXT
)
''')

# Создаем таблицу для к/р
cursor.execute('''
CREATE TABLE IF NOT EXISTS kr (
id INTEGER PRIMARY KEY,
name TEXT,
kr TEXT
)
''')

# Создаем таблицу для комментирования
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
tema TEXT,
comm TEXT,
ocenc INTEGER
)
''')
#Функция добавления фаила
def upload_file(tema, file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        cursor.execute('INSERT INTO comments (tema, comm) VALUES (?, ?)', (tema, file_content))
        connection.commit()
    messagebox.showinfo("Успех", "Файл успешно загружен.")
#Функция выбора файла
def select_file(tema):
    file_path = filedialog.askopenfilename()
    if file_path:
        upload_file(tema, file_path)

# Функция для вычисления среднего балла и обновления метки
def update_average_rating():
    cursor.execute('SELECT ocenc FROM comments WHERE ocenc IS NOT NULL')
    ratings = cursor.fetchall()
    if not ratings:
        average_rating.set("0.00")
    else:
        total_ratings = sum([rating[0] for rating in ratings])
        average = total_ratings / len(ratings)
        average_rating.set(f"{average:.2f}")

# Создаем метку для отображения среднего балла
gui = Tk()
gui.title("Помощник студента")
gui.geometry("800x550")

average_rating_label = Label(gui, text="Средний балл: ", foreground="black")
average_rating_label.place(x=20, y=20)

# Создаем переменную для хранения текущего среднего балла
average_rating = StringVar()
average_rating.set("0.00")  # Инициализируем значение среднего балла

# Создаем кнопку для обновления среднего балла
kn_average = Button(gui, textvariable=average_rating, command=update_average_rating, foreground="black")
kn_average.place(x=130, y=20, width=120, height=30)

# Вызываем функцию обновления среднего балла для инициализации значения
update_average_rating()

# Функция комментариев
def new_window2(text1, tema, gui):
    guis2 = Tk()
    guis2.title(text1)
    guis2.geometry("1000x750")
    kn = Button(guis2, text="Закрыть.", command=guis2.destroy, foreground="black")
    kn.place(x=500, y=600, width=100, height=30)
    label = Label(guis2, text=tema)
    label.pack()
    texta = Text(guis2, width=50, height=10)
    texta.pack()
    button = Button(guis2, text="Отправить комментарий/задание", command=lambda: comi(tema, texta.get("1.0", END)), foreground="black")
    button.pack()
    select_file_button = Button(guis2, text="Выбрать файл", command=lambda: select_file(tema), foreground="black")
    select_file_button.pack()

# Функция открытия тем и создания кнопок
def temaaaa(predmet):
    # Достаем темы из базы данных
    cursor.execute('SELECT name, tema FROM tema WHERE predmet=?', (predmet,))
    temas = cursor.fetchall()

    # Очищяем главное окно от предыдущих кнопок
    for widget in gui.winfo_children():
        widget.destroy()

    # Создаем новые кнопки с темами
    for index, tema_info in enumerate(temas):
        tema_name = tema_info[0]
        tema_description = tema_info[1]
        button = Button(gui, text=tema_name, command=lambda t=tema_description: new_window2("Выбранная тема", t, gui), foreground="black", wraplength=100)
        button.place(x=400, y=150 + 50 * index, width=200, height=30)

# Функция отправки комментариев в базу данных
def comi(tema, comment):
    # Сохраняем комментарий в базе данных ученика
    cursor.execute('INSERT INTO comments (tema, comm) VALUES (?, ?)', (tema, comment))
    connection.commit()
    messagebox.showinfo("Успех", "Комментарий успешно сохранен.")

center_x = 400
center_y = 150

# Создаем кнопки для выбора предмета
kn1 = Button(gui, text="Математика", command=lambda: temaaaa("Математика"), foreground="black")
kn1.place(x=center_x - 100, y=center_y - 100, width=200, height=30)

kn2 = Button(gui, text="Информатика", command=lambda: temaaaa("Информатика"), foreground="black")
kn2.place(x=center_x - 100, y=center_y - 50, width=200, height=30)

kn3 = Button(gui, text="Философия", command=lambda: temaaaa("Философия"), foreground="black")
kn3.place(x=center_x - 100, y=center_y, width=200, height=30)

kn4 = Button(gui, text="Геометрия", command=lambda: temaaaa("Геометрия"), foreground="black")
kn4.place(x=center_x - 100, y=center_y + 50, width=200, height=30)

kn5 = Button(gui, text="Русский язык", command=lambda: temaaaa("Русский язык"), foreground="black")
kn5.place(x=center_x - 100, y=center_y + 100, width=200, height=30)

kn6 = Button(gui, text="Физика", command=lambda: temaaaa("Физика"), foreground="black")
kn6.place(x=center_x - 100, y=center_y + 150, width=200, height=30)

kn7 = Button(gui, text="Химия", command=lambda: temaaaa("Химия"), foreground="black")
kn7.place(x=center_x - 100, y=center_y + 200, width=200, height=30)

gui.mainloop()
