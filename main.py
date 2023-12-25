#!/usr/bin/env python3

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Optional

from dataclass_wizard import JSONWizard

BOT_NICKNAME = "🐝UrselfBot"
BOT_USERID = "user5401852593"
JSON_STR = ""
bot_messages = []


"""
IDEAS:

Global:
- Top 3 days when ppl posted the most
- Top 3 most reactions

Per user:
- BeeUrself you've got the most reacts on
- 
"""


@dataclass
class TextEntity:
    type: str
    text: str


@dataclass
class Message:
    id: int
    type: str
    from_nickname: str
    from_id: str
    text: str
    text_entities: List[TextEntity]
    date: Optional[str] = None
    date_unixtime: Optional[str] = None
    edited: Optional[str] = None
    edited_unixtime: Optional[str] = None
    reply_to_message_id: Optional[int] = None
    photo: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    # There's more, but we only care about BeeUrself bot's messages,
    # so let's skip it


with open("poopsman.json", "r") as f:
    JSON_STR = f.read()

j = json.loads(JSON_STR)
messages = j.get("messages")

grouped_by_nickname = defaultdict(list)


def replace_nickname(input_nick):
    users = {
        "Egg": ["Egg", "eggu"],
        "Chinese_soup": ["Soup", "冰淇淋"],
        "Lo1ts": ["nick"],
        "Wakecold": ["Leonid", "Леонид"],
        "Colfar": ["Tamogolfra"],
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
        msg_data["from_nickname"] = msg_data.pop("from")
        # We need to pop it off, since we can't use "from" in Python
        message = Message(**msg_data)

        #    print("Nice bot, bro", message.text_entities[-1], message.date_unixtime, message.photo)
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

        '''if "hey tomsk" in last_text_entity:
            print(f"""Last = {last_text_entity} |
            match_non_late_and_caption = {match_non_late_and_caption}
            match_justnick_late = {match_justnick_late}
            match_late_and_caption = {match_late_and_caption}
            match_justnick = {match_justnick}
            nickname = {nickname}
            caption = {caption}
            late_Time = {late_time}
            """)
            print(f"{nickname} \t| {message.date} |\t Caption = {caption} |\t Late_time = {late_time}")
        '''
        print(
            f"{nickname} \t| {message.date} |\t {caption} |\t Late_time = {late_time}"
        )

        nickname = replace_nickname(nickname)

        data = {"timestamp": message.date, "caption": caption, "late_time": late_time}
        grouped_by_nickname[nickname].append(data)

        # print(message.from_nickname, message.from_id, message.date_unixtime)

    except Exception as e:
        # These are skipped, because BeeUrself bot's messages
        # will always pass, so whatever.
        # print(f"Missed this message = {e} {msg_data}")
        pass


from pprint import pprint

pprint(grouped_by_nickname)
