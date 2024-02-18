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

def __get_eventos_sympla(page=1, need_pay="", collections="", start_date = None, end_date = None, city: str = "Recife", state: str = "PE", sort="date"):
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
            "page": page,
            "collections": collections,
            "need_pay": need_pay,
            }
        }
    
    if start_date and end_date:
        data["params"]["range"] = f"{start_date},{end_date}"

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao obter eventos da API externa")
    
    return response.json()
    

def get_eventos_sympla():
    eventos = []

    # Pegar todos os eventos
    print("Pegando todos os eventos...")
    page = 1
    while True:
        response_data = __get_eventos_sympla(page=page)

        if "result" in response_data and "events" in response_data["result"]:
            for event in response_data["result"]["events"]["data"]:
                event["need_pay"] = True
                event["category"] = []
                eventos.append(event)

            if (response_data["result"]["events"]["page"] * 
                    response_data["result"]["events"]["limit"] >= response_data["result"]["events"]["total"]):
                break
        
        page += 1
        time.sleep(0.5)
    print(f"Total de todos os eventos: {len(eventos)}")

    # Pegar eventos gratuitos (gratuitos <<< pagos)
    print("Pegando eventos gratuitos...")
    count_events_free = 0
    count_events_not_registered = 0

    page = 1
    while True:
        response_data = __get_eventos_sympla(page=page, need_pay="0")

        if "result" in response_data and "events" in response_data["result"]:
            for event in response_data["result"]["events"]["data"]:
                count_events_free += 1
                event["need_pay"] = False

                for event_saved in eventos:
                    if event_saved["id"] == event["id"]:
                        event_saved["need_pay"] = False
                        break
                else:
                    count_events_not_registered += 1
                    eventos.append(event)

            if (response_data["result"]["events"]["page"] * 
                    response_data["result"]["events"]["limit"] >= response_data["result"]["events"]["total"]):
                break
        
        page += 1
        time.sleep(0.5)
    print(f"Total de eventos pagos: {count_events_free}; Total de eventos: {len(eventos)}; Total de eventos não registrados: {count_events_not_registered}")

    # Pegar eventos por categoria
    count_events_not_registered = 0
    print("Pegando eventos por categoria...")

    categories = {
        "GASTRONOMIA": 1,
        "FESTAS_SHOWS": 17,
        "RELIGIAO_ESPIRITUALIDADE": 13,
        "CURSOS_WORKSHOPS": 8,
        "ARTE_CINEMA_LAZER": 10,
        "GAMES_GEEK": 12,
        "CONGRESSOS_PALESTRAS": 4,
        "SAUDE_BEM_ESTAR": 9,
        "MODA_BELEZA": 11,
        "ESPORTES": 2,
        "INFANTIL": 15,
        "PRIDE": 14,
    }

    for category in categories:
        page = 1
        while True:
            response_data = __get_eventos_sympla(page=page, collections=categories[category])

            if "result" in response_data and "events" in response_data["result"]:
                for event in response_data["result"]["events"]["data"]:
                    event["category"] = [category]

                    for event_saved in eventos:
                        if event_saved["id"] == event["id"]:
                            if category not in event_saved["category"]:
                                event_saved["category"].append(category)
                            break
                    else:
                        count_events_not_registered += 1
                        eventos.append(event)

                if (response_data["result"]["events"]["page"] * 
                        response_data["result"]["events"]["limit"] >= response_data["result"]["events"]["total"]):
                    break

            page += 1
            time.sleep(0.5)

    print(f"Total de eventos após categorias: {len(eventos)}; Total de eventos não registrados: {count_events_not_registered}")
    return eventos
