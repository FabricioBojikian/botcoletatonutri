from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from db.database_bigquery import DatabaseBigQuery
from actions.coleta_log_error import log_error

def coleta_verificar_oc(n_oc):
    try:
        db = DatabaseBigQuery().get_client()
        query = f"""
                SELECT COUNT(*)
                FROM `datametria.PLANUS.notas_tonutri`
                WHERE n_oc = '{n_oc}';
        """
        requisicao = db.query(query)
        df = requisicao.result().to_dataframe()
        count = df.iloc[0, 0]

        return count > 0
    
    except Exception as e:
        error_message = f"Erro ao buscar OC: {n_oc} no banco de dados: {str(e)}"
        print(error_message)
        log_error(error_message)
        
        return False
