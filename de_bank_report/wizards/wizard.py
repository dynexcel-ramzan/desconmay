from odoo import api, fields, models, _
from odoo.exceptions import UserError


class BanksModel(models.Model):

    _name = 'banks.model'
    _description = 'Model wizard'
    
  
    cheque_no = fields.Char(string='Cheque no', required=True)
    branch = fields.Many2many('hr.payslip.run', string='Branch', relation="bank_id")
    bank = fields.Many2many('account.journal', string='Bank')
   

    def print_report(self):

        data = {}
        return self.env.ref('de_bank_report.bank_report_data').report_action(self, data=data)
