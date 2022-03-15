from odoo import api, fields, models


class EngineerReport(models.TransientModel):
    _name = "engineer.report.wizard"
    _description = "Wizard to print multiple timesheet records"

    engineer_id = fields.Many2one(string='Engineer name', comodel_name='hr.employee')
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    @api.multi
    def action_print_report(self):

        data = {
            'engineer_id': self.engineer_id,
            'date_from': self.date_from,
            'date_to': self.date_to
        }

        return self.env.ref('timesheets.action_engineer_report').report_action(self, data=data)


class AllEngReport(models.AbstactModel):
    _name = 'report.timesheets.report_engineer_wizard'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = []
        if data.get('date_from'):
            domain.append(('real_date', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('real_date', '>=', data.get('date_to')))
        # if data.get('engineer_id'):
        #     domain.append(('id', 'in', data.get('engineer_id')))
        docs = self.env['om.timesheet'].search(domain)
        return{
            'doc_ids': docids,
            'docs': docs,
            'data': data
        }
