import random
import os
import time

from db_work import (enemy_func,
                     record_update,
                     records_get,
                     player_func)
from chose_player import choice_1

game = 1


def curses():
    live_fade = False
    unknown_enemies = False
    unknown_yourself = False
    curs = random.randint(1, 100)
    if curs <= 5:
        live_fade = True
    elif 5 < curs <= 12:
        unknown_enemies = True
    elif 12 < curs <= 15:
        unknown_yourself = True
    if curs <= 15:
        print(' Вы прокляты!')
        time.sleep(2)
    return (live_fade, unknown_enemies, unknown_yourself)


def random_choice(choice):
    choice = random.randint(1, 2)
    return (choice)


while game != 0:
    crips = []
    stack = 0
    turn = 0
    multiplayer = 0
    while multiplayer not in [1, 2, 3, 4]:
        print(' Выберите колличество игроков(максимум 4)')
        multiplayer = int(input(' '))
    names, players, nahl = player_func(multiplayer)
    hp_pl = 0

    for i in players:
        hp_pl += i[1]

    while hp_pl > 0:
        live_fade, unknown_enemies, unknown_yourself = curses()
        enemy = random.choice(enemy_func())
        enemy_name = enemy[0]
        enemy_dmg = round(enemy[1] * 1.5 ** float(len(players) - 1), 0)
        enemy_hp = round(enemy[2] * 1.5 ** float(len(players) - 1), 0)
        event = random.randint(1, 1000)
        for player in players:
            if live_fade is True:
                player[1] -= 2
        playerses = players.copy()
        players = [list(player) for player in playerses]
        if event <= 200:
            for player in players:
                if player[1] > 0:
                    os.system('clear')
                    print(' Вы попали в лагерь\n',
                          'Вы можете подлечится 1 или уйти 2')
                    choice_lager = int(input(' '))
                    turn += 1
                    if choice_lager == 1:
                        if player[1] != player[4]:
                            player[1] = player[4]
                        else:
                            player[1] += random.randint(5, 10)
        else:
            while enemy_hp > 0 and hp_pl > 0:
                name = 0
                for player in players:
                    name += 1
                    if enemy_hp <= 0:
                        break
                    hp_pl = 0
                    for i in players:
                        hp_pl += i[1]
                    if hp_pl <= 0:
                        break
                    os.system('clear')
                    turn += 1 / len(players)
                    player[3] += 1
                    if player[1] > 0:
                        if nahl is True or unknown_yourself is True:
                            message = (f' Ваше имя: {names[name-1]}\n'
                                       ' Твой класс:?\n'
                                       ' Здоровье:?\n'
                                       ' Мана:?\n'
                                       ' Стак:?\n')
                            message_1 = (' Выберите действие\n'
                                         ' 1 - удар?\n'
                                         ' 2 - защищаться?\n'
                                         ' 3 - посмотреть инвентарь?\n'
                                         ' 4 - рандом?\n'
                                         ' 5 - ?')
                        elif player[0] == 'Маг':
                            message = (f' Ваше имя: {names[name-1]}\n'
                                       f' Твой класс:{player[0]}\n'
                                       f' Здоровье:{player[1]}\n'
                                       f' Мана:{player[3]}\n')
                            message_1 = (' Выберите действие\n'
                                         ' 1 - удар(если нет маны,'
                                         ' делится на 2)\n'
                                         ' 2 - защищаться\n'
                                         ' 3 - посмотреть инвентарь\n'
                                         ' 4 - рандом')
                        elif player[0] == 'Рога':
                            message = (f' Ваше имя: {names[name-1]}\n'
                                       f' Твой класс:{player[0]}\n'
                                       f' Здоровье:{player[1]}\n'
                                       f' Стак:?\n')
                            message_1 = (' Выберите действие\n'
                                         ' 1 - удар\n'
                                         ' 2 - защищаться\n'
                                         ' 3 - посмотреть инвентарь\n'
                                         ' 4 - рандом\n'
                                         ' 5 - возможность встать в стойку')
                        elif player[0] == 'Призыватель':
                            message = (f' Ваше имя: {names[name-1]}\n'
                                       f' Твой класс:{player[0]}\n'
                                       f' Здоровье:{player[1]}\n')
                            message_1 = (' Выберите действие\n'
                                         ' 1 - призвать крипа\n'
                                         ' 2 - защищаться\n'
                                         ' 3 - посмотреть инвентарь\n'
                                         ' 4 - рандом\n'
                                         ' 5 - посмотреть крипов')
                        else:
                            message = (f' Ваше имя: {names[name-1]}\n'
                                       f' Твой класс:{player[0]}\n'
                                       f' Здоровье:{player[1]}\n')
                            message_1 = (' Выберите действие\n'
                                         ' 1 - удар\n'
                                         ' 2 - защищаться\n'
                                         ' 3 - посмотреть инвентарь\n'
                                         ' 4 - рандом')

                        print(message)
                        if unknown_enemies is True:
                            print(' Вы встретили: ?\n',
                                  'Здоровья у противника: ?\n')
                        else:
                            print(f' Вы встретили: {enemy_name}\n',
                                  f'Здоровья у противника: {enemy_hp}\n')
                        print(message_1)
                        choice = int(input(' '))
                        help_choice = False
                        defence = 0
                        if choice == 4:
                            choice = random_choice(choice)
                            (choice,
                             enemy_hp,
                             player[1],
                             defence,
                             player[3],
                             stack,
                             crips) = choice_1(choice,
                                               enemy_hp,
                                               player[1],
                                               defence,
                                               player[3],
                                               stack,
                                               player,
                                               crips,
                                               True)
                        else:
                            (choice,
                             enemy_hp,
                             player[1],
                             defence,
                             player[3],
                             stack,
                             crips) = choice_1(choice,
                                               enemy_hp,
                                               player[1],
                                               defence,
                                               player[3],
                                               stack,
                                               player,
                                               crips)
                        action_enemy = random.randint(1, 100)
                        if action_enemy >= 30:
                            if enemy_hp > 0:
                                defence -= enemy_dmg
                                if defence >= 0:
                                    player[1] = player[1]
                                else:
                                    player[1] += defence
                        else:
                            pass
    else:
        print(f' Вы проиграли. Тебя убили на {int(turn)} ходу')
        time.sleep(2)
    player = ''
    for i in players:
        player += f'{i[0]} '
        record_update(int(turn), player)

    records = records_get()

    os.system('clear')

    print(' Последние рекорды:')
    for i in range(0, 5):
        print(f' {records[i][0]} - {records[i][1]}')

    time.sleep(1)

    os.system('clear')

    print(' Вы хотите сыграть ещё раз?(Да, Нет)')
    game = input(' ')
    if game == 'Да':
        game = 1
    else:
        game = 0
    os.system('clear')
