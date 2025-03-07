import unittest
import re

from main import Painting, Sculpture, remove_artwork, process_file_line


class TestArtWorks(unittest.TestCase):

    def test_add_painting(self):
        painting = Painting('Звёздная ночь', 1889, 'Ван Гог')
        self.assertEqual(painting.title, 'Звёздная ночь')
        self.assertEqual(painting.year, 1889)
        self.assertEqual(painting.artist, 'Ван Гог')

    def test_add_sculpture(self):
        sculpture = Sculpture('Давид', 1504, 'Мрамор')
        self.assertEqual(sculpture.title, 'Давид')
        self.assertEqual(sculpture.year, 1504)
        self.assertEqual(sculpture.material, 'Мрамор')

    def test_remove_artwork(self):
        paintings = [Painting('Мона Лиза', 1503, 'Да Винчи')]
        sculptures = [Sculpture('Дискобол', 450, 'Мрамор')]

        paintings, sculptures = remove_artwork('Мрамор', paintings, sculptures)

        # Проверяем, что скульптура была удалена
        self.assertEqual(len(sculptures), 0)
        self.assertEqual(len(paintings), 1)

    def test_process_file_line_add_painting(self):
        line = 'ADD Картина "Звёздная ночь" 1889 Ван Гог'
        paintings = []
        sculptures = []

        paintings, sculptures = process_file_line(line, paintings, sculptures)

        self.assertEqual(len(paintings), 1)
        self.assertEqual(paintings[0].title, 'Звёздная ночь')
        self.assertEqual(paintings[0].year, 1889)
        self.assertEqual(paintings[0].artist, 'Ван Гог')

    def test_process_file_line_add_sculpture(self):
        line = 'ADD Скульптура "Давид" 1504 Мрамор'
        paintings = []
        sculptures = []

        paintings, sculptures = process_file_line(line, paintings, sculptures)

        self.assertEqual(len(sculptures), 1)
        self.assertEqual(sculptures[0].title, 'Давид')
        self.assertEqual(sculptures[0].year, 1504)
        self.assertEqual(sculptures[0].material, 'Мрамор')

    def test_process_file_line_invalid_data(self):
        line = 'ADD Картина "Звёздная ночь" 1889'
        paintings = []
        sculptures = []

        paintings, sculptures = process_file_line(line, paintings, sculptures)

        # Проверяем, что картины не добавлены
        self.assertEqual(len(paintings), 0)
        self.assertEqual(len(sculptures), 0)

    def test_process_file_line_remove_artwork(self):
        paintings = [Painting('Мона Лиза', 1503, 'Да Винчи')]
        sculptures = [Sculpture('Дискобол', 450, 'Мрамор')]

        line = 'REM Мрамор'
        paintings, sculptures = process_file_line(line, paintings, sculptures)

        self.assertEqual(len(sculptures), 0)
        self.assertEqual(len(paintings), 1)

    def test_process_file_line_unknown_command(self):
        line = 'UNKNOWN Команда'
        paintings = []
        sculptures = []

        paintings, sculptures = process_file_line(line, paintings, sculptures)

        # Проверяем, что картины и скульптуры не изменились
        self.assertEqual(len(paintings), 0)
        self.assertEqual(len(sculptures), 0)


if __name__ == '__main__':
    unittest.main()


# Обновленная версия функции process_file_line с исправлением для правильного разбора строки:
def process_file_line(line, paintings, sculptures):
    print(f"Обрабатываем строку: {line}")

    # Используем регулярные выражения для извлечения данных
    pattern = r'ADD (Картина|Скульптура) "(.*?)" (\d{4}) (.*)'
    match = re.match(pattern, line)

    if match:
        type_of_artwork, title, year, artist_or_material = match.groups()
        print(f"Тип: {type_of_artwork}, Название: {title}, Год: {year}, Автор/Материал: {artist_or_material}")

        if type_of_artwork == 'Картина':
            paintings.append(Painting(title, int(year), artist_or_material))
            print(f"Добавлена картина: {title} {year} {artist_or_material}")

        elif type_of_artwork == 'Скульптура':
            sculptures.append(Sculpture(title, int(year), artist_or_material))
            print(f"Добавлена скульптура: {title} {year} {artist_or_material}")
    elif line.startswith('REM'):
        material = line.split(' ')[1]
        paintings, sculptures = remove_artwork(material, paintings, sculptures)
        print(f"Удаление произведений искусства с материалом: {material}")

    return paintings, sculptures
