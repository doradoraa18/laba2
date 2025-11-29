# Поиск и валидация дат в формате ДД.ММ.ГГГГ

import re
import requests
from datetime import datetime
from typing import List


def find_potential_dates(text: str) -> List[str]:
    candidates = []
    # 1. Стандартный формат: 04.11.2025
    candidates.extend(re.findall(r'\b\d{2}\.\d{2}\.\d{4}\b', text))
    # 2. Формат stankin.ru: 11/27 2025, 27/11 2025 и т.п.
    matches = re.findall(r'\b(\d{1,2})/(\d{1,2})\s+(\d{4})\b', text)
    for a, b, year in matches:
        d1, d2 = a.zfill(2), b.zfill(2)
        candidates.append(f"{d1}.{d2}.{year}")  # MM.DD.YYYY
        candidates.append(f"{d2}.{d1}.{year}")  # DD.MM.YYYY
    return candidates


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False


def extract_valid_dates_from_text(text: str) -> List[str]:
    # Очищаем HTML: <br>, \n, \r, множественные пробелы → один пробел
    cleaned = re.sub(r'(<br\s*/?>|\n|\r|\s{2,})', ' ', text)
    candidates = find_potential_dates(cleaned)
    # ВАЖНО: дубликаты НЕ удаляются — как в тесте
    return [d for d in candidates if is_valid_date(d)]


def extract_valid_dates_from_url(url: str) -> List[str]:
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Python script)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return extract_valid_dates_from_text(response.text)


def extract_valid_dates_from_file(filepath: str) -> List[str]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return extract_valid_dates_from_text(f.read())
