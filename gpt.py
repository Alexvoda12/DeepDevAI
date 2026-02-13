# import subprocess
# import g4f, os, keyboard
# from ollama import chat

# with open("system.txt", "r", encoding="utf-8") as f:
#     system = f.read()


# def gpt(text, hystory, role):
#     hystory.append({"role": role, "content": text})
#     print(hystory)
#     prompt = chat(
#         model='gemma3:12b',
#         messages=hystory,
#     )
# #     prompt = g4f.ChatCompletion.create(
# #         model=g4f.models.command_a,
# #         messages=hystory
# #     )
#     hystory.append({"role": "assistant", "content": prompt.message.content})
#     return prompt.message.content, hystory


# # h = [{"role": "system", "content": system}]
# h = []
# prompt, h = gpt(system, h, 'user')
# cmd = ''
# while True:
#     text = input("You: ")
#     prompt, h = gpt(text, h, 'user')
    
#     for i in prompt.split('\n'):
#         o = 1
#         cmd = ''
#         if i.startswith("coma "):
#             print("GPT: ", i)
#             os.system(i[5:])
#         elif i.startswith("key "):
#             print("GPT: ", i)   
#             keyboard.press_and_release(i[4:])
#         else:
#             print("GPT: " * o, i)
#             o = 0



# # from ollama import chat

# # response = chat(
# #     model='gemma3:12b',
# #     messages=[{'role': 'user', 'content': 'кто ты?!'}],
# # )

# # print(response.message.content)










# lockal and cmd
# import subprocess
# import g4f, os, keyboard
# from ollama import chat
# import traceback, get_bookmarks
# from telegram import Bot, Update
# from telegram.ext import ContextTypes

# with open("system.txt", "r", encoding="utf-8") as f:
#     system = f.read()


# def gpt(text, hystory, role):
#     hystory.append({"role": role, "content": text})
#     # print(hystory)
#     prompt = chat(
#         model='gemma3:12b',
#         messages=hystory,
#     )   
#     hystory.append({"role": "assistant", "content": prompt.message.content})
#     return prompt.message.content, hystory


# def execute_command(command):
#     """Выполняет команду и возвращает результат"""
#     try:
#         # Удаляем 'coma ' префикс если он есть
#         if command.startswith('coma '):
#             command = command[5:]
        
#         # Выполняем команду и захватываем вывод
#         result = subprocess.run(
#             command, 
#             shell=True, 
#             capture_output=True, 
#             text=True, 
#             encoding='utf-8',
#             errors='replace'
#         )
        
#         # Формируем результат
#         output = f"Команда: {command}\n"
#         if result.stdout:
#             output += f"Вывод:\n{result.stdout}\n"
#         if result.stderr:
#             output += f"Ошибки:\n{result.stderr}\n"
#         output += f"Код возврата: {result.returncode}"
        
#         return output
        
#     except Exception as e:
#         return f"Ошибка при выполнении команды '{command}': {str(e)}\n{traceback.format_exc()}"

# def press_key(key_sequence):
#     """Нажимает комбинацию клавиш и возвращает результат"""
#     try:
#         keyboard.press_and_release(key_sequence)
#         return f"Успешно выполнено нажатие клавиш: {key_sequence}"
#     except Exception as e:
#         return f"Ошибка при нажатии клавиш '{key_sequence}': {str(e)}"
    


# h = []
# marks = get_bookmarks.main()
# m = ''
# for i in marks:
#     print(i)
#     # {'title': 'Входящие - Почта Mail', 'url': 'https://e.mail.ru/inbox/'}
#     m += f"{i['title']}: {i['url']}\n "

# # print(m)
# prompt, h = gpt(system + '\n\n Часто используеммые ссылки:\n ' + m, h, 'user')
# o = 1
# command_executed = False
# command_result = ""

# # while True:
# def main():
#     global command_executed, command_result, h, o
#     if command_executed and command_result:
#         # Отправляем результат от имени системы
#         system_message = f"Результат выполнения команды:\n{command_result}"
#         prompt, h = gpt(system_message, h, 'system')
#         print(f"\nСистема отправила результат нейросети с ответом {prompt}")
#     else:
#         text = input("You: ")
#         prompt, h = gpt(text, h, 'user')
    
