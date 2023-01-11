from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id = "",
                 target_db = "",
                 destination_table = "",
                 sql = "",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.target_db = target_db
        self.destination_table = destination_table
        self.sql = sql

    def execute(self, context):
        self.log.info('LoadFactOperator starting...')
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        sql = f"\nINSERT INTO {self.destination_table} ({self.sql})"
        self.log.info(f"Loading data: {self.target_db}.{self.destination_table} table")
        self.log.info(f"Running SQL: {sql}")
        redshift.run(sql)
        self.log.info("*** LoadFactOperator: Complete ***\n")