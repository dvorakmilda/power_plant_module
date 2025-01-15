from odoo import http
from odoo.http import request
from datetime import datetime
import json

class PowerPlantAPI(http.Controller):
    @http.route('/api/power_plant_data', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_data(self, **post):
        data = request.httprequest.get_json()  # Čtení JSON požadavku
        current_time = datetime.now()

        # Iterace přes každý generátor a jeho hodnotu
        for generator_id, value in data.items():
            request.env['power.plant.data'].sudo().create({
                'name': f'generator{generator_id}',  # Vytváříme dynamický název generátoru
                'value': value,  # Uložíme hodnotu výkonu
                'timestamp': current_time,
                'is_real_data': True  # Označení jako skutečná data
            })

        return json.dumps({'status': 'success', 'message': 'Data received and stored successfully'})

    @http.route('/api/power_plant_data2', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_data2(self, **post):
        try:
            data = request.httprequest.get_json()
            current_time = datetime.now()
            values = []
            if isinstance(data, dict):
                data = [data]

            for row in data:
                values.append({
                'name': f'BPS {current_time}',  # Vytváříme dynamický název generátoru
                'KGJ1': row["1"],  # Uložíme hodnotu aktuálního výkonu KG1
                'KGJ2': row["2"],  # Uložíme hodnotu aktuálního výkonu KG2
                'BTC': row["btc"],  # Uložíme hodnotu spotřeby BTC v KWh
                'sKGJ1': row["sKGJ1"],  # Uložíme hodnotu spotřeby KGJ1 v KWh
                'vKGJ1': row["vKGJ1"],  # Uložíme hodnotu výroby KGJ1 v KWh
                'STrafo': row["STrafo"],  # Uložíme hodnotu spotřeby trafo v KWh
                'dTrafa': row["dTrafa"],  # Uložíme hodnotu dodávky trafo v KWh
                'sSusarna': row["sSusarna"],  # Uložíme hodnotu spotřeby sušárny v KWh
                'sOstatni': row["sOstatni"],  # Uložíme hodnotu spotřeby ostatních v KWh
                'CH4': row["CH4"],  # Uložíme hodnotu koncentrace CH4 v %
                'O2': row["O2"],  # Uložíme hodnotu koncentrace O2 v %
                'H2S': row["H2S"],  # Uložíme hodnotu koncentrace H2S v ppm
                'plynAnal': row["plynAnal"],  # Uložíme hodnotu průtoku plynu za hodinu v m3
                'hladinaPlynu': row["hladinaPlynu"],  # Uložíme hodnotu hladiny plynu v % v plynojemu
                'tlakPlynu': row["tlakPlynu"],  # Uložíme hodnotu tlaku plynu v bar
                'timestamp': current_time,
                'is_real_data': True  # Označení jako skutečná data
            })
            request.env['power.plant.data2'].sudo().create(values)
            return json.dumps({'status': 'success', 'message': 'Data2 received and stored successfully'})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})               # ... stejná struktura jako předtím ...
