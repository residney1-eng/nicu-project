from datetime import datetime
from zoneinfo import ZoneInfo

AVG_WINDOW_MIN = 5
OUTSIDE_MIN_DB = 7
OUTSIDE_MAX_DB = 120
INSIDE_MIN_DB = 7
INSIDE_MAX_DB = 45

def draw_screen(
    outside_db,
    outside_avg,
    inside_db,
    inside_avg,
    alarm_active,
    alarm_count
):
    ca_time = datetime.now(
	ZoneInfo("America/Los_Angeles")
    ).strftime("%H:%M:%S")

    print("-" * 60)
    print("Time (CA):", ca_time)

    print("Outside Noise Levels")
    print(f" Current: {outside_db:.1f} dB")
    print(f" Avg (last {AVG_WINDOW_MIN} min): {outside_avg:.1f} db")
    print(f" Expected range: {OUTSIDE_MIN_DB} to {OUTSIDE_MAX_DB} dB")

    print("Inside Noise Levels")
    print(f" Current: {inside_db:.1f} dB")
    print(f" Avg (last {AVG_WINDOW_MIN} min): {inside_avg:.1f} db")
    print(f" Expected range: {INSIDE_MIN_DB} to {INSIDE_MAX_DB} dB")

    print("Alarm Status")
    if alarm_active:
        print(f" ACTIVE | Count today: {alarm_count}")
    else:
        print(" OFF")

    print("=" * 60)
