import datetime
import json
import requests
import oracledb

def previsao_chuva(cidade):
    api_key = "82dc917aa83b073b74ba1298d6906b63"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        clima = dados.get("weather", [{}])[0].get("main", "").lower()
        descricao = dados.get("weather", [{}])[0].get("description", "")
        chuva = dados.get("rain", {}).get("1h", 0)

        print(f"Cidade: {dados.get('name')}")
        print(f"Clima atual: {descricao.capitalize()}")

        if clima == "rain" or chuva >= 2:
            print("Hoje há previsão de fortes chuvas. Fique em casa e tome cuidado ao sair na rua.")
            print()
        else:
            print("Sem previsão de fortes chuvas por enquanto.")
            print()
    else:
        print(f"Erro ao obter dados do clima para {cidade}.")

def localizacao_atual():
    permissao = input("Você deseja permitir o uso de sua localização atual? (SIM|NAO): ").lower().strip()
    if permissao == 'sim':
        print("Acesso permitido, em caso de extremo risco, localização será enviada à defesa civil.")
        print()
    else:
        print("Acesso negado.")
        print()

def cadastrar_localizacao():
    try:
        print("----- CADASTRAR ENDEREÇO -----\n")

        NOME_LOCAL = input("Nome do local (ex: CASA | TRABALHO): ")
        RUA_LOCAL = input("Rua: ")
        NUMERO_LOCAL = int(input("Número: "))
        CEP_LOCAL = int(input("CEP (OPCIONAL): "))

        script = """INSERT INTO T_SOS_LOCALIZACAO 
                    (NOME_LOCAL, RUA_LOCAL, NUMERO_LOCAL, CEP_LOCAL) 
                    VALUES (:1, :2, :3, :4)"""

        cursor.execute(script, (NOME_LOCAL, RUA_LOCAL, NUMERO_LOCAL, CEP_LOCAL))
        conn.commit()

        print("\nLocalização registrada com sucesso.")
        print()
    except ValueError:
        print("O Número da casa deve ser um número inteiro!")
    except Exception as error:
        print(f"Erro na transação com o banco de dados: {error}")

def exibir_localizacoes():
    try:
        print("----- MINHAS LOCALIZAÇÕES-----\n")

        script = f"""SELECT * FROM T_SOS_LOCALIZACAO ORDER BY ID_LOCAL"""
        cursor.execute(script)
        lista_dados = cursor.fetchall()

        if len(lista_dados) == 0:
            print(f"Não há dados cadastrados!")
        else:
            for item in lista_dados:
                print(item)
                print()
    except Exception as error:
         print(f"Erro na transação com o banco de dados: {error}")

def exibir_orientacoes():
    try:
        print("----- ORIENTAÇÕES E CUIDADOS -----\n")
        print("(1) - Inundação | (2) - Deslizamento | (3) Tempestades, Raios e Granizos")

        evento_id = int(input("Deseja ver orientações de qual evento? "))
        if evento_id in [1, 2, 3]:
            script = """
                SELECT 
                    NOME_EVENTO, DESCRICAO, 
                    TXT_PREVENCAO, TXT_DURANTE, TXT_APOS 
                FROM T_SOS_EVENTOS 
                WHERE ID_EVENTO = :1
            """
            cursor.execute(script, [evento_id])
            dados = cursor.fetchone()

            if dados is None:
                print("Não há dados cadastrados para este evento.")
            else:
                nome_evento, descricao, prevencao, durante, apos = dados
                print(f"\n Evento: {nome_evento}")
                print(f"\n Descrição:\n{descricao}")
                print(f"\n Antes do evento:\n{prevencao}")
                print(f"\n Durante o evento:\n{durante}")
                print(f"\n Após o evento:\n{apos}")
                print()
        else:
            print("Escolha um evento válido!")
    except Exception as error:
        print(f"Erro na transação com o banco de dados: {error}")


