from odoo import models, fields
from datetime import datetime

class PowerPlantAggregatedData(models.Model):
    _name = 'power.plant.aggregated.data'
    _description = 'Power Plant Aggregated Data'


    name = fields.Char(string="Generator Name")  # Pole pro název generátoru
    avg_value = fields.Float(string="Average Power (kW)")  # Průměrná hodnota pro každý generátor
    timestamp = fields.Datetime(string="Timestamp")


