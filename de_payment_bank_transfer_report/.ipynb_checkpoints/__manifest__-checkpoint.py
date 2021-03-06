# -*- coding: utf-8 -*-
{
    'name': "Payment Bank Transfer Detail",

    'summary': """
        Payment Bank Transfer Detail
        """,

    'description': """
        Payment Bank Transfer Detail
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/account_payment_report.xml',
        'report/account_payment_template.xml',
        'report/payment_report.xml',
        'report/payment_report_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
