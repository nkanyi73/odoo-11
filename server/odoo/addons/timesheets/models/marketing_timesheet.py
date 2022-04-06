from odoo import fields, models, api, _
from datetime import datetime, time, date


class MarketingTimesheet(models.Model):
    _name = 'marketing.timesheet'
    _description = 'This is a timesheet for the sales and marketing department.'

    department = fields.Selection([
        ('client_relations', 'Client Relations'), ('marketing', 'Marketing'),
        ('direct_sales', 'Direct Sales'), ('follow_up', 'Sales Follow Up')
    ], string="Department", required=True)
    task_activity = fields.Selection([
        ('debt_collection','Debt Collection'), ('sla', 'SLA Follow-up'), ('customer_visit', 'Customer Visit'),
        ('content_creation', 'Content Creation'), ('email_market', 'Email Marketing'), ('cold_call', 'Cold Calling'),
        ('lead_gen', 'Lead Generation'), ('lpo_follow', 'LPO Follow-Up'), ('quot_follow', 'Quotation Follow Up'),
        ('client_meet', 'Client Meeting'), ('research', 'Research'), ('report', 'Report'),  ('introductory', 'Introductory Email'),
        ('email_follow', 'Email Follow Up'), ('depart_meet', 'Departmental Meeting'), ('osh', 'Induction (OSH)'),
        ('inter_depart', 'Inter-departmental Meeting'), ('audit', 'ISO Audit'), ('management_meet', 'Management Meeting'),
        ('training', 'Training')
    ], string="Task Activity", required=True)
    customer_name = fields.Char(string='Customer Name (if applicable)')
    description = fields.Text(string='Task Description')
    quotation_ref = fields.Many2one(comodel_name='sale.order', string='Quotation Reference')
    potential_no = fields.Many2one(comodel_name='crm.potentials', string='Potential Reference')
    amount = fields.Float(string='Quotation Sum (if applicable)')
    status = fields.Selection([
        ('pending', 'Pending'), ('ongoing', 'Ongoing'),
        ('complete', 'Complete'), ('escalated', 'Escalated')
        ])
    follow_up = fields.Selection([
        ('n/a', 'N/A'), ('hot', 'Hot'), ('warm', 'Warm'),
        ('close_won', 'Closed Won'), ('close_lost', 'Closed Lost'),
        ('cold', 'Cold'), ('na', 'N/A')
    ], string='Follow up Status', default='na')
    status_comment = fields.Text(string='Status Comment')
    other_employee = fields.Char(string='Supported by')
    employee_id = fields.Many2one(comodel_name='res.users',string='Employee Name', default=lambda self: self.env.user.id)
    start_time = fields.Datetime(string='Start Time', required="True")
    end_time = fields.Datetime(string='End Time')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))
    duration = fields.Char(string='Time Taken', compute='_get_duration')


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('marketing.timesheet.entry') or _('New')
        return super(MarketingTimesheet, self).create(vals)

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)
            else:
                rec.duration = ""
