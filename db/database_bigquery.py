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
            "private_key_id": "c88c00a13bfa63d9601c4e08c0ec06a720f4b80a",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCizH4h5GpweLHZ\nnHVycIvznSIbgZPffQRQYtts/9LknoFMVQLwEW76PnG5eB00EdotF1UbYl6EUKE9\ng318ca8WxgnbDFNm15f+FxaJ04OD6JHXUkS1uiWDhFK2VvTiGqVw2rzm102koEMr\nvsvIlAs5rXsu4x9uIkOMw3PaJ+5Xt561Y3/nbh1t0Yvx2+H0lI8ukAfRrBU/sfoG\ncbZnqirZSLHUdwSh6VBduzZGjxd6jEXlBrtt1SGCWkZqDHg/4vVGqs47l9jkh7qK\nRkgiu2xtPZbKvKbYEQ78Ry9TNcOopgay0oeHam7l4svrMxUEja/sOzfEIMxsQrzX\ntvB7gpv9AgMBAAECggEAAebZGjOPsQ6UztLtaurbRdPW+DLACfgeUjSxH0cdAMMT\nQL/UGIiurbMlbS5+rXRO20VMPJBPkwmUZYnBHGaezkIvIueqYPsiwnERS9WR+WJ2\n2poInfvrzxx1ViBXYcJ7is/9ytlQo3TL98W9FDi4DBTc6Y8c95xaeM+GT/lIcP0r\nTDEyLGEi4NWO15iAtlAhDXizo2s7rRRplHslJjHym4pT5G6eL07ZB49uS/6FZHP2\n/GK+73ZX6PBCSfGMC5qIsj7FpwqABr2VQabGkvZ4k7N1ihe4KlEfMZ7MEO0k32wl\ngAlMAVt3N9u9CPTitGquEThYiOSlS3YfvrbQXYOvdwKBgQDjJ5AS92CjgAA5vruf\n1HplP+fAGtDUvafGGMNpE7dMRZUHprjGKHMh2asplXMaYQ1GZ4Vcsfvlke7Zrd/8\nGrvnKEqdSAuOwyJMXCFWrip/X22Ur9e/zpLi++yfkCkEKsY9DudqDlol1Aqr1mUM\nMvOrZlC/3rTj5bfldGtPTT2jQwKBgQC3eNNrR3S6ngXnDdRJrBIyPtae2K9+FcwL\nENhQdIToprTYQ1v1hoE4Kq2yeHqBECRzXgIa5ivVC9JT1SP8y7ClTCVmF3GX2MI/\n+BddFlSok0+6fXPBH5HBeBs8S76OMtlYK4rMIFuF9iSiDfasSPcjJy83Nwq+hiUk\n3aLaSjmvvwKBgAWLsbjE0VcsiNTgEzSTu2k9ZisKfI61EqODd0HZeWAjUsAdEeXE\nlwr8hXE+dNDwDaLqZBcfQUcZiPtHg3BkNrIuCaRNXfreSLgUh7vWBLOXYNWAdYP5\nRxzDicNbgaTYZn6XHo84Snsh8iC/2zexBsHofZAxn7jwosy3Sudku1yBAoGBAI1q\n6XMwUc4iTaRp6W6b3i6ydtVbafGCtZL1+fYRyfxVuuFTEkeu1F1JsDb3XF2s5puy\nI2c+cRy3DvilOib5jf/rMIx/l4QWhKuv+7o5oymI2pSBbD64qa15eWzBaXDLyvGG\nJmburf0U2+m5X6AuYafL5T3nBDYUyf6fg45EVjCbAoGAacF1RrxE3EkiNf24nSHt\nAOMoXXl3VdTjtxFB5W9g18NpnXGoFI/rUu6kOmTuqi4ZoTybhWw9ZeOzhZbXRodX\nhJLpRYR1vyCWCm49fTTSp2fQYAHrAZPwDSeo6mZDFd+WjeO6W5MaHOG4RLqDEnAB\nXnNJ39UJa6DqzlzC8ltRUG8=\n-----END PRIVATE KEY-----\n",
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
