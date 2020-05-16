from pathlib import Path
import pandas as pd


class StringFrame:
    """
    StringFrame reads a CSV file with
    """

    def __init__(self,
                 filename: Path,
                 schema_filename: Path,
                 file_type: str = 'csv'):

        self._check_filename(filename)
        self._check_schema_filename(schema_filename)
        self._check_file_type(file_type)

        self.filename = filename
        self.file_type = file_type

        self.schema_filename = schema_filename

        self.schema = None
        self.data = None

        self.read_schema()

    @staticmethod
    def _check_file_type(file_type):
        if not (file_type in ['csv']):
            raise ValueError

    @staticmethod
    def _check_filename(filename):
        if not isinstance(filename, Path):
            raise TypeError

        if not filename.exists():
            raise FileNotFoundError

    @staticmethod
    def _check_schema_filename(schema_filename):
        if not isinstance(schema_filename, Path):
            raise TypeError

        if not (schema_filename.suffix == '.xlsx'):
            raise ValueError

        if not schema_filename.exists():
            raise FileNotFoundError

    def read_schema(self):
        """
        Read Schema from XLSX file.

        :return:
        """
        self.schema = pd.read_excel(self.schema_filename, sheet_name='schema')

    def read(self, **kwargs):

        print(kwargs)
        if self.file_type == 'csv':
            self._read_csv_as_strings(**kwargs)

    def _read_csv_as_strings(self, **kwargs):

        kwargs['dtype'] = str
        self.data = pd.read_csv(self.filename, **kwargs)
        self.data.columns = self.schema.data_field.tolist()
