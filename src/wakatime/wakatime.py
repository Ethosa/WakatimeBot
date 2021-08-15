import requests
from pprint import pprint


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

    def get_method(self, apimethod):
        return self.session.get(Wakatime.URL + apimethod)

    def get_leaderboard(self, page="1"):
        return self.get_method(f"leaders?page={page}").json()

    def get_user_stats(self, user, time="7"):
        if user[0] != "@":
            user = f"@{user}"

        return self.get_method(f"users/{user}/stats/{Wakatime.TIME_TABLE[time]}").json()

    def post_method(self, apimethod):
        return self.session.post(Wakatime.URL + apimethod)
