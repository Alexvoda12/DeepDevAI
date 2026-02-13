# import asyncio
# import logging, gpt
# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Bot
# from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# BOT_TOKEN = "8403423760:AAEm6cqsu-HkbRkPyaWZHR5L716DArWo2YU"

# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         text="Привет! Я бот-помощник. Напиши мне что-нибудь, и я постараюсь помочь."
#     )

# async def main1():
#     application = Application.builder()\
#         .token(BOT_TOKEN)\
#         .read_timeout(20)\
#         .write_timeout(20)\
#         .connect_timeout(20)\
#         .pool_timeout(20)\
#         .build()

#     application.add_handler(CommandHandler("start", start_command))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt.main))

#     logger.info("Бот запускается...")
#     bot = Bot(BOT_TOKEN)
#     await bot.send_message(
#         chat_id=8373408145, 
#         text="Бот запущен"
#         ) # type: ignore
#     try:
#         application.run_polling(
#             poll_interval=0.3,
#             timeout=15,
#             drop_pending_updates=True,
#             allowed_updates=['message', 'callback_query']
#         )
#     except KeyboardInterrupt:
#         logger.info("Бот остановлен")
#     except Exception as e:
#         logger.error(f"Критическая ошибка: {e}")

# if __name__ == '__main__':
#     asyncio.run(main1())



import asyncio, json
import logging
import signal
import sys
import gpt
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# BOT_TOKEN = "8403423760:AAEm6cqsu-HkbRkPyaWZHR5L716DArWo2YU"
# ADMIN_CHAT_ID = 8373408145
with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
BOT_TOKEN = settings["TelegrammBot"]["BotToken"]
ADMIN_CHAT_ID = settings["TelegrammBot"]["AdminId"]

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        try:
            await update.message.reply_text("Доступ запрещен! Вы не мой хозяин. ⛔")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}") 
    else:
        await update.message.reply_text(
            text="Привет! Я бот-помощник в твоем компьютере. Напиши мне, и я постараюсь помочь."
        )

async def send_startup_message(application: Application):
    """Отправляет сообщение о запуске бота"""
    try:
        await application.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="✅ Бот запущен и готов к работе!"
        )
        logger.info("Сообщение о запуске отправлено администратору")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение о запуске: {e}")

async def send_shutdown_message(application: Application):
    """Отправляет сообщение об остановке бота"""
    try:
        await application.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="⏹️ Бот остановлен"
        )
        logger.info("Сообщение об остановке отправлено администратору")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение об остановке: {e}")
        
        
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_CHAT_ID:
        try:
            await update.message.reply_text("Доступ запрещен! Вы не мой хозяин. ⛔")
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}") 
    else:
        await gpt.main(update, context)

def main():
    """Основная синхронная функция"""
    # Создаем Application
    application = Application.builder()\
        .token(BOT_TOKEN)\
        .read_timeout(20)\
        .write_timeout(20)\
        .connect_timeout(20)\
        .pool_timeout(20)\
        .build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    logger.info("Бот запускается...")
    try:
        # Запускаем polling в отдельном потоке
        application.run_polling(
            poll_interval=0.3,
            timeout=15,
            drop_pending_updates=True,
            allowed_updates=['message', 'callback_query']
        )
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == '__main__':
    bot = Bot(BOT_TOKEN)
    asyncio.run(bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="✅ Компьютер запущен к работе!"
        ))
    main()