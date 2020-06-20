from pathlib import Path

import pandas as pd
import pandas.testing as pd_tm
import pytest

from pydi.models import StringFrame

DATA_FILENAME = './data/ipps_drg_top_100_fy2011.csv'
SCHEMA_FILENAME = './data/ipps_drg_top_100_fy2011.xlsx'


@pytest.fixture()
def _initialize_string_frame_with_test_data():
    dr = StringFrame(Path(DATA_FILENAME),
                     Path(SCHEMA_FILENAME),
                     file_type='csv')
    return dr


def test__data_reader__init_filename_as_path():
    """
    Given: filename as a Path
    When: initializing StringFrame
    Then: return StringFrame
    """
    dr = StringFrame(filename=Path(DATA_FILENAME),
                     schema_filename=Path(SCHEMA_FILENAME))

    assert dr.filename.name == 'ipps_drg_top_100_fy2011.csv'
    assert dr.schema_filename.name == 'ipps_drg_top_100_fy2011.xlsx'
    assert dr.file_type == 'csv'
    assert dr.data is None


# noinspection PyTypeChecker
def test__data_reader__init_filename_as_str_returns_typeerror():
    """
    Given: filename as a string.
    When: initializing StringFrame
    Then: raise TypeError
    """

    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        StringFrame(DATA_FILENAME,
                    schema_filename=Path(SCHEMA_FILENAME))


def test__data_reader__init_schema_filename_as_str_returns_typeerror():
    """
    Given: filename as a string.
    When: initializing StringFrame
    Then: raise TypeError
    """

    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        StringFrame(Path(DATA_FILENAME),
                    schema_filename=SCHEMA_FILENAME)


def test__data_reader__init_filename_with_file_that_does_not_exist():
    """
    Given: filename as a string.
    When: initializing StringFrame
    Then: raise TypeError
    """

    with pytest.raises(FileNotFoundError):
        StringFrame(Path(DATA_FILENAME) / '.unknown',
                    schema_filename=Path(SCHEMA_FILENAME))


def test__data_reader__init_file_type_as_csv():
    """
    Given: file_type set to 'csv'.
    When: initializing StringFrame
    Then: file_type shall be set to 'csv'
    """
    dr = StringFrame(Path(DATA_FILENAME),
                     schema_filename=Path(SCHEMA_FILENAME),
                     file_type='csv')

    assert dr.filename.name == 'ipps_drg_top_100_fy2011.csv'
    assert dr.schema_filename.name == 'ipps_drg_top_100_fy2011.xlsx'
    assert dr.file_type == 'csv'
    assert dr.data is None


def test__data_reader__init_schema_not_xlsx():
    """
    Given: schema is not a xlsx file.
    When: initializing StringFrame
    Then: return ValueError
    """

    with pytest.raises(ValueError):
        StringFrame(Path(DATA_FILENAME),
                    schema_filename=Path(DATA_FILENAME),
                    file_type='csv')


def test__data_reader__init_schema_filename_with_file_that_does_not_exist():
    """
    Given: schema is not a xlsx file.
    When: initializing StringFrame
    Then: return ValueError
    """

    with pytest.raises(FileNotFoundError):
        StringFrame(Path(DATA_FILENAME),
                    schema_filename=Path('../data/does_not_exist.xlsx'),
                    file_type='csv')


def test__data_reader__init_file_type_as_unknown_file_type():
    """
    Given: file_type set to unknown type.
    When: initializing StringFrame
    Then: then ValueError shall be returned
    """

    with pytest.raises(ValueError):
        StringFrame(Path(DATA_FILENAME),
                    schema_filename=Path(SCHEMA_FILENAME),
                    file_type='unknown')


def test__read_string_frame_only_first_10_rows(_initialize_string_frame_with_test_data):
    dr = _initialize_string_frame_with_test_data
    dr.read(**{'nrows': 10})

    assert isinstance(dr.data, pd.DataFrame)
    assert dr.data.shape == (10, 12)


def test__read_string_frame_as_string_regardless_of_dtype(_initialize_string_frame_with_test_data):
    """
    Given: A test data set
    When: Users explicitly sets dtypes.
    Then: Ignore dtypes and return only strings.

    """
    dr = _initialize_string_frame_with_test_data
    dr.read(**{'nrows': 10, 'dtype': int})

    assert len(dr.data.select_dtypes(object).columns) == 12
    assert dr.data.shape == (10, 12)


def test__read_schema_from_xlsx(_initialize_string_frame_with_test_data):
    dr = _initialize_string_frame_with_test_data

    expected = pd.Index(['column_name',
                         'data_field',
                         'description',
                         'data_type'])

    assert isinstance(dr.schema, pd.DataFrame)
    pd_tm.assert_index_equal(dr.schema.columns, expected)


def test__read_data(_initialize_string_frame_with_test_data):
    dr = _initialize_string_frame_with_test_data
    dr.read()

    expected = pd.Index(['drg_definition',
                         'provider_id',
                         'provider_name',
                         'provider_street_address',
                         'provider_city',
                         'provider_state',
                         'provider_zip_code',
                         'hospital_referral_region_description',
                         'total_discharges',
                         'average_covered_charges',
                         'average_medicare_payments',
                         'average_medicare_payments_2',
                         ])

    pd_tm.assert_index_equal(dr.data.columns, expected)
