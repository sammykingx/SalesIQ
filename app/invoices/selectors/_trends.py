PERIOD_DAYS = {"7d": 7, "30d": 30, "90d": 90}

# Django's ExtractWeekDay is 1=Sunday..7=Saturday
WEEKDAY_LABELS = {1: "Sun", 2: "Mon", 3: "Tue", 4: "Wed", 5: "Thu", 6: "Fri", 7: "Sat"}
WEEKDAY_DISPLAY_ORDER = [2, 3, 4, 5, 6, 7, 1]  # Mon → Sun
