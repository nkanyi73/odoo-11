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
    'depends':  ['mail','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/timesheet.xml',
        'data/data.xml',
        'data/mail_template.xml',
        'report/report.xml',
        'report/eng_timesheet.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
