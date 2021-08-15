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
    LANGUAGES = {
        'PHP': 0, 'Vue.js': 0, 'SCSS': 0,
        'XML': 0, 'SQL': 0, 'Blade Template': 0,
        'JSON': 0, 'JavaScript': 0, 'Docker': 0,
        'Bash': 0, 'Apache Config': 0, 'TypeScript': 0,
        'Markdown': 0, 'Ruby': 0, 'YAML': 0,
        'ERB': 0, 'Python': 0, 'Java': 0,
        'Properties': 0, 'Git Config': 0, 'Groovy': 0,
        'Rust': 0, 'C': 0, 'C#': 0,
        'C++': 0, 'Scheme': 0, 'Nim': 0,
        'Erlang': 0, 'COBOL': 0, 'F#': 0,
        'D': 0, 'R': 0, 'MATLAB': 0,
        'Perl': 0, 'Dart': 0, 'Batchfile': 0,
        'Slim': 0, 'Charmci': 0, 'HTML': 0,
        'Nginx configuration file': 0, 'GraphQL': 0, 'Text': 0,
        'CSS': 0, 'Gettext Catalog': 0, 'Solidity': 0,
        'Svelte': 0, 'AsciiDoc': 0, 'JSX': 0,
        'Protocol Buffer': 0, 'Scala': 0, 'INI': 0,
        'WiX Installer': 0, 'Kotlin': 0, 'Swift': 0,
        'XAML': 0, 'Stylus': 0, 'CSV': 0, 'Objective-C': 0,
        'EJS': 0, 'Prolog': 0, 'LESS': 0,
        'Terraform': 0, 'Makefile': 0, 'Smarty': 0,
        'Git': 0, 'Nix': 0, 'VimL': 0,
        'Mustache': 0, 'tmux': 0, 'systemd': 0,
        'TOML': 0, 'Modula-2': 0, 'sh': 0,
        'Common Lisp': 0, 'LLVM': 0, 'Go': 0,
        'Nginx': 0, 'Diff': 0, 'GAS': 0,
        'Gherkin': 0, 'Sass': 0, 'Elixir': 0,
        'Emacs Lisp': 0, 'Org': 0, 'BNF': 0,
        'MDX': 0, 'Cocoa': 0, 'Velocity': 0,
        'Objective-J': 0, 'CoffeeScript': 0, 'PowerShell': 0,
        'Lua': 0, 'VBScript': 0, 'Liquid': 0
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
