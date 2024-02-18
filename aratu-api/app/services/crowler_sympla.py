import requests
from fastapi import HTTPException
import json
import time

def count_eventos_sympla(start_date = None, end_date = None, city: str = "Recife", state: str = "PE", sort="date"):
    url = "https://www.sympla.com.br/api/v1/search"
    headers = {"Content-Type": "application/json"}

    data = {
        "service": "/v4/mapsearch",
        "params": {
            "only": "name,start_date,end_date,images,event_type,duration_type,location,id,global_score,start_date_formats,end_date_formats,url,company,type,organizer",
            "has_banner": "1",
            "city": city,
            "state": state,
            "sort": sort,
            "page": 1
        }
    }
    if start_date and end_date:
        data["params"]["range"] = f"{start_date},{end_date}"

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao obter o count dos eventos da API externa")

    response_data = response.json()

    count = response_data["result"]["events"]["total"]

    return count

def get_eventos_sympla(start_date = None, end_date = None, city: str = "Recife", state: str = "PE", sort="date"):
    url = "https://www.sympla.com.br/api/v1/search"
    headers = {"Content-Type": "application/json"}
    eventos = []
    page = 1

    while True:
        data = {
            "service": "/v4/mapsearch",
            "params": {
                "only": "name,start_date,end_date,images,event_type,duration_type,location,id,global_score,start_date_formats,end_date_formats,url,company,type,organizer",
                "has_banner": "1",
                "city": city,
                "state": state,
                "sort": sort,
                "page": page
            }
        }
        if start_date and end_date:
            data["params"]["range"] = f"{start_date},{end_date}"

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao obter eventos da API externa")

        response_data = response.json()
        if "result" in response_data and "events" in response_data["result"]:
            eventos.extend(response_data["result"]["events"]["data"])
            if (response_data["result"]["events"]["page"] * 
                    response_data["result"]["events"]["limit"] >= response_data["result"]["events"]["total"]):
                break

        page += 1
        time.sleep(0.5)

    return eventos
