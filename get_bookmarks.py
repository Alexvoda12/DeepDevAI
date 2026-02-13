import os
import json
import sqlite3
from pathlib import Path
import platform

def get_chrome_bookmarks_windows():
    """Получает закладки из Chrome на Windows"""
    chrome_path = Path(os.getenv('LOCALAPPDATA')) / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'Bookmarks'
    return extract_chrome_bookmarks(chrome_path)

def get_edge_bookmarks_windows():
    """Получает закладки из Edge на Windows"""
    edge_path = Path(os.getenv('LOCALAPPDATA')) / 'Microsoft' / 'Edge' / 'User Data' / 'Default' / 'Bookmarks'
    return extract_chrome_bookmarks(edge_path)

def get_chrome_bookmarks_mac():
    """Получает закладки из Chrome на macOS"""
    chrome_path = Path.home() / 'Library' / 'Application Support' / 'Google' / 'Chrome' / 'Default' / 'Bookmarks'
    return extract_chrome_bookmarks(chrome_path)

def get_chrome_bookmarks_linux():
    """Получает закладки из Chrome на Linux"""
    chrome_path = Path.home() / '.config' / 'google-chrome' / 'Default' / 'Bookmarks'
    return extract_chrome_bookmarks(chrome_path)

def extract_chrome_bookmarks(file_path):
    """Извлекает ссылки из файла закладок Chrome/Edge"""
    bookmarks = []
    
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            def traverse(node):
                if 'children' in node:
                    for child in node['children']:
                        traverse(child)
                elif 'url' in node:
                    bookmarks.append({
                        'title': node.get('name', 'Без названия'),
                        'url': node['url']
                    })
            
            if 'roots' in data:
                for root in data['roots'].values():
                    traverse(root)
                    
        return bookmarks
    except Exception as e:
        print(f"Ошибка при чтении {file_path}: {e}")
        return []

def get_firefox_bookmarks_windows():
    """Получает закладки из Firefox на Windows"""
    firefox_path = Path(os.getenv('APPDATA')) / 'Mozilla' / 'Firefox' / 'Profiles'
    return extract_firefox_bookmarks(firefox_path)

def get_firefox_bookmarks_mac():
    """Получает закладки из Firefox на macOS"""
    firefox_path = Path.home() / 'Library' / 'Application Support' / 'Firefox' / 'Profiles'
    return extract_firefox_bookmarks(firefox_path)

def get_firefox_bookmarks_linux():
    """Получает закладки из Firefox на Linux"""
    firefox_path = Path.home() / '.mozilla' / 'firefox'
    return extract_firefox_bookmarks(firefox_path)

def extract_firefox_bookmarks(profiles_path):
    """Извлекает ссылки из базы данных Firefox"""
    bookmarks = []
    
    try:
        if profiles_path.exists():
            # Находим последний профиль
            profiles = list(profiles_path.glob('*.default*'))
            if not profiles:
                return []
            
            db_path = profiles[0] / 'places.sqlite'
            
            if db_path.exists():
                # Копируем БД для чтения
                import tempfile
                import shutil
                
                with tempfile.NamedTemporaryFile(suffix='.sqlite', delete=False) as tmp:
                    shutil.copy2(db_path, tmp.name)
                    conn = sqlite3.connect(tmp.name)
                
                cursor = conn.cursor()
                
                # Получаем закладки
                query = """
                SELECT moz_bookmarks.title, moz_places.url
                FROM moz_bookmarks
                JOIN moz_places ON moz_bookmarks.fk = moz_places.id
                WHERE moz_bookmarks.type = 1
                """
                
                cursor.execute(query)
                
                for row in cursor.fetchall():
                    bookmarks.append({
                        'title': row[0] or 'Без названия',
                        'url': row[1]
                    })
                
                conn.close()
                os.unlink(tmp.name)
                
        return bookmarks
    except Exception as e:
        print(f"Ошибка при чтении Firefox закладок: {e}")
        return []

