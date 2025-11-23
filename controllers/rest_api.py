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
                'KGJ1': row.get("1", 0),  # Uložíme hodnotu aktuálního výkonu KG1
                'KGJ2': row.get("2", 0),  # Uložíme hodnotu aktuálního výkonu KG2
                'BTC': row.get("btc", 0),  # Uložíme hodnotu spotřeby BTC v KWh
                'sKGJ1': row.get("sKGJ1", 0),  # Uložíme hodnotu spotřeby KGJ1 v KWh
                'vKGJ1': row.get("vKGJ1", 0),  # Uložíme hodnotu výroby KGJ1 v KWh
                'STrafo': row.get("STrafo", 0),  # Uložíme hodnotu spotřeby trafo v KWh
                'dTrafa': row.get("dTrafa", 0),  # Uložíme hodnotu dodávky trafo v KWh
                'sSusarna': row.get("sSusarna", 0),  # Uložíme hodnotu spotřeby sušárny v KWh
                'sOstatni': row.get("sOstatni", 0),  # Uložíme hodnotu spotřeby ostatních v KWh
                'CH4': row.get("CH4", 0),  # Uložíme hodnotu koncentrace CH4 v %
                'O2': row.get("O2", 0),  # Uložíme hodnotu koncentrace O2 v %
                'H2S': row.get("H2S", 0),  # Uložíme hodnotu koncentrace H2S v ppm
                'plynAnal': row.get("plynAnal", 0),  # Uložíme hodnotu průtoku plynu za hodinu v m3
                'hladinaPlynu': row.get("hladinaPlynu", 0),  # Uložíme hodnotu hladiny plynu v % v plynojemu
                'tlakPlynu': row.get("tlakPlynu", 0),  # Uložíme hodnotu tlaku plynu v bar
                'ELM11': row.get("ELM11", 0),
                'ELM13': row.get("ELM13", 0),
                'ELM14': row.get("ELM14", 0),
                'ELM15': row.get("ELM15", 0),
                'ELM16': row.get("ELM16", 0),
                # Registr 74
                'LSB1': row.get("LSB1", 0),
                # Registr 76
                'PCA100': row.get("PCA100", 0),
                'PCA101': row.get("PCA101", 0),
                'PCA102': row.get("PCA102", 0),
                'FIQ500aktual': row.get("FIQ500aktual", 0),
                'FIQ500celkem': row.get("FIQ500celkem", 0),
                # Registr 86
                'M01': row.get("M01", False),
                'M02': row.get("M02", False),
                'M21otevreno': row.get("M21otevreno", False),
                'M21zavreno': row.get("M21zavreno", False),
                'M22otevreno': row.get("M22otevreno", False),
                'M22zavreno': row.get("M22zavreno", False),
                'timestamp': current_time,
                'is_real_data': True  # Označení jako skutečná data
            })
            request.env['power.plant.data2'].sudo().create(values)
            return json.dumps({'status': 'success', 'message': 'Data2 received and stored successfully'})
        except Exception as e:
            return json.dumps({'status': 'error', 'message': str(e)})               # ... stejná struktura jako předtím ...
