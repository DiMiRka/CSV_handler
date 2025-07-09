import csv
import re
from statistics import median


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
    match = re.match(r'^(\w+)=(avg|min|max|median)$', aggregate)
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
    elif func == 'median':
        return median(values)
    elif func == 'avg':
        return sum(values) / len(values)
    return None


def parse_order_by(order_by_str):
    match = re.match(r'^(\w+)=(asc|desc)$', order_by_str)
    if not match:
        raise ValueError(f"Некорректный формат сортировки: {order_by_str}")
    return match.groups()


def csv_order_by(data, column, direction='asc'):
    def get_sort_key(row):
        value = row.get(column, '')
        try:
            return float(value)
        except (ValueError, TypeError):
            return str(value).lower()

    reverse = (direction == 'desc')

    return sorted(data, key=get_sort_key, reverse=reverse)
