from odoo import fields, models, api, _
from datetime import date, datetime, time


class StoresTimesheet(models.Model):
    _name = 'stores.timesheet'
    _description = 'This is the stores timesheet'

    department = fields.Selection([
        ('stores', 'Stores'), ('procurement', 'Procurement'),
    ], string="Department", required=True)
    task_activity = fields.Selection([
        ('account', 'Account Registration'), ('credit_terms', 'Credit Terms Negotiation'),
        ('eta_status', 'ETA Status Report'),
        ('purchase_follow', 'Follow up on Purchases'), ('goods_return', 'Goods Return'),
        ('goods_issuance', 'Issuance of Goods'), ('invoice_receipts', 'Issuance of Invoices/Receipts'),
        ('sup_lpo', 'Issuance of Supplier LPO'), ('lead_gen', 'Lead Generation'),
        ('lpo_prep', 'LPO Preparation'), ('lpo_report', 'LPO Status Report'), ('meeting', 'Meeting'),
        ('overseas_process', 'Overseas Processing'), ('overseas_follow', 'Overseas Follow up'),
        ('analysis', 'Price Analysis'), ('purchase_approval', 'Purchase Approval'),
        ('purchase_req', 'Purchase Requisition'), ('receive_goods', 'Receipt of Goods'), ('receive_tools', 'Receipt of tools'), ('gatepass', 'Returnable Gatepasses'),
        ('admin_pricing', 'Sales Admin Pricing'), ('sourcing', 'Sourcing'), ('clearance', 'Staff Clearance'),
        ('stock_reconciliation', 'Stocks Reconciliation'), ('stock_label', 'Stock Labelling'),  ('stock_take', 'Stock Take/Update'),
        ('arrangement', 'Stores Arrangement/Transfer'), ('supplier_process', 'Supplier Payment Processing'),
        ('supplier_reconciliation', 'Supplier Payment Reconciliation'), ('prequal', 'Supplier Pre-qualification'),
        ('tools_issuance', 'Tools Issuance'), ('training', 'Training'), ('trans_update', ' Transaction Update'),
        ('transport', 'Transport Logistics'),
    ], string="Task Activity", required=True)
    employee_id = fields.Many2one(comodel_name='res.users', string='Assigned To', default=lambda self: self.env.user.id)
    customer_name = fields.Char(string='Customer Name (if applicable)')
    supplier_name = fields.Char(string='Supplier Name (if applicable)')
    description = fields.Text(string='Task Description')
    amount = fields.Float(string='Quotation Sum (if applicable)')
    status = fields.Selection([
        ('pending', 'Pending'), ('ongoing', 'Ongoing'),
        ('complete', 'Complete'), ('escalated', 'Escalated')
    ])
    status_comment = fields.Text(string='Status Comment')
    user = fields.Selection([
        ('internal', 'Internal'), ('external', "External")
    ])
    start_time = fields.Datetime(string='Start Time', required="True")
    end_time = fields.Datetime(string='End Time')
    duration = fields.Char(string='Time Taken', compute='_get_duration')
    lpo_number = fields.Many2one(string='Purchase Reference', comodel_name='purchase.order')
    request_no = fields.Many2one(string='Stores Request Reference', comodel_name='ticket.requisition')
    other_employee = fields.Char(string='Supported By')
    name = fields.Char(string='Entry Number', readonly=True, required=True, copy=False, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('stores.timesheet.entry') or _('New')
        return super(StoresTimesheet, self).create(vals)

    def _get_duration(self):
        for rec in self:
            if rec.start_time and rec.end_time:
                startTime = fields.datetime.strptime(rec.start_time, '%Y-%m-%d %H:%M:%S')
                endTime = fields.datetime.strptime(rec.end_time, '%Y-%m-%d %H:%M:%S')
                dur = datetime.combine(date.min, endTime.time()) - datetime.combine(date.min, startTime.time())
                rec.duration = str(dur)
            else:
                rec.duration = ""
