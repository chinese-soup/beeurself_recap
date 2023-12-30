from datetime import timedelta, datetime

def adjust_timestamp(entry):
    """
    This function adjusts the datetime of the timestamp by the time in the "late" string,
    so that if someone posted 25 hours late, they still count towards the right date,
    e.g.:
    1) 2023-01-01 bot says: POST BROS!
    2) Someone posts 25h30m20s late
    3) it still counts as 2023-01-01
    """
    late_time = entry["late_time"]
    if late_time == "":
        print("No late time")
        return datetime.fromisoformat(entry["timestamp"]).date()

    late_delta = timedelta()

    late_time = late_time.replace("late by ", "")

    # Parse late_time and add corresponding delta to late_delta
    if 'd' in late_time:
        days = int(late_time.split('d')[0])
        late_delta += timedelta(days=days)
        late_time = late_time.split('d')[1]

    if 'h' in late_time:
        hours = int(late_time.split('h')[0])
        late_delta += timedelta(hours=hours)
        late_time = late_time.split('h')[1]

    if 'm' in late_time:
        minutes = int(late_time.split('m')[0])
        late_delta += timedelta(minutes=minutes)
        late_time = late_time.split('m')[1]

    if 's' in late_time:
        seconds = int(late_time.split('s')[0])
        late_delta += timedelta(seconds=seconds)

    timestamp = datetime.fromisoformat(entry["timestamp"])
    adjusted_timestamp = timestamp - late_delta
    return adjusted_timestamp.date()