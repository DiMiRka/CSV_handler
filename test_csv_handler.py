import csv
import pytest

from utils import read_csv, parse_filter, csv_filter, parse_aggregate, csv_aggregate, parse_order_by, csv_order_by


@pytest.fixture
def data_test(tmp_path):
    data = [
        ['name', 'brand', 'price', 'rating'],
        ['iphone 15 pro', 'apple', '999', '4.9'],
        ['galaxy s23 ultra', 'samsung', '1199', '4.8'],
        ['redmi note 12', 'xiaomi', '199', '4.6'],
        ['poco x5 pro', 'xiaomi', '299', '4.4']
    ]
    file_path = tmp_path / "test.csv"
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return file_path


def test_read_csv(data_test):
    data = read_csv(data_test)
    assert len(data) == 4
    assert data[0] == {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'}


def test_parse_filter():
    assert parse_filter('price>500') == ('price', '>', '500')
    assert parse_filter('brand=apple') == ('brand', '=', 'apple')
    with pytest.raises(ValueError):
        parse_filter('invalid_data')


def test_csv_filter(data_test):
    data = read_csv(data_test)

    filtered = csv_filter(data, 'price', '>', '500')
    assert len(filtered) == 2
    assert {row['name'] for row in filtered} == {'iphone 15 pro', 'galaxy s23 ultra'}

    filtered = csv_filter(data, 'brand', '=', 'xiaomi')
    assert len(filtered) == 2
    assert {row['name'] for row in filtered} == {'redmi note 12', 'poco x5 pro'}


def test_parse_aggregate():
    assert parse_aggregate("rating=avg") == ('rating', 'avg')
    assert parse_aggregate("price=min") == ('price', 'min')
    with pytest.raises(ValueError):
        parse_aggregate('invalid_data')


def test_csv_aggregate(data_test):
    data = read_csv(data_test)

    assert csv_aggregate(data, 'price', 'avg') == 674.0
    assert csv_aggregate(data, 'rating', 'min') == 4.4
    assert csv_aggregate(data, 'price', 'median') == 649.0

    filtered = csv_filter(data, 'brand', '=', 'xiaomi')
    assert csv_aggregate(filtered, 'price', 'max') == 299.0


def test_parse_order_by():
    assert parse_order_by('price=desc') == ('price', 'desc')
    assert parse_order_by('brand=asc') == ('brand', 'asc')
    with pytest.raises(ValueError):
        parse_aggregate('invalid_data')


def test_csv_order_by(data_test):
    data = read_csv(data_test)

    sorted_asc = csv_order_by(data, 'price', 'asc')
    prices = [float(row['price']) for row in sorted_asc]
    assert prices == [199.0, 299.0, 999.0, 1199.0]

    sorted_desc = csv_order_by(data, 'rating', 'desc')
    ratings = [float(row['rating']) for row in sorted_desc]
    assert ratings == [4.9, 4.8, 4.6, 4.4]

    sorted_brand = csv_order_by(data, 'brand', 'asc')
    brands = [row['brand'] for row in sorted_brand]
    assert brands == ['apple', 'samsung', 'xiaomi', 'xiaomi']
