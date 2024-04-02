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
            message += f' {data[0]} - {data[1]}'
    return message


def choice_1(choice,
             enemy_hp,
             hp,
             defence,
             mana,
             stack,
             player,
             crips,
             max_crips,
             value=False,):
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
        else:
            enemy_hp -= player[2]
        if value is False:
            print(f' Вы совершили атаку на {damag - enemy_hp} единиц')
    elif choice == 2:
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
            for crip in crips:
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
        elif choice == 3:
            print('Это инвентарь, пока не работает')
            check = True
    time.sleep(2)
    os.system('clear')
    return (choice, enemy_hp, hp, defence, mana, stack, crips, check, mana_use)