def enviar_sms():
    try:
        print("----- ENVIAR SMS -----\n")

        MENSAGEM = input("Mensagem: ")
        DATA_ENVIO = datetime.date.today()

        script = """INSERT INTO T_SOS_SMS_ENVIADO 
                    (MENSAGEM, DATA_ENVIO) 
                    VALUES (:1, :2)"""

        cursor.execute(script, (MENSAGEM, DATA_ENVIO))
        conn.commit()

        print("\nSMS enviado com sucesso.")
        print()
    except Exception as error:
        print(f"Erro na transação com o banco de dados: {error}")

def buscar_local_por_nome():
    try:
        nome = input("Digite o nome do local (ex: CASA, TRABALHO): ").upper().strip()
        script = "SELECT * FROM T_SOS_LOCALIZACAO WHERE UPPER(NOME_LOCAL) = UPPER(:1)"
        cursor.execute(script, (nome,))
        resultados = cursor.fetchall()

        if resultados:
            with open("localizacoes_por_nome.json", "w", encoding="utf-8") as f:
                json.dump([dict(zip([col[0] for col in cursor.description], row)) for row in resultados], f, indent=4, ensure_ascii=False)
            print("Resultados exportados para 'localizacoes_por_nome.json'.\n")
        else:
            print("Nenhum resultado encontrado.\n")
    except Exception as error:
        print(f"Erro ao buscar localizações: {error}")


def buscar_evento_por_id():
    try:
        evento_id = int(input("Digite o ID do evento (1 a 3): "))
        script = "SELECT * FROM T_SOS_EVENTOS WHERE ID_EVENTO = :1"
        cursor.execute(script, (evento_id,))
        resultados = cursor.fetchall()

        if resultados:
            with open("eventos_filtrados.json", "w", encoding="utf-8") as f:
                json.dump([dict(zip([col[0] for col in cursor.description], row)) for row in resultados], f, indent=4, ensure_ascii=False)
            print("Resultados exportados para 'eventos_filtrados.json'.\n")
        else:
            print("Nenhum resultado encontrado.\n")
    except Exception as error:
        print(f"Erro ao buscar eventos: {error}")

def buscar_sms_por_data():
    try:
        data = input("Digite a data de envio (formato: YYYY-MM-DD): ")
        data_formatada = datetime.datetime.strptime(data, "%Y-%m-%d").date()

        script = "SELECT * FROM T_SOS_SMS_ENVIADO WHERE TRUNC(DATA_ENVIO) = :1"
        cursor.execute(script, (data_formatada,))
        resultados = cursor.fetchall()

        if resultados:
            colunas = [col[0] for col in cursor.description]
            dados_formatados = []
            for row in resultados:
                item = dict(zip(colunas, row))
                # Converte o campo DATA_ENVIO para string
                if 'DATA_ENVIO' in item and isinstance(item['DATA_ENVIO'], datetime.datetime):
                    item['DATA_ENVIO'] = item['DATA_ENVIO'].strftime("%Y-%m-%d")
                elif 'DATA_ENVIO' in item and isinstance(item['DATA_ENVIO'], datetime.date):
                    item['DATA_ENVIO'] = item['DATA_ENVIO'].isoformat()
                dados_formatados.append(item)

            with open("sms_por_data.json", "w", encoding="utf-8") as f:
                json.dump(dados_formatados, f, indent=4, ensure_ascii=False)

            print("Resultados exportados para 'sms_por_data.json'.\n")
        else:
            print("Nenhum SMS enviado nesta data.\n")

    except ValueError:
        print("Formato de data inválido! Use o formato YYYY-MM-DD.")
    except Exception as error:
        print(f"Erro ao buscar SMS: {error}")

