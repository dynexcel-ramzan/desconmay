# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Portal Attendance',
    'version': '14.0.0.0',
    'category': 'Attendance',
    'sequence': 10,
    'summary': 'Employee Attendance',
    'depends': [
        'hr_attendance',
        'portal',
        'rating',
        'de_employee_shift',
        'de_oracle_attendance_connector',
        'resource',
        'web',
        'web_tour',
        'digest',
        'base',
        'hr_payroll',
        'de_hr_attendance_approvals',
    ],
    'description': "",
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_templates.xml',
        'views/hr_attendance_views.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

