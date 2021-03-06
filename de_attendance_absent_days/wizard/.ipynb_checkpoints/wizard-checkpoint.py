from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseReport(models.TransientModel):

    _name = 'attendance.model'
    _description = 'Model wizard'

    company = fields.Many2many('res.company', string='Company')
    date_form = fields.Date(string='Date form', required=True)
    date_to = fields.Date(string='Date to', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Employee')
    
    
     def print_report(self):
         data = {}
         data['form'] = self.read(['date_from', 'date_to','employee_ids'])[0]
         return self._print_report(data)

    def print_report(self):

        data = {
            'company': self.company,
#             'absent_list': absent_list,
            'date_form': self.date_form,
            'date_to': self.date_to,

        }
        if self.company:
            return self.env.ref('de_attendance_absent_days.attendance_report_xlx').report_action(self, data=data)