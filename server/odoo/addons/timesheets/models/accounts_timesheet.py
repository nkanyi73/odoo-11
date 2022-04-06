from odoo import fields, models, api, _
from datetime import datetime, time, date


class AccountTimesheet(models.Model):
    _name = 'account.timesheet'
    _description = 'This is a timesheet for the Accounts Department'

    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))
    task_type = fields.Selection([
        ('receive', 'Account Receivables'), ('payable', 'Account Payables'),
    ], string="Department", required=True)
    employee_id = fields.Many2one(comodel_name='res.users', string='Assigned To', default=lambda self: self.env.user.id)
    customer_name = fields.Char(string='Customer Name (if applicable)')
    supplier_name = fields.Char(string='Supplier Name (if applicable)')
    task_activity = fields.Selection([
        ('admin_payment', 'Admin Payment'), ('bank_recon', 'Bank Reconciliation'), ('bid_bond', 'Bid/Bond Processing')
        , ('cash_flow', 'Cash Flow Report'), ('cheque', 'Cheque Processing'), ('collection', 'Collection Report')
        , ('credit', 'Credit Terms Negotiation'), ('customer_receipt', 'Customer Receipts'),
        ('debt_collect', 'Debt Collection'), ('debtor', 'Debtor\'s Reconciliation')
        , ('filing', 'Filing'), ('fuel_report', 'Fuel Report Analysis'), ('gatepass', 'Gatepass Approval')
        , ('invoicing', 'Invoicing'), ('petty_issue', 'Issuance of Petty Cash'), ('lead_gen', 'Lead Generation'),
        ('lpo_clear', 'LPO Clearance'), ('lpo_follow', 'LPO Follow Up')
        , ('pay_follow', 'Payment Follow-up'), ('petty_report', 'Petty Cash Report'), ('bills', 'Posting of Bills')
        , ('salary_pay', 'Salary Payment'), ('sales_report', 'Sales Report'), ('statutory', 'Statutory Payment')
        , ('sup_pay', 'Supplier Payment'), ('sup_reconcile', 'Supplier Reconciliation'), ('training', 'Training'),
        ('uber', 'Uber Report Analysis')
    ])
    status = fields.Selection([
        ('pending', 'Pending'), ('ongoing', 'Ongoing'),
        ('complete', 'Complete'), ('escalated', 'Escalated')
    ])
    status_comment = fields.Text(string='Status Comment')
    description = fields.Text(string='Task Description')
    other_employee = fields.Char(string='Supported By')
    start_time = fields.Datetime(string='Start Time', required="True")
    end_time = fields.Datetime(string='End Time')
    duration = fields.Char(string='Time Taken', compute='_get_duration')
    lpo_number = fields.Many2one(string='Purchase Reference', comodel_name='purchase.order')
    cash_request = fields.Many2one(string='Cash Request Reference', comodel_name='hr.expense')
    gatepass_no = fields.Char(string='GatePass Number')
    invoice_no = fields.Char(string='Invoice Number')
    lpo_quotation_reference = fields.Char(string='PO/Quotation Reference')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('account.timesheet.entry') or _('New')
        return super(AccountTimesheet, self).create(vals)

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)
            else:
                rec.duration = ""
