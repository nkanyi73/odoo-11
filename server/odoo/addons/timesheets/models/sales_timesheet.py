from odoo import api, fields, models, _
from datetime import datetime, date, timedelta



class SalesTimesheet(models.Model):
    _name = 'sales.timesheet'
    _description = 'This is a timesheet for the sales department'

    req_date = fields.Datetime(string="Requisition Date")
    sales_task_activity = fields.Selection([
        ('quotation_approval', 'Quotation Approval'), ('quotation_preparation', 'Quotation Preparation'),
        ('rfq', 'RFQ Solution Design'), ('tender_solution', 'Tender Solution Design'),
        ('meeting', 'Management Meeting'), ('rfq_prep', 'RFQ Preparation'), ('tendering', 'Tendering'),
        ('pre_qual', 'Pre-qualification'), ('lead_gen', 'Lead Generation'), ('cold_call', 'Cold Calling'),
        ('lpo_process', 'LPO Processing'), ('lpo_follow', 'LPO Follow-Up'), ('quot_follow', 'Quotation Follow-up'),
        ('price_follow', 'Price Request Follow-up'), ('push_P', 'Pushing for Prices'),
        ('stand_meet', 'Standing Meeting'), ('depart_meet', 'Departmental Meeting'),
        ('report', 'Report'), ('training', 'Training'), ('tend_meet', 'Tender Meeting'), ('client_meet', 'Client Meeting'),
        ('quot_soln', 'Quotation Solution Design')
    ], string='Task Activity')
    customer_name = fields.Many2one(string='Customer Name', comodel_name='res.partner')
    description = fields.Text(string='Task Description')
    line = fields.Selection([
        ('av', 'Audio Visual'), ('ict_sec', 'ICT Security'), ('ict', 'ICT'),
        ('netsol', 'Netsol'), ('cabling', 'Structured Cabling'),
        ('plantronics', 'Plantronics'), ('n_compute', 'NComputing')
    ], string='Product Line')
    employee_id = fields.Many2one(string='Assigned to', comodel_name='hr.employee')
    amount = fields.Float(string='Quotation Sum')
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
    start_time = fields.Datetime(string='Start Time', required="True")
    end_time = fields.Datetime(string='End Time')
    quotation_ref = fields.Many2one(comodel_name='sale.order', string='Quotation Reference')
    opportunity_id = fields.Many2one(comodel_name='crm.lead', string='Opportunity ID')
    potential_no = fields.Many2one(comodel_name='crm.potentials', string='Potential Number')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))
    approved_by = fields.Many2one(comodel_name='hr.employee', string='Approved By')
    authorized_by = fields.Many2one(comodel_name='hr.employee', string='Authorized By')
    duration = fields.Char(string='Time Taken', compute='_get_duration')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('sales.timesheet.entry') or _('New')
        return super(SalesTimesheet, self).create(vals)

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)
            else:
                rec.duration = ""