# -*- coding: utf-8 -*-
"""
source: https://servicos.jbrj.gov.br/flora/

Script que faz consultas a API do Reflora

Na url altere para o tipo desejado de consulta

As linhas do arquivo input.txt será o parâmetro variável da url

get_genus = True
Para o caso expecífico GET /genus/{family} , o resultado será armazenado no arquivo output.tsv

get_genus = False
Caso deseje obter gêneros de outras formas, por exemplo: GET /taxon/{scientificname}
"""

import json
import time
import requests
import pandas as pd
from requests import exceptions

with open('input.txt') as txt:
    lines = txt.readlines()

get_genus = False
if get_genus:
    tsv_final = ''
else:
    df_final = pd.DataFrame()

i = 1
for line in lines:
    line = line.replace('\n', '')

    loop = True
    while loop:
        try:
            url = f'https://servicos.jbrj.gov.br/flora/taxon/{line}'
            r = requests.get(url)
            loop = False
        except exceptions.HTTPError as errh:
            print("Http Error:", errh)
            time.sleep(3)
        except exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            time.sleep(3)
        except exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            time.sleep(3)
        except exceptions.RequestException as err:
            print("Request Exception", err)
            time.sleep(3)

    payload = r.content
    payload = payload.decode()
    payload = payload.replace("Conectado com: 10.10.100.29<br/> ", "")

    # dict
    data = json.loads(payload)

    # list
    result_list = data["result"]

    try:
        length = len(result_list)
    except TypeError:
        length = 1

    for n in range(length):

        if get_genus:
            try:
                genus = data["result"][n]
                tsv_final += f"{line}\t{genus}\n"
            except TypeError:
                tsv_final += f"{line}\tnull\n"

        else:
            try:
                data_temp = {
                    "taxonid": str(data["result"][n]["taxonid"]),
                    "family": str(data["result"][n]["family"]),
                    "genus": str(data["result"][n]["genus"]),
                    "scientificname": str(data["result"][n]["scientificname"]),
                    "specificepithet": str(data["result"][n]["specificepithet"]),
                    "infraspecificepithet": str(data["result"][n]["infraspecificepithet"]),
                    "scientificnameauthorship": str(data["result"][n]["scientificnameauthorship"]),
                    "taxonomicstatus": str(data["result"][n]["taxonomicstatus"]),
                    "acceptednameusage": str(data["result"][n]["acceptednameusage"]),
                    "higherclassification": str(data["result"][n]["higherclassification"]),
                    "source": str(data["result"][n]["source"]),
                    "references": str(data["result"][n]["references"])
                    # "acceptednameusageid": str(data["result"][n]["acceptednameusageid"]),
                    # "modified": str(data["result"][n]["modified"])
                }
            except TypeError:
                data_temp = {
                    "taxonid": "null",
                    "family": "null",
                    "genus": str(line),
                    "scientificname": "null",
                    "specificepithet": "null",
                    "infraspecificepithet": "null",
                    "scientificnameauthorship": "null",
                    "taxonomicstatus": "null",
                    "acceptednameusage": "null",
                    "higherclassification": "null",
                    "source": "null",
                    "references": "null"
                }
            df_temp = pd.DataFrame(data_temp, index=[0])
            df_final = pd.concat([df_final, df_temp])

    print(f'Linha {i} de {len(lines)}...')
    i += 1

if get_genus:
    with open('output.tsv', 'a') as saida:
        saida.write(tsv_final)
else:
    # save xlsx
    df_final.to_excel('INMA Reflora.xlsx')
