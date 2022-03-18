# -*- coding: utf-8 -*-
{
    'name': 'Timesheet Management',
    'version': '1.1',
    'summary': 'Manages organization timesheets',
    'sequence': -100,
    'description': """
    """,
    'category': 'Human Resources',
    'website': 'https://www.odoo.com/page/timesheets',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/timesheet.xml',
        'views/sales_timesheet.xml',
        'report/engineer_timesheet_report.xml',

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
