from odoo import api, fields, models, _


class SalesTimesheet(models.Model):
    _name = 'sales.timesheet'
    _description = 'This is a timesheet for the sales department'

    req_date = fields.Datetime(string="Requisition Date")
    task_activity = fields.Selection([
        ('quotation_approval', 'Quotation Approval'), ('quotation_preparation', 'Quotation Approval'),
        ('rfq', 'RFQ Solution Design'), ('tender_solution', 'Tender Solution Design'),
        ('meeting', 'Management Meeting'), ('rfq_prep', 'RFQ Preparation'), ('tendering', 'Tendering'),
        ('pre_qual', 'Pre-qualification'), ('lead_gen', 'Lead Generation'), ('cold_call', 'Cold Calling'),
        ('lpo_process', 'LPO Processing'), ('lpo_follow', 'LPO Follow-Up'), ('quot_follow', 'Quotation Follow-up'),
        ('price_follow', 'Price Request Follow-up'), ('push_P', 'Pushing for Prices'),
        ('stand_meet', 'Standing Meeting'), ('depart_meet', 'Departmental Meeting'),
        ('report', 'report'), ('training', 'Training'), ('tend_meet', 'Tender Meeting'), ('client_meet', 'Client Meeting'),
        ('quot_soln', 'Quotation Solution Design')
    ], string='Task Activity')
    customer_name = fields.Many2one(string='Customer Name', comodel_name='res.partner')
    description = fields.Text(string='Task Description')
    line = fields.Selection([
        ('av', 'Audio Visual'), ('ict_sec', 'ICT Security'), ('ict', 'ICT'),
        ('netsol', 'Netsol'), ('cabling', 'Structured Cabling'),
        ('plantronics', 'Plantronics'), ('n_compute', 'NComputing')
    ], string='Product Line')
    employee_id = fields.Many2one(string='Salesperson', comodel_name='hr.employee')
    # amount = fields.Monetary(string='Quotation Sum')
    status = fields.Selection([
        ('pending', 'Pending'), ('ongoing', 'Ongoing'),
        ('complete', 'Complete'), ('escalated', 'Escalated')
    ], string='Status')
    follow_up = fields.Selection([
        ('n/a', 'N/A'), ('hot', 'Hot'), ('warm', 'Warm'),
        ('close_won', 'Closed Won'), ('close_lost', 'Closed Lost'),
        ('cold', 'Cold')
    ], string='Follow up Status')
    status_comment = fields.Text(string='Status Comment')
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.timesheet.entry') or _('New')
        return super(SalesTimesheet, self).create(vals)

