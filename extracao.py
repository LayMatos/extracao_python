import requests
from bs4 import BeautifulSoup
import csv

# URL de login e URL da página de dados
login_url = "https://coneq.pm.mt.gov.br/api/login"
data_url = "https://coneq.pm.mt.gov.br/termo_cautela"

# Dados de login (CPF e senha)
login_data = {
    "cpf": "02046925122",
    "pswdHash": "64173c05e168682f34caa13c3400631b"  # Verifique o hash correto para sua senha
}

# Nome do arquivo CSV onde os dados serão salvos
csv_filename = "dados_extraidos.csv"

# Criando uma sessão para manter a conexão
with requests.Session() as session:
    # Enviando a requisição de login
    login_response = session.post(login_url, json=login_data)

    # Verificando se o login foi bem-sucedido e imprimindo a resposta
    if login_response.status_code == 200:
        response_data = login_response.json()

        # Imprimindo a resposta completa para verificar a estrutura do JSON
        print("Resposta de login:", response_data)
        
        # Verificando se o token está na resposta (ajustar conforme a resposta)
        if "data" in response_data and "token" in response_data["data"]:
            # Extraindo o token JWT
            token = response_data["data"]["token"]
            print("Token JWT obtido com sucesso!")

            # Configurando os cabeçalhos com o token de autenticação
            headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            }
            
            # Acessando a página de dados protegida
            data_response = session.get(data_url, headers=headers)

            # Verificando se o acesso à página de dados foi bem-sucedido
            if data_response.status_code == 200:
                # Analisando o conteúdo da página
                soup = BeautifulSoup(data_response.content, "html.parser")
                
                # Extraindo dados (ajuste conforme a estrutura HTML da página)
                table_data = soup.find("table")  # Localize a tabela desejada
                if table_data:
                    rows = table_data.find_all("tr")
                    
                    # Salvando os dados no arquivo CSV
                    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        
                        # Iterando sobre cada linha da tabela para extrair dados
                        for row in rows:
                            columns = row.find_all("td")
                            data = [column.get_text(strip=True) for column in columns]
                            writer.writerow(data)  # Escrevendo cada linha de dados no CSV
                        
                    print(f"Dados extraídos e salvos em {csv_filename}")
                else:
                    print("Tabela de dados não encontrada.")
            else:
                print("Falha ao acessar a página de dados.")
        else:
            print("Token não encontrado na resposta de login.")
    else:
        print("Falha no login.")
