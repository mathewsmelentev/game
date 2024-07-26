import random
import time
import os

from summoner import summon
from check import checkin


def player_message(datas: list) -> list:
    message = ' Выберите свой класс\n'
    for data in datas:
        if data != datas[-1]:
            message += f' {data[0]} - {data[1]}\n'
        else:
            message += f' {data[0]} - {data[1]}\n'
        d = data[0] + 1
    message += f' {d} - Случайный персонаж'
    return message, d


def choice_1(choice: int,
             enemy_health: int,
             player,
             players,
             enemy_dmg: int,
             value: bool = False,) -> list:
    defence = 0
    check = False
    player['исп маны'] = False
    dmg = player['урон']
    for inventory in player['инвентарь']:
        dmg += inventory[5]
    if choice == 1:
        damag = enemy_health
        if player['класс'] == 'Маг':
            if player['мана'] >= 4:
                enemy_health -= dmg
                player['мана'] -= 4
                player['исп маны'] = True
            else:
                enemy_health -= round(dmg/2)
        elif player['класс'] == 'Стрелок':
            crit_ch = random.randint(1, 10)
            if crit_ch <= 2:
                enemy_health -= dmg * 3
            else:
                enemy_health -= dmg
        elif player['класс'] == 'Рога':
            enemy_health -= (dmg + 4*player['стак'])
        elif player['класс'] == 'Призыватель':
            crip, player['мана'] = summon(
                len(player['крипы']),
                player['макс крипов'],
                player['мана']
            )
            if crip == 5:
                pass
            else:
                player['крипы'].append(crip)
                print(f' Вы призвали крипа. Его зовут: {crip[0]}')
                player['исп маны'] = True
            value = True
        elif player['класс'] == 'Вампир':
            enemy_health -= dmg
            if checkin(
                    int(player['хп']),
                    int(player['макс хп']),
                    int(round(dmg / 2, 0)),
                    False
                    ):
                player['хп'] += int(round(dmg / 2, 0))
        elif player['класс'] == 'Хиллер':
            if player['мана'] - 5 > 0:
                os.system('clear')
                dmg = round(dmg, 0)
                hill = random.randint(dmg, dmg + 2)
                hillers = []
                for played in players:
                    if played != player and played['хп'] > 0:
                        hillers.append(played)
                n = 0
                print('Выберите кого полечить:')
                for hill_target in hillers:
                    print(
                        f' {n + 1}.\n',
                        f' Имя игрока: {hill_target["имя"]}\n',
                        f' Класс игрока: {hill_target["класс"]}\n',
                        f' Здоровье: {hill_target["хп"]}\n'
                    )
                    n += 1
                choice2 = int(input(' ')) - 1
                try:
                    if checkin(
                            hillers[choice2]['хп'],
                            hillers[choice2]['макс хп'],
                            hill,
                            False
                            ):
                        hillers[choice2]['хп'] += hill
                        if checkin(
                                hillers[choice2]['мана'],
                                hillers[choice2]['макс мана'],
                                5,
                                False
                                ):
                            hillers[choice2]['мана'] += 5
                        else:
                            hillers[choice2]['мана'] = hillers[
                                choice2
                                ]['макс мана']
                    else:
                        hillers[choice2]['хп'] = hillers[choice2]['макс хп']
                except Exception:
                    print('Лечить некого')
                print(f'Вы вылечили игрока на: {hill}')
                player['мана'] -= 5
                player['исп маны'] = True
            value = True
        elif player['класс'] == 'Бард':
            if player['мана'] - 7 >= 0:
                bufs = []
                for played in players:
                    if played != player:
                        bufs.append(played)
                for played in bufs:
                    played['урон'] *= 1.25
                    played['стак урон апа'] += 1
                    if played['время урон апа'] == 0:
                        played['время урон апа'] = 3
                player['мана'] -= 7
                player['исп маны'] = True
            value = True
        elif player['класс'] == 'Шаман':
            if player['мана'] - 14 >= 0:
                enemy_dmg /= 2
                player['мана'] -= 14
                player['исп маны'] = True
            value = True
        elif player['класс'] == 'Чернокнижник':
            enemy_health -= dmg
            player['хп'] -= 8
        else:
            enemy_health -= dmg
        if value is False:
            print(f' Вы совершили атаку на {damag - enemy_health} единиц')
    elif choice == 2:
        if player['класс'] == 'Хиллер':
            hp_plus = random.randint(dmg + 1, dmg + 3)
            if checkin(player['хп'], player['макс хп'], hp_plus, False):
                if checkin(player['хп'], player['макс хп'], 6, True):
                    player['хп'] += hp_plus
                    print(f' Вы вылечились на {hp_plus} единиц')
            else:
                print(' Ваше здоровье и так полное')
            player['мана'] -= 6
            value = True
        elif player['класс'] == 'Бард':
            if player['мана'] - 9 >= 0:
                bufs = []
                for played in players:
                    if played != player:
                        bufs.append(played)
                for played in bufs:
                    played['стак рег хп апа'] += 1
                    if played['время рег хп апа'] == 0:
                        played['время рег хп апа'] = 3
                player['мана'] -= 9
                player['исп маны'] = True
            value = True
        elif player['класс'] == 'Чернокнижник':
            hill = random.randint(7, 9)
            if player['мана'] - 7 >= 0:
                if checkin(
                        player['хп'],
                        player['макс хп'],
                        hill,
                        False
                        ):
                    player['хп'] += hill
                    player['мана'] -= 7
                    player['исп маны'] = True
                    print(f'Вы вылечились на {hill} единиц')
            value = True
        else:
            defence = random.randint(3, 10)
        if value is False:
            print(f' Вы защитились на {defence} единиц')
    elif choice == 5:
        if player['класс'] == 'Рога':
            print(' Вы встаёте в стойку')
            time.sleep(1)
            stoika = False
            inv_ch = random.randint(1, 10)
            stack_ch = random.randint(1, 10)
            inv_ch_pl = 3
            stack_ch_pl = 5
            for inventory in player['инвентарь']:
                if 'Браслет "Скрывающегося в тени"' in inventory:
                    inv_ch_pl = 4
                    stack_ch_pl = 6
                    break
            if inv_ch <= inv_ch_pl:
                stoika = True
                defence = 100
            if stack_ch <= stack_ch_pl:
                stoika = True
                player['стак'] += 1
            time.sleep(1)
            if stoika is True:
                print(' Вы успешно встали в стойку!')
            else:
                print(' Попытка встать в стойку провалилась(')
        elif player['класс'] == 'Призыватель':
            os.system('clear')
            for crip in player['крипы']:
                if player['крипы']:
                    print(f' Имя крипа: {crip[0]}\n',
                          f'Здоровье крипа: {crip[1]}\n')
            print(' Выберите, что будут делать крипы\n',
                  '1 - атаковать\n',
                  '0 - выйти')
            a = True
            while a:
                try:
                    crip_choice = int(input(' '))
                    a = False
                except ValueError:
                    a = True
            if crip_choice == 1:
                for crip in player['крипы']:
                    enemy_health -= crip[2]
            else:
                check = True
        elif player['класс'] == 'Хиллер':
            hill = random.randint(dmg, dmg + 4)
            if checkin(player['хп'],
                       player['макс хп'],
                       9,
                       True):
                for hill_target in players:
                    if checkin(hill_target['хп'],
                               hill_target['макс хп'],
                               hill,
                               False):
                        hill_target['хп'] += hill
                player['мана'] -= 9
                print(f' Все были вылечены на {hill}')
                player['исп маны'] = True
        elif player['класс'] == 'Бард':
            if player['мана'] - 5 >= 0:
                bufs = []
                for played in players:
                    if played != players:
                        bufs.append(played)
                for played in bufs:
                    played['стак рег мана апа'] += 1
                    if played['время рег мана апа'] == 0:
                        played['время рег мана апа'] = 3
                player['исп маны'] = True
                player['мана'] -= 5
    elif choice == 3:
        os.system('clear')
        print('Такие предметы у тебя в инвентаре')
        for inventory in player['инвентарь']:
            print(
                f'{inventory[0]}: {inventory[10]}\n'
            )
        check = True
    time.sleep(2)
    os.system('clear')
    return (choice,
            enemy_health,
            player,
            players,
            check,
            enemy_dmg,
            defence)
