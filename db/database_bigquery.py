import sys
import os
from google.oauth2 import service_account
from google.cloud import bigquery
import pandas as pd
import pandas_gbq
sys.path.insert(0, os.path.abspath(os.curdir))
from config.system import *
from db.database_interface import DatabaseInterface

TABLE_NAME = "notas_tonutri"
PROJECT_ID = "datametria"
DATASET_ID = "PLANUS"

class DatabaseBigQuery(DatabaseInterface):

    def __init__(self):
        self.credencial = self.get_credential()
        self.client = self.get_client()

    def __str__(self) -> str:
        return f"BigQuery: {PROJECT_ID}.{DATASET_ID}"

    def get_credential(self):
        # return service_account.Credentials.from_service_account_file(BIGQUERY_JSON)
        service = service_account.Credentials.from_service_account_info(
            {
                "type": "service_account",
                "project_id": "datametria",
                "private_key_id": "f4a2b3649a823e54767c7e09cb93de089afad633",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC7neIEPj7rMmX4\n7yVzTHmebGaN6NOv2WqjQIkLEXEchfd4JB/JTOxSwO7BTQxLE/E4Lp7BIxwzlslI\nA5dogrjNg0dqa8DjpU8IdClcNgZxEOItfq3ldWMY3EI7v4ReSv/kk08trwHCtIxi\n34na4SuryEXIspTqiZO8FKF5zdWPi3ybMgsiLE03GiwkoYOylExvO8BqWbseT+TF\nRbggAVtls5a1rY0GvzbQyJvjmifz9BV7UYMG4xjNn9EAYzqhoHevs+E7MBbyKvht\ncP7ga+hAtK6p9SBRcH60xvI2ZxURYGfkKI20ZD9YPpqGauMuNNCsdrCNe8KTzF22\nhgqZeK/FAgMBAAECggEAB7cTX0dMARH+fYEgEiC385rTkMxdQCL5rqLtv8XE1/5u\nUcNyhy2hnjmO1+YaNlAooD3Si3CtLTXrKwnyxPpzLQhT/H1X3kSi/l8AgGk8VJP0\nKRjHf+MW4yPTmW9juxjscvLX07IZqW8RQtOccKLHz/WZYQpu80IbECXtCfw75v4s\nOszEs1u7NQv65w3Y9E4nLmAEa7T3kckv6odVAkCLiMexk+poE9rAF2l3GHwdvxHq\nCDiYkJAaWJD4GbqDEUPiRlMiVLfbL8rt2BW9ARDM4+biOWscc+jh58TM2KQPWLeY\nTOUFn8qrsyUqomzreyD9ftbFl/Yww6HEGoUmiUUgdQKBgQD8LRPWzYGK3EcEae7S\nXb3Icra8MuwpVN1WpqJ2L5lVHfUHHqUAEFzTeeiwYfVv0EjzadHzJWQjpoMzPYTe\nvjSP9WFgcWJArTxwnPiETBeR0oqsQzjikr3sMPf/cBhnXlztyCEL1U2uykuzlgRj\nKfzEGanhmqc0b8Si/NjfSEEj0wKBgQC+djFAAKd5zY5KrsDAIqwy0GzQMBOul7IJ\niiTGHFWd2sSziJim9xDL0FCgLvs736/3yN2figqB9eBsfV9H3dJZUSDzXHOzJ/LW\n8LZPL/FcibueQJy3bRGUo0c+QBgnsEOwZc52riPREhf4K8/aibssCBaTOYYectJ2\n+EBN8uxXBwKBgQCMMTtARYto+UD58TJ1/OtPDocMZXrpF2bdj1HuRlQF/9uCk8TD\nHlWcs79qn2rlOHP17rRrajQbpax2xhKiCjgKeC4kgaRPtH9PU9TNJ8hKpzO0xMJR\nI6c2MZsNhPHsNYeQIZxNic3gCFLBifrybhs5odLRuzqNaj11JwAiUXb1RQKBgFXc\n4L0Szm2Z3qEKgTjdKLZLwhJk6iqWlpu4XHW3hl2Ap5asaO00iqznf8GHDJnkcOcK\n9eabi7slBoTCTHcQqGi9q1YrArnss4x0viua2Hu4WA2y4TPMBtX0egS1Tm5uB0X5\nz4cvYFQ7jPTDg5Po7amfB9ZdY3pMl1cs+YhqkGN3AoGBAJZ3pvb62sdGfGSac4Mz\nYOoEzr0ugFHR79gDYf8RYk0E7dUl6/g0rXRgg3qqfb7P5modRNGN4CoHR2u/v02U\nev+klFK6Z8NtUeyTUGl5ny9P4Ed/qBP6+3yGGzcov2JKzsPJt5unGv2dUbqciP8R\nTc1mOtNl0BLs8usOSKkffB1X\n-----END PRIVATE KEY-----\n",
                "client_email": "datametria@datametria.iam.gserviceaccount.com",
                "client_id": "103699222612549853078",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/datametria%40datametria.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
        )

        return service

    def get_client(self):
        return bigquery.Client(credentials=self.credencial, project=PROJECT_ID)

    def data_load(self, dataframe:pd.DataFrame, destination_table: str, replace: bool = False) -> None:
        pandas_gbq.to_gbq(
            dataframe=dataframe,
            destination_table=DATASET_ID + "." + destination_table,
            credentials=self.credencial,
            project_id=PROJECT_ID,
            if_exists=("replace" if replace else "append"),
        )
