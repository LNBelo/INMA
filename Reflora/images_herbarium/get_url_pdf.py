# -*- coding: utf-8 -*-
import re
import time
import requests
from bs4 import BeautifulSoup


i = 1
for page in range(1, 263):
    base_url = f'https://reflora.jbrj.gov.br/reflora/herbarioVirtual/ConsultaPublicoHVUC' \
               f'/BemVindoConsultaPublicaHVConsultar.do'
    parameters = {
        "quantidadeResultado": "100",
        "apenasComImagens": "on",
        "d-16544-p": str(page),
        "d-16544-t": "testemunhos",
        "modoConsulta": "LISTAGEM",
        "herbarioOrigem": "mbml"
    }
    error = True
    while error:
        try:
            response = requests.get(url=base_url, params=parameters)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                table = soup.find('table', {'id': 'row'}).tbody
                lines = table.find_all("tr")

                for line in lines:
                    # codigoBarra
                    codigo = line.find('div', {'class': "codigoBarra"}).text

                    # idFigura
                    img = line.find('img', {"class": "miniatura"})
                    try:
                        idFigura = img.get('onclick')
                        idFigura = re.search(r"\?idFigura=(\d+)'\)", idFigura).group(1)
                    except AttributeError:
                        idFigura = ''

                    # idTestemunho
                    a = line.find('a')
                    try:
                        idTestemunho = a.get('onclick')
                        idTestemunho = re.search(r"recuperarDadosTestemunho\((\d+)\)", idTestemunho).group(1)
                    except AttributeError:
                        idTestemunho = ''

                    # url_pdf
                    if idFigura and idTestemunho != '':
                        url_pdf = f'https://reflora.jbrj.gov.br/reflora/herbarioVirtual/ConsultaPublicoHVUC' \
                                  f'/ResultadoDaConsultaRelatorioFigura.do?idFigura={idFigura}&' \
                                  f'idTestemunho={idTestemunho} '
                    else:
                        url_pdf = ''

                    # save
                    tsv_final = f'{codigo}\t{idFigura}\t{idTestemunho}\t{url_pdf}\n'
                    with open('output.tsv', 'a') as saida:
                        saida.write(tsv_final)

                    print(f'{i}')
                    i += 1
                error = False
            else:
                print(f"response status {response.status_code}")
                time.sleep(5)
        except requests.exceptions.HTTPError as errh:
            print(f"Error HTTP: {errh}")
            time.sleep(5)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error connection: {errc}")
            time.sleep(5)
        except requests.exceptions.Timeout as errt:
            print(f"Error timeout: {errt}")
            time.sleep(5)
        except requests.exceptions.RequestException as err:
            print(f"Error request: {err}")
            time.sleep(5)
