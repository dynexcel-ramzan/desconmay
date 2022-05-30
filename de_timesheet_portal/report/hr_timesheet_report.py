# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-
import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class HrTimesheetReport(models.AbstractModel):
    _name = 'report.de_timesheet_portal.timesheet_report'
    _description = 'Timesheet Report'
    
    
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        employees = docs.employee_ids
        type = docs.type
        date_from = docs.date_from
        date_to =  docs.date_to
        
        for employee in employees:
            detail_timesheet_data = []
            summary_timesheet_data =[]
            tot_planned_hrs = 0
            tot_worked_hrs = 0
            tot_idle_hrs = 0
            timesheet_lines=self.env['account.analytic.line'].sudo().search([('employee_id','=',employee.id),('line_date','>=',date_from),('line_date','<=',date_to)], order='line_date ASC')
            if type=='summary':
                days = (date_to - date_from).days
                start_date = date_from
                general_shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general')], limit=1)
                for day in range(days):
                    day_total_worked_hrs = 0
                    daytime=self.env['account.analytic.line'].sudo().search([('employee_id','=',employee.id),('line_date','=',start_date)], order='line_date ASC')
                    for ora_time in daytime:
                        day_total_worked_hrs += ora_time.unit_amount
                    shift_planned_hrs = 0
                    shift_schedule_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=',ts.employee_id.id),('date','=',line.line_date),('state','=','posted')], limit=1)
                    if not shift_schedule_line:
                        shift_planned_hrs += general_shift.hours_per_day  
                        
                    shift_planned_hrs += shift_schedule_line.first_shift_id.hours_per_day
                    if shift_schedule_line.second_shift_id:
                        shift_planned_hrs += shift_schedule_line.second_shift_id.hours_per_day
                    diff_hrs = shift_planned_hrs - day_total_worked_hrs
                    if diff_hrs < 0:
                        diff_hrs = 0
                    if diff_hrs > 0:
                        diff_hrs += tot_idle_hrs
                    tot_worked_hrs += shift_planned_hrs
                    tot_idle_hrs += day_total_worked_hrs
                    summary_timesheet_data.append({
                        'date': start_date.strftime('%d-%b-%y'),
                        'planned_hrs': shift_planned_hrs,
                        'worked_hrs': day_total_worked_hrs,
                        'idle_hrs': diff_hrs,
                    })    
                    start_date = date_from + timedelta(day) 
            if type=='detail':    
                detail_timesheet_data=timesheet_lines        
            timesheet_data.append({
                'employee_no': employee.emp_number ,
                'tot_planned_hrs': tot_planned_hrs,
                'tot_worked_hrs': tot_worked_hrs,
                'tot_idle_hrs': tot_idle_hrs,
                'name': employee.name,
                'date_from': date_from,
                'date_to': date_to,
                'department': employee.department_id.name,
                'manager': employee.parent_id.name,
                'summary_timesheet_data': summary_timesheet_data,
                'detail_timesheet_data': detail_timesheet_data,
            })
        return {
                'docs': docs,
                'timesheet_data': timesheet_data,
               }