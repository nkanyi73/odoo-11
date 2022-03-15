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
    'depends': ['mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/mail_template.xml',
        'wizard/engineer_report.xml',
        'views/timesheet.xml',
        'report/report.xml',
        'report/eng_timesheet.xml',
        'report/eng_report_details.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
