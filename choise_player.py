import random
import time
import os

from summoner import summon


def player_message(datas):
    message = ' Выберите свой класс\n'
    for data in datas:
        if data != datas[-1]:
            message += f' {data[0]} - {data[1]}\n'
        else:
            message += f' {data[0]} - {data[1]}\n'
        d = data[0] + 1
    message += f' {d} - Случайный персонаж'
    return message, d


def choice_1(choice,
             enemy_hp,
             hp,
             defence,
             mana,
             stack,
             player,
             crips,
             max_crips,
             players,
             value=False,):
    err = False
    check = False
    mana_use = False
    if choice == 1:
        damag = enemy_hp
        if player[0] == 'Маг':
            if mana >= 4:
                enemy_hp -= player[2]
                mana -= 4
                mana_use = True
            else:
                enemy_hp -= round(player[2]/2)
        elif player[0] == 'Стрелок':
            crit_ch = random.randint(1, 10)
            if crit_ch <= 2:
                enemy_hp -= player[2] * 3
            else:
                enemy_hp -= player[2]
        elif player[0] == 'Рога':
            enemy_hp -= (player[2] + 4*stack)
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
            enemy_hp -= player[2]
            hp += int(round(player[2] / 2, 0))
        elif player[0] == 'Хиллер':
            hillers = []
            for hiller in players:
                if not hiller == player:
                    hillers.append(hiller)
            try:
                rand_pl = random.randint(0, hillers.index(hillers[-1]))
            except ValueError:
                print(' Нет игроков, кого можно, нужно полечить')
                err = True
            except IndexError:
                print(' Нет игроков, кого можно, нужно полечить')
                err = True
            if not err:
                print(hillers)
                for hiller in hillers:
                    time.sleep(3)
                    if int(hiller[1]) == int(hiller[4]):
                        hillers = hillers.pop(hillers.index(hiller))
                if hillers:
                    hp_plus = random.randint(5, 7)
                    mana_plus = random.randint(2, 6)
                    if not (players[rand_pl][1] == players[rand_pl][4]
                            and
                            players[rand_pl][1] + mana_plus ==
                            players[rand_pl][4]):
                        players[rand_pl][1] += hp_plus
                    else:
                        players[rand_pl][1] = players[rand_pl][4]
                    if not (players[rand_pl][3] == players[rand_pl][5]
                            and
                            players[rand_pl][3] + mana_plus ==
                            players[rand_pl][5]):
                        players[rand_pl][3] += mana_plus
                    print(f' Вы вылечили игрока с классом'
                          f' {players[rand_pl][0]} на {hp_plus} единиц')
                else:
                    print(' Нет игроков, кого можно, нужно полечить')
            mana -= 5
            value = True
            mana_use = True
        else:
            enemy_hp -= player[2]
        if value is False:
            print(f' Вы совершили атаку на {damag - enemy_hp} единиц')
    elif choice == 2:
        defence = random.randint(3, 10)
        if player[0] == 'Хиллер':
            if not player[1] == player[4]:
                hp_plus = random.randint(6, 8)
                player[1] += hp_plus
                print(f' Вы вылечились на {hp_plus} единиц')
            else:
                print(' Ваше здоровье и так полное')
            mana -= 6
            value = True

        if value is False:
            print(f' Вы защитились на {defence} единиц')
    elif choice == 5:
        if player[0] == 'Рога':
            print(' Вы встаёте в стойку')
            time.sleep(1)
            stoika = False
            inv_ch = random.randint(1, 10)
            stack_ch = random.randint(1, 10)
            if inv_ch <= 3:
                stoika = True
                defence = 100
            if stack_ch <= 5:
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
            crip_choice = int(input(' '))
            if crip_choice == 1:
                for crip in crips:
                    enemy_hp -= crip[2]
            else:
                check = True
        elif player[0] == 'Хиллер':
            hill = random.randint(5, 9)
            for hill_target in players:
                if (hill_target[1] == hill_target[4]
                        and hill_target[1] + hill >= hill_target[4]):
                    hill_target[1] += hill
            mana -= 9
            print(f' Все были вылечены на {hill}')
            mana_use = True

    elif choice == 3:
        os.system('clear')
        print('Это инвентарь, он пока не работает')
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
            players)
