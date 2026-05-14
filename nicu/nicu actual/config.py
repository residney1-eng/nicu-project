### THRESHOLDS ###

offset_db = 75   # 126 inside best w 75
offset_db_out = 95   #93


# timing
SAMPLE_INTERVAL = 1.0
AVG_WINDOW_MIN = 1   #5


# noises for display
OUTSIDE_MIN_DB = 30
OUTSIDE_MAX_DB = 80

INSIDE_MIN_DB = 30
INSIDE_MAX_DB = 80

INSIDE_MIC_OFFSET = 120

# alarm settings
ALARM_THRESHOLD_DB = 55   #actual will be 55 after mics are calibrated
ALARM_RESET_DB = 52   #actual will be 52

#microphones
INSIDE_MIC_DEVICE = []   # Samson UB1 inside
OUTSIDE_MIC_DEVICE = [0]   # 0 Samson UB1 outside