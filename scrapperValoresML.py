import requests
from bs4 import BeautifulSoup
import pandas as pd

#url = "https://produto.mercadolivre.com.br/MLB-2907647003-parafuso-sextavado-flangeado-m8-x-12mm-10-pecas-_JM"

#url = "https://produto.mercadolivre.com.br/MLB-3782577805-placa-me-galaxy-s20-plus-g985f-100-original-retirado-128gb-_JM#polycard_client=recommendations_vip-v2p&reco_backend=recomm-platform_ranker_v2p_coldstart&reco_model=rk_ent_v5_retsys_org&reco_client=vip-v2p&reco_item_pos=0&reco_backend_type=low_level&reco_id=406d1dd5-9575-4452-a2b9-86e197dceffb&wid=MLB3782577805&sid=recos"

url = "https://produto.mercadolivre.com.br/MLB-3782577805-placa-me-galaxy-s20-plus-g985f-100-original-retirado-128gb-_JM#polycard_client=recommendations_vip-v2p&reco_backend=recomm-platform_ranker_v2p_coldstart&reco_model=rk_ent_v5_retsys_org&reco_client=vip-v2p&reco_item_pos=0&reco_backend_type=low_level&reco_id=406d1dd5-9575-4452-a2b9-86e197dceffb&wid=MLB3782577805&sid=recos"

response = requests.get(url)

nome_arquivo = "Informacoes_ML.xlsx"

if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1", class_="ui-pdp-title").text
    valor = soup.find("span", class_="andes-money-amount__fraction").text
    quantidade = soup.find("span", class_="ui-pdp-buybox__quantity__available").text
    #Aqui pra pegar o nome do vendedor:
    div_vendedor = soup.find("button", class_="ui-pdp-seller__link-trigger-button non-selectable")
    vendedor = div_vendedor.find_all("span")[1].text
    descricao = soup.find("p", class_="ui-pdp-description__content").text

    df_novo_dado = pd.DataFrame({"Titulo": [title], "Valor": ["R$" + valor], "Quantidade": [quantidade], "Vendedor": [vendedor], "Descrição": [descricao]})

    try:
        #Tentando abrir o arquivo existente
        df_existente = pd.read_excel(nome_arquivo, engine="openpyxl")

        #adicionando a nova linha ao DataFrame
        df_final = pd.concat([df_existente, df_novo_dado], ignore_index=True)
    except FileNotFoundError:
        #Se o arquivo não existir, cria um novo DataFrame
        df_final = df_novo_dado

    #Criando um DataFrame
    #df = pd.DataFrame(obj_tudo)

    df_final.to_excel("Informacoes_ML.xlsx", index=False, engine="openpyxl")

    print("Planilha salva com sucesso")
else:
    print("Big foda")