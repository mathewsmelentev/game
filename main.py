import random
import os
import time

from db_work import (enemy_func,
                     record_update,
                     records_get,
                     player_func,
                     boss_func,
                     get_item_data)
from chose_player import choice_1
from player_message import message
from check import checkin

game = 1


def curses() -> int:
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


def random_choice(choice: int) -> int:
    choice = random.randint(1, 2)
    return (choice)


while game != 0:
    mana_use = False
    mana_plus = 0
    stack = 0
    turn = 0
    max_crips = 2
    multiplayer = 0
    death = [['1']]
    while multiplayer not in [1, 2, 3, 4]:
        print(' Выберите колличество игроков(от 1 до 4)')
        a = True
        while a:
            try:
                multiplayer = int(input(' '))
                a = False
            except ValueError:
                a = True
    names, players, nahl = player_func(multiplayer)
    hp_pl = 0
    playerses = [list(player) for player in players]
    players = [list(player) for player in players]
    # характеристики игрока
    # -17 название класса 0,
    # -16 хп 1,
    # -15 урон 2,
    # -14 мана 3,
    # -13 максимальное хп 4,
    # -12 максимальная мана 5,
    # -11 инвентарь 6,
    # -10 максимальное значение крипов 7,
    # -9 имя игрока 8,
    # -8 стак урон апа 9,
    # -7 время урон апа 10,
    # -6 стак рег мана апа 11,
    # -5 время рег мана апа 12,
    # -4 стак рег хп апа 13,
    # -3 время рег хп 14,
    # -2 использовал ману? 15,
    # -1 крипы 16
    n = 0
    m = 0
    for player in players:
        player.append([])
        player.append(2)
        player.append(names[n])
        n += 1
        for i in range(6):
            player.append(0)
        player.append(mana_use)
        player.append([])

    for i in players:
        hp_pl += i[1]

    while players:
        live_fade, unknown_enemies, unknown_yourself = curses()
        turn += 1
        if turn % 7 != 0:
            enemy = random.choice(enemy_func())
            enemy_name = enemy[0]
            enemy_dmg = round(enemy[1] * 1.1 ** float(len(players) - 1)
                              * 1.09 ** turn, 0)
            enemy_hp = round(enemy[2] * 1.5 ** float(len(players) - 1)
                             * 1.09 ** turn, 0)
            event = random.randint(1, 1000)
        else:
            enemy = random.choice(boss_func())
            enemy_name = enemy[0]
            enemy_dmg = round(enemy[1] * 1.3 ** float(len(players) - 1), 0)
            enemy_hp = round(enemy[2] * 1.7 ** float(len(players) - 1), 0)
            event = random.randint(1, 100)
        na = 0
        for player in players:
            hp_plus = 0
            mana_up = 0
            if live_fade is True:
                player[1] -= 2
            for inventory in player[-11]:
                hp_plus += inventory[2]
            if playerses[na][4] + hp_plus != player[4]:
                if playerses[na][4] + hp_plus > player[4]:
                    hp_plus = 0 - (player[4] - playerses[na][4] - hp_plus)
                    player[4] += hp_plus
            for inventory in player[-11]:
                mana_up += inventory[4]
            if playerses[na][5] + hp_plus != player[5]:
                if playerses[na][5] + hp_plus > player[5]:
                    mana_up = 0 - (player[5] - playerses[na][5] - mana_up)
                    player[5] += mana_up
            na += 1
        if event <= 200 and turn % 7 != 0:
            for player in players:
                if player[1] > 0:
                    os.system('clear')
                    print(' Вы попали в лагерь\n',
                          'Вы можете подлечится 1 или уйти 2')
                    choice_lager = int(input(' '))
                    if choice_lager == 1:
                        if player[1] + 10 >= player[4]:
                            player[1] = player[4]
                        else:
                            player[1] += random.randint(5, 10)
        elif 200 < event < 300 and turn % 7 != 0:
            mimic = random.randint(1, 100)
            m += 1
            for player in players:
                os.system('clear')
                if player[1] > 0:
                    print(' Вы нашли сундук, вы хотите его открыть?',
                          '(Да - 1, Нет - 2)')
                    choice_chest = int(input(' '))
                    if mimic <= 100:
                        if choice_chest == 1:
                            item_data = get_item_data(player[0], player[-11])
                            player[-11].append(item_data)
                    else:
                        if choice_chest == 1:
                            player[1] -= 3
            os.system('clear')
            if mimic > 50:
                print('Это был мимик!')
        else:
            while enemy_hp > 0 and players:
                damage = True
                for player in players:
                    if enemy_hp <= 0:
                        break
                    hp_pl = 0
                    for inventory in player[-11]:
                        player[1] += inventory[1]
                    if not players:
                        break
                    os.system('clear')
                    if player[-7] > 0:
                        player[-7] -= 1
                    else:
                        player[2] /= 1.25 ** player[-8]
                        player[-8] = 0
                    if player[-3] > 0:
                        player[-3] -= 1
                        if checkin(
                                player[1],
                                player[4],
                                2 * player[-4],
                                False
                                ):
                            player[1] += 2 * player[-4]
                        else:
                            player[1] = player[4]
                    else:
                        player[-4] = 0
                    if player[-5] > 0:
                        if checkin(
                                player[2],
                                player[5],
                                4 * player[-6],
                                False
                                ):
                            player[2] += 4 * player[-6]
                        else:
                            player[2] = player[5]
                    else:
                        player[-6] = 0
                    if player[-2]:
                        player[-2] = False
                    else:
                        try:
                            mana_plus += player[-11][3]
                        except IndexError:
                            pass
                        if player[0] == 'Призыватель':
                            mana_plus = 5
                        elif player[0] == 'Маг':
                            mana_plus = 1
                        elif player[0] == 'Хиллер':
                            mana_plus = 7
                        elif player[0] == 'Бард':
                            mana_plus = 6
                        elif player[0] == 'Шаман':
                            mana_plus = 3
                        if player[3] + mana_plus >= player[5]:
                            player[3] = player[5]
                        else:
                            player[3] += mana_plus
                    if player[1] > 0:
                        check = True
                        while check:
                            check = False
                            message_1, message_2 = message(player,
                                                           player[-9],
                                                           nahl,
                                                           unknown_yourself)
                            print(message_1)
                            print(f' Колличество ходов: {turn}\n')
                            if unknown_enemies is True:
                                print(' Вы встретили: ?\n',
                                      'Здоровья у противника: ?\n')
                            else:
                                print(f' Вы встретили: {enemy_name}\n',
                                      f'Уровень: {turn - 1}\n',
                                      f'Здоровья у противника: {enemy_hp}\n')
                            print(message_2)
                            if enemy_hp <= 0:
                                break
                            a = True
                            while a:
                                try:
                                    choice = int(input(' '))
                                    a = False
                                except ValueError:
                                    a = True
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
                                 player[-1],
                                 check,
                                 player[-2],
                                 players,
                                 enemy_dmg) = choice_1(choice,
                                                       enemy_hp,
                                                       player[1],
                                                       defence,
                                                       player[3],
                                                       stack,
                                                       player,
                                                       player[-1],
                                                       max_crips,
                                                       players,
                                                       enemy_dmg,
                                                       True)
                            else:
                                (choice,
                                 enemy_hp,
                                 player[1],
                                 defence,
                                 player[3],
                                 stack,
                                 player[-1],
                                 check,
                                 player[-2],
                                 players,
                                 enemy_dmg) = choice_1(choice,
                                                       enemy_hp,
                                                       player[1],
                                                       defence,
                                                       player[3],
                                                       stack,
                                                       player,
                                                       player[-1],
                                                       max_crips,
                                                       players,
                                                       enemy_dmg)
                        action_enemy = random.randint(1, 100)
                        cripses = player[-1].copy()
                        player[-1] = [list(crip) for crip in cripses]
                        have_war = False
                        for played in players:
                            for dead in death:
                                if (played[0] == 'Воин'
                                        and player[0] != dead[0]):
                                    have_war = True
                        pl = players.index(player)
                        for inventory in player[-11]:
                            defence += inventory[7]
                        if action_enemy >= 30:
                            if enemy_hp > 0:
                                if have_war:
                                    defence -= enemy_dmg
                                    if player[0] == 'Воин':
                                        if defence >= 0:
                                            player[1] = player[1]
                                        else:
                                            player[1] += defence
                                            if player[1] <= 0:
                                                death.append(
                                                    players.pop(
                                                        pl
                                                        )
                                                    )
                                else:
                                    if damage:
                                        defence -= enemy_dmg
                                        if (player[0] == 'Призыватель'
                                                and player[-1]):
                                            player[-1][0][-2] -= enemy_dmg
                                        else:
                                            if defence >= 0:
                                                player[1] = player[1]
                                            else:
                                                player[1] += defence
                                                if player[1] < 0:
                                                    death.append(
                                                        players.pop(
                                                            pl
                                                            )
                                                        )
                                        a = random.randint(1, 10)
                                        if a < 9:
                                            damage = False
                        n = 0
                        for crip in player[-1]:
                            if crip[2] <= 0:
                                player[-1].pop(n)
                            n += 1
                    else:
                        death.append(players.pop(players.index(player)))
    else:
        print(f' Вы проиграли. Тебя убили на {int(turn)} ходу')
        time.sleep(2)
    player = ''
    for i in playerses:
        player += f'{i[0]} '
    record_update(turn, player)

    records = records_get()

    os.system('clear')

    print(' Последние рекорды:')
    for i in range(0, 5):
        print(f' {records[i][0]} - {records[i][1]}')

    time.sleep(2)

    os.system('clear')

    print(' Вы хотите сыграть ещё раз?(Да - 1, Нет - 2)')
    game = int(input(' '))
    if game == 2:
        game = 0
    os.system('clear')
