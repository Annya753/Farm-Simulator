import time
import threading


class TimeManager:
    def __init__(self):
        self.day = 1
        self.timer_active = False  # Флаг, чтобы предотвратить повторные таймеры
        self.dayflag = True

    def timer_increment(self, interval, callback):
        def timer_thread():
            print(f"Таймер запущен на {interval} секунд...")
            time.sleep(interval)
            print("Таймер истек!")
            callback()
            self.timer_active = False  # Разрешаем запуск следующего таймера

        if not self.timer_active:
            self.timer_active = True
            thread = threading.Thread(target=timer_thread, daemon=True)
            thread.start()

    def toggle_dayflag(self):
        self.dayflag = not self.dayflag
        print(f"Флаг дня изменён: {self.dayflag}")


    def advance_time(self, farmer, dayflag):
        def on_timer_end():
            if (dayflag == False):
                self.day += 1
            else: self.day += 0
            self.toggle_dayflag()  # Меняем фон
            print(f"Наступил день {self.day}")

            for plant in farmer.plants:
                plant.grow()
            for animal in farmer.animals:
                animal.hungry = True

        self.timer_increment(60, on_timer_end)  # Запускаем таймер на 60 секунд
