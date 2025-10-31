import json
import os
from random import randint
from datetime import datetime, timedelta
from core.logger import log

# Загружаем данные из vesna86.json
vesna_data = None
try:
    with open('data/vesna86.json', 'r', encoding='utf-8') as f:
        vesna_data = json.load(f)
except Exception as err:
    log.error(f"Failed to load vesna86.json: {err}")

# Загружаем данные календаря для весенних картинок
calendar_data = None
try:
    with open('data/calendar2016.json', 'r', encoding='utf-8') as f:
        calendar_data = json.load(f)
except Exception as err:
    log.error(f"Failed to load calendar2016.json: {err}")


def _get_random_spring_image():
    """
    Возвращает случайную весеннюю картинку из календаря (март-май)
    Управляется переменной окружения VESNA_IMAGE_ENABLED (yes/no)
    """
    try:
        # Проверяем, включены ли картинки
        image_enabled = os.environ.get('VESNA_IMAGE_ENABLED', 'yes').lower()
        if image_enabled not in ['yes', 'true', '1']:
            return None
        
        if not calendar_data:
            return None
        
        # Выбираем случайную дату между 1 марта и 31 мая
        # Март: 1-31, Апрель: 1-30, Май: 1-31
        month = randint(3, 5)  # 3=март, 4=апрель, 5=май
        
        if month == 3:
            day = randint(1, 31)
        elif month == 4:
            day = randint(1, 30)
        else:  # май
            day = randint(1, 31)
        
        # Формируем ключ в формате "20160301"
        key = f"2016{month:02d}{day:02d}"
        
        if key in calendar_data:
            imageurl = calendar_data[key]['imageurl']
            host = os.environ.get('CALENDAR_IMAGE_HOST', '')
            if not host:
                return None
            return host + imageurl
        
        return None
    except Exception as err:
        log.error(f"Error getting spring image: {err}")
        return None


def find_vesna_haiku(params=None):
    """
    Находит стих о весне по номеру автора или случайный
    
    Args:
        params: номер автора (1-86) или None для случайного выбора
    
    Returns:
        tuple: (text, None) где text - форматированный стих
        
    Логика:
        - С параметром: выводит ВСЕ стихи автора с разделителем "------"
        - Без параметра: выводит 1 случайный стих случайного автора
    """
    try:
        if not vesna_data:
            return None
        
        # Определяем номер автора
        if params:
            # С параметром - конкретный автор, все стихи
            try:
                author_num = int(params.strip())
                if author_num < 1 or author_num > 86:
                    return None
            except ValueError:
                return None
            
            # Форматируем ключ с лидирующим нулем
            key = f"{author_num:02d}"
            
            if key not in vesna_data:
                return None
            
            author_data = vesna_data[key]
            author_name = author_data['author']
            author_info = author_data.get('author_info', '')
            poems = author_data['poems']
            
            # Выводим ВСЕ стихи с разделителем
            lines = []
            for i, poem in enumerate(poems):
                lines.append(poem)
                if i < len(poems) - 1:  # Не добавляем разделитель после последнего стиха
                    lines.append('------')
            
            # Добавляем информацию об авторе в конце
            lines.append(f"\n{author_name}")
            if author_info:
                lines.append(author_info)
            
            text = '\n'.join(lines)
            image_url = _get_random_spring_image()
            return text, image_url
            
        else:
            # Без параметра - случайный автор, случайный стих
            author_num = randint(1, 86)
            key = f"{author_num:02d}"
            
            if key not in vesna_data:
                return None
            
            author_data = vesna_data[key]
            author_name = author_data['author']
            author_info = author_data.get('author_info', '')
            poems = author_data['poems']
            
            # Выбираем ОДИН случайный стих
            poem_index = randint(0, len(poems) - 1)
            poem_text = poems[poem_index]
            
            # Форматируем вывод
            lines = [poem_text]
            
            # Добавляем информацию об авторе
            lines.append(f"\n{author_name}")
            if author_info:
                lines.append(author_info)
            
            text = '\n'.join(lines)
            image_url = _get_random_spring_image()
            return text, image_url
        
    except Exception as err:
        log.error(f"Error in find_vesna_haiku: {err}")
        return None
