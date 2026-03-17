import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from database import Database

logger = logging.getLogger(__name__)


class TelegramInfoSeeker:
    def __init__(self, token: str, db: Database, keywords: list[str]):
        self.token = token
        self.db = db
        self.keywords = [kw.lower().strip() for kw in keywords if kw.strip()]
        self.app = Application.builder().token(token).build()
        self._register_handlers()

    def _register_handlers(self):
        self.app.add_handler(CommandHandler("start", self._cmd_start))
        self.app.add_handler(CommandHandler("stats", self._cmd_stats))
        self.app.add_handler(CommandHandler("keywords", self._cmd_keywords))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_message)
        )

    def _matches_keywords(self, text: str) -> bool:
        if not self.keywords:
            return True
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.keywords)

    async def _on_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.effective_message
        chat = update.effective_chat
        sender = update.effective_user

        if not message or not message.text:
            return

        if not self._matches_keywords(message.text):
            return

        sender_name = ""
        sender_id = None
        sender_username = None

        if sender:
            sender_id = sender.id
            sender_username = sender.username
            name_parts = [sender.first_name or "", sender.last_name or ""]
            sender_name = " ".join(p for p in name_parts if p).strip()

        self.db.save_message(
            message_id=message.message_id,
            chat_id=chat.id,
            chat_title=chat.title or chat.username or str(chat.id),
            sender_id=sender_id,
            sender_name=sender_name,
            sender_username=sender_username,
            text=message.text,
            date=message.date,
        )

        logger.info(
            "Saved message %d from chat '%s' (sender: %s)",
            message.message_id,
            chat.title or chat.id,
            sender_name or sender_id,
        )

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        kw_info = (
            f"当前关键词过滤：{', '.join(self.keywords)}"
            if self.keywords
            else "未设置关键词，保存所有消息"
        )
        await update.message.reply_text(
            f"Telegram Info Seeker 已启动\n"
            f"将我加入群组，我会自动保存消息到 SQLite 数据库。\n\n"
            f"{kw_info}\n\n"
            f"命令：\n"
            f"/stats - 查看统计信息\n"
            f"/keywords - 查看当前关键词"
        )

    async def _cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        stats = self.db.get_stats()
        await update.message.reply_text(
            f"统计信息：\n"
            f"已保存消息：{stats['total_messages']} 条\n"
            f"覆盖群组：{stats['total_chats']} 个"
        )

    async def _cmd_keywords(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.keywords:
            await update.message.reply_text(
                f"当前关键词：{', '.join(self.keywords)}"
            )
        else:
            await update.message.reply_text("未设置关键词，保存所有消息。")

    def run(self):
        logger.info(
            "Bot started. Keywords: %s",
            self.keywords if self.keywords else "all messages"
        )
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)
