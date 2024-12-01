import pandas as pd
import re

#Функция для заполнения excel файла
def process_excel(input_file, output_file):
    data = pd.ExcelFile(input_file, engine='openpyxl')
    sheet_name = data.sheet_names[0]
    df = data.parse(sheet_name)

    # Функция для разделения текста по маркерам
    def split_text(text):
        if not isinstance(text, str):
            return [text]
        # Паттерн для поиска маркеров
        pattern = r'(?=\b\d+\)|\b[а-я]\)|\b\d+\.\d+)'
        # Разделение текста по найденным маркерам, если мы не нашли следущий патерн, то текст склеивается
        return [part.strip() for part in re.split(pattern, text) if part.strip()]

    # получаем названия начиная с 3 строки, так как есть баги с получением названия начиная с 1
    titles = []
    for i in range(2, len(df), 3):  # Start from row index 2 (3rd row), step by 3
        title = df.iloc[i, 0] if isinstance(df.iloc[i, 0], str) else ''
        titles.append(title)

    # Обрабатываем таблицу
    processed_data = []
    title_index = 0
    for i, row in df.iterrows():
        # Присваиваем соответствующее название для каждой строки
        title = titles[title_index] if i >= 2 and (i - 2) % 3 == 0 else None
        # Если строка является третьей и при этом она >= 2, увеличиваем индекс названия
        if i >= 2 and (i - 2) % 3 == 0:
            title_index += 1

        # Разделяем текст в первом столбце
        split_col1 = split_text(row.iloc[0])
        # Разделяем текст во втором столбце, если он существует
        split_col2 = split_text(row.iloc[1]) if len(row) > 1 else [None]

        # Определяем максимальное количество строк, необходимое для объединения
        max_length = max(len(split_col1), len(split_col2))

        # Дополняем более короткие списки пустыми строками
        split_col1.extend([''] * (max_length - len(split_col1)))
        split_col2.extend([''] * (max_length - len(split_col2)))

        # Объединяем строки
        for part1, part2 in zip(split_col1, split_col2):
            processed_data.append([title, part1, part2])

    # Создаём новую таблицу
    processed_df = pd.DataFrame(processed_data, columns=["Название", df.columns[0], df.columns[1]])

    # Заполняем пропущенные значения в столбце
    processed_df["Название"] = processed_df["Название"].ffill()

    # Сохраняем обработанные данные в новый excel файл
    try:
        processed_df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"Файл успешно сохранён: {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


# пути к исходникам и конечному файлу
input_path = 'final.xlsx'
output_path = 'final_filled.xlsx'

#запуск программы
process_excel(input_path, output_path)
