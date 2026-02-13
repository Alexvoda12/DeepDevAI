import json
import time as time1
import os
import datetime

while True:
    with open('comands.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

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

    days_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # Список для команд, которые нужно удалить
    commands_to_remove = []
    
    for cmd, time_value in data.items():  # Более понятная распаковка
        print(f"Command: {cmd}, Time: {time_value}")
        print(time_value.split())
        
        if time_value.split()[0] in days_names:
            if time_value.split()[0] == name_day:
                if time_value.split()[1] == f'{hour}:{minute}':
                    os.system(cmd)
                else:
                    print(time_value.split()[1])
        else:
            if time_value.split()[0] == f'{year}-{month}-{day}':
                print(time_value.split()[0])
                print(f'{year}-{month}-{day}')
                if time_value.split()[1] == f'{hour}:{minute}':
                    # Отмечаем для удаления
                    commands_to_remove.append(cmd)
                    os.system(cmd)
            else:
                print(time_value.split()[0], f'{year}-{month}-{day}')
    
    # Удаляем отмеченные команды после итерации
    if commands_to_remove:
        for cmd in commands_to_remove:
            data.pop(cmd)
        # ВНИМАНИЕ: Здесь был 'reminds.json', оставляю как в оригинале
        with open('reminds.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    time1.sleep(60)