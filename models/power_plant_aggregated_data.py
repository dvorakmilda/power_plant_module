from odoo import models, fields
from datetime import datetime

class PowerPlantAggregatedData(models.Model):
    _name = 'power.plant.aggregated.data'
    _description = 'Power Plant Aggregated Data'
    _auto = False  # Zajistí, že Odoo nebude vytvářet fyzickou tabulku

    generator_name = fields.Char(string="Generator Name")  # Pole pro název generátoru
    avg_value = fields.Float(string="Average Power (kW)")  # Průměrná hodnota pro každý generátor
    period_type = fields.Selection([
        ('hour', 'Hourly'),
        ('day', 'Daily'),
        ('week', 'Weekly'),
        ('month', 'Monthly'),
        ('year', 'Yearly')], string="Period Type")
    timestamp = fields.Datetime(string="Timestamp", default=datetime.now)

    def init(self):
        # Definice SQL view
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW power_plant_aggregated_data AS (
                SELECT
                    generator_name,
                    date_trunc('hour', timestamp) AS period,
                    AVG(value) AS avg_value
                FROM
                    power_plant_data
                WHERE
                    is_real_data = true
                GROUP BY
                    generator_name, period
            )
        """)
