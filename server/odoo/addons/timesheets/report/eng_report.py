from odoo import api, models, fields


class AllEngReport(models.AbstactModel):
    _name = 'report.timesheets.report_eng_wizard'
    _description = 'Report'

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env['om.timesheet'].search([])
        print(docs)
        return {
            'docs': docs
        }
