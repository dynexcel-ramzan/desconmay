# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class OnExpenseSheetWizard(models.TransientModel):
    _name = "expense.sheet.wizard"
    _description = "Expense Report"

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date to', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    


    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to', 'company_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date_from', 'date_to', 'company_id'])[0])
        return self.env.ref('de_expense_reports.on_expense_sheet_report').report_action(self, data=data,
                                                                                                  config=False)