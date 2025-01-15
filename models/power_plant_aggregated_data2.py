from odoo import models, fields, api
from datetime import datetime

class PowerPlantAggregatedData2(models.Model):
    _name = 'power.plant.aggregated.data2'
    _description = 'Power Plant Aggregated Data2'

    id = fields.Integer(index=True)
    name = fields.Char(string="Record Name")
    KGJ1 = fields.Integer(string="KGJ1 (kWH)")
    KGJ2 = fields.Integer(string="KGJ2 (kWH)")
    sKGJ1 = fields.Float(string="sKGJ1 (kWH)")
    vKGJ1 = fields.Float(string="vKGJ1 (kWH)")
    BTC = fields.Float(string="BTC (kWH)")
    STrafo = fields.Float(string="STrafo (kWH)")
    dTrafa = fields.Float(string="dTrafa (kWH)")
    sSusarna = fields.Float(string="sSusarna (kWH)")
    sOstatni = fields.Float(string="sOstatni (kWH)")
    CH4 = fields.Float(string="CH4 (%)")
    O2 = fields.Float(string="O2 (%)")
    H2S = fields.Float(string="H2S (ppm)")
    plynAnal = fields.Float(string="plynAnal (m3)")
    hladinaPlynu = fields.Float(string="hladinaPlynu (%)")
    tlakPlynu = fields.Float(string="tlakPlynu (bar)")
    timestamp = fields.Datetime(string="Timestamp", default=fields.Datetime.now)


