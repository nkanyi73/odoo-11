# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, date, timedelta


class Timesheet(models.Model):
    _name = 'om.timesheet'
    _description = 'Timesheet Information'

    dept_name = fields.Char(string='Place of departure', required=True)
    dest_name = fields.Char(string='Destination name', required=True)
    exp_dept_time = fields.Datetime(string="Expected departure time")
    dept_time = fields.Datetime(string='Departure time', required=True)
    arr_time = fields.Datetime(string='Arrival time')
    wait_time = fields.Char(string="Wait Time", compute="_get_wait_time")
    travel_time = fields.Char(string="Time taken on travel", compute="_get_travel_time")
    purpose = fields.Text(string='Description of work', translate=True)
    # related = fields.Selection([
    #     ('ticket', 'Ticket'),
    #     ('project', 'Project')
    # ], string='Related To')
    ticket_no = fields.Many2one(comodel_name='helpdesk_lite.ticket', string="Related Ticket Number", required="True")
    time_in = fields.Datetime(string='Time in')
    time_out = fields.Datetime(string='Time out')
    job_time = fields.Char(string="Time taken to complete task", compute="_get_job_time")
    # project_id = fields.Many2one(comodel_name='project.project', string='Associated Project')
    engineer_id = fields.Many2one(comodel_name='hr.employee', string='Employee')
    status = fields.Many2one(string='Status', comodel_name='helpdesk_lite.stage', related='ticket_no.stage_id')
    status_comment = fields.Text(string='Status Comment', translate=True)
    category = fields.Selection([
        ('inhouse', 'In-house'),
        ('demopoc', 'Demo & POC'), ('delivery', 'Delivery'),
        ('callout', 'Call Out'), ('installation', 'Installation'),
        ('wlan', 'WLan'), ('aksurvey', 'AK Survey'),
        ('installation', 'AK Installation'), ('relocation', 'AK Relocation'),
        ('survey', 'Survey'), ('telcom', 'Telcom Call Out'),
        ('support', 'AK Support'), ('kit_collection', 'Kit Collection')
    ], required=True)
    company_hours = fields.Char(string='Company Hours', compute='_get_company_hours')
    no_of_jobs = fields.Integer(string='Number of jobs today', compute='_get_no_of_jobs')
    final_time = fields.Char(string='Job date', compute='_transform_created_on')
    delay = fields.Char(string='Delay in departure', compute='_get_delay')
    coordinator = fields.Many2one(comodel_name='res.users', string='Coordinator')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))
    exp_completion_time = fields.Char(string='Expected Completion Time', compute='_get_completion')
    exceeded = fields.Boolean(string='Job', compute='_get_exceeded')
    other_employees = fields.Char(string='Other Employees')
    reason = fields.Text(string='Reason for delay')
    over_time = fields.Char(string='Time exceeded', compute='_get_over_time')
    stored_date = fields.Char(compute='_get_stored')
    real_date = fields.Char(compute='_get_date', store=True)
    status_com = fields.Char(compute='_get_status', string='Job Status', store=True)

    def _get_status(self):
        for rec in self:
            if rec.status:
                rec.status_com = rec.status.name

    def _get_stored(self):
        for rec in self:
            rec.stored_date = rec.final_time

    def _get_date(self):
        for rec in self:
            rec.real_date = rec.final_time

    def _get_over_time(self):
        for over in self:
            if over.exp_completion_time and over.time_out:
                completion = fields.datetime.strptime(over.exp_completion_time, '%Y-%m-%d %H:%M:%S')
                timeOut = fields.datetime.strptime(over.time_out, '%Y-%m-%d %H:%M:%S')
                timeOut = timeOut + timedelta(hours=3)
                overTime = datetime.combine(date.min, timeOut.time()) - datetime.combine(date.min, completion.time())
                overTime = str(overTime)
                if '-' in overTime:
                    over.over_time = "N/A"
                else:
                    over.over_time = overTime

    def _get_exceeded(self):
        for ex in self:
            # if the expected completion time is filled
            if ex.exp_completion_time:
                # The date and time is stored as a string so I have to convert it to a
                # datetime object. The code is below.
                completion = fields.datetime.strptime(ex.exp_completion_time, '%Y-%m-%d %H:%M:%S')
                # Check if the time_out field is filled
                if ex.time_out:
                    # Pick the time out then convert it to a datetime object
                    timeOut = fields.datetime.strptime(ex.time_out, '%Y-%m-%d %H:%M:%S')
                    timeOut = timeOut + timedelta(hours=3)
                    # compare the time
                    if timeOut > completion:
                        # if the time out has exceeded the expected time of completion,
                        # there is a boolean variable which is set to true
                        ex.exceeded = True
                    else:
                        # else it is set to false
                        ex.exceeded = False
                else:
                    now = datetime.now() + timedelta(hours=3)
                    if now > completion:
                        ex.exceeded = True
                    else:
                        ex.exceeded = False

    def _get_completion(self):
        for el in self:
            if el.time_in:
                timeIn = fields.datetime.strptime(el.time_in, '%Y-%m-%d %H:%M:%S')
                if el.category == "telcom" or el.category == "support" or el.category == "callout":
                    completion = timeIn + timedelta(hours=5, minutes=00)
                    # completion = completion.time()
                    el.exp_completion_time = str(completion)
                elif el.category == "survey" or el.category == "demopoc" or el.category == "aksurvey":
                    completion = timeIn + timedelta(hours=4, minutes=00)
                    # completion = completion.time()
                    el.exp_completion_time = str(completion)
                elif el.category == "installation"  or el.category == "relocation":
                    completion = timeIn + timedelta(hours=7, minutes=00)
                    # completion = completion.time()
                    el.exp_completion_time = str(completion)
                else:
                    completion = timeIn + timedelta(hours=5, minutes=00)
                    # completion = completion.time()
                    el.exp_completion_time = str(completion)
            else:
                el.exp_completion_time = ""

    def _get_travel_time(self):
        for arr in self:
            if arr.arr_time and arr.dept_time:
                arrTime = fields.datetime.strptime(arr.arr_time, '%Y-%m-%d %H:%M:%S')
                deptTime = fields.datetime.strptime(arr.dept_time, '%Y-%m-%d %H:%M:%S')
                total_time = datetime.combine(date.min, arrTime.time()) - datetime.combine(date.min, deptTime.time())
                # total_time = str(int((arrTime - deptTime).seconds / 3600))
                total_time = str(total_time)
                arr.travel_time = total_time
            else:
                arr.travel_time = "Not provided ..."

    def _get_job_time(self):
        for job in self:
            if job.time_in and job.time_out:
                timeIn = fields.datetime.strptime(job.time_in, '%Y-%m-%d %H:%M:%S')
                timeOut = fields.datetime.strptime(job.time_out, '%Y-%m-%d %H:%M:%S')
                total_time = datetime.combine(date.min, timeOut.time()) - datetime.combine(date.min, timeIn.time())
                # total_time = str(int((arrTime - deptTime).seconds / 3600))
                total_time = str(total_time)
                job.job_time = total_time
            else:
                job.job_time = "Not provided ..."

    def _get_company_hours(self):
        for dy in self:
            if dy.arr_time:
                arrTime = fields.datetime.strptime(dy.arr_time, '%Y-%m-%d %H:%M:%S')
                dy_no = arrTime.weekday()
                if dy_no > 4:
                    dy.company_hours = "04:00"
                else:
                    dy.company_hours = "08:00"
            else:
                dy.company_hours = ""

    def _get_no_of_jobs(self):
        for jb in self:
            if jb.real_date:
                job_count = jb.env['om.timesheet'].search_count(
                    ['&', ('real_date', '=', jb.real_date), ('engineer_id', '=', jb.engineer_id.id)])
                # , ('final_time', '=', self.final_time)
                jb.no_of_jobs = job_count
            else:
                jb.no_of_jobs = 0

    def _transform_created_on(self):
        for tme in self:
            print("date1")
            if tme.create_date:
                print("date")
                createDate = fields.datetime.strptime(tme.create_date, '%Y-%m-%d %H:%M:%S')
                createDate = createDate.date()
                tme.final_time = str(createDate)

    def _get_wait_time(self):
        for wait in self:
            if wait.time_in and wait.arr_time:
                timeIn = fields.datetime.strptime(wait.time_in, '%Y-%m-%d %H:%M:%S')
                arrivalTime = fields.datetime.strptime(wait.arr_time, '%Y-%m-%d %H:%M:%S')
                total_time = datetime.combine(date.min, timeIn.time()) - datetime.combine(date.min, arrivalTime.time())
                # total_time = str(int((arrTime - deptTime).seconds / 3600))
                total_time = str(total_time)
                wait.wait_time = total_time
            else:
                wait.wait_time = "Not provided ..."

    def _get_delay(self):
        for d in self:
            if d.dept_time and d.exp_dept_time:
                deptTime = fields.datetime.strptime(d.dept_time, '%Y-%m-%d %H:%M:%S')
                expDept = fields.datetime.strptime(d.exp_dept_time, '%Y-%m-%d %H:%M:%S')
                if deptTime > expDept:
                    d.delay = str(
                        datetime.combine(date.min, deptTime.time()) - datetime.combine(date.min, expDept.time()))
                else:
                    d.delay = "00:00:00"
            else:
                d.delay = "00:00:00"

    def action_eng_report(self):
        template_id = self.env.ref('timesheets.engineer_report_mail').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)


    @api.onchange('ticket_no')
    def onchange_ticket_no(self):
        if self.ticket_no:
            if self.ticket_no.description:
                self.purpose = self.ticket_no.description
            if self.ticket_no.stage_id:
                self.status = self.ticket_no.stage_id
            if self.ticket_no.user_id:
                self.coordinator = self.ticket_no.user_id
            if self.ticket_no.status_cmt:
                self.status_comment = self.ticket_no.status_cmt
            if self.ticket_no.emp_charge:
                self.engineer_id = self.ticket_no.emp_charge
            if self.ticket_no.category:
                self.category = self.ticket_no.category
            if self.ticket_no.other_employees:
                self.other_employees = self.ticket_no.other_employees

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('timesheet.entry') or _('New')
        return super(Timesheet, self).create(vals)
