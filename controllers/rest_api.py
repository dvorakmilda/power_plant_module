import json
from odoo import http
from odoo.http import request
from datetime import datetime

class PowerPlantAPI(http.Controller):
    @http.route('/api/power_plant_data', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_data(self, **post):
        data = request.jsonrequest  # Očekává formát {"1": [1024, 750]}
        current_time = datetime.now()

        for generator_id, values in data.items():
            generator1 = values[0]
            generator2 = values[1]

            # Uložit data do databáze jako skutečná data
            request.env['power.plant.data'].sudo().create({
                'generator_id': generator_id,
                'generator1': generator1,
                'generator2': generator2,
                'timestamp': current_time,
                'is_real_data': True  # Označit jako skutečná data
            })
        
        return json.dumps({'status': 'success', 'message': 'Data received and stored successfully'})