def alterar_localizacao():
    try:
        print("----- ALTERAR DADOS LOCALIZAÇÃO -----\n")

        nome_local = input("Digite o nome do local (ex: CASA, TRABALHO): ").upper().strip()
        script = "SELECT * FROM T_SOS_LOCALIZACAO WHERE UPPER(NOME_LOCAL) = :1"
        cursor.execute(script, (nome_local,))
        lista_dados = cursor.fetchall()

        if len(lista_dados) == 0:
            print(f"Não há dados cadastrados com o NOME = {nome_local}")
        else:
            print("Informe os novos dados para atualização:")
            novo_nome = input("Novo nome do local (ex: CASA | TRABALHO): ")
            rua = input("Nova rua: ")
            numero = int(input("Novo número: "))
            cep = input("Novo CEP (opcional): ")

            update_script = """
                UPDATE T_SOS_LOCALIZACAO
                SET NOME_LOCAL = :1,
                    RUA_LOCAL = :2,
                    NUMERO_LOCAL = :3,
                    CEP_LOCAL = :4
                WHERE UPPER(NOME_LOCAL) = :5
            """
            cursor.execute(update_script, (novo_nome, rua, numero, cep, nome_local))
            conn.commit()

            print("\nLocalização alterada com sucesso!\n")

    except ValueError:
        print("O número da casa deve ser um valor inteiro.")
    except Exception as error:
        print(f"Erro na transação do BD: {error}")


def excluir_localizacao():
    try:
        print("----- EXCLUIR LOCALIZAÇÃO CADASTRADA -----\n")

        nome_local = input("Digite o nome do local (ex: CASA, TRABALHO): ").upper().strip()
        script = "SELECT * FROM T_SOS_LOCALIZACAO WHERE UPPER(NOME_LOCAL) = :1"

        cursor.execute(script, (nome_local,))
        lista_dados = cursor.fetchall()

        if len(lista_dados) == 0:
            print(f"Não há dados cadastrados com o NOME = {nome_local}")
        else:
            confirmar = input(f"Confirma exclusão do local '{nome_local}'? (SIM/NAO): ").lower().strip()
            if confirmar == 'sim':
                delete_script = "DELETE FROM T_SOS_LOCALIZACAO WHERE UPPER(NOME_LOCAL) = :1"
                cursor.execute(delete_script, (nome_local,))
                conn.commit()
                print("\nLocalização excluída com sucesso.\n")
            else:
                print("Exclusão cancelada.\n")

    except Exception as error:
        print(f"Alerta na transação do BD: {error}")

# Menu principal
login = input("Usuário..: ")
senha = input("Senha....: ")
try:
    conn = oracledb.connect(user=login,
                            password=senha,
                            host="oracle.fiap.com.br",
                            port=1521,
                            service_name="ORCL")
    cursor = conn.cursor()

    while True:
        print("SOS LOCALIZA")
        print("1 - Permitir uso de localização atual.")
        print("2 - Cadastrar localização (CEP / Endereço).")
        print("3 - Consultar minhas localizações.")
        print("4 - Alterar localização.")
        print("5 - Excluir localização.")
        print("6 - Verificar previsão do clima.")
        print("7 - Visualizar orientações e cuidados para eventos adversos.")
        print("8 - Está em área de risco? Enviar SMS de emergência.")
        print("9 - Buscar localizações por nome.")
        print("10 - Buscar eventos por ID.")
        print("11 - Buscar SMS por data.")
        print("12 - Sair.")

        escolha = int(input("Escolha uma opção: "))

        match escolha:
            case 1:
                localizacao_atual()
            case 2:
                cadastrar_localizacao()
            case 3:
                exibir_localizacoes()
            case 4:
                alterar_localizacao()
            case 5:
                excluir_localizacao()
            case 6:
                cidade = input("Digite o nome da cidade para verificar a previsão: ")
                previsao_chuva(cidade)
            case 7:
                 exibir_orientacoes()
            case 8:
                 enviar_sms()
            case 9:
                 buscar_local_por_nome()
            case 10:
                buscar_evento_por_id()
            case 11:
                buscar_sms_por_data()
            case 12:
                print('Programa finalizado.')
                conn.close()
                break
            case _:
                print('Opção inválida.')
except Exception as erro:
    print(f"Erro: {erro}")

