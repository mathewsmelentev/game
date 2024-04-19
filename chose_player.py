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
             enemy_hp: int,
             hp: int,
             defence: int,
             mana: int,
             stack: int,
             player: list,
             crips: list,
             max_crips: int,
             players: list,
             enemy_dmg: int,
             value: bool = False,) -> list:
    check = False
    mana_use = False
    dmg = player[2]
    for inventory in player[-11]:
        dmg += inventory[5]
    if choice == 1:
        damag = enemy_hp
        if player[0] == 'Маг':
            if mana >= 4:
                enemy_hp -= dmg
                mana -= 4
                mana_use = True
            else:
                enemy_hp -= round(dmg/2)
        elif player[0] == 'Стрелplayerок':
            crit_ch = random.randint(1, 10)
            if crit_ch <= 2:
                enemy_hp -= dmg * 3
            else:
                enemy_hp -= dmg
        elif player[0] == 'Рога':
            enemy_hp -= (dmg + 4*stack)
        elif player[0] == 'Призыватель':
            crip, mana = summon(len(crips), max_crips, mana)
            if crip == 5:
                pass
            else:
                crips.append(crip)
                print(f' Вы призвали крипа. Его зовут: {crip[0]}')
                mana_use = True
            value = True
        elif player[0] == 'Вампир':
            enemy_hp -= dmg
            if checkin(
                    int(hp),
                    int(player[4]),
                    int(round(dmg / 2, 0)),
                    False
                    ):
                hp += int(round(dmg / 2, 0))
        elif player[0] == 'Хиллер':
            if mana - 5 > 0:
                os.system('clear')
                dmg = round(dmg, 0)
                hill = random.randint(dmg, dmg + 2)
                hillers = []
                for played in players:
                    if played != player and played[1] > 0:
                        hillers.append(played)
                n = 0
                print('Выберите кого полечить:')
                for hill_target in hillers:
                    print(
                        f' {n + 1}.\n',
                        f' Имя игрока: {hill_target[-9]}\n',
                        f' Класс игрока: {hill_target[0]}\n',
                        f' Здоровье: {hill_target[1]}\n'
                    )
                    n += 1
                choice2 = int(input(' ')) - 1
                try:
                    if checkin(
                            hillers[choice2][1],
                            hillers[choice2][4],
                            hill,
                            False
                            ):
                        hillers[choice2][1] += hill
                        if checkin(
                                hillers[choice2][3],
                                hillers[choice2][5],
                                5,
                                False
                                ):
                            hillers[choice2][3] += 5
                        else:
                            hillers[choice2][3] = hillers[choice2][5]
                    else:
                        hillers[choice2][1] = hillers[choice2][4]
                except Exception:
                    print('Лечить некого')
                print(f'Вы вылечили игрока на: {hill}')
                mana -= 5
                mana_use = True
            value = True
        elif player[0] == 'Бард':
            if mana - 7 >= 0:
                bufs = []
                for played in players:
                    if played != player:
                        bufs.append(played)
                for played in bufs:
                    played[2] *= 1.25
                    played[-8] += 1
                    if played[-7] == 0:
                        played[-7] = 3
                mana -= 7
                mana_use = True
            value = True
        elif player[0] == 'Шаман':
            if mana - 14 >= 0:
                enemy_dmg /= 2
                mana -= 14
                mana_use = True
            value = True
        elif player[0] == 'Чернокнижник':
            enemy_hp -= dmg
            hp -= 8
        else:
            enemy_hp -= dmg
        if value is False:
            print(f' Вы совершили атаку на {damag - enemy_hp} единиц')
    elif choice == 2:
        if player[0] == 'Хиллер':
            hp_plus = random.randint(dmg + 1, dmg + 3)
            if checkin(player[1], player[4], hp_plus, False):
                if checkin(player[3], player[5], 6, True):
                    player[1] += hp_plus
                    print(f' Вы вылечились на {hp_plus} единиц')
            else:
                print(' Ваше здоровье и так полное')
            mana -= 6
            value = True
        elif player[0] == 'Бард':
            if mana - 9 >= 0:
                bufs = []
                for played in players:
                    if played != player:
                        bufs.append(played)
                for played in bufs:
                    played[-4] += 1
                    if played[-3] == 0:
                        played[-3] = 3
                mana -= 9
                mana_use = True
            value = True
        elif player[0] == 'Чернокнижник':
            hill = random.randint(7, 9)
            if mana - 7 >= 0:
                if checkin(
                        player[1],
                        player[4],
                        hill,
                        False
                        ):
                    player[1] += hill
                    mana -= 7
                    mana_use = True
                    print(f'Вы вылечились на {hill} единиц')
            value = True
        else:
            defence = random.randint(3, 10)
        if value is False:
            print(f' Вы защитились на {defence} единиц')
    elif choice == 5:
        if player[0] == 'Рога':
            print(' Вы встаёте в стойку')
            time.sleep(1)
            stoika = False
            inv_ch = random.randint(1, 10)
            stack_ch = random.randint(1, 10)
            for inventory in player[-11]:
                if 'Браслет "Скрывающегося в тени"' in inventory:
                    inv_ch_pl = 4
                    stack_ch_pl = 6
                    break
                else:
                    inv_ch_pl = 3
                    stack_ch_pl = 5
            if inv_ch <= inv_ch_pl:
                stoika = True
                defence = 100
            if stack_ch <= stack_ch_pl:
                stoika = True
                stack += 1
            time.sleep(1)
            if stoika is True:
                print(' Вы успешно встали в стойку!')
            else:
                print(' Попытка встать в стойку провалилась(')
        elif player[0] == 'Призыватель':
            os.system('clear')
            for crip in player[-1]:
                if crips:
                    print(f' Имя крипа: {crip[0]}\n',
                          f'Здоровье крипа: {crip[1]}\n')
            print(' Выберите, что будут делать крипы\n',
                  '1 - атаковать\n',
                  '0 - выйти')
            a = True
            while a:
                try:
                    crip_choice = int(input(' '))
                except ValueError:
                    a = True
            if crip_choice == 1:
                for crip in crips:
                    enemy_hp -= crip[2]
            else:
                check = True
        elif player[0] == 'Хиллер':
            hill = random.randint(dmg, dmg + 4)
            if checkin(player[3],
                       player[5],
                       9,
                       True):
                for hill_target in players:
                    if checkin(hill_target[1],
                               hill_target[4],
                               hill,
                               False):
                        hill_target[1] += hill
                mana -= 9
                print(f' Все были вылечены на {hill}')
                mana_use = True
        elif player[0] == 'Бард':
            if mana - 5 >= 0:
                bufs = []
                for played in players:
                    if played != players:
                        bufs.append(played)
                for played in bufs:
                    played[-6] += 1
                    if played[-5] == 0:
                        played[5] = 3
                mana_use = True
                mana -= 5
    elif choice == 3:
        os.system('clear')
        print('Такие предметы у тебя в инвентаре')
        for inventory in player[-11]:
            print(
                f'{inventory[0]}\n'
            )
        check = True
    time.sleep(2)
    os.system('clear')
    return (choice,
            enemy_hp,
            hp,
            defence,
            mana,
            stack,
            crips,
            check,
            mana_use,
            players,
            enemy_dmg)
