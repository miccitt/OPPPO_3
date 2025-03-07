# Базовый класс для всех произведений искусства
class ArtWork:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f'"{self.title}", {self.year}'


# Класс для картин
class Painting(ArtWork):
    def __init__(self, title, year, artist):
        super().__init__(title, year)
        self.artist = artist

    def __str__(self):
        return super().__str__() + f', {self.artist}'


# Класс для скульптур
class Sculpture(ArtWork):
    def __init__(self, title, year, material):
        super().__init__(title, year)
        self.material = material

    def __str__(self):
        return super().__str__() + f', {self.material}'


# Удаление произведений по художнику или материалу
def remove_artwork(identifier, paintings, sculptures):
    paintings = [p for p in paintings if p.artist != identifier]
    sculptures = [s for s in sculptures if s.material != identifier]

    print(f'Удаляем: {identifier}\n')
    return paintings, sculptures


# Вывод картин
def print_paintings(paintings):
    print('Картины:')
    for p in paintings:
        print('   ', p)


# Вывод скульптур
def print_sculptures(sculptures):
    print('Скульптуры:')
    for s in sculptures:
        print('   ', s)


# Вывод всех произведений
def print_all(paintings, sculptures):
    print('\n--- Все произведения ---')
    if paintings:
        print_paintings(paintings)
    else:
        print('   Нет картин')

    if sculptures:
        print_sculptures(sculptures)
    else:
        print('   Нет скульптур')


# Основная функция программы
def main():
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
            parts = line.strip().split(' ', 2)
            if not parts:
                continue

            cmd = parts[0]

            if cmd == 'PRINT':
                print_all(paintings, sculptures)

            elif cmd == 'ADD':
                if len(parts) < 3:
                    print('Ошибка добавления:', line)
                    continue

                item_type, data = parts[1], parts[2]

                try:
                    # Парсим данные, учитывая кавычки в названии
                    first_quote = data.find('"')
                    last_quote = data.rfind('"')
                    if first_quote == -1 or last_quote == -1 or first_quote == last_quote:
                        print('Ошибка данных (кавычки):', data)
                        continue

                    title = data[first_quote + 1:last_quote]
                    remaining = data[last_quote + 1:].strip().split(' ', 1)
                    year = int(remaining[0])
                    info = remaining[1] if len(remaining) > 1 else ''

                except (ValueError, IndexError):
                    print('Ошибка данных:', data)
                    continue

                if item_type == 'Картина':
                    paintings.append(Painting(title, year, info))
                elif item_type == 'Скульптура':
                    sculptures.append(Sculpture(title, year, info))
                else:
                    print('Неизвестный тип:', item_type)

            elif cmd == 'REM':
                if len(parts) < 2:
                    print('Ошибка удаления:', line)
                    continue

                paintings, sculptures = remove_artwork(parts[1], paintings, sculptures)

            else:
                print('Неизвестная команда:', line)

    except FileNotFoundError:
        print('Файл не найден!')


if __name__ == "__main__":
    main()
