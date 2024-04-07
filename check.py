def checkin(now_value: int,
            max_value: int,
            value: int,
            minus: bool
            ) -> bool:
    if minus:
        if (int(now_value) == max_value and
                int(now_value) - value < 0):
            return False
        else:
            return True
    else:
        if (int(now_value) == max_value and
                int(now_value) + value > max_value):
            return False
        else:
            return True
