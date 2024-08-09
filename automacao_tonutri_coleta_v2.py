import requests
import json
import time

from actions.coleta_resposta import *
from actions.coleta_log_error import *
from actions.coleta_salvar_nota import *
from actions.coleta_verificar_oc import *
from actions.coleta_verificar_nota import *

def main():
    get_url = "http://tinywebdb.appinventor.mit.edu/getvalue"
    data = {"tag": "datametria.io_codigo_barras"}
    old_n_oc = None
    ativacao_estado = True

    print("---------------------------------------------------------------------------")
    print("Ativando Bot para o aplicativo...")
    print(" ")

    enviar_ativacao(ativacao_estado)
    print("Aplicativo notificado!")
    print(" ")

    print("---------------------------------------------------------------------------")
    print("Coletando codigos de barras...")
    print(" ")

    try:
        while True:
            try:
                response = requests.post(get_url, data=data)

                if response.status_code == 200:
                    try:
                        json_data = json.loads(response.text)
                        texto_limpo = json_data[2].replace('\'"', '').replace('"\'', '').replace('\\', '')
                        texto_limpo = texto_limpo[1:-1]
                        json_valido = json.loads(texto_limpo)

                        print("Aguardando leitura do aplicativo...")
                        print(f" - OC recebida: {json_valido['OC']}")
                        print(f" - Ultima OC: {old_n_oc}")
                        print(" ")

                        if old_n_oc != json_valido['OC']:
                            if old_n_oc is not None:
                                print("---------------------------------------------------------------------------")
                                print("Conferindo se a nota já foi salva...")
                                print(" ")

                                falha_oc = coleta_verificar_oc(json_valido['OC'])

                                if falha_oc:
                                    print("Nota já salva!")
                                    print(" ")
                                    
                                    enviar_alerta()

                                else:
                                    retorno = verificar_codigo_barras(json_valido['NF'])

                                    if retorno:
                                        print("---------------------------------------------------------------------------")
                                        print("Salvando NF no banco de dados...")
                                        print(" ")

                                        falha_salvar = salvar_nota(json_valido['NF'], json_valido['OC'], json_valido['BOLETOS'])

                                        if falha_salvar:

                                            error_message = f"Erro ao salvar no banco de dados: {str(e)}"
                                            print(error_message)
                                            log_error(error_message)
                                            break

                                    else:
                                        print("Nota com codigo de barras inválido!")
                                        print(" ")
                                        
                                        enviar_alerta()

                            old_n_oc = json_valido['OC']
                            
                        time.sleep(1)

                    except (json.JSONDecodeError, IndexError) as e:
                        error_message = f"Erro no processamento do JSON: {str(e)} - {response.text}"
                        print(error_message)
                        log_error(error_message)

                else:
                    error_message = f"Erro ao fazer a requisição: {response.status_code}"
                    print(error_message)
                    log_error(error_message)

            except requests.ConnectionError:
                print("Sem conexão com a internet, tentando novamente em 5 segundos...")
                time.sleep(5)
                
            except Exception as e:
                error_message = f"Ocorreu um erro inesperado: {str(e)}"
                print(error_message)
                log_error(error_message)

    finally:
        ativacao_estado = False
        enviar_ativacao(ativacao_estado)

if __name__ == "__main__":
    main()
