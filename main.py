import logging
import os
from dotenv import load_dotenv

from database import Database
from bot import TelegramInfoSeeker

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN 未设置，请在 .env 文件中配置")

    db_path = os.getenv("DB_PATH", "messages.db")
    keywords_raw = os.getenv("KEYWORDS", "")
    keywords = [kw.strip() for kw in keywords_raw.split(",") if kw.strip()]

    db = Database(db_path)
    seeker = TelegramInfoSeeker(token=token, db=db, keywords=keywords)
    seeker.run()


if __name__ == "__main__":
    main()
