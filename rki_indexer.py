import time
import json
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# The covid data from RKI that is necessary for this script can be found here:
# https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0
# Once downloaded, place it in the same folder as this file.

file_name = "./RKI_COVID19.csv"
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index_name = 'corona_rki'


def bulk_index(data):
    bulk_size = 10000
    position = 0
    while True:
        to = position + (bulk_size - 1)
        if to >= len(data.index):
            to = len(data.index)
        percentage = int((position / len(data.index)) * 1000) / 10
        print(f'{percentage}%  {position}/{len(data.index)}')
        bulk(es, get_section(data, position, to), index=index_name)
        if to >= len(data.index):
            return
        position += bulk_size


def get_section(data, frm, to):
    for i in range(frm, to):
        yield json.dumps(create_dict(data.iloc[i]))


def create_dict(row):
    year = row['Meldedatum'][0:4]
    month = row['Meldedatum'][5:7]
    day = row['Meldedatum'][8:10]
    date = year+'/'+month+'/'+day
    result = {'date': date,
              'kreis': row['Landkreis'],
              'land': row['Bundesland'],
              'anzahlFall': int(row['AnzahlFall']),
              'anzahlTodesfall': int(row['AnzahlTodesfall']),
              'geschlecht': str(row['Geschlecht']),
              'altersgruppe': str(row['Altersgruppe'])
              }
    return result


if __name__ == '__main__':
    if es.indices.exists(index=index_name):
        print(f"Deleting index '{index_name}'.")
        es.indices.delete(index=index_name)
    time.sleep(5)

    print('Reading data.')
    df = pd.read_csv(file_name)

    print(f'Indexing {df.size} documents.')
    bulk_index(df)
