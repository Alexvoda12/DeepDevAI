import json
import asyncio
import time as time1
import datetime
from telegram import Bot
from telegram.constants import ParseMode

while True:
    with open('reminds.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('settings.json', 'r', encoding='utf-8') as f:
        settings = json.load(f)

    print(settings["TelegrammBot"]['AdminId'])
    ADMIN_CHAT_ID = settings["TelegrammBot"]['AdminId']
    BOT_TOKEN = settings["TelegrammBot"]['BotToken']

    bot = Bot(BOT_TOKEN)
    
    async def write_to_admin(bot: Bot, text: str):
        global ADMIN_CHAT_ID
        """Отправляет сообщение администратору"""
        try:
            # Escape special characters for MarkdownV2
            escaped_text = escape_markdown(text)
            await bot.send_message(
                chat_id=ADMIN_CHAT_ID, 
                text=escaped_text[:4000],  # Ограничение Telegram
                parse_mode=ParseMode.MARKDOWN_V2
            )
            print(f"Отправлено администратору: {text[:100]}...")
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
    
    def escape_markdown(text):
        """Escape special characters for Telegram MarkdownV2"""
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text

    # Get current time
    now = datetime.datetime.now()
    year = now.year
    month = f"{now.month:02d}"
    day = f"{now.day:02d}"
    hour = f"{now.hour:02d}"
    minute = f"{now.minute:02d}"
    name_day = now.strftime("%A")

    days_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # List for reminders to remove
    reminders_to_remove = []
    
    for cmd, time_value in data.items():
        print(f"Command: {cmd}, Time: {time_value}")
        time_parts = time_value.split()
        
        if len(time_parts) >= 2:
            if time_parts[0] in days_names:
                # Weekly reminder
                if time_parts[0] == name_day and time_parts[1] == f'{hour}:{minute}':
                    escaped_cmd = escape_markdown(cmd)
                    asyncio.run(write_to_admin(bot, f'Вы просили напомнить: **{escaped_cmd}**'))
                    print(cmd)
            else:
                # One-time reminder
                if time_parts[0] == f'{year}-{month}-{day}' and time_parts[1] == f'{hour}:{minute}':
                    escaped_cmd = escape_markdown(cmd)
                    asyncio.run(write_to_admin(bot, f'Вы просили напомнить: **{escaped_cmd}**'))
                    reminders_to_remove.append(cmd)
                    print(cmd)
    
    # Remove executed one-time reminders
    if reminders_to_remove:
        for cmd in reminders_to_remove:
            data.pop(cmd)
        with open('reminds.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    time1.sleep(60)