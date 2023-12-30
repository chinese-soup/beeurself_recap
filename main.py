#!/usr/bin/env python3
import calendar
import json
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Optional
from model import Message
from utils import adjust_timestamp

BOT_NICKNAME = "🐝UrselfBot"
BOT_USERID = "user5401852593"
JSON_STR = ""
bot_messages = []

"""
IDEAS:

Global:
---- Most ppl posted on <MONDAY/TUESDAY/..etc>
- Top 3 most reactions [???? no data]
- Some graphs [DONE, somewhat]
- Heatmap of the year [DONE, somewhat]
--> Days when ppl posted the most [DONE]
- Days OF WEEK when ppl posted the most

--- How late were you
-----> WHO WAS LATE THE MOST

Per user:
-- RECAP CALENDAR --- Heatmap of their postings
-- RECAP VIDEO (ffmpeg shit, slow and FAST and end)
- BeeUrself you've got the most reacts on
- How on Time were you 
-- Percentage how on time (graph?)
-- How top % poster were you (or at least position)
--- WHICH DAY OF WEEK you posted the most

Colfra:
--- 0% of your beerselfs included your face 


"""

# jq ".chats.list[0]" result.json > poopsman.json
# with open("poopsman.json", "r") as f:
with open("dl28/poopsman.json", "r") as f:
    JSON_STR = f.read()

j = json.loads(JSON_STR)
messages = j.get("messages")

grouped_by_nickname = defaultdict(list)


def get_placements(sorted_data):
    placements = {}
    current_position = 1
    current_count = None

    for index, (username, count) in enumerate(sorted_data):
        if count != current_count:
            current_position = index + 1
            current_count = count
        placements[username] = current_position

    # Convert tuples to lists and add placement as the third item
    lists_with_placement = [
        [placements[username], username, count] for username, count in sorted_data
    ]

    return lists_with_placement


def replace_nickname(input_nick):
    users = {
        "Egg": ["Egg", "eggu"],
        "Soup": ["Soup", "冰淇淋"],
        "Lo1ts": ["nick"],
        "Wakecold": ["Leonid", "Леонид"],
        "Colfra": ["Tamogolfra", "Colfra"],
        "Tomsk": ["Andrei"],
        "Orange": ["Seth"],
    }
    for main, sublist in users.items():
        if input_nick in sublist:
            print(f"Replacing {input_nick} with {main}")
            return main

    return input_nick  # Fall back to original nickname, if we didn't find a replacement


for msg_data in messages:
    # print(msg_data)
    try:
        # Creating Message dataclass object
        if msg_data["type"] != "message":
            continue

        msg_data["from_nickname"] = msg_data.pop("from")
        # We need to pop it off, since we can't use "from" in Python
        message = Message(**msg_data)

        #    print("Nice bot, bro", message.text_entities[-1], message.date_unixtime, message.photo)

        if int(message.date_unixtime) < 1672527600:
            continue  # Skip anything that's before January 2023

        if len(message.text_entities) == 0:
            continue

        last_text_entity = message.text_entities[-1]["text"]

        if msg_data["from_id"] != BOT_USERID:
            continue

        if message.photo is None:
            print(f"Skipping a non-photo message.")
            continue

        pattern_justnick_late = re.compile(
            r"^(.*?)\s\(late by (.*)\)$"
        )  # Sully (late by 1h52m21s)
        pattern_non_late_and_caption = re.compile(
            r"^(.*?)\s\(([\w]+)\)$"
        )  # "CAPTION" (Syyyr)
        pattern_late_and_caption = re.compile(
            r"^(.*?)\"\s\((.*?)\, (late by.*)\)$"
        )  # "am tired" (Syyyr, late by 12m20s)
        pattern_justnick = re.compile(r"^(.*?)$")

        nickname = ""
        caption = ""
        late_time = ""

        match_justnick_late = pattern_justnick_late.match(last_text_entity)
        match_non_late_and_caption = pattern_non_late_and_caption.match(
            last_text_entity
        )
        match_late_and_caption = pattern_late_and_caption.match(last_text_entity)
        match_justnick = pattern_justnick.match(last_text_entity)

        if match_late_and_caption:
            caption = match_late_and_caption.group(1)
            nickname = match_late_and_caption.group(2)
            late_time = match_late_and_caption.group(3)

        elif match_non_late_and_caption:
            caption = match_non_late_and_caption.group(1)
            nickname = match_non_late_and_caption.group(2)

        elif match_justnick_late:
            nickname = match_justnick_late.group(1)
            late_time = match_justnick_late.group(2)

        elif match_justnick:
            nickname = match_justnick.group(1)

        print(
            f"{nickname} \t| {message.date} |\t {caption} |\t Late_time = {late_time}"
        )

        nickname = replace_nickname(nickname)

        unix_timestamp = float(message.date_unixtime)
        date_obj = datetime.fromtimestamp(unix_timestamp)

        data = {
            "timestamp": message.date,
            "unix_ts": unix_timestamp,
            "datetime": date_obj,
            "caption": caption,
            "late_time": late_time,
            "nickdupe": nickname,
            "photo": message.photo
        }
        grouped_by_nickname[nickname].append(data)

        # print(message.from_nickname, message.from_id, message.date_unixtime)

    except Exception as e:
        # These are skipped, because BeeUrself bot's messages
        # will always pass, so whatever.
        print(f"Missed this message = {e} {msg_data}")
        pass

from pprint import pprint, pformat

pprint(grouped_by_nickname)

