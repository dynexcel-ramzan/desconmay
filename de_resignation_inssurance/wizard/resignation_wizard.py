# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResignationInssurance(models.TransientModel):
    _name = "resignation.inssurance.wizard"
    _description = "Resignation Inssurance wizard"

    start_date = fields.Date(string='Date From', required=True)
    end_date = fields.Date(string='Date To', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)

    def action_check_report(self):
        data = {}
        data['form'] = self.read(['start_date','end_date','company_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['start_date', 'end_date','company_id'])[0])
        return self.env.ref('de_resignation_inssurance.resignation_report_xlx').report_action(self, data=data, config=False)