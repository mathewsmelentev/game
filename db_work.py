import sqlite3
import random

from chose_player import player_message

connection = sqlite3.connect('mygame.sqlite3')
cursor = connection.cursor()


def enemy_func():
    connection = sqlite3.connect('mygame.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Enemies')
    enemy_all = cursor.fetchall()
    enemy_id = random.randint(1, len(enemy_all))
    cursor.execute(f'SELECT name, dmg, hp FROM Enemies WHERE id = {enemy_id}')
    enemy = cursor.fetchall()
    return enemy


def class_func(choice):
    connection = sqlite3.connect('mygame.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT name, hp, dmg, mana, max_hp FROM Classes'
                   f' WHERE id = {choice}')
    pl_class = cursor.fetchall()
    return pl_class[0]


def record_update(turn, pl_class):
    connection = sqlite3.connect('mygame.sqlite3')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Records (record, class)'
                   ' VALUES (?, ?)', (turn, pl_class))
    connection.commit()


def records_get():
    connection = sqlite3.connect('mygame.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT record, class FROM Records ORDER BY record DESC')
    records = cursor.fetchall()
    return records


def get_data():
    connection = sqlite3.connect('mygame.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Classes')
    data = cursor.fetchall()
    return data


def player_func(multiplayer):
    nahl = False
    names = []
    players = []
    for n in range(multiplayer):
        print(' Введите имя игрока:')
        names.append(input(' '))
        print(player_message(get_data()))
        class_player = int(input(' '))
        if class_player == 6:
            class_player = random.randint(1, 5)
            # отвечает за скрытие ника и класса
            nahl = True
        players.append(class_func(class_player))
    return names, players, nahl


connection.close()
