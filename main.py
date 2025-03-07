"""
Модуль для работы с произведениями искусства, включая картины и скульптуры.
Предоставляет функциональность для добавления, удаления и вывода произведений.
"""

class ArtWork:
    """
    Базовый класс для всех произведений искусства.
    """

    def __init__(self, title, year):
        """
        Инициализация произведения искусства.

        :param title: Название произведения.
        :param year: Год создания произведения.
        """
        self.title = title
        self.year = year

    def __str__(self):
        """
        Строковое представление произведения искусства.

        :return: Строка с названием и годом создания.
        """
        return f'"{self.title}", {self.year}'


class Painting(ArtWork):
    """
    Класс для картин, наследующий от ArtWork.
    """

    def __init__(self, title, year, artist):
        """
        Инициализация картины.

        :param title: Название картины.
        :param year: Год создания картины.
        :param artist: Художник, создавший картину.
        """
        super().__init__(title, year)
        self.artist = artist

    def __str__(self):
        """
        Строковое представление картины.

        :return: Строка с названием, годом и художником.
        """
        return super().__str__() + f', {self.artist}'


class Sculpture(ArtWork):
    """
    Класс для скульптур, наследующий от ArtWork.
    """

    def __init__(self, title, year, material):
        """
        Инициализация скульптуры.

        :param title: Название скульптуры.
        :param year: Год создания скульптуры.
        :param material: Материал, из которого сделана скульптура.
        """
        super().__init__(title, year)
        self.material = material

    def __str__(self):
        """
        Строковое представление скульптуры.

        :return: Строка с названием, годом и материалом.
        """
        return super().__str__() + f', {self.material}'


def remove_artwork(identifier, paintings, sculptures):
    """
    Удаляет произведения искусства по имени художника или материалу.

    :param identifier: Имя художника или материал, по которому происходит удаление.
    :param paintings: Список картин.
    :param sculptures: Список скульптур.
    :return: Обновленные списки картин и скульптур.
    """
    paintings = [p for p in paintings if p.artist != identifier]
    sculptures = [s for s in sculptures if s.material != identifier]

    print(f'Удаляем: {identifier}\n')
    return paintings, sculptures


def print_paintings(paintings):
    """
    Выводит все картины.

    :param paintings: Список картин.
    """
    print('Картины:')
    for p in paintings:
        print(f'   {p}')


def print_sculptures(sculptures):
    """
    Выводит все скульптуры.

    :param sculptures: Список скульптур.
    """
    print('Скульптуры:')
    for s in sculptures:
        print(f'   {s}')


def print_all(paintings, sculptures):
    """
    Выводит все произведения искусства: картины и скульптуры.

    :param paintings: Список картин.
    :param sculptures: Список скульптур.
    """
    print('\n--- Все произведения ---')
    if paintings:
        print_paintings(paintings)
    else:
        print('   Нет картин')

    if sculptures:
        print_sculptures(sculptures)
    else:
        print('   Нет скульптур')


def process_file_line(line, paintings, sculptures):
    """
    Обрабатывает строку файла с командой.

    :param line: Строка с командой.
    :param paintings: Список картин.
    :param sculptures: Список скульптур.
    :return: Обновленные списки картин и скульптур.
    """
    parts = line.strip().split(' ', 2)
    if not parts:
        return paintings, sculptures

    cmd = parts[0]

    if cmd == 'PRINT':
        print_all(paintings, sculptures)

    elif cmd == 'ADD':
        if len(parts) < 3:
            print(f'Ошибка добавления: {line}')
            return paintings, sculptures

        item_type, data = parts[1], parts[2]

        try:
            first_quote = data.find('"')
            last_quote = data.rfind('"')
            if first_quote == -1 or last_quote == -1 or first_quote == last_quote:
                print(f'Ошибка данных (кавычки): {data}')
                return paintings, sculptures

            title = data[first_quote + 1:last_quote]
            remaining = data[last_quote + 1:].strip().split(' ', 1)
            year = int(remaining[0])
            info = remaining[1] if len(remaining) > 1 else ''

        except (ValueError, IndexError):
            print(f'Ошибка данных: {data}')
            return paintings, sculptures

        if item_type == 'Картина':
            paintings.append(Painting(title, year, info))
        elif item_type == 'Скульптура':
            sculptures.append(Sculpture(title, year, info))
        else:
            print(f'Неизвестный тип: {item_type}')

    elif cmd == 'REM':
        if len(parts) < 2:
            print(f'Ошибка удаления: {line}')
            return paintings, sculptures

        paintings, sculptures = remove_artwork(parts[1], paintings, sculptures)

    else:
        print(f'Неизвестная команда: {line}')

    return paintings, sculptures


def main():
    """
    Основная функция программы для работы с произведениями искусства.
    """
    paintings = []
    sculptures = []

    paintings.append(Painting('Мона Лиза', 1503, 'Да Винчи'))
    sculptures.append(Sculpture('Дискобол', 450, 'Мрамор'))

    print_all(paintings, sculptures)

    paintings, sculptures = remove_artwork('Мрамор', paintings, sculptures)

    print_all(paintings, sculptures)

    print('\n--- Работа с файлом ---')

    try:
        with open('input-artworks.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()

        for line in lines:
            paintings, sculptures = process_file_line(line, paintings, sculptures)

    except FileNotFoundError:
        print('Файл не найден!')


if __name__ == "__main__":
    main()
