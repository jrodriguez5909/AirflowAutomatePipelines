from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 tests=[],
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tests = tests

    def execute(self, context):
        self.log.info('DataQualityOperator Starting....')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        for test in self.tests:
            self.log.info(f'Get records for query: "{test.sql}"')
            test.records = redshift_hook.get_records(test.sql)
            result = test.validate()