def get_all_bookmarks():
    """Получает все закладки из доступных браузеров"""
    all_bookmarks = []
    system = platform.system()
    
    print(f"Операционная система: {system}")
    
    if system == 'Windows':
        # print("Чтение закладок Chrome...")
        chrome_bookmarks = get_chrome_bookmarks_windows()
        # print(f"Найдено: {len(chrome_bookmarks)} закладок")
        all_bookmarks.extend(chrome_bookmarks)
        
        # print("Чтение закладок Edge...")
        edge_bookmarks = get_edge_bookmarks_windows()
        # print(f"Найдено: {len(edge_bookmarks)} закладок")
        all_bookmarks.extend(edge_bookmarks)
        
        # print("Чтение закладок Firefox...")
        firefox_bookmarks = get_firefox_bookmarks_windows()
        # print(f"Найдено: {len(firefox_bookmarks)} закладок")
        all_bookmarks.extend(firefox_bookmarks)
        
    elif system == 'Darwin':  # macOS
        # print("Чтение закладок Chrome...")
        chrome_bookmarks = get_chrome_bookmarks_mac()
        # print(f"Найдено: {len(chrome_bookmarks)} закладок")
        all_bookmarks.extend(chrome_bookmarks)
        
        # print("Чтение закладок Firefox...")
        firefox_bookmarks = get_firefox_bookmarks_mac()
        # print(f"Найдено: {len(firefox_bookmarks)} закладок")
        all_bookmarks.extend(firefox_bookmarks)
        
    elif system == 'Linux':
        # print("Чтение закладок Chrome...")
        chrome_bookmarks = get_chrome_bookmarks_linux()
        # print(f"Найдено: {len(chrome_bookmarks)} закладок")
        all_bookmarks.extend(chrome_bookmarks)
        
        # print("Чтение закладок Firefox...")
        firefox_bookmarks = get_firefox_bookmarks_linux()
        # print(f"Найдено: {len(firefox_bookmarks)} закладок")
        all_bookmarks.extend(firefox_bookmarks)
    
    return all_bookmarks

def display_bookmarks(bookmarks_list):
    """Выводит список закладок в консоль"""
    # print("\n" + "="*80)
    # print("ВСЕ НАЙДЕННЫЕ ЗАКЛАДКИ:")
    # print("="*80)
    
    if not bookmarks_list:
        print("Закладки не найдены!")
        return
    
    # for i, bookmark in enumerate(bookmarks_list, 1):
    #     print(f"\n{i:4}. {bookmark['title']}")
    #     print(f"     URL: {bookmark['url']}")
    
    # print("\n" + "="*80)
    # print(f"Всего закладок: {len(bookmarks_list)}")
    # print("="*80)

def main():
    """Основная функция"""
    # Получаем все закладки
    all_bookmarks = get_all_bookmarks()
    
    # Выводим список
    display_bookmarks(all_bookmarks)
    
    # Возвращаем список для дальнейшего использования
    return all_bookmarks

# Дополнительные функции для работы со списком

def get_urls_only(bookmarks_list):
    """Возвращает только URL из списка закладок"""
    return [bookmark['url'] for bookmark in bookmarks_list]

def get_titles_only(bookmarks_list):
    """Возвращает только названия из списка закладок"""
    return [bookmark['title'] for bookmark in bookmarks_list]

def filter_by_keyword(bookmarks_list, keyword):
    """Фильтрует закладки по ключевому слову"""
    keyword_lower = keyword.lower()
    filtered = []
    
    for bookmark in bookmarks_list:
        if (keyword_lower in bookmark['title'].lower() or 
            keyword_lower in bookmark['url'].lower()):
            filtered.append(bookmark)
    
    return filtered

def save_to_simple_list(bookmarks_list, filename='bookmarks_list.txt'):
    """Сохраняет только URL в простой список"""
    with open(filename, 'w', encoding='utf-8') as f:
        for bookmark in bookmarks_list:
            f.write(f"{bookmark['url']}\n")
    
    # print(f"\nСписок URL сохранен в файл: {filename}")