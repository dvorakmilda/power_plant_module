from datetime import datetime, timedelta
from odoo import models, fields, api

class PowerPlantData2(models.Model):
    _name = 'power.plant.data2'
    _description = 'Power Plant Data2'

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
    is_real_data = fields.Boolean(string="Is Real Data", default=True)

    @api.model
    def aggregate_hourly_data(self):
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=2)

        # Získání dat za poslední hodinu
        records = self.env['power.plant.data2'].search([
            ('timestamp', '>=', one_hour_ago),
            ('timestamp', '<=', current_time)
            #,('is_real_data', '=', True)
        ])

        if records:

            # Vypočítání průměrných hodnot pro jednotlivé sloupce
            KGJ1 = sum(record.KGJ1 for record in records) / len(records)
            KGJ2 = sum(record.KGJ2 for record in records) / len(records)

            sKGJ1 = max(record.sKGJ1 for record in records)
            vKGJ1 = max(record.vKGJ1 for record in records)
            BTC = max(record.BTC for record in records)
            STrafo = max(record.STrafo for record in records)
            dTrafa = max(record.dTrafa for record in records)
            sSusarna = max(record.sSusarna for record in records)
            sOstatni = max(record.sOstatni for record in records)


            CH4 = sum(record.CH4 for record in records) / len(records)
            O2 = sum(record.O2 for record in records) / len(records)
            H2S = sum(record.H2S for record in records) / len(records)
            plynAnal = sum(record.plynAnal for record in records) / len(records)
            hladinaPlynu = sum(record.hladinaPlynu for record in records) / len(records)
            tlakPlynu = sum(record.tlakPlynu for record in records) / len(records)

            # Odstranění starých agregovaných dat pro tento generátor a časové období

            # Uložení nových agregovaných dat
            self.env['power.plant.aggregated.data2'].create({
                'name': current_time.replace(minute=0, second=0, microsecond=0),
                'KGJ1': KGJ1,
                'KGJ2': KGJ2,
                'sKGJ1': sKGJ1,
                'vKGJ1': vKGJ1,
                'BTC': BTC,
                'STrafo': STrafo,
                'dTrafa': dTrafa,
                'sSusarna': sSusarna,
                'sOstatni': sOstatni,
                'CH4': CH4,
                'O2': O2,
                'H2S': H2S,
                'plynAnal': plynAnal,
                'hladinaPlynu': hladinaPlynu,
                'tlakPlynu': tlakPlynu,
                'timestamp': current_time,
                #'period_type': 'hour'
            })
            records.unlink()

    @api.model
    def get_grouped_avg_data(self):
        """ Vrátí data seskupená podle názvu záznamu a časového razítka s průměrnou hodnotou """
        query = """
            SELECT
                name,
                AVG(KGJ1) as KGJ1,
                AVG(KGJ2) as KGJ2,
                MAX(sKGJ1) as sKGJ1,
                MAX(vKGJ1) as vKGJ1,
                MAX(BTC) as BTC,
                MAX(STrafo) as STrafo,
                MAX(dTrafa) as dTrafa,
                MAX(sSusarna) as sSusarna,
                MAX(sOstatni) as sOstatni,
                AVG(CH4) as CH4,
                AVG(O2) as O2,
                AVG(H2S) as H2S,
                AVG(plynAnal) as plynAnal,
                AVG(hladinaPlynu) as hladinaPlynu,
                AVG(tlakPlynu) as tlakPlynu,
                date_trunc('hour', timestamp) as timestamp
            FROM
                power_plant_data2
            GROUP BY
                name, date_trunc('hour', timestamp)
            ORDER BY
                timestamp DESC
        """
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    @api.model
    def aggregate_historical_data2(self):
        current_time = datetime.now()

        first_record = self.search([], order='timestamp asc', limit=1)
        if first_record:

            # Počáteční čas pro iteraci
            start_time = first_record.timestamp.replace(minute=0, second=0, microsecond=0)

            # Iterace přes každou hodinu v minulosti až do současného času
            while start_time + timedelta(hours=1) <= current_time:
                end_time = start_time + timedelta(hours=1)

                # Výběr záznamů pro aktuální časový interval
                records = self.search([
                    ('timestamp', '>=', start_time),
                    ('timestamp', '<', end_time)
                    #,('is_real_data', '=', True)
                ])

                if records:

                    KGJ1 = sum(rec.KGJ1 for rec in records) / len(records)
                    KGJ2 = sum(rec.KGJ2 for rec in records) / len(records)

                    sKGJ1 = max(rec.sKGJ1 for rec in records)
                    vKGJ1 = max(rec.vKGJ1 for rec in records)
                    BTC = max(rec.BTC for rec in records)
                    STrafo = max(rec.STrafo for rec in records)
                    dTrafa = max(rec.dTrafa for rec in records)
                    sSusarna = max(rec.sSusarna for rec in records)
                    sOstatni = max(rec.sOstatni for rec in records)

                    CH4 = sum(rec.CH4 for rec in records) / len(records)
                    O2 = sum(rec.O2 for rec in records) / len(records)
                    H2S = sum(rec.H2S for rec in records) / len(records)
                    plynAnal = sum(rec.plynAnal for rec in records) / len(records)
                    hladinaPlynu = sum(rec.hladinaPlynu for rec in records) / len(records)
                    tlakPlynu = sum(rec.tlakPlynu for rec in records) / len(records)

                    # Uložení agregovaných dat do nové tabulky
                    self.env['power.plant.aggregated.data2'].create({
                        'name': end_time,
                        'KGJ1': KGJ1,
                        'KGJ2': KGJ2,
                        'sKGJ1': sKGJ1,
                        'vKGJ1': vKGJ1,
                        'BTC': BTC,
                        'STrafo': STrafo,
                        'dTrafa': dTrafa,
                        'sSusarna': sSusarna,
                        'sOstatni': sOstatni,
                        'CH4': CH4,
                        'O2': O2,
                        'H2S': H2S,
                        'plynAnal': plynAnal,
                        'hladinaPlynu': hladinaPlynu,
                        'tlakPlynu': tlakPlynu,
                        'timestamp': start_time,
                    })

                    # Odstranění původních záznamů
                    records.unlink()

                # Posun na další hodinový interval
                start_time = end_time


    @api.model
    def action_aggregate_historical_data2(self):
        # Zde zavolejte metodu pro agregaci dat
        self.aggregate_historical_data2()