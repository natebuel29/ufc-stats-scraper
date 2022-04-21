from datetime import date


def normalize_results(results):
    normalize_list = list(map(str.strip, results))
    while "" in normalize_list:
        normalize_list.remove("")
    return normalize_list


def compute_percentage(stat):
    if "of" not in stat:
        return 0
    results = stat.split(" of ")
    if int(results[1]) == 0:
        return 0
    return round(int(results[0]) / int(results[1]), 2)


def null_check(stat):
    if stat == "---" or stat == "--":
        return "0"
    else:
        return stat


def convert_minutes_to_seconds(time):
    if ":" not in time:
        return 0
    else:
        time_list = time.split(":")
        return int(time_list[0]) * 60 + int(time_list[1])


def compute_age(dob):
    month_map = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    dob_split = dob.replace(",", "").split(" ")
    month = month_map.get(dob_split[0])
    today = date.today()
    bday = date(int(dob_split[2]), int(month), int(dob_split[1]))
    return today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))


def convert_feet_to_inches(height):
    height = height.replace('"', "")
    split_height = height.split("' ")
    return int(split_height[0]) * 12 + int(split_height[1])
