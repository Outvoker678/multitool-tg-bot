# multitool-tg-bot

Мультифункциональный Telegram-бот на aiogram 3.x

## Возможности

- Скачивание видео из TikTok без водяных знаков
- Скачивание музыки из Spotify
- Автоматическая пересылка сообщений друзьям

## Быстрый старт

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/yourusername/multitool-tg-bot.git
   cd multitool-tg-bot
   ```

2. Установите зависимости:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` и добавьте токен бота:
   ```
   ENV_TOKEN="ваш_токен_бота"
   ```

4. Запустите бота:
   ```
   python main.py
   ```

## Структура проекта

- `main.py` — точка входа, запуск бота
- `handlers/` — обработчики команд и сообщений
- `keyboards/` — клавиатуры Telegram
- `services/` — вспомогательные сервисы (например, база данных)
- `config/` — настройки и переменные окружения

## Требования

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [spotdl](https://github.com/spotDL/spotify-downloader)

