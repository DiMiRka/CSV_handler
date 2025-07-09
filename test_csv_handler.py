import csv
import pytest

from main import read_csv, parse_filter, csv_filter


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
