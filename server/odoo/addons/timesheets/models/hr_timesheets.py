from odoo import fields, models, api, _
from datetime import datetime, timedelta, date

class HrTimesheet(models.Model):
    _name = 'hr.timesheet'
    _description = 'This is a timesheet for the HR department'

    department = fields.Selection([
        ('hr', 'HR Department'), ('admin', 'Executive Assistant')
    ], string="Department", default="hr")
    activity_type = fields.Selection([
        ('meet_schedule', 'Meeting Scheduling'), ('lead_gen', 'Lead Generation'), ('lpo_follow', 'LPO Follow Up'),
        ('leave_management', 'Leave Management'), ('meeting', 'Meetings & Meeting Coordination'),
        ('supervision', 'Supervision'), ('respond', 'Responding to calls/emails'), ('training', 'Training'),
        ('attendance', 'Attendance'), ('recruitment', 'Recruitment'),('disciplinary', 'Discplinary'), ('admin_repairs', 'Admin Repairs'),
        ('doc_customization', 'Document Customization'), ('reporting', 'Reporting'), ('minute_writing', 'Minute Writing'),
        ('requisition', 'Requisition'), ('errand', 'Running Errands'), ('onboarding', 'Onboarding'), ('performance', 'Performance Management'),
        ('depart_meeting', 'Departmental Meeting'), ('inter', 'Inter-departmental meeting'),
        ('management_meet', 'Management Meeting'), ('filing', 'Filing'),
        ('scheduling', 'Scheduling'),('gen_hr', 'General HR Work'), ('gen_admin', 'General Admin Work'),
    ], string='Activity Type')
    task_description = fields.Text(string='Task Description')
    status =fields.Selection([
        ('completed', 'Completed'), ('ongoing', 'Ongoing'), ('pending', 'Pending'), ('scheduled', 'Scheduled'), ('escalated', 'Escalated'),
        ('rescheduled', 'Rescheduled'), ('cancelled', 'Cancelled'), ('sent', 'Sent'), ('not_sent', 'Not Sent')
    ], string='Status')
    task_category = fields.Selection([
        ('management_meeting', 'Management\'s meeting'), ('management_task', 'Management\'s tasks'),
        ('pa_task', 'P.A\'s Task'), ('admin_task', 'Admin Task'), ('hr_task', 'HR\'s Task')
    ], string='Task Category')
    employee_id = fields.Many2one(comodel_name='res.users',string='Employee Name', default=lambda self: self.env.user.id)
    status_comment = fields.Text(string='Status Comment')
    escalation = fields.Many2one(comodel_name='hr.employee', string='Escalated To (if any)')
    start_time = fields.Datetime(string='Start Time')
    other_employee = fields.Char(string='Supported by')
    end_time = fields.Datetime(string='End Time')
    duration = fields.Char(string='Time Taken', compute='_get_duration')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)
            else:
                rec.duration = ""

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.timesheet.entry') or _('New')
        return super(HrTimesheet, self).create(vals)
