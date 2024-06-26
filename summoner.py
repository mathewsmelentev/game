import sqlite3
import random


def summon(count_summons: int,
           max_count_summons: int,
           mana: int
           ) -> list:
    if count_summons == max_count_summons:
        return 5, mana
    else:
        connection = sqlite3.connect('mygame.sqlite3')
        cursor = connection.cursor()
        cursor.execute('SELECT name, hp, dmg, mana_cost FROM Crips'
                       f' WHERE mana_cost < {mana}')
        summon_data = cursor.fetchall()
        if summon_data:
            count = len(summon_data)
            summon_id = random.randint(0, count-1)
            mana -= summon_data[summon_id][3]
            return summon_data[summon_id], mana
        else:
            return 5, mana