HOW_MANY_BEEURSELFS = defaultdict(int)
CAPTIONS_COUNT_GROUPED_BY = defaultdict(int)
LIST_OF_ALL_BEEURSELFS_COMBINED = sum(grouped_by_nickname.values(), [])


def group_by_months(all_posts: List):
    grouped_by_month_dict = defaultdict(lambda: defaultdict(list))

    for d in all_posts:
        date_obj = d["datetime"]  # Assuming date_obj is a datetime object
        month = calendar.month_name[date_obj.month]
        d.pop("datetime")
        nickname = d["nickdupe"]
        # Append the dict to the corresponding month key in the organized_dict
        grouped_by_month_dict[nickname][month].append(d)

    # If you want to sort each month's list of dicts by timestamp, you can do this:

    # for month, nicknames in grouped_by_month_dict.items():
    #   for nickname, values in nicknames.items():
    #   grouped_by_month_dict[nickname][month] = sorted(values, key=lambda x: x["unix_ts"])
    # Now, organized_dict contains dicts organized by month
    return grouped_by_month_dict


def group_by_day(all_posts: List):
    grouped_by_month_dict = defaultdict(lambda: defaultdict(list))

    for d in all_posts:
        date_obj = d["datetime"]  # Assuming date_obj is a datetime object
        month = calendar.month_name[date_obj.month]
        d.pop("datetime")
        nickname = d["nickdupe"]
        # Append the dict to the corresponding month key in the organized_dict
        grouped_by_month_dict[nickname][month].append(d)

    return grouped_by_month_dict


GROUPED_BY_MONTHS = group_by_months(LIST_OF_ALL_BEEURSELFS_COMBINED)

POSTED_LATE = [x for x in LIST_OF_ALL_BEEURSELFS_COMBINED if x.get("late_time") != ""]
POSTED_ON_TIME = [
    x for x in LIST_OF_ALL_BEEURSELFS_COMBINED if x.get("late_time") == ""
]

for nickname, list_of_beeurselfs in grouped_by_nickname.items():
    HOW_MANY_BEEURSELFS[nickname] = len(list_of_beeurselfs)
    CAPTIONS_COUNT_GROUPED_BY[nickname] = sum(
        1 for b in list_of_beeurselfs if b["caption"] != ""
    )

sorted_post_count_per_nickname = list(
    sorted(HOW_MANY_BEEURSELFS.items(), key=lambda x: x[1], reverse=True)
)
sorted_caption_count_per_nickname = list(
    sorted(CAPTIONS_COUNT_GROUPED_BY.items(), key=lambda x: x[1], reverse=True)
)

sorted_post_count_per_nickname = get_placements(sorted_post_count_per_nickname)
sorted_caption_count_per_nickname = get_placements(sorted_caption_count_per_nickname)


DATES = [adjust_timestamp(entry) for entry in LIST_OF_ALL_BEEURSELFS_COMBINED]
COUNT_PER_DATE = {date: DATES.count(date) for date in set(DATES)}
COUNT_PER_DATE_STR_FORMATTED = {
    date.strftime("%Y-%-m-%-d"): count for date, count in COUNT_PER_DATE.items()
}
tmp_max_count_date = max(COUNT_PER_DATE, key=COUNT_PER_DATE.get)
MAX_COUNT_OF_POSTS = COUNT_PER_DATE[tmp_max_count_date]

MAX_COUNT_ALL_DATES = [date.strftime("%a, %B %d") for date, count in COUNT_PER_DATE.items() if count == MAX_COUNT_OF_POSTS]

grouped_by_dates = defaultdict(list)


for entry in LIST_OF_ALL_BEEURSELFS_COMBINED:
    adjusted_ts = adjust_timestamp(entry).strftime("%Y-%-m-%-d")
    entry["adjusted_timestamp"] = adjusted_ts
    grouped_by_dates[adjusted_ts].append(entry)

grouped_by_dates = dict(grouped_by_dates)


# TODO: Get the top posted days
sorted(COUNT_PER_DATE_STR_FORMATTED.items(), key=lambda x: x[1], reverse=True)

with open("rofl.py", "w") as writef:
    writef.write(f"import datetime")
    writef.write(f"\n\n")
    writef.write(
        f"sorted_post_count_per_nickname = {pformat(sorted_post_count_per_nickname)}"
    )
    writef.write("\n\n")
    writef.write(
        f"sorted_caption_count_per_nickname = {pformat(sorted_caption_count_per_nickname)}"
    )
    writef.write("\n\n")
    writef.write(f"posted_late_count = {len(POSTED_LATE)}")
    writef.write("\n\n")
    writef.write(f"posted_on_time_count = {len(POSTED_ON_TIME)}")
    writef.write("\n\n")
    writef.write(f'MAX_COUNT_ALL_DATES = {MAX_COUNT_ALL_DATES}')
    writef.write("\n\n")
    writef.write(f"MAX_COUNT_OF_POSTS = {MAX_COUNT_OF_POSTS}")
    writef.write("\n\n")
    writef.write(f"grouped_by_dates = {grouped_by_dates}")

with open("grouped_by_nicknames_and_by_months.json", "w") as groupedfp:
    json.dump(GROUPED_BY_MONTHS, groupedfp)

with open("count_per_day.json", "w") as countfp:
    json.dump(COUNT_PER_DATE_STR_FORMATTED, countfp)

#with open("grouped_by_dates.json", "w") as bydatefp:
#    json.dump(grouped_by_dates, bydatefp)
