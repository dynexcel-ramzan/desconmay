# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
from odoo.exceptions import ValidationError
#import cx_Oracle
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

logger = logging.getLogger(__name__)


class OracleSettingConnector(models.Model):
    _inherit = 'oracle.setting.connector'
   
            
    def get_normal_overtime_type(self, employee_company, work_location):
        """
         In this method you can get Normal Overtime 
         1- Work Location Wise.
         2- Compnay Wise 
         3- Universal 
        """
        overtime_type = self.env['hr.overtime.type'].search([('type','=','normal')], limit=1)
        if employee_company:
            overtime_type = self.env['hr.overtime.type'].search([('type','=','normal'),('company_id','=',employee_company)], limit=1)
            if not overtime_type:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','normal')], limit=1)
            if work_location:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','normal'),('company_id','=',employee_company),('work_location_id','=',work_location)], limit=1)
                if not overtime_type:
                    if employee_company:
                        overtime_type = self.env['hr.overtime.type'].search([('type','=','normal'),('company_id','=',employee_company)], limit=1)
                        if not overtime_type:
                            overtime_type = self.env['hr.overtime.type'].search([('type','=','normal')], limit=1)
                        
        return overtime_type
    
    
    
    def get_gazetted_overtime_type(self, employee_company, work_location):
        """
         In this method you can get Gazetted Overtime 
         1- Work Location Wise.
         2- Compnay Wise 
         3- Universal 
        """
        overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted')], limit=1) 
        if employee_company:
            overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted'),('company_id','=',employee_company)], limit=1)
            if not overtime_type:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted')], limit=1) 

                if work_location: 
                    overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted'),('company_id','=',employee_company),('work_location_id','=',work_location)], limit=1)
                    if not overtime_type:
                        if employee_company:
                            overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted'),('company_id','=',employee_company)], limit=1)
                            if not overtime_type:
                                overtime_type = self.env['hr.overtime.type'].search([('type','=','gazetted')], limit=1)    

                        
        return overtime_type
    
    
    
        
    def get_rest_days_overtime_type(self, employee_company, work_location):
        """
         In this method you can get Rest Day Overtime 
         1- Work Location Wise.
         2- Compnay Wise 
         3- Universal 
        """
        overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day')], limit=1)
        if employee_company:
            overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day'),('company_id','=',employee_company)], limit=1)
            if not overtime_type:
                overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day')], limit=1)
                if work_location:
                    overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day'),('company_id','=',employee_company),('work_location_id','=',work_location)], limit=1)
                    if not overtime_type:
                        if employee_company:
                            overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day'),('company_id','=',employee_company)], limit=1)
                            if not overtime_type:
                                overtime_type = self.env['hr.overtime.type'].search([('type','=','rest_day')], limit=1)    

                        
        return overtime_type    
        
    def _action_create_overtime(self):
        ora_start_create_date = fields.date.today() - timedelta(5)
        ora_end_create_date = fields.date.today() - timedelta(1)  
        attendances=self.env['hr.attendance'].search([('employee_id.allow_overtime','=',True),('is_overtime','=',False),('att_date','>=',ora_start_create_date),('att_date','<=',ora_end_create_date),('check_in','!=',False),('check_out','!=',False)])
        for att in attendances:
            day_min_ovt = 0
            overtime_rule = self.env['hr.overtime.rule'].search([('company_id','=',att.employee_id.company_id.id)])
            for rule in overtime_rule:
                if rule.rule_period == 'day' and rule.rule_type == 'minimum':
                    day_min_ovt = rule.hours
            overtime_limit = 0
            if att.shift_id:
                overtime_limit = att.rounded_hours - att.shift_id.hours_per_day
            else:
                overtime_limit = att.rounded_hours - 8
            overtime_type = self.get_normal_overtime_type(att.employee_id.company_id.id, att.employee_id.work_location_id.id)
            shift_schedule_lines = self.env['hr.shift.schedule.line'].search([('employee_id','=', att.employee_id.id),('rest_day','=',True),('date','=',att.att_date)])
            for rest_day in shift_schedule_lines:
                if rest_day.rest_day==True:
                    # get Rest Days overtime type
                    overtime_type = self.get_rest_days_overtime_type(att.employee_id.company_id.id, att.employee_id.work_location_id.id)
            shift_gazetted_lines = self.env['shift.gazetted.line'].search([('date','=',att.att_date),('shift_id','=', att.shift_id.id)], limit=1)
            if shift_gazetted_lines:
                overtime_type = self.get_gazetted_overtime_type(att.employee_id.company_id.id, att.employee_id.work_location_id.id)
            if overtime_type.type=='gazetted':    
                vals = {
                        'employee_id': att.employee_id.id,
                        'company_id': att.employee_id.company_id.id,
                        'work_location_id': att.employee_id.work_location_id.id,
                        'workf_location_id': att.employee_id.work_location_id.id, 
                        'date':  att.att_date,
                        'date_from': att.check_in,
                        'date_to': att.check_out,
                        'hours': att.rounded_hours,
                        'actual_ovt_hours': att.rounded_hours,
                        'overtime_hours': overtime_limit,
                        'overtime_type_id': overtime_type.id,
                    }
                overtime_lines = self.env['hr.overtime.request'].create(vals)
                att.update({
                    'is_overtime': True
                })
            elif overtime_type.type=='rest_day':
                vals = {
                        'employee_id': att.employee_id.id,
                        'company_id': att.employee_id.company_id.id,
                        'work_location_id': att.employee_id.work_location_id.id,
                        'workf_location_id': att.employee_id.work_location_id.id,
                        'date':  att.att_date,
                        'date_from': att.check_in,
                        'date_to': att.check_out,
                        'hours': att.rounded_hours,
                        'actual_ovt_hours': att.rounded_hours,
                        'overtime_hours': overtime_limit,
                        'overtime_type_id': overtime_type.id,
                    }
                overtime_lines = self.env['hr.overtime.request'].create(vals)
                att.update({
                    'is_overtime': True
                })
            else:
                if overtime_limit > 0 and overtime_limit > day_min_ovt:
                    vals = {
                            'employee_id': att.employee_id.id,
                            'company_id': att.employee_id.company_id.id,
                            'work_location_id': att.employee_id.work_location_id.id,
                            'workf_location_id': att.employee_id.work_location_id.id,
                            'date':  att.att_date,
                            'date_from': att.check_in,
                            'date_to': att.check_out,
                            'hours': att.rounded_hours,
                            'actual_ovt_hours': overtime_limit,
                            'overtime_hours': overtime_limit,
                            'overtime_type_id': overtime_type.id,
                        }
                    overtime_lines = self.env['hr.overtime.request'].create(vals)
                    att.update({
                        'is_overtime': True
                    })