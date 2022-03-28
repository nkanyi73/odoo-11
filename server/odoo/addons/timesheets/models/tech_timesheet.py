from odoo import api, fields, models, _
from datetime import datetime, date, timedelta


class TechTimesheet(models.Model):
    _name = 'tech.timesheet'
    _description = 'This is the technical timesheet'

    task_activity = fields.Selection([
        ('sol_design', 'Solution Design'), ('pre_sales', 'Pre Sales'),
        ('implementation', 'Technical Implementation'), ('follow_up', 'Follow Up'),
        ('rnd', 'R&D'), ('meeting', 'Meeting'), ('lpo_follow', 'LPO Follow Up'), ('vendor', 'Vendor Engagement'),
        ('approval', 'Quotation Approval'), ('support', 'Inter-departmental Support')
    ], string='Activity Type', default='sol_design', required='true')
    solution_cat = fields.Selection([
        ('tender_soln', 'Tender Solution Design'), ('rfq', 'RFQ Solution Design'),
        ('quotation_soln', 'Quotation Solution Design'), ('na', 'N/A')
    ], string='Category (Solution Design)', default='na')
    sales_cat = fields.Selection([
        ('demo', 'Demo'), ('poc', 'POC'), ('pitching', 'Pitching'),
        ('lead_gen', 'Lead Generation'), ('na', 'N/A')
    ], string='Category (Pre Sales)', default='na')
    implementation_cat = fields.Selection([
        ('inhouse', 'In-house'),
        ('delivery', 'Delivery'),
        ('callout', 'Call Out'), ('installation', 'Installation'),
        ('wlan', 'WLan'), ('survey', 'Survey'), ('lan', 'LAN Audit'), ('na', 'N/A')
    ], string='Category (Technical Implementation)', default='na')
    follow_cat = fields.Selection([
        ('customer_meet', 'Customer Meeting'), ('cold_call', 'Cold Calling'),
        ('mail_follow', 'Email Follow Up'), ('na', 'N/A')
    ], string='Category (Follow Up)', default='na')
    meeting_cat = fields.Selection([
        ('departmental', 'Departmental Meeting'), ('sales', 'Sales Meeting'), ('external', 'External Meeting'),
        ('management', 'Management Meeting'), ('na', 'N/A', )
    ], string='Category', default='na')
    rnd_cat = fields.Selection([
        ('certification', 'Certifications'), ('webinar', 'Webinars'), ('training', 'Training'),
        ('na', 'N/A',)
    ], string='Category (R&D)', default='na')
    lpo_cat = fields.Selection([
        ('customer_meet', 'Customer Meeting'), ('cold_call', 'Cold Calling'),
        ('mail_follow', 'Email Follow Up'), ('na', 'N/A')
    ], string='Category (LPO Follow Up)', default='na')
    vendor_cat = fields.Selection([
        ('register', 'Deal Registration'), ('update', 'Vendor Portal Update'),
        ('other', 'Other'), ('na', 'N/A')
    ], string="Category (Vendor Engagement)", default='na')
    line = fields.Selection([
        ('av', 'Audio Visual'), ('ict_sec', 'ICT Security'), ('ict', 'ICT'),
        ('netsol', 'Netsol'), ('cabling', 'Structured Cabling'),
        ('plantronics', 'Plantronics'), ('n_compute', 'NComputing'),
        ('green_tech', 'Green Technology')
    ], string='Product Line')
    user_id = fields.Many2one(comodel_name='res.users',string='Assigned To', default=lambda self: self.env.user.id)
    coordinator = fields.Char(string='Other Employees')
    status = fields.Selection([
        ('pending', 'Pending'), ('ongoing', 'Ongoing'),
        ('complete', 'Complete'), ('escalated', 'Escalated')
    ], string='Status')
    status_comment = fields.Text(string='Status Comment')
    start_time = fields.Datetime(string='Start Time', required='True')
    end_time = fields.Datetime(string='End Time')
    follow_up_status = fields.Selection([
        ('hot', 'Hot'), ('warm', 'Warm'),
        ('close_won', 'Closed Won'), ('close_lost', 'Closed Lost'),
        ('cold', 'Cold'), ('n/a', 'N/A'),
    ], string='Follow up Status', default='na')
    duration = fields.Char(string='Time Taken', compute='_get_duration')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))
    customer_name = fields.Char(string='Customer Name')
    description = fields.Text(string='Task Description')
    ticket_no = fields.Many2one(comodel_name='helpdesk_lite.ticket', string='Related Ticket Number')
    quotation_ref = fields.Many2one(comodel_name='sale.order', string='Quotation Reference')
    opportunity_id = fields.Many2one(comodel_name='crm.lead', string='Opportunity ID')
    potential_no = fields.Many2one(comodel_name = 'crm.potentials', string='Potential Number')
    assigned_date = fields.Datetime(string='Assigned Date')
    response_time = fields.Char(string='Response Time', compute='_get_response_time')
    delayed = fields.Boolean(string='Delayed', compute='_get_response_time')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('tech.timesheet.entry') or _('New')
        return super(TechTimesheet, self).create(vals)

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)
            else:
                rec.duration = ""

    def _get_response_time(self):
        for rec in self:
            if rec.assigned_date and rec.start_time:
                assignedDate = fields.datetime.strptime(rec.assigned_date, '%Y-%m-%d %H:%M:%S')
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                dur = startTime - assignedDate
                if '-' in str(dur):
                    rec.response_time = "Check your date values"
                else:
                    rec.response_time = str(dur)
                    if dur > timedelta(days=2):
                        rec.delayed = True
                    else:
                        rec.delayed = False

            else:
                rec.response_time = ""


