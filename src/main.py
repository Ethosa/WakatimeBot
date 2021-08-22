# -*- coding: utf-8 -*-
# author: Ethosa
import sqlite3
import regex
from configparser import ConfigParser
from collections import OrderedDict
from random import randint
from os import remove
from saya import Vk, Uploader
from wakatime.wakatime import Wakatime


# Read and parse config file.
# [VK]
# USER_TOKEN, GROUP_ID, GROUP_TOKEN
#
# [WAKATIME]
# APP_ID, APP_SECRET
config = ConfigParser()
with open("secret.cfg", "r", encoding="utf-8") as f:
    config.read_string(f.read())

# connect to SQLite3
connect = sqlite3.connect('users.db')
cursor = connect.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS wakatime_users (id int, username text)')
connect.commit()


class WakaTimeBot(Vk):
    def add_user(self, data, user_id):
        for user in cursor.execute('SELECT * FROM wakatime_users'):
            if user[0] == user_id:
                return -1
        if user_id > 0 and data:
            cursor.execute('INSERT INTO wakatime_users VALUES (?, ?)', (user_id, data[0]))
            connect.commit()
            return 1
        return 0

    def build_stats(self, user, days, response, data_type="languages"):
        """
        Builds answer to `languages` command.
        """
        data = "📦 Языки" if data_type == "languages" else "📖 Редакторы" if data_type == "editors" else "💻 Операционные системы"
        result = f"{data}, используемые {user} за последние {days} дней:\n"
        result += "\n".join(f"{lang['name']}: {lang['text']} ({lang['percent']}%)"
                            for lang in response["data"][data_type])
        return result + "\nСреднее время кодинга за сутки: " + response["data"]["human_readable_daily_average"]

    def build_top(self, data, maxv=10, data_type="languages"):
        """
        Build top from data.
        """
        result = f"💯Топ-{maxv} используемых языков за последние 7 дней на Wakatime:\n"
        if maxv > len(data):
            maxv = len(data)
        for i in range(1, maxv+1):
            result += f"{i}. {data[i-1][0]} - {round(data[i-1][1] / 60 / 60, 2)} часов.\n"
        return result[:-1]

    def create_diagram(self, data):
        # Create pie diagram.
        name = f"{randint(0,100)}_{randint(0,100)}_{randint(0,100)}.png"
        wakatime.image_from_data(name, data)
        photo_response = self.upload_photo(name)
        remove(name)
        # Formatting
        return f"photo{photo_response['response'][0]['owner_id']}_{photo_response['response'][0]['id']}"

    def message_new(self, event):
        """
        Calls when get new message.
        """
        msg = event["object"]["message"]["text"]
        peer_id = event["object"]["message"]["peer_id"]
        from_id = event["object"]["message"]["from_id"]

        # languages/editors/os Username -7days
        if msg.startswith("languages"):
            self.send_stats(peer_id, msg, user_id=from_id)
        elif msg.startswith("editors"):
            self.send_stats(peer_id, msg, "editors", user_id=from_id)
        elif msg.lower().startswith("os"):
            self.send_stats(peer_id, msg, "operating_systems", user_id=from_id)

        # langtop
        # Shows top languages.
        elif msg.startswith("langtop"):
            self.send_top(peer_id)

        # reg @Username
        # Register as @username
        elif msg.startswith("reg "):
            username = regex.findall(r'@[\w\d]+', msg)
            response = self.add_user(username, from_id)
            if response == 1:
                self.send_msg(f"✅ Пользователь [id{from_id}|{username[0]}] был успешно добавлен!", peer_id)
            elif response == -1:
                self.send_msg("❌ Данный пользователь уже добавлен!", peer_id)
            else:
                self.send_error(peer_id)

    def parse_args(self, words):
        """
        Parses args in message and returns parsed settings dict.
        """
        result = dict()
        for i in words:
            if regex.match(r"\-(7|30|180|365)days", i):
                result["days"] = regex.findall(r"\d+", i)[0]
        return result

    def send_top(self, peer_id):
        """
        Builds languages top.
        """
        response = wakatime.get_leaderboard()
        data = {}

        if "data" in response:
            for user in response["data"]:
                for lang in user["running_total"]["languages"]:
                    try:
                        data[lang['name']] += lang['total_seconds']
                    except KeyError:
                        data[lang['name']] = lang['total_seconds']
            data = [
                (k, v) for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
            ]
            photo = self.create_diagram(data)
            
            self.send_msg(self.build_top(data), peer_id, attachment=photo)

    def send_stats(self, peer_id, msg, data_type="languages", user_id=0):
        """
        Builds User stat
        top_type may be "languages", "operating_systems", "editors"
        """
        text = regex.findall(r"\S+", msg)  # Get message words.
        days = "7"  # Get last 7 days stat
        user = ""
        if len(text) < 2:  # Get from SQLite DB
            for u in cursor.execute('SELECT * FROM wakatime_users'):
                if u[0] == user_id:
                    user = u[1]
        else:
            user = text[1]  # Get username [USERNAME | @USERNAME]

        if not user:  # Send error if username is empty
            self.send_msg("❌ Укажите никнейм пользователя на Wakatime или зарегестрируйтесь в боте, используя команду:\n<<reg @Username>>.", peer_id)
            return

        parsed = self.parse_args(text)
        if "days" in parsed:
            days = parsed["days"]

        response = wakatime.get_user_stats(user, days)  # get stats in json
        # Check error
        if "data" in response:
            data = {lang["name"]: lang["total_seconds"] for lang in response["data"][data_type]}
            data = [
                (k, v) for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)
            ]
            photo = self.create_diagram(data)

            self.send_msg(self.build_stats(user, days, response, data_type), peer_id, attachment=photo)
        else:
            self.send_error(peer_id)

    def send_error(self, peer_id):
        self.messages.send(message="❌ Упс! Кажется, произошла какая-то ошибка ...",
                           random_id=randint(0, 100000), peer_id=peer_id)

    def send_msg(self, msg, peer_id, attachment=""):
        return self.messages.send(message=msg, random_id=randint(0, 100000),
                                  peer_id=peer_id, attachment=attachment)

    def upload_photo(self, file):
        """
        Uploads photo in message.
        """
        response = self.call_method("photos.getMessagesUploadServer", {"group_id": config["VK"]["GROUP_ID"]})
        with open(file, "rb") as f:
            response = self.session.post(response["response"]["upload_url"], files={'file': f}).json()

        data = {
            "server": response["server"],
            "hash": response["hash"],
            "photo": response["photo"]
        }

        return self.call_method("photos.saveMessagesPhoto", data)


if __name__ == '__main__':
    wakatime = Wakatime(config["WAKATIME"]["APP_ID"], config["WAKATIME"]["APP_SECRET"])
    bot = WakaTimeBot(token=config["VK"]["GROUP_TOKEN"], group_id=config["VK"]["GROUP_ID"], debug=True, api="5.131")
    bot.start_listen()
