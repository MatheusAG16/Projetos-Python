import requests
from bs4 import BeautifulSoup
import pandas as pd

produto = input("Digite o item a ser buscado: ")

url = f"https://lista.mercadolivre.com.br/{produto}"

# Cabeçalho para simular um navegador e evitar bloqueios
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)

nome_arquivo = "ListaDeProdutos.xlsx"

if response.status_code == 200:

    dadosDosProdutos = []

    soup = BeautifulSoup(response.text, "html.parser")

    itemPesquisado = soup.find("ol", class_="ui-search-layout")

    listaDeProdutos = []

    listaDeProdutos = itemPesquisado.find_all("li", class_="ui-search-layout__item")

    for item in listaDeProdutos:

        imgTag = item.find("img")
        tituloItem = imgTag["title"] if imgTag and imgTag.has_attr("title") else "N/A"

        preco = item.find("span", class_="andes-money-amount__fraction").text

        link = item.find("a", class_="poly-component__title")["href"]

        dadosDosProdutos.append({
            'Titulo': tituloItem,
            'preco': preco,
            'link': link
        })
        print(tituloItem)
        print(f'R${preco}')
        print(link)
        print("=" * 15)

    print(f"Encontramos {len(listaDeProdutos)} itens nesta página!")

    if itemPesquisado:
        print("Pesquisa concluida, items salvos!")
    else:
        print("Algum erro foi encontrado, tente novamente")

    print("Planilha salva com sucesso")
else:
    print("Big foda")