#     command_executed = False
#     command_result = ""
    
    
#     for line in prompt.split('\n'):
#         if line.startswith("coma "):
#             print(f"GPT (команда): {line}")
#             command_executed = True
#             command_result = execute_command(line)
#             print(f"Результат команды:\n{command_result}")
            
#         elif line.startswith("key "):
#             print(f"GPT (клавиши): {line}")
#             command_executed = True
#             command_result = press_key(line[4:])
#             print(f"Результат: {command_result}")
            
#         else:
#             if line.strip():  # Показываем только непустые строки
#                 if o == 1:
#                     print("GPT: " + line)
#                     o = 0
#                 else:
#                     print(line)
    
#     # Если была выполнена команда, отправляем результат нейросети
    
#     o = 1  # Сбрасываем флаг для следующего ответа
    
    
# while True:
#     main()











# lockal and telegram
import datetime
import json
import subprocess
import g4f, os, keyboard
from ollama import chat
import traceback, get_bookmarks
from telegram import Bot, Update
from telegram.ext import ContextTypes

with open("system.txt", "r", encoding="utf-8") as f:
    system = f.read()

with open("settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    
BOT_TOKEN = settings["TelegrammBot"]["BotToken"]
ADMIN_CHAT_ID = settings["TelegrammBot"]["AdminId"]
MODEL = settings["Model"]
ISLOCKAL = settings["Lockal"]
ISFREE = settings["Free"]
OPENAI_API_KEY = settings["OpenAI_api"]

# BOT_TOKEN = "8403423760:AAEm6cqsu-HkbRkPyaWZHR5L716DArWo2YU"
# ADMIN_CHAT_ID = 8373408145

def gpt(text, hystory, role):
    year   = datetime.datetime.now().year
    month  = datetime.datetime.now().month
    if len(str(month)) == 1:
        month = f'0{month}'
    day    = datetime.datetime.now().day
    if len(str(day)) == 1:
        day = f'0{day}'
    hour   = datetime.datetime.now().hour
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    minute = datetime.datetime.now().minute
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    name_day = datetime.datetime.now().strftime("%A")
    global MODEL, ISLOCKAL
    hystory.append({"role": role, "content": text + f"\n\n\nВремя сейчас(Если понабится):{name_day}, день - {day}, месяц - {month}, год - {year}, час - {hour}, минута - {minute}'"})
    if ISLOCKAL:
        prompt = chat(
            model=MODEL,
            # model='system',
            # model='qwen2.5:14b',
            # model='command-r:12b',
            messages=hystory,
        ).message.content
    else:
        if ISFREE:
            prompt = g4f.ChatCompletion.create(
                model=MODEL,
                # model='qwen2.5:14b',
                # model='command-r:12b',
                messages=hystory,
            )
        else:
            import openai
            client = openai.OpenAI(api_key=OPENAI_API_KEY)

            prompt = client.chat.completions.create(
                model=MODEL,
                messages=hystory
            ).choices[0].message.content
    hystory.append({"role": "assistant", "content": prompt})
    print(hystory)
    return prompt, hystory

def execute_command(command):
    """Выполняет команду и возвращает результат"""
    try:
        # Удаляем 'coma ' префикс если он есть
        if command.startswith('coma '):
            command = command[5:]
        
        # Выполняем команду и захватываем вывод
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='cp866',
            errors='replace'
        )
        
        # Формируем результат
        output = f"Команда: {command}\n"
        if result.stdout:
            output += f"Вывод:\n{result.stdout}\n"
        if result.stderr:
            output += f"Ошибки:\n{result.stderr}\n"
        output += f"Код возврата: {result.returncode}"
        
        return output
        
    except Exception as e:
        return f"Ошибка при выполнении команды '{command}': {str(e)}\n{traceback.format_exc()}"

def press_key(key_sequence):
    """Нажимает комбинацию клавиш и возвращает результат"""
    try:
        keyboard.press_and_release(key_sequence)
        return f"Успешно выполнено нажатие клавиш: {key_sequence}"
    except Exception as e:
        return f"Ошибка при нажатии клавиш '{key_sequence}': {str(e)}"

