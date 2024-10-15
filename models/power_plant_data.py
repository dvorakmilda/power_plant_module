from odoo import models, fields, api
from datetime import datetime, timedelta

class PowerPlantData(models.Model):
    _name = 'power.plant.data'
    _description = 'Power Plant Data'

    generator_id = fields.Char(string="Generator ID")
    generator1 = fields.Float(string="Generator 1 Power (kW)")
    generator2 = fields.Float(string="Generator 2 Power (kW)")
    timestamp = fields.Datetime(string="Timestamp", default=fields.Datetime.now)
    is_real_data = fields.Boolean(string="Is Real Data", default=True)  # True for real data, False for calculated

    @api.model
    def check_missing_records(self):
        # Získání času předchozí minuty
        current_time = datetime.now()
        one_minute_ago = current_time - timedelta(minutes=1)

        # Získání záznamů vytvořených za poslední minutu
        records_last_minute = self.search([('timestamp', '>=', one_minute_ago), ('timestamp', '<', current_time)])

        # Najít všechny generátory
        generator_ids = self.search([]).mapped('generator_id')

        for generator_id in generator_ids:
            # Získat počet záznamů pro daný generátor za poslední minutu
            records_for_generator = records_last_minute.filtered(lambda r: r.generator_id == generator_id)
            count = len(records_for_generator)

            # Pokud počet záznamů není 60, je potřeba je doplnit
            if count < 60:
                # Získat poslední známé hodnoty pro tento generátor
                last_record = self.search([('generator_id', '=', generator_id)], order='timestamp desc', limit=1)

                if last_record:
                    # Vytvoření chybějících záznamů na základě posledního známého záznamu
                    for i in range(60 - count):
                        missing_time = one_minute_ago + timedelta(seconds=i)  # Vytvoření přesného času
                        self.create({
                            'generator_id': generator_id,
                            'generator1': last_record.generator1,
                            'generator2': last_record.generator2,
                            'timestamp': missing_time,  # Nastavit dopočítaný čas
                            'is_real_data': False  # Označit jako počítaná data
                        })
