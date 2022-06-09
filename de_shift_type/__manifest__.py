# -*- coding: utf-8 -*-
{
    'name': "Shift Type",

    'summary': """
        Shift Type
        """,

    'description': """
        Shift Type
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_oracle_attendance_connector','de_employee_shift'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}