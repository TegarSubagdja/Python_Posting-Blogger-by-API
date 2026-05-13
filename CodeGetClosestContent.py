import re
import requests
import pandas as pd
import json
import sys
from rank_bm25 import BM25Okapi
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

def getDataFromWebsite(listLink, output_file="Z_ContentWebsite.json", saveFile=False):
    documents = []

    for i in listLink.index:
        link = listLink.at[i, 'Link']

        try:
            response = requests.get(link, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")

            text = soup.get_text(" ", strip=True).lower()
            text = re.sub(r'\s+', ' ', text)

            documents.append(text)

            print(f"Berhasil menarik {link}")

        except Exception as e:
            documents.append("")
            print(f"Gagal menarik {link}")
            print(e)

    if saveFile:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False)

    return documents


def getClosestContent(query, top_n=5, fileName="Z_ContentWebsite.json"):
    listLink = pd.read_csv("list_website.csv", sep=";")

    with open(fileName, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    tokenized_docs = [
        doc.split()
        for doc in documents
    ]

    bm25 = BM25Okapi(tokenized_docs)

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    results = list(zip(listLink['Link'], scores))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]


results = getClosestContent("pneumatic valve")

for link, score in results:
    print(link)
    print(f"Score : {score}")
    print()