async def write_to_admin(bot: Bot, text: str):
    """Отправляет сообщение администратору"""
    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID, 
            text=text[:4000]  # Ограничение Telegram
        )
        print(f"Отправлено администратору: {text[:100]}...")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

async def initialize_gpt():
    """Инициализирует GPT и загружает закладки"""
    h = []
    marks = get_bookmarks.main()
    m = ''
    for i in marks:
        m += f"{i['title']}: {i['url']}\n"
    
    # Инициализируем GPT с системным сообщением
    if MODEL == 'deepdev-assistant':
        prompt, h = gpt('Часто используемые ссылки:\n' + m, h, 'user')
    else:
        prompt, h = gpt(system + 'Часто используемые ссылки:\n' + m, h, 'user')
    
    # Создаем бота для отправки уведомлений
    bot = Bot(BOT_TOKEN)
    await write_to_admin(bot, "GPT инициализирован с закладками")
    
    return h, bot

# Глобальные переменные
h = None
bot_instance = None
command_executed = False
command_result = ""
o = 1

async def main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global h, bot_instance, command_executed, command_result, o
    
    # Инициализируем при первом вызове
    if h is None or bot_instance is None:
        h, bot_instance = await initialize_gpt()
    
    message = update.message.text
    
    if command_executed and command_result:
        # Отправляем результат от имени системы
        system_message = f"Результат выполнения команды:\n{command_result}"
        prompt, h = gpt(system_message, h, 'system')
        await write_to_admin(bot_instance, f"Система отправила результат нейросети с ответом: {prompt}...")
    else:
        text = message
        prompt, h = gpt(text, h, 'user')
    
    command_executed = False
    command_result = ""
    
    # Отправляем ответ пользователю
    response_lines = []
    for line in prompt.split('\n'):
        if line.startswith("coma "):
            print(4)
            response_lines.append(f"🤖 Выполняю команду: {line[5:]}")
            command_executed = True
            print(5)
            command_result = execute_command(line)
            print(6)
            await write_to_admin(bot_instance, f"Выполнена команда: {line[5:]}\nРезультат: {command_result}")
            
        elif line.startswith("key "):
            response_lines.append(f"⌨️ Нажимаю клавиши: {line[4:]}")
            command_executed = True
            print(1)
            command_result = press_key(line[4:])
            print(2)
            await write_to_admin(bot_instance, f"Нажаты клавиши: {line[4:]}")
            print(3)
        elif line.startswith("remind "):
            p = line.find("'", 8)
            say = line[8:p]
            response_lines.append(f"⏰ Запоминаю: {line[7:]}")
            command_executed = True
            command_result = "Запомнено"
            # Читаем файл
            with open('reminds.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Изменяем данные
            data[say] = line[p + 2:]

            # Перезаписываем файл полностью
            print('Записано')
            with open('reminds.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            await write_to_admin(bot_instance, f"Запомнено: {say} в {line[p + 2:]}")
            
        elif line.startswith("task "):
            p = line.find("'", 8)
            say = line[6:p]
            response_lines.append(f"⏰ Запоминаю: {line[5:]}")
            command_executed = True
            command_result = "Запомнено"
            # Читаем файл
            with open('comands.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Изменяем данные
            data[say] = line[p + 2:]

            # Перезаписываем файл полностью
            print('Записано')
            with open('comands.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            await write_to_admin(bot_instance, f"Запомнено: {say} в {line[p + 2:]}")
            
        else:
            if line.strip():  # Показываем только непустые строки
                response_lines.append(line)
    
    # Отправляем ответ пользователю
    if response_lines:
        response_text = "\n".join(response_lines)
        await update.message.reply_text(response_text)
    
    # Если была выполнена команда, отправляем результат нейросети
    if command_executed and command_result:
        system_message = f"Результат выполнения команды:\n{command_result}"
        prompt, h = gpt(system_message, h, 'system')
        await write_to_admin(bot_instance, f"{prompt}")
        command_executed = False
        command_result = ""
        # Можно отправить дополнительное сообщение или обработать как-то иначе
    
    o = 1  # Сбрасываем флаг для следующего ответа