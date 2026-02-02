### TEST WITHOUT THE HARDWARE (TEMP)

import time
from alarm_func import inside_db

alarm = inside_db()

test_values = [40, 60, 70, 65, 48, 80, 45]

for db in test_values:
    alarm.process_noise(db)

    if db >= alarm.threshold_db:
        noise_status = "LOUD"
    else:
        noise_status = "SAFE"

    alarm_status = "ALARM" if alarm.is_active() else "—"

    print(
        f"Noise: {db} dB | "
        f"Noise state: {noise_status} | "
        f"Alarm: {alarm_status} | "
        f"Count today: {alarm.get_count()}"
    )

    time.sleep(1)

