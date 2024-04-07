# Подключаем библиотеки
from tkinter import *
from tkinter import messagebox
import sqlite3

# Подключаемся к базе данных
connection = sqlite3.connect('database_server.db')
cursor = connection.cursor()

#Сделаем таблицу для входа в систему
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
username TEXT NOT NULL,
password TEXT NOT NULL,
role TEXT NOT NULL 
)
''')
#Функция регистрации
def registr(user, password, role):
    cursor.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)', (user, password, role))
    connection.commit()

#Функция определения пользователя
def check_cr():
    usernamevx = entry_username.get()
    passwordvx = entry_password.get()

    #Ищем пользователя в базе данных
    cursor.execute('SELECT * FROM Users WHERE username = ? AND password = ?', (usernamevx, passwordvx))
    user = cursor.fetchone()

    #Проверяем существует ли пользователь с такими данными
    if user is not None:
        messagebox.showinfo("Успех", "Вход выполнен успешно!")
        if user[2] == "teacher":
            # Запуск программы для учителя
            import ticher_programm
            gui.destroy()
        elif user[2] == "student":
            # Запуск программы для студента
            import student_programm
            gui.destroy()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

#Окно регистрации и кнопки
gui = Tk()
gui.title("Вход в систему")

text_username = Label(gui, text="Логин:")
text_username.grid(row=0, column=0, padx=5, pady=5, sticky=E)

entry_username = Entry(gui)
entry_username.grid(row=0, column=1, padx=5, pady=5)

text_password = Label(gui, text="Пароль:")
text_password.grid(row=1, column=0, padx=5, pady=5, sticky=E)

entry_password = Entry(gui, show="*")
entry_password.grid(row=1, column=1, padx=5, pady=5)

kn_login = Button(gui, text="Войти", command=check_cr)
kn_login.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

kn1_reg = Button(gui, text="Зарегистрироваться как ученик", command=lambda: registr(entry_username.get(), entry_password.get(), "student"))
kn1_reg.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

kn1_reg2 = Button(gui, text="Зарегистрироваться как учитель", command=lambda: registr(entry_username.get(), entry_password.get(), "teacher"))
kn1_reg2.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

gui.mainloop()
