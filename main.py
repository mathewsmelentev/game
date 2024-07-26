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
    playerses = players.copy()
    n = 0
    m = 0
    for player in players:
        player['инвентарь'] = []
        player['макс крипов'] = 2
        player['имя'] = names[n]
        n += 1
        player['исп маны'] = mana_use
        player['крипы'] = []
        player['стак рег мана апа'] = 0
        player['стак рег хп апа'] = 0
        player['стак урон апа'] = 0
        player['время рег мана апа'] = 0
        player['время рег хп апа'] = 0
        player['время урон апа'] = 0
        player['стак'] = 0

    for i in players:
        hp_pl += i['хп']

    while players:
        live_fade, unknown_enemies, unknown_yourself = curses()
        turn += 1
        if turn % 7 != 0:
            enemy = random.choice(enemy_func())
            enemy_name = enemy[0]
            enemy_dmg = round(enemy[1] * 1.1 ** float(len(players) - 1), 0)
            enemy_hp = round(enemy[2] * 1.5 ** float(len(players) - 1), 0)
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
                player['хп'] -= 2
            for inventory in player['инвентарь']:
                hp_plus += inventory[2]
            if playerses[na]['макс хп'] + hp_plus != player['макс хп']:
                if playerses[na]['макс хп'] + hp_plus > player['макс хп']:
                    hp_plus = 0 - (
                        player['макс хп']
                        - playerses[na]['макс хп']
                        - hp_plus)
                    player['макс хп'] += hp_plus
            for inventory in player['инвентарь']:
                mana_up += inventory[4]
            if playerses[na]['макс мана'] + mana_up != player['макс мана']:
                if playerses[na]['макс мана'] + hp_plus > player['макс мана']:
                    mana_up = 0 - (
                        player['макс мана']
                        - playerses[na]['макс мана']
                        - mana_up)
                    player['макс мана'] += mana_up
            na += 1
        if event <= 200 and turn % 7 != 0:
            for player in players:
                if player['хп'] > 0:
                    os.system('clear')
                    print(' Вы попали в лагерь\n',
                          'Вы можете подлечится 1 или уйти 2')
                    choice_lager = int(input(' '))
                    if choice_lager == 1:
                        if player['хп'] + 10 >= player['макс хп']:
                            player['хп'] = player['макс хп']
                        else:
                            player['хп'] += random.randint(5, 10)
        elif 200 > event <= 300 and turn % 7 != 0:
            mimic = random.randint(1, 100)
            m += 1
            for player in players:
                os.system('clear')
                if player['хп'] > 0:
                    print(' Вы нашли сундук, вы хотите его открыть?',
                          '(Да - 1, Нет - 2)')
                    choice_chest = int(input(' '))
                    if mimic <= 50:
                        if choice_chest == 1:
                            item_data = get_item_data(
                                player['класс'],
                                player['инвентарь']
                            )
                            player['инвентарь'].append(item_data)
                    else:
                        if choice_chest == 1:
                            player['хп'] -= 3
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
                    for inventory in player['инвентарь']:
                        player['хп'] += inventory[1]
                    if not players:
                        break
                    os.system('clear')
                    if player['время урон апа'] > 0:
                        player['время урон апа'] -= 1
                    else:
                        player['урон'] /= 1.25 ** player['стак урон апа']
                        player['стак урон апа'] = 0
                    if player['время рег хп апа'] > 0:
                        player['время рег хп апа'] -= 1
                        if checkin(
                                player['хп'],
                                player['макс хп'],
                                2 * player['стак рег хп апа'],
                                False
                                ):
                            player['хп'] += 2 * player['стак рег хп апа']
                        else:
                            player['хп'] = player['макс хп']
                    else:
                        player['стак рег хп апа'] = 0
                    if player['время рег мана апа'] > 0:
                        if checkin(
                                player['мана'],
                                player['макс мана'],
                                4 * player['стак рег мана апа'],
                                False
                                ):
                            player['мана'] += 4 * player['стак рег мана апа']
                        else:
                            player['мана'] = player['макс мана']
                    else:
                        player['стак рег мана апа'] = 0
                    if player['исп маны']:
                        player['исп маны'] = False
                    else:
                        try:
                            mana_plus += player['инвентарь'][3]
                        except IndexError:
                            pass
                        if player['класс'] == 'Призыватель':
                            mana_plus = 5
                        elif player['класс'] == 'Маг':
                            mana_plus = 1
                        elif player['класс'] == 'Хиллер':
                            mana_plus = 7
                        elif player['класс'] == 'Бард':
                            mana_plus = 6
                        elif player['класс'] == 'Шаман':
                            mana_plus = 3
                        if player['мана'] + mana_plus >= player['макс мана']:
                            player['мана'] = player['макс мана']
                        else:
                            player['мана'] += mana_plus
                    if player['хп'] > 0:
                        check = True
                        while check:
                            check = False
                            message_1, message_2 = message(player,
                                                           player['имя'],
                                                           nahl,
                                                           unknown_yourself)
                            print(message_1)
                            print(f' Колличество ходов: {turn}\n')
                            if unknown_enemies is True:
                                print(' Вы встретили: ?\n',
                                      'Здоровья у противника: ?\n')
                            else:
                                print(f' Вы встретили: {enemy_name}\n',
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
                                 enemy_health,
                                 player,
                                 players,
                                 check,
                                 enemy_dmg,
                                 defence) = choice_1(choice,
                                                     enemy_hp,
                                                     player,
                                                     players,
                                                     enemy_dmg,
                                                     True)
                            else:
                                (choice,
                                 enemy_hp,
                                 player,
                                 players,
                                 check,
                                 enemy_dmg,
                                 defence) = choice_1(choice,
                                                     enemy_hp,
                                                     player,
                                                     players,
                                                     enemy_dmg,)
                        action_enemy = random.randint(1, 100)
                        cripses = player['крипы'].copy()
                        player['крипы'] = [list(crip) for crip in cripses]
                        have_war = False
                        for played in players:
                            for dead in death:
                                if (played['класс'] == 'Воин'
                                        and player != dead):
                                    have_war = True
                        pl = players.index(player)
                        for inventory in player['инвентарь']:
                            defence += inventory[7]
                        if action_enemy >= 30:
                            if enemy_hp > 0:
                                if have_war:
                                    defence -= enemy_dmg
                                    if player['класс'] == 'Воин':
                                        if int(round(defence, 0)) >= 0:
                                            player['хп'] = player['хп']
                                        else:
                                            player['хп'] += defence
                                            if player['хп'] <= 0:
                                                death.append(
                                                    players.pop(
                                                        pl
                                                        )
                                                    )
                                else:
                                    if damage:
                                        defence -= enemy_dmg
                                        if (player['класс'] == 'Призыватель'
                                                and player['крипы']):
                                            player['крипы'][0][-2] -= enemy_dmg
                                        else:
                                            if int(round(defence, 0)) >= 0:
                                                player['хп'] = player['хп']
                                            else:
                                                player['хп'] += defence
                                                if player['хп'] < 0:
                                                    death.append(
                                                        players.pop(
                                                            pl
                                                            )
                                                        )
                                        a = random.randint(1, 10)
                                        if a < 9:
                                            damage = False
                        n = 0
                        for crip in player['крипы']:
                            if crip[2] <= 0:
                                player['крипы'].pop(n)
                            n += 1
                    else:
                        death.append(players.pop(players.index(player)))
    else:
        print(f' Вы проиграли. Тебя убили на {int(turn)} ходу')
        time.sleep(2)
    player = ''
    for i in playerses:
        player += f'{i["класс"]} '
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
