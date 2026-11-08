import csv
from urllib.parse import urlparse
from pathlib import Path

try:
    with open('config.csv', 'r') as file:
        config = {}
        errors = []

        reader = csv.DictReader(file)
        if reader.fieldnames != ['key', 'value']:
            errors.append("Ошибка: некорректный заголовок CSV")

        else: 
            for row in reader:
                if row['key'] in config:
                    errors.append("Ошибка: повторяющийся параметр")
                    continue
                if not row['key'] or not row['key'].strip():
                    errors.append('Ошибка: путой ключ')
                    continue
                if row['value'] is None:
                    errors.append("Ошибка: отсутствует значение")
                    continue
                if None in row:
                    errors.append("Ошибка: лишние столбцы в CSV")
                    continue
                else:
                    config[row['key']] = row['value']
                

            test_mode = config.get('test_mode', '')
            if test_mode not in ('true', 'false'):
                errors.append("Ошибка: некорректный режим работы")

            url = urlparse(config.get('repository', ''))
            if (test_mode == 'false') and (url.scheme not in ('http', 'https') or not url.netloc):
                errors.append("Ошибка: некорректный URL репозитория")

            if not config.get('package', '').strip():
                errors.append("Ошибка: имя пакета не указано")

            if not config.get('repository', '').strip():
                errors.append("Ошибка: имя репозитория не указано")

            if test_mode == 'true' and not Path(config.get('repository', '')).is_file():
                errors.append("Ошибка: тестовый файл не найден")

            if not config.get('version', '').strip():
                errors.append("Ошибка: имя версии пакета  не указано")

            if 'filter' not in config:
                errors.append("Ошибка: параметр filter отсутствует")

        if errors:
            for error in errors:
                print(error)
        else:
            for key, value in config.items():
                print(key, value)

except FileNotFoundError:
    print("Ошибка: файл не найден(((")