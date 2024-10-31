from odoo import models, fields, api
from datetime import datetime, timedelta

class PowerPlantData(models.Model):
    _name = 'power.plant.data'
    _description = 'Power Plant Data'

    id = fields.Integer(index=True)
    name = fields.Char(string="Generator Name")  # Nové pole pro název generátoru
    value = fields.Float(string="Power (kW)")  # Jednotná hodnota pro každý záznam
    timestamp = fields.Datetime(string="Timestamp", default=fields.Datetime.now)
    is_real_data = fields.Boolean(string="Is Real Data", default=True)  # True pro reálná data, False pro vypočítaná

    # Vypočítaná pole pro průměrné hodnoty
    avg_value = fields.Float(string='Avg Power',  store=True, compute='_compute_avg_value', compute_sudo=True, readonly=True, group_operator='avg')

    @api.depends('value')
    def _compute_avg_value(self):
        for record in self:
            record.avg_value = record.value  # Můžete sem přidat vlastní logiku pro průměr

    def get_current_datetime(self):
        return fields.Datetime.now()

    def _get_action_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Power Plant Data',
            'res_model': 'power.plant.data',
            'view_mode': 'tree,form',
            'context': {
                'current_datetime': fields.Datetime.now(),  # Přidání aktuálního data a času do kontextu
            }
        }


    @api.model
    def aggregate_hourly_data(self):
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)

        # Najít všechny názvy generátorů
        names = self.search([]).mapped('name')

        for name in names:
            # Získání dat za poslední hodinu
            records = self.search([
                ('name', '=', name),
                ('timestamp', '>=', one_hour_ago),
                ('timestamp', '<=', current_time),
                ('is_real_data', '=', True)
            ])

            if records:
                avg_value = sum(record.value for record in records) / len(records)

                # Uložení agregovaných dat do nové tabulky
                self.env['power.plant.aggregated.data'].create({
                    'name': name,
                    'avg_value': avg_value,
                    'period_type': 'hour',
                    'timestamp': current_time,
                })

    def get_grouped_avg_data(self):
        """ Vrátí data seskupená podle názvu generátoru a časového razítka s průměrnou hodnotou """
        query = """
            SELECT
                name,
                AVG(value) as avg_value,
                date_trunc('hour', timestamp) as timestamp
            FROM
                power_plant_data
            GROUP BY
                name, date_trunc('hour', timestamp)
            ORDER BY
                timestamp DESC
        """
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    # Přepracování read_group pro správné agregování avg_value
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        # Zavolejte původní implementaci read_group
        res = super(PowerPlantData, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        # Pokud je avg_value mezi poli, ručně ji vypočítáme pro každou skupinu
        if 'avg_value' in fields:
            for line in res:
                if '__domain' in line:
                    # Získání všech záznamů odpovídajících aktuální doméně
                    lines = self.search(line['__domain'])
                    total_avg_value = 0.0
                    count = 0
                    for record in lines:
                        total_avg_value += record.avg_value
                        count += 1

                    # Uložení průměrné hodnoty do výsledku skupiny
                    line['avg_value'] = total_avg_value / count if count > 0 else 0.0

        return res


    @api.model
    def aggregate_historical_data(self):
        # Získání aktuálního času
        current_time = datetime.now()

        # Najít všechny názvy generátorů
        names = self.search([]).mapped('name')

        for name in names:
            # Počáteční čas záznamů (od nejstaršího záznamu)
            first_record = self.search([('name', '=', name)], order='timestamp asc', limit=1)
            if not first_record:
                continue

            start_time = first_record.timestamp.replace(minute=0, second=0, microsecond=0)

            # Iterace přes každou hodinu v minulosti až do současného času
            while start_time + timedelta(hours=1) <= current_time:
                end_time = start_time + timedelta(hours=1)

                # Výběr záznamů v aktuální hodinovém intervalu
                records = self.search([
                    ('name', '=', name),
                    ('timestamp', '>=', start_time),
                    ('timestamp', '<', end_time),
                    ('is_real_data', '=', True)
                ])

                if records:
                    avg_value = sum(record.value for record in records) / len(records)

                    # Uložení agregovaných dat do nové tabulky
                    self.env['power.plant.aggregated.data'].create({
                        'name': name,
                        'avg_value': avg_value,
                        'timestamp': start_time,
                    })

                    # Odstranění původních záznamů z této hodiny
                    records.unlink()

                # Posun na další hodinový interval
                start_time = end_time

    @api.model
    def action_aggregate_historical_data(self):
        # Zde zavolejte metodu pro agregaci dat
        self.aggregate_historical_data()

