def checkin(now_value, max_value, value, minus):
    if minus:
        if (now_value == max_value and
                now_value - value < 0):
            return False
        else:
            return True
    else:
        if (now_value == max_value and
                now_value + value > max_value):
            return False
        else:
            return True
