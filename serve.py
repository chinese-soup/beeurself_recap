import json

from flask import Flask, render_template

from main import sorted_post_count_per_nickname, GROUPED_BY_MONTHS
from rofl import sorted_caption_count_per_nickname, posted_on_time_count, posted_late_count

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
print(GROUPED_BY_MONTHS_AND_NICKS)

@app.route("/")
def index():
    return render_template("index.html", top_posters=sorted_post_count_per_nickname,
                           top_captions=sorted_caption_count_per_nickname,
                           posted_on_time_count=posted_on_time_count,
                           posted_late_count=posted_late_count,
                           GROUPED_BY_MONTHS=GROUPED_BY_MONTHS_AND_NICKS,
                           users=users,
                           )


if __name__ == "__main__":
    app.run(debug=True)
