# -*- coding: utf-8 -*-

from odoo import models, fields, api



class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"
    reason = fields.Char(string="Reason")
    
    
    def refuse_sheet(self):
        ''' Open the account.payment.register wizard to pay the selected journal entries.
        :return: An action opening the account.payment.register wizard.
        '''
        return {
            'name': _('Refause reason'),
            'res_model': 'hr.expense.refuse.wizard',
            'view_mode': 'form',
            'context': {
                'active_model': 'hr.expense.sheet',
                'active_ids': self.ids,
                'default_reason': self.reason
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }