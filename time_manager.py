import time

class TimeManager:
    def __init__(self):
        self.day = 1

    def next_day(self):
        self.day += 1
        print(f"Наступил новый день: {self.day}")
        time.sleep(1)  