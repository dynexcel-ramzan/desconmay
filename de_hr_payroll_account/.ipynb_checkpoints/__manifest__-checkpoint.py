# -*- coding: utf-8 -*-
{
    'name': "HR Payroll Account",

    'summary': """
        HR Payroll Account  Journal Entry
        """,

    'description': """
        HR Payroll Account  Journal Entry
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Payroll',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_payroll_account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_payroll_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
