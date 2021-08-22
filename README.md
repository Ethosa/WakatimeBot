<h1 align="center">WakatimeBot</h1>
<div align="center">
    wakatime bot for VK
</div>
<div align="center">
    <a href="https://wakatime.com/badge/github/Ethosa/WakatimeBot">
        <img src="https://wakatime.com/badge/github/Ethosa/WakatimeBot.svg">
    </a>
    <a href="https://www.codefactor.io/repository/github/ethosa/wakatimebot">
        <img src="https://www.codefactor.io/repository/github/ethosa/wakatimebot/badge" alt="CodeFactor" />
    </a>
</div>

## Commands
- `languages <Username> -7/30/180/365days` - shows user used languages in time range (default is 7 days);
- `editors <Username> -7/30/180/365days` - shows user used editors in time range (default is 7 days);
- `os <Username> -7/30/180/365days` - shows user used OS in time range (default is 7 days);
- `langtop` - shows most used languages at this moment.
- `reg <Username>` - register in bot base for use `language`, `editors` and `os` commands without args.

## Usage
You need have:
- Group ID (like vk.com/club123123 (`123123` is group ID));
- Group token (like wioeufvh0834hvoji34bli3tbh8tv3u5bto85tubhvejirboe85uvb);
- Wakatime App ID (get it on wakatime.com! ^^);
- Wakatime App secret (get it on wakatime ... ^^)

```bash
git clone https://github.com/Ethosa/WakatimeBot
cd WakatimeBot
```

- Create `secret.cfg` in WakatimeBot/src
- run with ```python src/main.py```

### Example of `secret.cfg`
```
[VK]
GROUP_TOKEN = jk2bihugb2ruhvbwo8rfbovhli4jvtvhubw48ryv0984vgo84tyvgo8ytrbvotyw4vl8rtuvbowtr8vuebrtl
GROUP_ID = 123456789

[WAKATIME]
APP_ID = S4asdasdasdasdasdasdasdd
APP_SECRET = sec_asjdbiahfbaisjdbasjdhasjdasjdasjdhsakjdhasijdhaisduhiasdjhiasdhsiadhiasjdhiasjdh
```
