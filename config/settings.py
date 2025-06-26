from dotenv import load_dotenv
import os

load_dotenv()  # Загружает переменные из .env

BOT_TOKEN = os.getenv("ENV_TOKEN")  # Безопасное получение токена