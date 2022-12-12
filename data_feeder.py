from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import csv
from tqdm import tqdm
es = Elasticsearch('https://localhost:9200',ca_certs="/home/tejender/elasticsearch-8.5.2/config/certs/http_ca.crt",basic_auth=('elastic','W68wQJhDyzEy1xQQBR=1'))


def documents():
    actions={}
    with open('IN.txt') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in tqdm(reader, total=649011):
            try:
                doc = {
                        "name" : row[1],
                        "latitude":row[4],
                        "longitude":row[5]
                    }
                action = {"_index" : "india_index",
                            "_source" : doc}
                yield action
            except:
                continue        
        return actions

if __name__ == "__main__":
    actions = documents()
    helpers.bulk(es, actions, chunk_size=500)
    es.indices.refresh(index='india_index')

