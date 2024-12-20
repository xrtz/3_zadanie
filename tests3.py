import unittest
from xml.etree.ElementTree import tostring
from io import StringIO
from xml.dom import minidom
from config import eval_expression, parse_value, process_array, parse_input, generate_xml


class TestXMLGenerator(unittest.TestCase):
    def test_eval_expression(self):
        """Тест корректной обработки математических выражений."""
        context = {"x": 4, "y": 2}
        self.assertEqual(eval_expression("@(sqrt(x))", context), 2.0)
        self.assertEqual(eval_expression("@(pow(x, y))", context), 16)
        self.assertEqual(eval_expression("@(x + y)", context), 6)

    def test_parse_value(self):
        """Тест парсинга значений (числа, строки, массивов, выражений)."""
        context = {"a": 9}
        self.assertEqual(parse_value("@(sqrt(a))", context), 3.0)  # Выражение
        self.assertEqual(parse_value("123", context), 123)         # Число
        self.assertEqual(parse_value("'text'", context), "text")   # Строка
        self.assertEqual(parse_value("{1, 2, 3}", context), [1, 2, 3])  # Массив

    def test_process_array(self):
        """Тест обработки массива с вложенностью и выражениями."""
        context = {"x": 4, "y": 16}
        array = "{1, @(sqrt(x)), {2, @(sqrt(y))}}"
        result = process_array(array, context)
        self.assertEqual(result, [1, 2.0, [2, 4.0]])

    def test_parse_input(self):
        """Тест парсинга конфигурации на основе строк."""
        input_lines = [
            "4 -> x;",
            "@(sqrt(x)) -> result;",
            "{1, @(x), @(result)}"
        ]
        target_array, context = parse_input(input_lines)
        self.assertEqual(context["x"], 4)
        self.assertEqual(context["result"], 2.0)
        self.assertEqual(target_array, [1, 4, 2.0])

    def test_generate_xml(self):
        """Тест генерации XML из простого массива."""
        test_array = [1, 2, 3]
        xml_root = generate_xml(test_array)
        xml_string = tostring(xml_root, 'utf-8').decode()
        self.assertIn("<array>", xml_string)
        self.assertIn("<value>1</value>", xml_string)
        self.assertIn("<value>2</value>", xml_string)
        self.assertIn("<value>3</value>", xml_string)

    def test_generate_xml_with_nested_array(self):
        """Тест генерации XML с вложенными массивами."""
        test_array = [1, [2, 3], 4]
        xml_root = generate_xml(test_array)
        xml_string = tostring(xml_root, 'utf-8').decode()
        self.assertIn("<value>1</value>", xml_string)
        self.assertIn("<value>4</value>", xml_string)
        self.assertIn("<array>", xml_string)  # Проверка вложенности

    def test_no_target_array(self):
        """Тест на случай отсутствия целевого массива."""
        input_lines = [
            "4 -> x;",
            "@(sqrt(x)) -> result;"
        ]
        target_array, context = parse_input(input_lines)
        self.assertIsNone(target_array)

    def test_invalid_expression(self):
        """Тест некорректного выражения, вызывающего ошибку."""
        context = {"x": 4}
        with self.assertRaises(ValueError):
            eval_expression("@(undefined_function(x))", context)


if __name__ == "__main__":
    unittest.main()
