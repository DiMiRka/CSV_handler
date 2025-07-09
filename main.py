import argparse
import sys
from tabulate import tabulate

from utils import read_csv, parse_filter, csv_filter, parse_aggregate, csv_aggregate, parse_order_by, csv_order_by


def main():
    parser = argparse.ArgumentParser(description='Обработка CSV-файла')
    parser.add_argument('--file', required=True, help='Путь к CSV-файлу')
    parser.add_argument('--where', help='Фильтрация в формате название колонки оператор значение (пример: rating>4.7')
    parser.add_argument('--aggregate', help='Агрегация в формате название колонки=агрегатор (пример: price=avg')
    parser.add_argument('--order-by', help='Сортировка данных: "column=asc" или "column=desc"')
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

    if args.order_by:
        try:
            column, direction = parse_order_by(args.order_by)
            filtered_data = csv_order_by(filtered_data, column, direction)
        except Exception as e:
            print(f"Ошибка сортировки: {e}")
            sys.exit(1)

    if filtered_data:
        print(tabulate(filtered_data, headers='keys', tablefmt='grid'))
    else:
        print("Нет данных для отображения")


if __name__ == '__main__':
    main()
