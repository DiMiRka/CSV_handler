import argparse
import csv
import re
import sys
from tabulate import tabulate


def read_csv(file_path) -> list:
    with open(file_path, mode='r', encoding='utf-8') as file:
        read = csv.DictReader(file)
        return list(read)


def parse_filter(condition: str) -> tuple:
    match = re.match(r'^(\w+)([><=])(.+)$', condition)
    if not match:
        raise ValueError(f"Invalid condition format: {condition}")
    return match.groups()


def csv_filter(data: list, column: str, operator: str, value: str) -> list:
    filtered = []
    for row in data:
        cell_value = row[column]

        cell_value_num = 0
        value_num = 0
        try:
            cell_value_num = float(cell_value)
            value_num = float(value)
            use_numeric = True
        except (ValueError, TypeError):
            use_numeric = False

        if operator == '=':
            if use_numeric:
                if cell_value_num == value_num:
                    filtered.append(row)
            else:
                if cell_value == value:
                    filtered.append(row)
        elif operator == '>':
            if use_numeric and cell_value_num > value_num:
                filtered.append(row)
        elif operator == '<':
            if use_numeric and cell_value_num < value_num:
                filtered.append(row)
    return filtered


def parse_aggregate(aggregate):
    match = re.match(r'^(\w+)=(avg|min|max)$', aggregate)
    if not match:
        raise ValueError(f"Invalid aggregate format: {aggregate}")
    return match.groups()


def csv_aggregate(data, column, func):
    values = []
    for row in data:
        try:
            values.append(float(row[column]))
        except (ValueError, TypeError):
            continue

    if not values:
        return None

    if func == 'min':
        return min(values)
    elif func == 'max':
        return max(values)
    else:
        return sum(values) / len(values)


def main():
    parser = argparse.ArgumentParser(description='Обработка CSV-файла')
    parser.add_argument('--file', required=True, help='Путь к CSV-файлу')
    parser.add_argument('--where', help='Фильтрация в формате название колонки оператор значение (пример: rating>4.7')
    parser.add_argument('--aggregate', help='Агрегация в формате название колонки=агрегатор (пример: price=avg')
    args = parser.parse_args()

    try:
        data = read_csv(args.file)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        sys.exit(1)

    filtered_data = data
    if args.where:
        try:
            column, operator, value = parse_filter(args.where)
            filtered_data = csv_filter(data, column, operator, value)
        except Exception as e:
            print(f"Ошибка фильтрации: {e}")
            sys.exit(1)

    if args.aggregate:
        try:
            column, func = parse_aggregate(args.aggregate)
            result = csv_aggregate(filtered_data, column, func)
            print(tabulate([[func], [result]], tablefmt='grid'))
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка агрегации: {e}")
            sys.exit(1)

    if filtered_data:
        print(tabulate(filtered_data, headers='keys', tablefmt='grid'))
    else:
        print("Нет данных для отображения")


if __name__ == '__main__':
    main()
