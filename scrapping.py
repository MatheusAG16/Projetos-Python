import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.cifraclub.com.br/"

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, "html.parser")

    titles = [title.text for title in soup.find_all("h2")]
    paragrafos = [p.text for p in soup.find_all("p")]

    # Garantindo que as listas tenham o mesmo tamanho
    max_len = max(len(titles), len(paragrafos))
    titles.extend([""] * (max_len - len(titles)))  # Preenche títulos faltantes
    paragrafos.extend([""] * (max_len - len(paragrafos))) # Preenche paragrafos faltantes

    #Criando um DataFrame
    df = pd.DataFrame({"Titulos": titles, "Paragrafos": paragrafos})

    df.to_excel("h2_p_cifra_club.xlsx", index=False, engine="openpyxl")

    print("Planilha salva com sucesso")
else:
    print("Big foda")