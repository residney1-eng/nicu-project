### NOT USED

### TEST OF EVERYTHING ###
## this is the main coding, everything imported here, good to demo ##
# control + C to stop

import time
from noise_sensor import get_noise_level
from nicu.NU_alarm_logic import inside_db
from nicu.NU_led import led_on, led_off
from nicu.NU_display import draw_screen
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

    alarm.process_noise(noise_level)

    # LED + alarm status
    if alarm.is_active():
        led_on()
        print(f"ALARM ACTIVE | Count today: {alarm.get_count()}")
    else:
        led_off()
        print("Alarm: OFF")

    draw_screen(
        outside_db=noise_level,
	outside_avg=noise_level,
	inside_db=noise_level,
	inside_avg=noise_level,
	alarm_active=alarm.is_active(),
	alarm_count=alarm.get_count()
    )

    time.sleep(SAMPLE_INTERVAL)
