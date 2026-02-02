### TEST OF EVERYTHING ###
## this is the main coding, everything imported here, good to demo ##
# control + C to stop

import time
from noise_sensor import get_noise_level
from alarm_logic import inside_db
from led import led_on, led_off
from config import SAMPLE_INTERVAL, ALARM_THRESHOLD_DB, ALARM_RESET_DB, ALARM_COOLDOWN_SEC

# Create ONE alarm instance
alarm = inside_db(
    threshold_db=ALARM_THRESHOLD_DB,
    reset_db=ALARM_RESET_DB,
    cooldown=ALARM_COOLDOWN_SEC,
)

while True:
    noise_level = get_noise_level()
    print(f"Noise Level: {noise_level:.1f} dB")

    # Update alarm state
    alarm.process_noise(noise_level)

    # LED + alarm status
    if alarm.is_active():
        led_on()
        print(f"ALARM ACTIVE | Count today: {alarm.get_count()}")
    else:
        led_off()
        print("Alarm: OFF")

    time.sleep(SAMPLE_INTERVAL)

