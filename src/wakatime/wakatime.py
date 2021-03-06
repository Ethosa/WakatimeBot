from PIL import Image, ImageDraw
from random import randint
import requests
import regex


class Wakatime:

    URL = "https://wakatime.com/api/v1/"
    TIME_TABLE = {
        "7": "last_7_days",
        "30": "last_30_days",
        "180": "last_6_months",
        "365": "last_year",
    }

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.session = requests.Session()

    def _load_maxvalue(self, data, maxv):
        maxvalue = 0
        for i in range(1, maxv+1):
            maxvalue += data[i-1][1]
        return maxvalue

    def get_method(self, apimethod):
        return self.session.get(Wakatime.URL + apimethod)

    def get_leaderboard(self, page="1"):
        return self.get_method(f"leaders?page={page}").json()

    def get_user_stats(self, user, time="7"):
        if user[0] != "@":
            user = f"@{user}"

        return self.get_method(f"users/{user}/stats/{Wakatime.TIME_TABLE[time]}").json()

    def image_from_data(self, imgname, data, maxv=10):
        """
        data is list of tuples:
        [('Java', 10), ('Rust', 7), ...]
        """
        if maxv > len(data):
            maxv = len(data)
        img = Image.new("RGBA", (550, 360), (33, 33, 33))
        draw = ImageDraw.Draw(img)

        current = 0
        maxvalue = self._load_maxvalue(data, maxv)
        for i in range(1, maxv+1):
            color = (randint(66, 222), randint(66, 222), randint(66, 222))
            percent = 360*(data[i-1][1]/maxvalue + current)

            draw.pieslice((16, 0, 376, 360), 360*current, percent, color)

            draw.rectangle((390, 6 + i * 18, 390+16, 6 + i * 18 + 16), color)
            draw.text((390+20, 6 + i * 18), f" - {data[i-1][0]}", (200, 200, 200))

            current += data[i-1][1]/maxvalue
        del draw

        img.save(imgname)

    def post_method(self, apimethod):
        return self.session.post(Wakatime.URL + apimethod)
