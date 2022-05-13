
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class HrResignWizard(models.TransientModel):
    _name = "hr.resign.wizard"
    _description = "HR Resign wizard"
    

    resign_date = fields.Date(string='Resign Date', required=True)
    notice_days = fields.Integer(string='Effective Days', default=0)  
    resign_type =  fields.Char(string='Resign Type')   
    resign_remarks =  fields.Char(string='Resign Remarks') 
    employee_ids = fields.Many2many('hr.employee', string='Employee')    
    
    def action_update_resign(self):
        for employee in self.employee_ids:
            employee.update({
                'resigned_date':  self.resign_date,
                'effective_date':  self.resign_date + timedelta(self.notice_days),
                'resign_type':  self.resign_type,
                'resigned_remarks': self.resign_remarks,
            })
            if self.notice_days ==0:
                employee.user_id.update({
                  'active': False,
                })
            contracts=self.env['hr.contract'].search([('employee_id','=',employee.id),('state','=','open')]) 
            for contract in contracts:
                if self.notice_days ==0:
                    contract.update({
                      'state': 'close',
                      'date_end':  self.resign_date,
                    })
                
            #employee.address_home_id.update({
            #     'active': False,
            #})
            if self.notice_days ==0:
                employee.update({
                  'active': False,
                })