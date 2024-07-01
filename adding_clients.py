import tkinter as tk
from tkinter import ttk
import psycopg2
import random


def card_number(): # Функция для создания случайного номера карты
    card_number = random.randint(0, 9999999)
    return card_number


# Счётчик для фраз
count = 0

# Коннекд к БД
connection = psycopg2.connect(
    dbname='client',
    user='postgres',
    password='123456789',
    host='127.0.0.1',
    options="-c client_encoding='windows-1251")


# Функция для добавления ответов в бд
def add_to_database(array):
    array.append(card_number())
    with connection.cursor() as cursor:
        cursor.execute('''
        INSERT INTO client (first_name, second_name, third_name, age, gender, cash_balance, card_number)
        VALUES (%s, %s, %s, %s, %s, 0, %s)
        ''', array)
    connection.commit()


# Функция для создания нового окна
def session():
    global count

    # Список ответов пользователя
    data_list = list()

    # Функция для очистки поля для ввода
    def delete_entry():
        entry.delete(0, tk.END)

    # Функция сбора и добавления информации в бд
    def add():
        global count

        output_entry = entry.get()

        if count <= 4: # Если не все вопросы были заданы
            data_list.append(output_entry)
            count += 1
            label.config(text=list_of_questions[count])
            delete_entry()
        else: # Если все вопросы были заданы

            add_to_database(data_list) # Список ответов вносим в функцию, которая добавит их в бд
            data_list.clear()
            count = 0
            window.destroy()

    # Создаём новое окно
    window = tk.Toplevel(root)
    window.geometry('200x100')
    window.title('add')

    # Создаём и добавляем виджеты
    label = ttk.Label(window, text=list_of_questions[count])
    entry = ttk.Entry(window)
    button = ttk.Button(window, text='Добавить', command=add)

    label.grid()
    entry.grid()
    button.grid()


list_of_questions = ['Введите имя клиента', 'Введите фамилию клиента', 'Введите отчество клиента',
                     'Введите возраст клиента', 'Введите пол клиента', 'Стоп'] # Список вопросов

# Основное окно
root = tk.Tk()
root.geometry('600x300')
root.title('adding_clients')

initial_button = ttk.Button(root, text='Начать ссесию', command=session)
initial_button.grid()

root.mainloop()



