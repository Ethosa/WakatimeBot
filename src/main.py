# -*- coding: utf-8 -*-
# author: Ethosa
import configparser
from collections import OrderedDict
from random import randint
import regex
from saya import Vk
from wakatime.wakatime import Wakatime

# Read and parse config file.
# [VK]
# GROUP_ID, GROUP_TOKEN
#
# [WAKATIME]
# APP_ID, APP_SECRET
config = configparser.ConfigParser()
with open("secret.cfg", "r", encoding="utf-8") as f:
    config.read_string(f.read())


class WakaTimeBot(Vk):
    def build_languages(self, user, days, response):
        """
        Builds answer to `languages` command.
        """
        result = f"📦 Языки, используемые {user} за последние {days} дней:\n"
        return result + "\n".join(f"{lang['name']}: {lang['text']} ({lang['percent']}%)"
                                  for lang in response["data"]["languages"])

    def build_top(self, languages, maxv=10):
        """
        Build languages top.
        """
        result = f"💯Топ-{maxv} используемых языков за последние 7 дней на Wakatime:\n"
        for i in range(1, maxv+1):
            result += f"{i}. {languages[i][0]} - {round(languages[i][1] / 60 / 60, 2)} часов.\n"
        return result[:-1]

    def message_new(self, event):
        """
        Calls when get new message.
        """
        msg = event["object"]["message"]["text"]
        peer_id = event["object"]["message"]["peer_id"]

        # languages Username -7days
        if msg.startswith("languages"):
            text = regex.findall(r"\S+", msg)  # Get message words.
            user = text[1]  # Get username [USERNAME | @USERNAME]
            days = "7"  # Get last 7 days stat

            parsed = self.parse_args(text)
            if "days" in parsed:
                days = parsed["days"]

            response = wakatime.get_user_stats(user, days)  # get stats in json
            # Check error
            if "data" in response:
                self.send_msg(self.build_languages(user, days, response), peer_id)
            else:
                self.send_error(peer_id)

        # langtop
        # Shows top languages.
        elif msg.startswith("langtop"):
            response = wakatime.get_leaderboard()
            languages = dict(Wakatime.LANGUAGES)

            if "data" in response:
                print(response["data"])
                for user in response["data"]:
                    for lang in user["running_total"]["languages"]:
                        try:
                            languages[lang['name']] += lang['total_seconds']
                        except:
                            languages[lang['name']] = lang['total_seconds']
                            print(lang['name'])
                languages = [
                    (k, v) for k, v in sorted(languages.items(), key=lambda item: item[1], reverse=True)
                ]
                self.send_msg(self.build_top(languages), peer_id)

    def parse_args(self, words):
        """
        Parses args in message and returns parsed settings dict.
        """
        result = dict()
        for i in words:
            if regex.match(r"\-(7|30|180|365)days", i):
                result["days"] = regex.findall(r"\d+", i)[0]
        return result

    def send_error(self, peer_id):
        self.messages.send(message="❌ Упс! Кажется, произошла какая-то ошибка ...", random_id=randint(0, 100000), peer_id=peer_id)

    def send_msg(self, msg, peer_id):
        self.messages.send(message=msg, random_id=randint(0, 100000), peer_id=peer_id)


if __name__ == '__main__':
    wakatime = Wakatime(config["WAKATIME"]["APP_ID"], config["WAKATIME"]["APP_SECRET"])
    bot = WakaTimeBot(token=config["VK"]["GROUP_TOKEN"], group_id=config["VK"]["GROUP_ID"], debug=True)
    bot.start_listen()
