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


    # Computed fields for averages
    avg_generator1 = fields.Float(string='Avg Generator 1 Power', compute='_compute_avg_generator1')
    avg_generator2 = fields.Float(string='Avg Generator 2 Power', compute='_compute_avg_generator2')

    @api.depends('generator1')
    def _compute_avg_generator1(self):
        for record in self:
            record.avg_generator1 = record.generator1  # This should reflect your custom logic for avg

    @api.depends('generator2')
    def _compute_avg_generator2(self):
        for record in self:
            record.avg_generator2 = record.generator2  # This should reflect your custom logic for avg

    @api.model
    def aggregate_hourly_data(self):
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)

        # Najít všechny generátory
        generator_ids = self.search([]).mapped('generator_id')

        for generator_id in generator_ids:
            # Získání dat za poslední hodinu
            records = self.search([
                ('generator_id', '=', generator_id),
                ('timestamp', '>=', one_hour_ago),
                ('timestamp', '<=', current_time),
                ('is_real_data', '=', True)
            ])

            if records:
                avg_generator1 = sum(record.generator1 for record in records) / len(records)
                avg_generator2 = sum(record.generator2 for record in records) / len(records)

                # Uložení agregovaných dat do nové tabulky
                self.env['power.plant.aggregated.data'].create({
                    'generator_id': generator_id,
                    'avg_generator1': avg_generator1,
                    'avg_generator2': avg_generator2,
                    'period_type': 'hour',
                    'timestamp': current_time,
                })