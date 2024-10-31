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
