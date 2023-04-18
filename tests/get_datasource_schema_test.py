from unittest import TestCase
from autogpt.commands.get_datasource_schema import get_datasource_schema

class TestGetDatasourceSchema(TestCase):
    """
    Test get data source schema command
    """

    def setUp(self):
        pass

    def test_get_datasource_schema(self):
        """
        Test if get_datasource_schema works, all necessary inputs should already be in local file.
        """

        print(get_datasource_schema())

