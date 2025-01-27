import requests
import json
import random
import time

# URL vašeho REST API
url= "http://100.84.49.40:8070/api/power_plant_data2"
#url = "https://www.multireality.cz/api/power_plant_data"
#url = "https://posttestserver.dev/p/ixm03e9bosab4lch/post"
# Hlavičky HTTP požadavku
headers = {
    "Content-Type": "application/json"
}

# Funkce pro generování náhodných dat
def generate_data():
    return {
        "1": random.randint(150, 1000),
        "2": random.randint(150, 1000),  # Data pro generátor ID 1
        "btc": 18594,
        "sKGJ1": 14906.099609375,
        "vKGJ1": 3034098.75,
        "STrafo": 166424.203125,
        "dTrafa": 835734.3125,
        "sSusarna": 893205.375,
        "sOstatni": 427105.90625,
        "CH4": 53.91999816894531,
        "O2": 0.029999999329447746,
        "H2S": 58,
        "plynAnal": 124.4000015258789,
        "hladinaPlynu": 98.26815032958984,
        "tlakPlynu": -0.9069366455078125,
        "ELM11":0,
        "ELM13":0,
        "ELM14":0,
        "ELM15":0,
        "ELM16":0,

    }

# Smyčka pro odesílání POST požadavků každou vteřinu
try:
    while True:
        # Generování dat
        data = generate_data()

        # Odeslání POST požadavku
        response = requests.post(url, headers=headers, data=json.dumps(data))

        print(response.text)

        # Zobrazení výsledku
        if response.status_code == 200:
            print("Data successfully sent:", response.json())
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
            print(response.text)

        # Čekání jednu vteřinu před dalším požadavkem
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user.")
