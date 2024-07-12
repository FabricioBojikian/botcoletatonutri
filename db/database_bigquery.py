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
            "private_key_id": "efcf82aafe2b223282f249dbc46a1c6440d43b3e",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDiQwKO0elWShES\nufCFArHkC1iCT3z8H0U6ED/52imErMlisiou991ML7WBxicJb1+bHLZv9AObSVWS\nn1/RmxPbTFe1OWU6OG3ugk8EiqjyCh8j/GcnnGOv/2z+QyN0v5FaS95BnBSmJMNI\nQz/Rc+f444hCs8tMCnvGx+hv8maYeHVD8MMR+eafeA26GNnN6sMsV3JxN8p7Yu6B\nLyCiR9OJW4Vf7tU19lI209mf1eENCVkc2NbSvMDU5cGdKyZU6Qdmw1smMQKtHPhL\nFHmPTyIaRg4lyzA3VUdVKTpFoLOeLss3RoRlYMggNhNwqY8t8eFYZn237iHts3ib\nS33hzPVpAgMBAAECggEAa5ry3Hl4P1F6TS2g9aESeSHsNg0Xo9A7XCHeSzU2CaMj\nI40YAr5ewJzv9YgHiLUvAtXk7dle3btCtziUmVrnVqQ4Ejf5rHap0YSnj8FiF7o4\nlSS06mG2Bz2y2DmV4zA4MHlkek+AgoN5XCSfdT1qVTPg2dgoF0HlG+R25sahhGDg\ndS+wu0MMUDWJkau9+a25b3d/wMq+M5WmffUzRHxcVCX6UIAU9Ij607TQxxiyxJJ8\ntCr0nXVxT85F3rBfxNP0DDA30vO0FC8KaPyP1INu1EJir8uZ/qF3nI6iPCman5d4\n/kFsY6+SeuHhX5H3Uw8hduwA7VLoP92jHxzNXL3HAQKBgQDzRA5oKz/js5cpPHY5\nAcwGp85VdGOSr0ogp0pgSfvbj2yUNh5ION9WRlkKzD0tDJCw2X7BP+jjIPHaPctg\nr/3dIKqAaOHXE8h09FMfKj8PxSVAtQ4qTcOeOU8jxdETMev8qWKe369NESrSMBBp\nBBoIWiEO9NzZG1LFqXhN0tGzCwKBgQDuGxYVr6HEvAcN9ZNBWB1D5m73uoI43MFU\nQsyxJwS76iT3jK+m1v7wqiy1oMqxIhIkRBPV5hAyStKb1TQngcy8JTU1INQbPQzF\nYCj39GloWO3jGzM3xEisR25WBC6V1YI17qir63FuGBNu+TYitJD6D4HzjDw2ROzD\nyu0bFblB2wKBgQDZ26UbXUBGZ9uELoWh4B4cB8Qde7KA90Lno2pUeW144CVZRm4w\nN96roSy1ItvWsF4UQ3PlFZs3bZWq4ZR17qbnlg2cGlHHEAyB0R1v16HKOcB3Bq68\n7A+4b5KUcuAe1KKHEBsmNSUFW86BllHb+rRlrnHUty3hsTqbkn4PFDKAqQJ/OapV\nruraQstG6hqPj0PH0qn8NgL1hs/wAngrGrxYaSpLyahI4h8vnxmXumU2sa+OtTnH\nlAYj5go494SrHOZSrz5TpIpO1En0zdh8E5Ed9ieTdW0g+mCPOSoTjsF0htUus+EY\n+IoM7pzmF/pDIiSY9/bJgjJ0YrBOpxx+UBDyzQKBgQDYu/kowjsbcBAca7RkFpk9\n9SXXMF6AAWzsm39zX5dvp9Ievtlh6OpxnZIkIbc2uhq/iSOVjoHfbVYw7B6cBZA4\nLTZFHLz75eM9XCrwy9bH9nHr/CB9Z7zGRnI81vp2c80m/98oMJvvAzguqnKz/9Vi\ndBjI6TPDUwJQiDmB5aNxIA==\n-----END PRIVATE KEY-----\n",
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
