from _datetime import datetime


class Timer:
    start_time = 0
    total_time = 0

    def __init__(self, time_in_minutes):
        self.start_time = datetime.now().timestamp()
        self.total_time = time_in_minutes*60

    def time_left(self):
        time_elapsed = datetime.now().timestamp() - self.start_time
        time_remaining = max(self.total_time - time_elapsed, 0)
        return str(int(time_remaining/60)) + " minutes " + str(int(time_remaining % 60)) + " seconds"

    def __str__(self):
        return '\nTime Remaining: ' + self.time_left()


def new_timer(time_in_minutes):
    tim = Timer(time_in_minutes)
    print(tim)
    return tim


def date_from_string(date):
    split_date = date.split("Date:")[1].split()
    str_to_date = " ".join([split_date[i] for i in range(0, len(split_date))])
    return datetime.strptime(str_to_date, "%a %b %d %X %Y %z")
