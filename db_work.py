import sqlite3
import random
import os
import time

from chose_player import player_message


def connect() -> list:
    connection = sqlite3.connect('mygame.sqlite3')
    cursor = connection.cursor()
    return connection, cursor


def enemy_func() -> list:
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Enemies')
    enemy_all = cursor.fetchall()
    enemy_id = random.randint(1, len(enemy_all))
    cursor.execute(f'SELECT name, dmg, hp FROM Enemies WHERE id = {enemy_id}')
    enemy = cursor.fetchall()
    return enemy


def class_func(choice: int) -> list:
    connection, cursor = connect()
    cursor.execute('SELECT name, hp, dmg, mana, max_hp, max_mana FROM Classes'
                   f' WHERE id = {choice}')
    pl_class = cursor.fetchall()
    return pl_class[0]


def record_update(turn: int, pl_class: str) -> None:
    connection, cursor = connect()
    resp = ('INSERT INTO Records (record, class)'
            ' VALUES (?, ?)')
    cursor.execute(resp, (turn, pl_class))
    time.sleep(1)
    connection.commit()


def records_get() -> list:
    connection, cursor = connect()
    cursor.execute('SELECT record, class FROM Records'
                   ' ORDER BY record DESC')
    records = cursor.fetchall()
    return records


def get_data() -> list:
    connection, cursor = connect()
    cursor.execute('SELECT * FROM Classes')
    data = cursor.fetchall()
    return data


def player_func(multiplayer: int) -> list:
    os.system('clear')
    nahl = False
    names = []
    players = []
    for n in range(multiplayer):
        print(' Введите имя игрока:')
        a = True
        while a:
            try:
                names.append(input(' '))
                a = False
            except ValueError:
                a = True
        message, data = player_message(get_data())
        print(message)
        a = True
        while a:
            try:
                class_player = int(input(' '))
                a = False
            except ValueError:
                a = True
        if class_player == data:
            class_player = random.randint(1, 5)
            # отвечает за скрытие ника и класса
            nahl = True
        players.append(class_func(class_player))
    return names, players, nahl


connection, cursor = connect()
connection.close()
