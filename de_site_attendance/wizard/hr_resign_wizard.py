
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrResignWizard(models.TransientModel):
    _name = "hr.resign.wizard"
    _description = "HR Resign wizard"
    

    resign_date = fields.Date(string='Resign Date', required=True) 
    resign_type =  fields.Char(string='Resign Type')   
    resign_remarks =  fields.Char(string='Resign Remarks') 
    employee_ids = fields.Many2many('hr.employee', string='Employee')    
    
    def action_update_resign(self):
        for employee in self.employee_ids:
            employee.update({
                'resigned_date':  self.resign_date,
                'resign_type':  self.resign_type,
                'resigned_remarks': self.resign_remarks,
            })
            employee.user_id.update({
                 'active': False,
            })
            contracts=self.env['hr.contract'].search([('employee_id','=',employee.id),('state','=','open')]) 
            for contract in contracts:
                contract.update({
                     'state': 'close',
                     'date_end':  self.resign_date,
                })
        