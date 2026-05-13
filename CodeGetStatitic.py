import requests
import dotenv
import os
from datetime import date, timedelta

dotenv.load_dotenv()

def getSerankingPosition(days=1):
    siteId = os.getenv("siteId")
    apiKey = os.getenv("api_key_serangking")

    dateFrom = date.today() - timedelta(days=days)
    dateTo = date.today()

    headers = {
        "Authorization": f"Token {apiKey}",
        "Content-Type": "application/json"
    }

    endPoint = (
        f"https://api4.seranking.com/sites/"
        f"{siteId}/positions?date_from={dateFrom}&date_to={dateTo}"
    )

    response = requests.get(endPoint, headers=headers)

    return response

def calculateWeight(days=1):
    position = getSerankingPosition(days=days).json()[0]

    listWeight = []
    for p in position['keywords']:
        weight = 0
        for s in p['positions']:
            weight += s['pos'] - s['change']
        listWeight.append([p['name'], weight])

    return listWeight