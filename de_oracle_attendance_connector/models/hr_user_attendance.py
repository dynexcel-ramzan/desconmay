# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import cx_Oracle

class HrUserAttendance(models.Model):
    _name = 'hr.user.attendance'
    _description = 'This is User Attendance'
    
    

    employee_id = fields.Many2one('hr.employee', string="Employee")
    is_mapped = fields.Boolean(string="Mapped Employee")
    company_id = fields.Many2one('res.company', string="Company")
    timestamp = fields.Datetime(string='Timestamp')
    device_id = fields.Char(string='Device ID')
    card_no = fields.Char(string="Card NO.")
    time = fields.Char(string="Stamp Time")
    attendance_date = fields.Date(string='Attendance Date')
    creation_date = fields.Char(string='Attendance Date')
    remarks = fields.Char(string='Remarks')
    updation_date = fields.Char(string='Updation Date')
    is_attedance_created = fields.Boolean(string="Attendance Posted")

    
    def action_attendace_validated(self, employeeslst, deltadays):        
        month_datetime = fields.date.today() - timedelta(deltadays)
        for month_date in range(deltadays):
            attendance_date1 =  month_datetime + timedelta(month_date)
            total_employee = self.env['hr.employee'].search([('id', 'in', employeeslst)])
            for employee in total_employee:
                oracle_attendance = self.env['hr.user.attendance']
                count = oracle_attendance.search_count([('employee_id','=',employee.id),('attendance_date','=',attendance_date1)])
                if count > 2:
                    next_day_attendancea = attendance_date1 + timedelta(1)
                    shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                    shift_linea = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendancea)], limit=1)                             
                    if shift_linea.first_shift_id:
                        shift = shift_linea.first_shift_id
                    
                    if shift.shift_type == 'night':
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=2)
                        if attendance_list_in and attendance_list_out:
                            check_out_time = False
                            outtime_id1 = 0
                            for out_time in attendance_list_out:
                                check_out_time =  out_time.timestamp 
                                outtime_id1 = out_time.id
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': check_out_time,
                                'att_date': check_out_time,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            mattendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc")
                            for mline in mattendance_list:
                                mline.update({
                                        'is_attedance_created' : True
                                })
                            
                            outtimeid1 = oracle_attendance.search([('id','=', outtime_id1)])
                            outtimeid1.update({
                               'is_attedance_created' : True
                            })
                            checkin_time = False
                            outtime_id2 = 0
                            for in_time in attendance_list_out:
                                checkin_time = in_time.timestamp
                                outtime_id2 = in_time.id
                                break
                            night_vals = {
                                'check_in': checkin_time,
                                'att_date': checkin_time,
                                'employee_id': employee.id,
                                    }   
                            attendance = self.env['hr.attendance'].create(night_vals)
                            mattendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc")
                            for mline in mattendance_list:
                                mline.update({
                                        'is_attedance_created' : True
                                })
                            outtimeid2 = oracle_attendance.search([('id','=', outtime_id2)])
                            outtimeid2.update({
                               'is_attedance_created' : True
                            })
                    else:
                        attendance_list_in = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc", limit=1)
                        attendance_list_out = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc", limit=1)

                        if attendance_list_in and attendance_list_out:
                            vals = {
                                'check_in': attendance_list_in.timestamp,
                                'check_out': attendance_list_out.timestamp,
                                'att_date': attendance_list_out.attendance_date,
                                'employee_id': attendance_list_in.employee_id.id,
                                }   
                            attendance = self.env['hr.attendance'].create(vals)
                            mattendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp desc")
                            for mline in mattendance_list:
                                mline.update({
                                        'is_attedance_created' : True
                                })   
                else:
                    attendance_list = oracle_attendance.search([('employee_id','=',employee.id),('attendance_date','=',attendance_date1),('is_attedance_created','=',False)], order="timestamp asc")
                    if attendance_list: 
                        check_in = fields.date.today()
                        for attendace in attendance_list:
                            previous_attendance = attendace.attendance_date - timedelta(1)
                            pre_existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', previous_attendance),('check_out','=',False)] , order="check_in asc", limit=1)
                            if pre_existing_attendance:
                                delta_out = attendace.timestamp - pre_existing_attendance.check_in
                                deltaout_time = delta_out.total_seconds()
                                next_day_attendance = attendace.attendance_date + timedelta(1) 
                                shift = self.env['resource.calendar'].sudo().search([('shift_type','=','general'),('company_id','=',employee.company_id.id)], limit=1)
                                shift_line = self.env['hr.shift.schedule.line'].sudo().search([('employee_id','=', employee.id),('date','=',next_day_attendance)], limit=1)                             
                                if shift_line.first_shift_id:
                                    shift = shift_line.first_shift_id
                                    if shift.shift_type == 'night':    
                                        pre_existing_attendance.update({
                                           'att_date': attendace.timestamp,
                                           'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                            'is_attedance_created' : True
                                            })
                                    else:
                                        existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                        if existing_attendance:
                                            delta_time = attendace.timestamp - existing_attendance.check_in
                                            delta = delta_time.total_seconds()
                                            if delta < 1200 :
                                                existing_attendance.update({
                                                'att_date': attendace.timestamp,
                                                'check_in': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                            else:
                                                existing_attendance.update({
                                                   'att_date': attendace.timestamp,
                                                  'check_out': attendace.timestamp,
                                                })
                                                attendace.update({
                                                                'is_attedance_created' : True
                                                                })
                                        else:
                                            vals = {
                                                'check_in': attendace.timestamp,
                                                'att_date': attendace.attendance_date,
                                                'employee_id': attendace.employee_id.id,
                                            }
                                            attendance = self.env['hr.attendance'].create(vals)
                                            attendace.update({
                                                        'is_attedance_created' : True
                                                        })

                            else:
                                existing_attendance = self.env['hr.attendance'].search([('employee_id','=',employee.id),('att_date','=', attendace.attendance_date),('check_out','=',False)] , order="check_in asc", limit=1)
                                if existing_attendance:
                                    delta_time = attendace.timestamp - existing_attendance.check_in  
                                    delta = delta_time.total_seconds() 
                                    if delta < 1200 :
                                        existing_attendance.update({
                                        'att_date': attendace.timestamp,    
                                        'check_in': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                    else:
                                        existing_attendance.update({
                                           'att_date': attendace.timestamp,  
                                          'check_out': attendace.timestamp,
                                        }) 
                                        attendace.update({
                                                        'is_attedance_created' : True
                                                        })
                                else:    
                                    vals = {
                                        'check_in': attendace.timestamp,
                                        'att_date': attendace.attendance_date,
                                        'employee_id': attendace.employee_id.id,
                                    }   
                                    attendance = self.env['hr.attendance'].create(vals)
                                    attendace.update({
                                                'is_attedance_created' : True
                                                })
    
    


    
    #                                 attendance.action_process_attendance(attendance.id)