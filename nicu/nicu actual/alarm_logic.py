### NOT USED

### COMBINED CODE W HONNAH ###

threshold_db = 55
reset_db = 52
cooldown = 5

import time
from datetime import date

class inside_db:
    def __init__(self, threshold_db=55, reset_db=52, cooldown=5):
        self.threshold_db = threshold_db
        self.reset_db = reset_db
        self.cooldown = cooldown

        self.alarm_active = False
        self.last_alarm_time = 0
        self.alarm_count_today = 0
        self.current_day = date.today()

    def process_noise(self, db_level):
        now = time.time()

        # Reset daily count
        if date.today() != self.current_day:
            self.alarm_count_today = 0
            self.current_day = date.today()

        # Trigger alarm
        if (
            db_level >= self.threshold_db
            and not self.alarm_active
            and now - self.last_alarm_time >= self.cooldown
        ):
            self.alarm_active = True
            self.last_alarm_time = now
            self.alarm_count_today += 1

        # Reset alarm (hysteresis)
        elif db_level <= self.reset_db:
            self.alarm_active = False

    def is_active(self):
        return self.alarm_active

    def get_count(self):
        return self.alarm_count_today
