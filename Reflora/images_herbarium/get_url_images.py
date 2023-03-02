# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


i = 1
for page in range(1, 263):
    parameters = {
        "quantidadeResultado": "100",
        "apenasComImagens": "on",
        "d-16544-p": str(page),
        "d-16544-t": "testemunhos",
        "modoConsulta": "LISTAGEM",
        "herbarioOrigem": "mbml"
    }
    url = f'https://reflora.jbrj.gov.br/reflora/herbarioVirtual/ConsultaPublicoHVUC/BemVindoConsultaPublicaHVConsultar.do'
    r = requests.get(url=url, params=parameters)
    soup = BeautifulSoup(r.content, "html.parser")
    table = soup.find('table', {'id': 'row'}).tbody
    lines = table.find_all("tr")

    for line in lines:

        # codigoBarra
        codigo = line.find('div', {'class': "codigoBarra"}).text

        # url image
        img = line.find('img', {"class": "miniatura"})
        try:
            url_image = img.get('onclick').replace("criarPopUp('", "https://reflora.jbrj.gov.br").replace("')", "")
        except AttributeError:
            url_image = ''

        # save
        tsv_final = f'{codigo}\t{url_image}\n'
        with open('output.tsv', 'a') as saida:
            saida.write(tsv_final)

        print(f'{i}')
        i += 1
