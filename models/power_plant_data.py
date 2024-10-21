from odoo import models, fields, api
from datetime import datetime, timedelta

class PowerPlantData(models.Model):
    _name = 'power.plant.data'
    _description = 'Power Plant Data'

    generator_name = fields.Char(string="Generator Name")  # Nové pole pro název generátoru
    value = fields.Float(string="Power (kW)")  # Jednotná hodnota pro každý záznam
    timestamp = fields.Datetime(string="Timestamp", default=fields.Datetime.now)
    is_real_data = fields.Boolean(string="Is Real Data", default=True)  # True pro reálná data, False pro vypočítaná

    # Vypočítaná pole pro průměrné hodnoty
    avg_value = fields.Float(string='Avg Power',  store=True, compute='_compute_avg_value', compute_sudo=True, readonly=True, group_operator='avg')

    @api.depends('value')
    def _compute_avg_value(self):
        for record in self:
            record.avg_value = record.value  # Můžete sem přidat vlastní logiku pro průměr

    @api.model
    def aggregate_hourly_data(self):
        current_time = datetime.now()
        one_hour_ago = current_time - timedelta(hours=1)

        # Najít všechny názvy generátorů
        generator_names = self.search([]).mapped('generator_name')

        for generator_name in generator_names:
            # Získání dat za poslední hodinu
            records = self.search([
                ('generator_name', '=', generator_name),
                ('timestamp', '>=', one_hour_ago),
                ('timestamp', '<=', current_time),
                ('is_real_data', '=', True)
            ])

            if records:
                avg_value = sum(record.value for record in records) / len(records)

                # Uložení agregovaných dat do nové tabulky
                self.env['power.plant.aggregated.data'].create({
                    'generator_name': generator_name,
                    'avg_value': avg_value,
                    'period_type': 'hour',
                    'timestamp': current_time,
                })

    def get_grouped_avg_data(self):
        """ Vrátí data seskupená podle názvu generátoru a časového razítka s průměrnou hodnotou """
        query = """
            SELECT
                generator_name,
                AVG(value) as avg_value,
                date_trunc('hour', timestamp) as timestamp
            FROM
                power_plant_data
            GROUP BY
                generator_name, date_trunc('hour', timestamp)
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
