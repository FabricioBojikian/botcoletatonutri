import requests
import json
import time

from actions.coleta_log_error import log_error
from actions.coleta_salvar_nota import salvar_nota
from actions.coleta_resposta import enviar_ativacao

get_url = "http://tinywebdb.appinventor.mit.edu/getvalue"
data = {"tag": "datametria.io_codigo_barras"}
old_n_oc = None
flag_n_oc = False
falha_salvar_contador = 0  # Contador para as tentativas de falha

def main():
    global old_n_oc
    global falha_salvar_contador

    print("---------------------------------------------------------------------------")
    print("Ativando Bot para o aplicativo...")
    print(" ")

    enviar_ativacao()

    print("Aplicativo notificado!")
    print("---------------------------------------------------------------------------")
    print("Coletando codigos de barras...")
    print(" ")

    while True:
        try:
            response = requests.post(get_url, data=data)

            if response.status_code == 200:
                try:
                    json_data = json.loads(response.text)
                    texto_limpo = json_data[2].replace('\'"', '').replace('"\'', '').replace('\\', '')
                    texto_limpo = texto_limpo[1:-1]
                    json_valido = json.loads(texto_limpo)

                    if old_n_oc != json_valido['OC']:
                        if old_n_oc is not None:
                            print("---------------------------------------------------------------------------")
                            print("Salvando NF no banco de dados...")
                            print(" ")

                            falha_salvar = salvar_nota(json_valido['NF'], json_valido['OC'], json_valido['BOLETOS'])

                            if falha_salvar:
                                old_n_oc = None
                                falha_salvar_contador += 1
                                print("Nota não processada!")
                                print(" ")

                                if falha_salvar_contador >= 3:
                                    print("Erro ao salvar notas, favor verificar!")
                                    break

                            else:
                                falha_salvar_contador = 0
                        
                        old_n_oc = json_valido['OC']

                    print("Aguardando leitura do aplicativo...")
                    print(f" - Ultima OC: {json_valido['OC']}")
                    print(" ")

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

if __name__ == "__main__":
    main()
