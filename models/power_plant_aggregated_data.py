from odoo import models, fields
from datetime import datetime

class PowerPlantAggregatedData(models.Model):
    _name = 'power.plant.aggregated.data'
    _description = 'Power Plant Aggregated Data'
    _auto = False  # Zajistí, že Odoo nebude vytvářet fyzickou tabulku

    generator_id = fields.Char(string="Generator ID")
    avg_generator1 = fields.Float(string="Average Generator 1 Power (kW)")
    avg_generator2 = fields.Float(string="Average Generator 2 Power (kW)")
    period_type = fields.Selection([('hour', 'Hourly'), ('day', 'Daily'), ('week', 'Weekly'), ('month', 'Monthly'), ('year', 'Yearly')], string="Period Type")
    timestamp = fields.Datetime(string="Timestamp", default=datetime.now)


    def init(self):
        # Definice SQL view
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW power_plant_aggregated_data AS (
                SELECT
                    generator_id,
                    date_trunc('hour', timestamp) AS period,
                    AVG(generator1) AS avg_generator1,
                    AVG(generator2) AS avg_generator2
                FROM
                    power_plant_data
                WHERE
                    is_real_data = true
                GROUP BY
                    generator_id, period
            )
        """)
