from pathlib import Path

import pandas as pd
import pytest
from numpy import array

from pydi import goof


@pytest.fixture
def _load_fake_data_set():
    return pd.DataFrame({'Email Id': {0: 'Javier.Carter@testDomain.com', 1: 'Michelle.Snyder@testDomain.com'},
                  'Prefix': {0: 'Dr.', 1: 'Mrs.'}, 'Name': {0: 'Amanda Kim', 1: 'James Martinez'},
                  'Birth Date': {0: '14-04-1971', 1: '22-03-1990'}, 'SSN': {0: '324-16-0447', 1: '766-70-2680'},
                  'Phone Number': {0: '+1-594-822-0151', 1: '+1-015-776-6485x57871'},
                  'Address': {0: '5768 Timothy Springs Suite 067\nLake Lisa, KS 85356',
                              1: '8717 Michael Stravenue\nSouth Hannahtown, KS 07095'},
                  'Zip Code': {0: '12974', 1: '55033'}, 'City': {0: 'South George', 1: 'North Tiffanyville'},
                  'State': {0: 'Colorado', 1: 'Mississippi'}, 'Country': {0: 'Turks and Caicos Islands', 1: 'Guyana'},
                  'Number of Children': {0: array([4]), 1: array([0])},
                  'Annual Salary': {0: array([498700.22074111]), 1: array([885093.78932159])}})


def test__generate_fake_data_set__correct_headers():
    fake_data = goof.generate_fake_data_set(1)
    assert set(fake_data.columns) == set(goof.DATA_HEADERS)


@pytest.mark.parametrize('n_records',
                         [1, 2, 5])
def test__generate_fake_data__correct_number_of_records(n_records):
    fake_data = goof.generate_fake_data_set(n_records)
    assert len(fake_data) == n_records


def test__generate_fake_data__two_identical_data_sets_with_same_seed():
    fake_data_1 = goof.generate_fake_data_set(1, seed=0)
    fake_data_2 = goof.generate_fake_data_set(1, seed=0)

    assert fake_data_1.equals(fake_data_2)


def test__generate_fake_data__two_different_data_sets_with_different_seeds():
    fake_data_1 = goof.generate_fake_data_set(1, seed=123)
    fake_data_2 = goof.generate_fake_data_set(1, seed=42)

    assert not fake_data_1.equals(fake_data_2)


def test__generate_fake_data__correct_number_of_records():

    with pytest.raises(ValueError):
        goof.generate_fake_data_set(-1)


def test__write_full_data_set_to_file(_load_fake_data_set, tmpdir):
    fake_data = _load_fake_data_set
    # print(fake_data.to_dict())
    output_filename = Path(tmpdir) / 'test_output_file.csv'
    goof.write_to_csv_file(fake_data, output_filename)

    assert output_filename.exists()
