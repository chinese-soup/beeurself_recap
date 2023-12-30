import json

from flask import Flask, render_template, jsonify

from rofl import sorted_post_count_per_nickname, sorted_caption_count_per_nickname, posted_on_time_count, \
    posted_late_count, grouped_by_dates
from rofl import MAX_COUNT_ALL_DATES, MAX_COUNT_OF_POSTS

import math

app = Flask(__name__)

users = {
    "Jod": {"avatar": "static/bee.jpg"},
    "Syyyr": {"avatar": "static/bee.jpg"},
    "Chinese_soup": {"avatar": "static/bee.jpg"},
    "Egg": {"avatar": "static/bee.jpg"},
    "Lime": {"avatar": "static/bee.jpg"},
    "Wakecold": {"avatar": "static/bee.jpg"},
    "Colfra": {"avatar": "static/bee.jpg"},
    "Tomsk": {"avatar": "static/avatars/Tomsk.jpg"},
    "Lo1ts": {"avatar": "static/bee.jpg"},
    "Seth": {"avatar": "static/bee.jpg"},
    "Sully": {"avatar": "static/bee.jpg"},
}

GROUPED_BY_MONTHS_AND_NICKS = {}

with open("grouped_by_nicknames_and_by_months.json", "r") as f:
    GROUPED_BY_MONTHS_AND_NICKS = json.load(f)

with open("count_per_day.json", "r") as f:
    count_per_day = json.load(f)

#with open("grouped_by_dates.json", "r") as bydate:
#    grouped_by_dates = json.load(f)


one_hundred = posted_on_time_count + posted_late_count 
on_time_perc = math.floor((posted_on_time_count / one_hundred)*100)
late_perc =  math.floor(100 - on_time_perc)

@app.route("/")
def index():
    return render_template("index.html", top_posters=sorted_post_count_per_nickname,
                           top_captions=sorted_caption_count_per_nickname,
                           posted_on_time_count=posted_on_time_count,
                           posted_late_count=posted_late_count,
                           GROUPED_BY_MONTHS=GROUPED_BY_MONTHS_AND_NICKS,
                           COUNT_PER_DATE=count_per_day,
                           MAX_COUNT_ALL_DATES=MAX_COUNT_ALL_DATES,
                           MAX_COUNT_OF_POSTS=MAX_COUNT_OF_POSTS,
                           users=users,
                           on_time_perc=on_time_perc,
                           late_perc=late_perc,
                           )

@app.route("/by_date/<date>")
def by_date(date):
    posts = grouped_by_dates.get(date)
    if posts:
        return jsonify(posts)
    else:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True)
