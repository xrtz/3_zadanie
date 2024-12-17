import xml.etree.ElementTree as ET
import math
import sys
from xml.dom import minidom


def eval_expression(expr, context):
    """Оценивает выражение, подставляя значения из контекста."""
    if expr.startswith('@(') and expr.endswith(')'):
        expr = expr[2:-1]  # Убираем @( и )
        expr = expr.replace('sqrt', 'math.sqrt').replace('pow', 'math.pow')
        try:
            result = eval(expr, {"math": math}, context)  # Оцениваем выражение
            return result
        except Exception as e:
            raise ValueError(f"Ошибка в выражении: {expr} -> {e}")
    return None


def parse_value(value, context):
    """Парсит значение (число, строку, массив или выражение)."""
    if value.startswith("@(") and value.endswith(")"):
        return eval_expression(value, context)
    elif value.isdigit():
        return int(value)  # Число
    elif value.startswith("{") and value.endswith("}"):
        return process_array(value, context)  # Массив
    else:
        try:
            return float(value)  # Число с плавающей точкой
        except ValueError:
            return value.strip("'")  # Строка, если не число


def process_array(array_str, context):
    """Обрабатывает массив, вычисляет значения и возвращает их список."""
    array_str = array_str[1:-1].strip()  # Убираем фигурные скобки {}
    elements = []  # Массив для хранения элементов

    # Переменная для хранения текущего элемента, который может быть вложенным массивом
    current_element = ""
    depth = 0  # Глубина вложенности массивов

    for char in array_str:
        if char == '{':
            depth += 1
            current_element += char
        elif char == '}':
            depth -= 1
            current_element += char
        elif char == ',' and depth == 0:
            # Разделяем элементы массива на уровне текущей глубины
            elements.append(parse_value(current_element.strip(), context))
            current_element = ""
        else:
            current_element += char

    # Добавляем последний элемент массива
    if current_element.strip():
        elements.append(parse_value(current_element.strip(), context))

    return elements


def parse_input(input_lines):
    """Парсит строки конфигурации, если встречается нужный массив."""
    context = {}  # Контекст для хранения значений переменных
    target_array = None  # Будет хранить массив, если он найден

    for line in input_lines:
        line = line.strip()
        if not line:
            continue

        if "->" in line:
            # Пример: значение -> имя;
            value, name = line.split("->")
            name = name.strip().rstrip(';')
            value = value.strip().rstrip(';')
            parsed_value = parse_value(value, context)
            context[name] = parsed_value

        elif line.startswith("{") and line.endswith("}"):
            # Если строка - массив
            target_array = process_array(line, context)

    return target_array, context


def generate_xml(array):
    """Генерирует XML из массива значений."""
    root = ET.Element("values")
    for value in array:
        value_element = ET.SubElement(root, "value")
        if isinstance(value, list):
            # Если значение - это вложенный массив, рекурсивно создаем для него XML
            value_element.append(generate_xml(value))
        else:
            value_element.text = str(value)
    return root


def pretty_print_xml(root):
    """Функция для красивого форматирования XML с отступами."""
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")  # Отступы в 4 пробела


def main(output_file):
    # Чтение входных данных с клавиатуры (стандартный ввод)
    print("Введите конфигурации (для завершения ввода нажмите Ctrl+D):")
    input_lines = []

    try:
        while True:
            line = input()  # Считываем строку
            input_lines.append(line)
    except EOFError:
        pass  # Завершаем, когда достигаем конца ввода (Ctrl+D)

    # Парсинг входных данных
    target_array, context = parse_input(input_lines)
    if target_array is None:
        print("Целевой массив не найден во входных данных.")
        return

    # Генерация XML
    root = generate_xml(target_array)
    formatted_xml = pretty_print_xml(root)

    # Запись в файл с кодировкой utf-8
    with open(output_file, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(formatted_xml[formatted_xml.find('\n') + 1:])  # Убираем лишний заголовок

    print(f"Результат записан в {output_file}")


if __name__ == "__main__":
    output_file = sys.argv[1]  # Путь к выходному файлу
    main(output_file)
