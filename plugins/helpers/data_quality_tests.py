import logging


class DataQualityTest:
    """Test cases for data quality"""

    def __init__(self, sql, validation, table=None):
        """
        Description: Initialize test case

        Arguments:
        * sql: SQL statement to execute
        * validation: Validation method for query results
        * table: Table name
        """
        self.sql = sql
        self.validation = validation
        self.table = table
        self.records = None

    def validate(self):
        return self.validation(self.records, self.table)

    @staticmethod
    def no_results_validation(records, table=None):
        """
        Description: Validate non-empty table and return "True" if DQ test passed

        Arguments:
        * records: Query results
        * table: Table name
        """
        if len(records) < 1 or len(records[0]) < 1:
            raise ValueError(f'Error: Table {table} returns no results')
        n_records = records[0][0]
        if n_records < 1:
            raise ValueError(f'Error: Table {table} contains 0 records')
        logging.info(f'Passed: Table {table} contains {n_records} records')
        return True

    @staticmethod
    def no_results_test(table):
        """
        Description: Create test case to verify that table is not empty and return DataQualityTest

        Arguments:
        * table: Table name
        """
        return DataQualityTest(
            sql=f'SELECT count(*) FROM {table}',
            validation=DataQualityTest.no_results_validation,
            table=table,
        )