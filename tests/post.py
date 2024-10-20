import requests
import json
import random
import time

# URL vašeho REST API
url = "http://localhost:8070/api/power_plant_data"

# Hlavičky HTTP požadavku
headers = {
    "Content-Type": "application/json"
}

# Funkce pro generování náhodných dat
def generate_data():
    return {
        "1": [random.randint(150, 1000), random.randint(150, 1000)]
    }

# Smyčka pro odesílání POST požadavků každou vteřinu
try:
    while True:
        # Generování dat
        data = generate_data()

        # Odeslání POST požadavku
        response = requests.post(url, headers=headers, data=json.dumps(data))

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
