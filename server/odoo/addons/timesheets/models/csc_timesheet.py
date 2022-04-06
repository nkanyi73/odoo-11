from odoo import fields, models, api, _
from datetime import datetime, date


class CscTimesheet(models.Model):
    _name = 'csc.timesheet'
    _description = 'This is the timesheet for the Customer Service Department'

    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))
    task_activity = fields.Selection([
        ('client_follow', 'Client Follow-Up'), ('cold_call', 'Cold Calling'),
        ('project_schedule', 'Implementation Schedule Preparation'), ('daily_plot', 'Daily Plot Preparation'),
        ('dispatch', 'Dispatching Technicians'), ('lead_gen', 'Lead Generation'), ('lpo_process', 'LPO Processing'),
        ('mileage', 'Mileage Report'), ('pm', 'PM Scheduling'), ('report', 'Preparing Reports'),
        ('proj_meet', 'Project Implementation Meeting'), ('quote_prep', 'Quotes Preparation'),
        ('gatepass', 'Raising Gatepasses'), ('stores_req', 'Raising Stores Requisiton'),
        ('receipt_goods', 'Receipt of Goods'), ('report_submit', 'Reports Submission'), ('stock', 'Stock Take'),
        ('training', 'Training'), ('update_technical', 'Updating Technical Timesheet')
    ])
    employee_id = fields.Many2one(comodel_name='res.users', string='Assigned To', default=lambda self: self.env.user.id)
    status = fields.Selection([
        ('pending', 'Pending'), ('ongoing', 'Ongoing'),
        ('complete', 'Complete'), ('escalated', 'Escalated')
    ])
    status_comment = fields.Text(string='Status Comment')
    customer_name = fields.Many2one(comodel_name='res.partner', string='Customer Name')
    description = fields.Text(string='Task Description')
    other_employee = fields.Char(string='Supported By')
    start_time = fields.Datetime(string='Start Time', required="True")
    end_time = fields.Datetime(string='End Time')
    duration = fields.Char(string='Time Taken', compute='_get_duration')
    ticket_no = fields.Many2one(comodel_name='helpdesk_lite.ticket', string='Related Ticket Number')
    potential_no = fields.Many2one(comodel_name='crm.potentials', string='Potential Number')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('csc.timesheet.entry') or _('New')
        return super(CscTimesheet, self).create(vals)

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)