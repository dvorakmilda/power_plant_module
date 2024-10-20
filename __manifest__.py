{
    'name': 'Power Plant Data Module',
    'version': '1.0',
    'category': 'Energy',
    'summary': 'Module to store and visualize power plant data',
    'description': 'This module creates a data structure to store power plant data, provides a REST API for data input, and displays data using tree and graph views. It also includes a cron job to check for missing records every minute.',
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'views/power_plant_view.xml',
        'views/power_plant_aggregated_view.xml',
        'views/power_plant_menu.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
    ],
    'installable': True,
    'application': True,
}
