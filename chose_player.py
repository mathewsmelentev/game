import random
import time

from db_work import 

def player_message(datas):
    message = ' Выберите свой класс\n'
    for data in datas:
        if data != datas[-1]:
            message += f' {data[0]} - {data[1]}\n'
        else:
            message += f' {data[0]} - {data[1]}'
    return message


def choice_1(choice, enemy_hp, hp, defence, mana, stack, player, crips, value=False,):
    if choice == 1:
        damag = enemy_hp
        if player[0] == 'Маг':
            if mana >= 4:
                enemy_hp -= player[2]
                mana -= 4
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

        else:
            enemy_hp -= player[2]
        if value is False:
            print(f' Вы совершили атаку на {damag - enemy_hp} единиц')
            time.sleep(2)
    elif choice == 2:
        defence = random.randint(3, 10)
        if value is False:
            print(f' Вы защитились на {defence} единиц')
            time.sleep(2)
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

        time.sleep(1)
    return (choice, enemy_hp, hp, defence, mana, stack)
