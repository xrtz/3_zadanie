# Задание №3 Индивидуальный вариант №18
Постановка задачи
Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной.

Входной текст из стандартного ввода. Выходной текст на учебном конфигурационном языке попадает в xml файл, путь к которому задан ключом командной строки.

Массивы:
{<значение>, <значение>..., <значение>}

Имена:
[a-zA-Z][a-zA-Z0-9]*

Значения:
• Числа.

• Строки.

• Массивы.

Строки:
'Hello'

Объявление константы на этапе трансляции:
значение -> имя

Вычисление константного выражения на этапе трансляции, пример:
@(имя + 1)

Результатом вычисления константного выражения является значение.

Для константных вычислений определены операции и функции:
Сложение.

Вычитание.

Умножение.

pow(). 

sqrt().

# Описание функций 

eval_expression(expr, context) - Выполняет вычисление выражения, используя значения из контекста. Поддерживает математические функции, такие как sqrt и pow. Если выражение некорректно, выбрасывает ошибку.

parse_value(value, context) - Обрабатывает переданное значение, определяя его тип. Может быть числом, строкой, массивом или выражением, которое требует вычисления.

process_array(array_str, context) - Парсит строку, представляющую массив. Рекурсивно обрабатывает вложенные массивы и вычисляет значения, возвращая их в виде списка.

parse_input(input_lines) - Разбирает входные строки конфигурации, определяет переменные и массивы. Возвращает найденный массив и словарь контекста с переменными.

generate_xml(array) - Рекурсивно строит XML-документ из массива значений. Вложенные массивы обрабатываются отдельно, создавая иерархическую структуру.

pretty_print_xml(root) - Форматирует XML-документ с отступами, чтобы сделать его читаемым. Использует minidom для красивого вывода.

main(output_file) - Считывает входные данные из стандартного ввода, парсит их для нахождения массива, генерирует XML-файл и записывает его в указанный файл. 

# Запуск программы 

python config.py <выходной xml файл> 

# Тесты 


