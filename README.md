# Discord Activity Logger Bot

A [discord.py](https://discordpy.readthedocs.io/) bot that logs server activity — messages and voice-channel events — into a dedicated log channel as rich embeds.

## Features

- **Message logging** — every message (author, channel, content, attachments) is mirrored to a log channel as an embed
- **Voice activity tracking** — join / leave / move-between-channels / mute-deafen-stream state changes, each posted as a color-coded embed (green = join, red = leave, orange = move, purple = state change)
- **Per-user voice threads** — each member's voice session gets its own thread under their "join" message, so their mute/unmute/stream history stays grouped and gets auto-archived when they leave
- Session duration is tracked and shown when a member leaves a voice channel

## Requirements

- Python 3.10+
- A Discord bot application with **Message Content** and **Server Members** privileged intents enabled

## Installation

```bash
git clone https://github.com/skyvva1k3r/discord-bot.git
cd discord-bot
pip install discord.py python-dotenv
```

## Configuration

Create a `.env` file in the project root:

```
token=your_discord_bot_token
```

Then update the hard-coded log channel ID in [`main.py`](main.py) (`bot.get_channel(...)`) to a text channel ID in your server.

## Running

```bash
python main.py
```

## License

[MIT](LICENSE)

---

# Discord Activity Logger Bot (Русский)

Бот на [discord.py](https://discordpy.readthedocs.io/), который логирует активность сервера — сообщения и события голосовых каналов — в отдельный канал-лог в виде embed-сообщений.

## Возможности

- **Логирование сообщений** — каждое сообщение (автор, канал, текст, вложения) дублируется в лог-канал
- **Отслеживание голосовой активности** — вход/выход/переход между каналами/мут-деаф-стрим, каждое событие — цветной embed (зелёный — вход, красный — выход, оранжевый — переход, фиолетовый — изменение состояния)
- **Треды на каждого пользователя** — голосовая сессия участника получает свой тред под сообщением о входе, где собирается вся история мутов/стримов, тред автоматически архивируется при выходе
- Длительность сессии отслеживается и показывается при выходе из канала

## Требования

- Python 3.10+
- Discord-приложение бота с включёнными привилегированными интентами **Message Content** и **Server Members**

## Установка

```bash
git clone https://github.com/skyvva1k3r/discord-bot.git
cd discord-bot
pip install discord.py python-dotenv
```

## Настройка

Создайте файл `.env` в корне проекта:

```
token=токен_вашего_бота
```

Затем замените захардкоженный ID лог-канала в [`main.py`](main.py) (`bot.get_channel(...)`) на ID текстового канала на вашем сервере.

## Запуск

```bash
python main.py
```

## Лицензия

[MIT](LICENSE)
