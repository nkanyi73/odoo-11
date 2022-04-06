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
    'depends': ['helpdesk_lite', 'crm', 'sale_crm', 'purchase', 'hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/timesheet.xml',
        'views/sales_timesheet.xml',
        'views/tech_timesheet.xml',
        'views/hr_timesheet.xml',
        'views/marketing_timesheet.xml',
        'views/stores_timesheet.xml',
        'views/accounts_timesheet.xml',
        'views/csc_timesheet.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
