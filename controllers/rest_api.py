import json
from odoo import http
from odoo.http import request
from datetime import datetime

class PowerPlantAPI(http.Controller):
    @http.route('/api/power_plant_data', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_data(self, **post):
        data = request.httprequest.get_json()  # Čtení JSON požadavku
        current_time = datetime.now()

        # Iterace přes všechny generátory a jejich hodnoty
        for generator_id, values in data.items():
            if len(values) >= 2:
                # Uložení záznamu pro každý generátor
                generator1_value = values[0]
                generator2_value = values[1]

                request.env['power.plant.data'].sudo().create({
                    'generator_name': f'generator{generator_id}_1',
                    'value': generator1_value,
                    'timestamp': current_time,
                    'is_real_data': True  # Označení jako skutečná data
                })

                request.env['power.plant.data'].sudo().create({
                    'generator_name': f'generator{generator_id}_2',
                    'value': generator2_value,
                    'timestamp': current_time,
                    'is_real_data': True  # Označení jako skutečná data
                })

        return json.dumps({'status': 'success', 'message': 'Data received and stored successfully'})
