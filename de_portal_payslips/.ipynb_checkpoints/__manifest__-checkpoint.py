# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Portal Payslips',
    'version': '14.0.0.0',
    'category': 'Project',
    'sequence': 10,
    'summary': 'Organize and schedule your projects ',
    'depends': [
        'hr_payroll',
        'portal',
        'rating',
        'resource',
        'web',
        'web_tour',
        'digest',
        'de_employee_overtime',
        'de_account_pf_ledger',
        'base',
    ],
    'description': "",
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/portal_payslip_template.xml',
        'views/partner_pf_ledger_template.xml',
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

